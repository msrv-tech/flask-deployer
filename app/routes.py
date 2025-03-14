from flask import render_template, request, redirect, url_for
from app import app
from app.forms import DeploymentForm
from app.utils.deploy import deploy_script

@app.route('/', methods=['GET', 'POST'])
def index():
    form = DeploymentForm()
    if form.validate_on_submit():
        result = deploy_script(
            form.vm_ip.data,
            form.ssh_user.data,
            form.ssh_key_path.data,
            form.repo_url.data
        )
        return redirect(url_for('result', success=result[0], message=result[1]))
    return render_template('index.html', form=form)

@app.route('/result')
def result():
    success = request.args.get('success', type=bool)
    message = request.args.get('message', '')
    return render_template('result.html', success=success, message=message)