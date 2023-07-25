#!/usr/bin/python3
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/technology")
def technology():
    return render_template("technology.html")


@app.route("/entertainment")
def entertainment():
    return render_template("entertainment.html")


@app.route("/fashion")
def fashion():
    return render_template("fashion.html")


@app.route("/aboutus")
def aboutus():
    return render_template("aboutus.html")


if __name__ == "__main__":
    app.run(port=3036, debug=True)
