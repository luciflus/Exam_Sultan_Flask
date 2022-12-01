from app import app
from flask_wtf import FlaskForm
import wtforms as ws
from .models import Employee, User

class EmployeeForm(FlaskForm):
    fullname = ws.StringField('ФИО Сотрудника', validators=[ws.validators.DataRequired(), ])
    phone = ws.TelField('Номер телефона', validators=[ws.validators.DataRequired(), ])
    short_info = ws.TextAreaField('Краткая информация', validators=[ws.validators.DataRequired(), ])
    experience = ws.IntegerField('Опыт работы', validators=[ws.validators.DataRequired(), ])
    preferred_position = ws.StringField('Предпочитаемая позиция')
    user_name = ws.SelectField('Пользователь', choices=[])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_choices = []
        with app.app_context():
            for user in User.query.all():
                self.user_choices.append((user.username))
        self._fields['user_name'].choices = self.user_choices

    def validate_fullname(self, field):
        names_split = field.data.split(' ')
        print(names_split)
        if len(names_split) == 1:
            raise ws.ValidationError('ФИО не может состоять из 1го слова')
        for name in names_split:
            if not name.isalpha():
                raise ws.ValidationError('Имя должно состоять из букв')

class UserForm(FlaskForm):
    username = ws.StringField('Имя пользователя', validators=[
        ws.validators.DataRequired(),
        ws.validators.Length(min=4, max=20)
    ])
    password = ws.PasswordField('Пароль', validators=[
        ws.validators.DataRequired(),
        ws.validators.Length(min=8, max=24)
    ])
