from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    IntegerField,
    DateField,
    TextAreaField,
)

from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Length, EqualTo, Email, Regexp, Optional, NumberRange
import email_validator
from flask_login import current_user
from wtforms import ValidationError, validators
from models import User


class login_form(FlaskForm):
    student_id = StringField(validators=[
        InputRequired(message="아이디는 필수 입력사항입니다!"),
        Length(min=4, max=12, message="아이디는 4~12자 사이여야 합니다.")
    ])
    password = PasswordField(validators=[
        InputRequired(message="비밀번호는 필수 입력사항입니다!"),
        Length(min=4, max=8, message="비밀번호는 4~8자 사이여야 합니다.")
    ])

    # Placeholder labels to enable form rendering
    name = StringField(validators=[Optional()])
    phone_number = StringField(validators=[Optional()])
    school_name = StringField(validators=[Optional()])
    grade = StringField(validators=[Optional()])
    class_no = StringField(validators=[Optional()])


class register_form(FlaskForm):
    """ Registration form"""

    student_id = StringField(validators=[
        InputRequired(message="아이디는 필수 입력사항입니다!"),
        Length(min=4, max=12, message="아이디는 4~12자 사이여야 합니다.")
    ])
    name = StringField(validators=[InputRequired(message="이름는 필수 입력사항입니다!")])
    phone_number = StringField(validators=[
        InputRequired(message="전화번호는 필수 입력사항입니다!"),
        Length(min=11, max=12, message="전화번호는 11~12자 사이여야 합니다 (숫자만 - 없음)."),
    ])
    school_name = StringField(
        'school_name', validators=[InputRequired(message="학교는 필수 입력사항입니다!")])
    grade = StringField(validators=[
        InputRequired(message="학년는 필수 입력사항입니다!"),
        Length(min=1, max=3, message="학년는 1~3자 사이여야 합니다."),
    ])
    class_no = StringField(validators=[
        InputRequired(message="반는 필수 입력사항입니다!"),
        Length(min=1, max=3, message="반는 1~3자 사이여야 합니다.")
    ])
    password = PasswordField(validators=[
        InputRequired(message="비밀번호는 필수 입력사항입니다!"),
        Length(min=4, max=8, message="비밀번호는 4~8자 사이여야 합니다.")
    ])

    def validate_student_id(self, student_id):
        if User.query.filter_by(student_id=student_id.data).first():
            raise ValidationError("사용자가 이미 존재 합니다")