from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, TextAreaField, FloatField
from wtforms.validators import DataRequired, Length, NumberRange, EqualTo, URL

class AddMovieForm(FlaskForm):
    title_ka = StringField("სათაური (KA)", validators=[DataRequired(message="შეიყვანეთ ქართული სათაური")])
    title_en = StringField("Title (EN)", validators=[DataRequired(message="Enter English title")])

    description_ka = TextAreaField("აღწერა (KA)", validators=[DataRequired(), Length(min=10)])
    description_en = TextAreaField("Description (EN)", validators=[DataRequired(), Length(min=10)])

    director = StringField("Director", validators=[DataRequired()])
    year = IntegerField("Year", validators=[DataRequired(), NumberRange(min=1888, max=2026)])

    genre = StringField("Genre (გამოყავით მძიმით)", validators=[DataRequired()])

    img_url = StringField("Image URL", validators=[DataRequired(), URL(message="შეიყვანეთ ვალიდური სურათის ლინკი")])

    movie_url = StringField(" Movie URL", validators=[DataRequired(), URL(message="შეიყვანეთ ვალიდური ფილმის ლინკი")])

    rating = FloatField("Rating (0-10)", validators=[
        DataRequired(),
        NumberRange(min=0, max=10, message="რეიტინგი უნდა იყოს 0-დან 10-მდე")
    ])

    submit = SubmitField("Add Movie / ფილმის დამატება")


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[
        DataRequired(),
        Length(min=4, max=20, message="სახელი უნდა იყოს 4-დან 20 სიმბოლომდე")
    ])
    password = PasswordField("Password", validators=[
        DataRequired(),
        Length(min=6, message="პაროლი უნდა იყოს მინიმუმ 6 სიმბოლო")
    ])
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")