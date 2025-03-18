from flask import render_template, redirect, url_for, flash

from app import app
from app.utils.forms import DeploymentForm
import paramiko
import os

@app.route('/', methods=['GET', 'POST'])
def index():
    form = DeploymentForm()
    return render_template('index.html', form=form)

@app.route('/deploy', methods=['POST'])
def deploy():
    form = DeploymentForm()
    print(f"\n=== Данные формы ===")  # Логирование
    print(f"Server IP: {form.server_ip.data}")
    print(f"Username: {form.username.data}")
    print(f"Password: {form.password.data}")
    print(f"Валидна ли форма: {form.validate_on_submit()}")

    if form.validate_on_submit():
        server_ip = form.server_ip.data
        username = form.username.data
        password = form.password.data

        print(f"\n=== Попытка подключения к {server_ip} ===")

        try:
            # Подключение SSH
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=server_ip, username=username, password=password)
            print("[SSH] Подключение успешно")
            flash('Connected successfully!', 'success')

            # Копирование скрипта
            try:
                print("\n=== Копирование скрипта ===")
                sftp = ssh.open_sftp()  # Используем текущее соединение
                sftp.put('setup_flask.sh', '/tmp/setup_flask.sh')
                sftp.close()
                print("[SFTP] Скрипт скопирован")
                flash('Script uploaded!', 'success')
            except Exception as e:
                print(f"[SFTP] Ошибка: {str(e)}")
                flash(f'Copy failed: {str(e)}', 'danger')
                return redirect(url_for('index'))

            # Запуск скрипта
            try:
                print("\n=== Запуск скрипта ===")
                stdin, stdout, stderr = ssh.exec_command('chmod +x /tmp/setup_flask.sh && /tmp/setup_flask.sh')
                output = stdout.read().decode()
                error = stderr.read().decode()

                print(f"[EXEC] Вывод: {output}")
                if error:
                    print(f"[EXEC] Ошибки: {error}")
                    flash(f'Ошибка: {error}', 'danger')
                else:
                    flash(f'Успех! Вывод: {output}', 'success')

            except Exception as e:
                print(f"[EXEC] Ошибка: {str(e)}")
                flash(f'Execution error: {str(e)}', 'danger')

            finally:
                ssh.close()

        except paramiko.AuthenticationException:
            print("[SSH] Ошибка аутентификации")
            flash('Auth failed!', 'danger')
        except Exception as e:
            print(f"[SSH] Ошибка: {str(e)}")
            flash(f'Connection error: {str(e)}', 'danger')

    else:
        print("\n=== Ошибки формы ===")
        for field, errors in form.errors.items():
            for error in errors:
                print(f"[FORM] {field}: {error}")
                flash(f'{field}: {error}', 'danger')

    return redirect(url_for('index'))