from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm # Это базовый класс для создания форм
from wtforms import StringField, SubmitField # Это классы для создания полей внутри формы
from wtforms.validators import DataRequired # Валидатор, нуный для проверки
