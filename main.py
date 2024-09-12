from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float


app = Flask(__name__)


class Base(DeclarativeBase):
    pass


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/cafes")
def cafes():
    return render_template("cafes.html")


if __name__ == '__main__':
    app.run(debug=True)