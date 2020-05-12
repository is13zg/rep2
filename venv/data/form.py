from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    clas = StringField('Класс', validators=[DataRequired()])
    occupation = StringField('Вы учитель? Введите "да" или "нет" без кавычек.', validators=[DataRequired()])
    submit = SubmitField('Войти')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class TestsForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    subject = StringField("Предмет", validators=[DataRequired()])
    count_of_questions = StringField("Количество вопросов", validators=[DataRequired()])
    user_id = StringField("Ваш персональные номер", validators=[DataRequired()])
    submit = SubmitField('Добавить вопросы')


class TasksForm(FlaskForm):
    title = StringField('Вопрос', validators=[DataRequired()])
    ans1 = StringField("Вариант ответа 1", validators=[DataRequired()])
    ans2 = StringField("Вариант ответа 2", validators=[DataRequired()])
    ans3 = StringField("Вариант ответа 3", validators=[DataRequired()])
    ans4 = StringField("Вариант ответа 4", validators=[DataRequired()])
    correct_answer = StringField("Номер верного ответа", validators=[DataRequired()])
    submit = SubmitField('Добавить вопрос')


class AnserForm(FlaskForm):
    submit = SubmitField('Ответить')



