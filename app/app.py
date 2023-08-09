#!/usr/bin/python3
from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import exc
from sqlalchemy.sql import text
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_cors import CORS
import secrets
import os


basedir = os.path.abspath(os.path.dirname(__file__))

# Init app
app = Flask(__name__, template_folder="templates")
CORS(app)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config.from_pyfile('config.py')

# Set secret_key
app.secret_key = secrets.token_hex(16)

# set optional bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

admin = Admin(app, name='techtutors', template_mode='bootstrap3')

# Add administrative views here
# test
# print("this is where the template folder is: ", app.template_folder)
# print("this is where the base directory is: ", basedir)


# Database
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + \
#     os.path.join(basedir, "db.sqlite")
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{app.config['DB_USER']}:{app.config['DB_PASSWORD']}@{app.config['DB_HOST']}/{app.config['DB_NAME']}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# Init db
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# Init ma
ma = Marshmallow(app)

# test connectionnn
with app.app_context():
    try:
        db.session.execute(text("SELECT 1"))
        print("Database connection successful")
    except exc.SQLAlchemyError as e:
        print("Database connection failed:", str(e))

# bitcontent Class/Model


class Bitcontent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200))
    category_name = db.Column(db.String(50), db.ForeignKey(
        "category.name"), nullable=False)

    category = db.relationship(
        "Category", backref=db.backref("bitcontent", lazy=True))

    def __init__(self, category_name, content):
        self.category_name = category_name
        self.content = content


class Category(db.Model):
    id = db.Column(db.Integer, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, primary_key=True)

    def __repr__(self):
        return "<Category %r>" % self.name


# Create the database tables
with app.app_context():
    db.create_all()


# bitcontent Schema


class BitcontentSchema(ma.Schema):
    class Meta:
        fields = ("id", "category_name", "content")


class CategorySchema(ma.Schema):
    class Meta:
        fields = ("id", "name")

# Create admin views for Bitcontent and Category


class BitcontentModelView(ModelView):
    # Specify the columns to display
    column_list = ["id", "category", "content"]
    # Specify the columns in the edit form
    form_columns = ("category", "content")

    def __init__(self, session, **kwargs):
        super(BitcontentModelView, self).__init__(
            Bitcontent, session, **kwargs)
        self.form_args = {
            "category": {
                "query_factory": lambda: db.session.query(Category.name),
                "get_label": "name"
            }
        }


class CategoryModelView(ModelView):
    column_list = ["id", "name"]
    form_columns = ("id", "name")


# Add the BitcontentModelView to the admin interface
admin.add_view(BitcontentModelView(db.session))
admin.add_view(CategoryModelView(Category, db.session))
# Init schema
bitcontent_schema = BitcontentSchema()
bitcontents_schema = BitcontentSchema(many=True)
category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)

# Create a category
categories = []


@app.route("/api/addcategory", methods=["POST"])
def add_category():
    category_name = request.json["name"]

    new_category = Category(name=category_name)

    db.session.add(new_category)
    db.session.commit()

    return category_schema.jsonify(new_category)

# Create a bitcontent


@app.route("/api/addbitcontent", methods=["POST"])
def add_bitcontent():
    category_name = request.json["category_name"]
    content = request.json["content"]

    category = Category.query.filter_by(name=category_name).first()

    if not category:
        return jsonify({"message": "Category not found"}), 404

    new_bitcontent = Bitcontent(category_name=category, content=content)

    db.session.add(new_bitcontent)
    db.session.commit()

    return bitcontent_schema.jsonify(new_bitcontent)


@app.route("/api/categories", methods=["GET"])
def get_categories(category_name=None):
    categories = Category.query.all()
    response = categories_schema.dump(categories)
    result = jsonify(response)
    data = result.get_json()
    return data


@app.route("/api/bitcontents", methods=["GET"])
def get_bitcontents():
    all_bitcontent = Bitcontent.query.all()
    response = bitcontents_schema.dump(all_bitcontent)
    result = jsonify(response)
    data = result.get_json()
    return data


@app.route("/api/bitcontent/<category_name>", methods=["GET"])
def get_bitcontent(category_name):
    if category_name:

        bitcontent = Bitcontent.query.filter_by(
            category_name=category_name).all()
        response = bitcontents_schema.dump(bitcontent)
        result = jsonify(response)
        data = result.get_json()
        return data
    else:
        return "No content for the category", 404


@app.route("/api/bitcontent/<category_name>/<id>", methods=["GET"])
def get_bitcontent_id(category_name, id):
    if category_name:

        bitcontent = Bitcontent.query.filter_by(
            category_name=category_name, id=id).all()
        response = bitcontents_schema.dump(bitcontent)
        result = jsonify(response)
        data = result.get_json()
        return data
    else:
        return "No content for the category", 404


# Routes
with app.app_context():
    categories_database = get_categories()
    categories_list = []
    for category in categories_database:
        categories_list.append(category["name"])


@app.route("/")
def initial():
    return redirect(url_for("home"))


@app.route("/home")
def home():
    return render_template("home.html", categories=categories_list)


@app.route("/<category_name>")
def display_category(category_name):
    category_data = get_categories(category_name.lower())
    bitcontent = get_bitcontent(category_name)
    template_name = category_name + ".html"
    template_dir = basedir + '/'+app.template_folder
    if os.path.exists(template_dir + "/" + template_name):
        if category_data:
            print("HERE YOU GOOOO:", template_dir)
            return render_template(template_name, categories=categories_list, data=bitcontent)
        else:
            return "Category not found", 404
    else:
        html_template_content = """
        {% extends "base.html" %}
        {% block content %}
        <ul>
            {%for each in data:%}
                <li>{{each.content}}</li>
            {%endfor%}
        </ul>
    {% endblock %}
        """

        with open(template_dir + "/" + template_name, "w") as f:
            f.write(html_template_content)
        return render_template(template_name, categories=categories_list, data=bitcontent)


@app.route("/aboutus")
def aboutus():
    return render_template("aboutus.html")


# run server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
