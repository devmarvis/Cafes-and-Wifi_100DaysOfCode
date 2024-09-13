from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float, Boolean


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///cafes.db"
db.init_app(app)


class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)

    def to_dict(self):

        dictionary = {}

        for col in self.__table__.columns:
            dictionary[col.name] = getattr(self, col.name)

        return dictionary


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/cafes")
def cafes():
    with app.app_context():
        cafes_ = db.session.execute(db.select(Cafe)).scalars().all()
    return render_template("cafes.html", cafes=cafes_)


@app.route("/add-cafe", methods=['POST', 'GET'])
def add_cafe():
    if request.method == 'POST':
        name = request.form['cafe_name']
        location = request.form['cafe_location']
        url = request.form['cafe_url']
        img = request.form['cafe_img']
        price = request.form['coffee_price']
        toilets = request.form['toilets_aval']
        sockets = request.form['sockets_aval']
        wifi = request.form['wifi_aval']
        calls = request.form['calls_allow']
        seats = request.form['seats_capacity']

        with app.app_context():
            db.create_all()
            new_cafe = Cafe(
                name=name,
                map_url=url,
                img_url=img,
                location=location,
                seats=seats,
                has_toilet=bool(int(toilets)),
                has_sockets=bool(int(sockets)),
                has_wifi=bool(int(wifi)),
                can_take_calls=bool(int(calls)),
                coffee_price=price
            )
            db.session.add(new_cafe)
            db.session.commit()
            return redirect(url_for('cafes'))
    return render_template("add-cafe.html")


@app.route("/remove/<cafe_name>")
def remove(cafe_name):
    print(cafe_name)
    with app.app_context():
        cafe_to_remove = db.session.execute(db.select(Cafe).where(Cafe.name == cafe_name)).scalars().first()
        db.session.delete(cafe_to_remove)
        db.session.commit()
        print('Cafe successfully removed!')
    return redirect(url_for('cafes'))


if __name__ == '__main__':
    app.run(debug=True)
