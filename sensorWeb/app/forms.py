from flask.ext.wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import Required

class LoginForm(Form):
    userid = TextField('userid', validators = [Required()])
    passwd = PasswordField('passwd', validators = [Required()])
