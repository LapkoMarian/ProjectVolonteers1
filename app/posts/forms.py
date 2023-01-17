from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, BooleanField, IntegerField
from wtforms.validators import Length, DataRequired, InputRequired
from flask_wtf.file import FileField, FileAllowed


class CreatePostForm(FlaskForm):
    title = StringField('Назва', validators=[InputRequired(), Length(min=5, max=70)])
    category = SelectField(u'Виберіть категорію', coerce=int)
    text = TextAreaField('Опис', validators=[InputRequired(), Length(min=30, max=5000)])
    picture = FileField('Виберіть фото', validators=[FileAllowed(['jpg', 'png'])])
    phone = StringField('Номер телефону', validators=[InputRequired(), Length(min=10, max=20)])
    city = SelectField(u'Виберіть місто', coerce=int)
    status = SelectField(u'Актуальність', coerce=int)
    submit = SubmitField('')


class CategoryForm(FlaskForm):
    name = StringField('Категорія', validators=[DataRequired(), Length(min=0, max=120)])
    submit = SubmitField('')


class CityForm(FlaskForm):
    city = StringField('Місто', validators=[DataRequired(), Length(min=0, max=120)])
    submit = SubmitField('')


class StatusForm(FlaskForm):
    status = StringField('Актуальність', validators=[DataRequired(), Length(min=0, max=30)])
    submit = SubmitField('')
