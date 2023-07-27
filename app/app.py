#!/usr/bin/python3
from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)


@app.route("/")
def initial():
    return redirect(url_for("home"))


@app.route("/home")
def home():
    return render_template("home.html")


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
