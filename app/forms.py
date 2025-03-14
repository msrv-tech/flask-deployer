from flask_wtf import FlaskForm
from wtforms import StringField, validators

class DeploymentForm(FlaskForm):
    vm_name = StringField('Имя виртуальной машины', [validators.InputRequired()])
    vm_ip = StringField('IP-адрес', [validators.InputRequired(), validators.IPAddress()])
    ssh_user = StringField('SSH-пользователь', [validators.InputRequired()])
    ssh_key_path = StringField('Путь к SSH-ключу', [validators.InputRequired()])
    repo_url = StringField('Репозиторий скрипта', 
                         default='https://github.com/msrv-tech/flask-inventory.git',
                         validators=[validators.InputRequired(), validators.URL()])