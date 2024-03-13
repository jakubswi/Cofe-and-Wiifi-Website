from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField, RadioField
from wtforms.validators import DataRequired
import os

API_KEY = os.environ.get("google_API_KEY")
app = Flask(__name__)
Bootstrap5(app)
db = SQLAlchemy()
app.config['SECRET_KEY'] = os.environ.get("secret_key")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cafes.db"
db.init_app(app)


def change_to_bool(input):
    if input == 'True':
        return True
    else:
        return False


class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    coffee_price = db.Column(db.String(250), nullable=False)


class AddCafe(FlaskForm):
    name = StringField('Name of Cafe', validators=[DataRequired()])
    map_url = URLField('Map URL', validators=[DataRequired()])
    img_url = URLField('Blog Image URL', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    has_sockets = RadioField('Has sockets', choices=[(True, "Does have sockets"), (False, "Doesn't have sockets")])
    has_toilet = RadioField('Has a toilet', choices=[(True, "Does have sockets"), (False, "Doesn't have sockets")])
    has_wifi = RadioField('Has WIFI', choices=[(True, "Does have Wifi"), (False, "Doesn't have Wifi")])
    can_take_calls = RadioField('Can take calls',
                                choices=[(True, "You can take calls"), (False, "You can't take calls")])
    seats = StringField('Seats', validators=[DataRequired()])
    coffee_price = StringField('Coffee price', validators=[DataRequired()])
    submit = SubmitField('Submit')


with app.app_context():
    db.create_all()


@app.route('/')
def main_page():
    result = db.session.execute(db.select(Cafe)).scalars().all()
    posts = [post for post in result]
    return render_template("index.html", all_posts=posts)


@app.route('/<id>')
def show_post(id):
    requested_post = db.session.execute(db.select(Cafe).where(Cafe.id == id)).scalar()
    return render_template("cafe.html", post=requested_post, API_KEY=API_KEY)


@app.route('/add-new-post', methods=["GET", "POST"])
def add_new_post():
    try:
        form = AddCafe()
        if request.method == "POST":
            new_post = Cafe(name=request.form["name"],
                            map_url=request.form["map_url"],
                            img_url=request.form["img_url"],
                            location=request.form['location'],
                            has_sockets=bool(request.form['has_sockets']),
                            has_toilet=bool(request.form['has_toilet']),
                            has_wifi=bool(request.form['has_wifi']),
                            can_take_calls=bool(request.form['can_take_calls']),
                            seats=request.form['seats'],
                            coffee_price=request.form['coffee_price'])
            db.session.add(new_post)
            db.session.commit()
            return url_for('main_page')
    except sqlite3.IntegrityError:
        return url_for('main_page')
    return render_template('make-post.html', form=form)


@app.route('/<id>/edit-post', methods=["GET", "POST"])
def edit_new_post(id):
    post = db.session.execute(db.select(Cafe).where(Cafe.id == id)).scalar()
    edit_form = AddCafe(
        name=post.name,
        map_url=post.map_url,
        img_url=post.img_url,
        location=post.location,
        has_sockets=post.has_sockets,
        has_toilet=post.has_toilet,
        has_wifi=post.has_wifi,
        can_take_calls=post.can_take_calls,
        seats=post.seats,
        coffee_price=post.coffee_price
    )
    if request.method == "POST":
        post.name = request.form["name"]
        post.map_url = request.form["map_url"]
        post.img_url = request.form["img_url"]
        post.location = request.form['location']
        post.has_sockets = change_to_bool(request.form['has_sockets'])
        post.has_toilet = change_to_bool(request.form['has_toilet'])
        post.has_wifi = change_to_bool(request.form['has_wifi'])
        post.can_take_calls = change_to_bool(request.form['can_take_calls'])
        post.seats = request.form['seats']
        post.coffee_price = request.form['coffee_price']
        db.session.commit()
        return redirect(f'/{id}')

    return render_template('make-post.html', form=edit_form, is_edit=True)


if __name__ == "__main__":
    app.run(debug=False)
