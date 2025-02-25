from flask import Flask, render_template, url_for, redirect, request, flash
from flask_bootstrap import Bootstrap5
from flask_hashing import Hashing
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import relationship

app = Flask(__name__)


app.config["SECRET_KEY"] = "your_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///computer_parts.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
bootstrap=Bootstrap5(app)
# Models
class Manufacturer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    country = db.Column(db.String(100), nullable=False)
    parts = db.relationship("Part", backref="manufacturer", lazy=True)

    def __repr__(self):
        return f"Manufacturer('{self.name}', '{self.country}')"

class Part(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    manufacturer_id = db.Column(db.Integer, db.ForeignKey("manufacturer.id"), nullable=False)

    def __repr__(self):
        return f"Part('{self.name}', '{self.category}', ${self.price})"

@app.route("/")
def index():
    parts = Part.query.all()
    return render_template("parts.html", parts=parts)

@app.route("/add_part", methods=["GET", "POST"])
def add_part():
    if request.method == "POST":
        name = request.form["name"]
        category = request.form["category"]
        price = request.form["price"]
        manufacturer_name = request.form["manufacturer_name"]

        manufacturer = Manufacturer.query.filter_by(name=manufacturer_name).first()
        if not manufacturer:
            manufacturer = Manufacturer(name=manufacturer_name, country="Unknown")
            db.session.add(manufacturer)
            db.session.commit()

        new_part = Part(name=name, category=category, price=float(price), manufacturer_id=manufacturer.id)
        db.session.add(new_part)
        db.session.commit()
        flash("Part added successfully!", "success")
        return redirect(url_for("index"))

    return render_template("add_parts.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
