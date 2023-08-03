#!/usr/bin/python3
from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

basedir = os.path.abspath(os.path.dirname(__file__))

# Init app
app = Flask(__name__, template_folder="templates")
app.config['TEMPLATES_AUTO_RELOAD'] = True

# test
print("this is where the template folder is: ", app.template_folder)
print("this is where the base directory is: ", basedir)


# Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + \
    os.path.join(basedir, "db.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Init db
db = SQLAlchemy(app)

# Init ma
ma = Marshmallow(app)

# bitcontent Class/Model


class Bitcontent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200))
    category_name = db.Column(db.String(50), db.ForeignKey(
        "category.name"), nullable=False)

    category = db.relationship(
        "Category", backref=db.backref("bitcontent", lazy=True))

    def __init__(self, category_name, content):
        self.category = category_name
        self.content = content


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    def __repr__(self):
        return "<Category %r>" % self.name

# bitcontent Schema


class BitcontentSchema(ma.Schema):
    class Meta:
        fields = ("id", "category_name", "content")


class CategorySchema(ma.Schema):
    class Meta:
        fields = ("id", "name")


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
        print("yo00000!!!!!!!! bitcontent: ")
        bitcontent = Bitcontent.query.filter_by(
            category_name=category_name).all()
        print("yo00000!!!!!!!! bitcontent: ", bitcontent)
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
