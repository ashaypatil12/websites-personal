import wtf as wtf
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired
import requests


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///moves_database.db'
db = SQLAlchemy(app)
all_movies = []

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=False, nullable=False)
    year = db.Column(db.Integer, unique=True, nullable=False)
    description = db.Column(db.String(800), unique=False, nullable=False)
    rating = db.Column(db.Integer, primary_key=False)
    ranking = db.Column(db.Integer, primary_key=False)
    review = db.Column(db.String(80), unique=False, nullable=False)
    img_url = db.Column(db.String(80), unique=False, nullable=False)

db.create_all()

class RateMovieForm(FlaskForm):
    rating = StringField("Your Rating Out of 10 e.g. 7.5")
    review = StringField("Your Review")
    submit = SubmitField("Done")

class AddMovieForm(FlaskForm):
    title = StringField(validators=[validators.input_required()])
    year = IntegerField(validators=[validators.input_required(), validators.number_range(min=1800, max=2021)])
    description = StringField(validators=[validators.input_required()])
    rating = FloatField(validators=[validators.input_required(), validators.number_range(min=0, max=10)])
    ranking = IntegerField(validators=[validators.input_required(), validators.number_range(min=1, max=10)])
    review = StringField(validators=[validators.input_required()])
    img_url = StringField(validators=[validators.URL(), validators.input_required()])
    submit = SubmitField("Add")

@app.route("/")
def home():
    all_movies = Movie.query.all()
    return render_template("index.html", movies=all_movies)


@app.route("/edit", methods=["GET", "POST"])
def rate_movie():
    form = RateMovieForm()
    movie_id = request.args.get("id")
    movie = Movie.query.get(movie_id)
    if form.validate_on_submit():
        movie.rating = float(form.rating.data)
        movie.review = form.review.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", movie=movie, form=form)


@app.route("/delete", methods=["GET", "POST"])
def delete_movie():
    movie_id = request.args.get("id")
    movie_to_delete = Movie.query.get(movie_id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return render_template("index.html")


@app.route("/add", methods=["GET", "POST"])
def add_movie():
    form = AddMovieForm()
    movie = Movie.query.all()
    if form.validate_on_submit():
        new_movie = Movie(title=form.title.data, year=form.year.data, description=form.description.data,
                          rating=float(form.rating.data), ranking=form.ranking.data,
                          review=form.review.data, img_url=form.img_url.data)
        all_movies.append(new_movie)
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add.html", form=form)

# @app.route()
# @app.route("/add", methods=["GET", "POST"])
# def add_movie():
#     form = AddMovieForm()
#     movie = Movie.query.all()
#     if form.validate_on_submit():
#         new_movie = Movie(title=form.title.data, year=form.year.data, description=form.description.data,
#                           rating=float(form.rating.data), ranking=form.ranking.data,
#                           review=form.review.data, img_url=form.img_url.data)
#         all_movies.append(new_movie)
#         db.session.add(new_movie)
#         db.session.commit()


if __name__ == '__main__':
    app.run(debug=True)
