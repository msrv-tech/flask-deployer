import paramiko

def deploy_script(vm_ip, ssh_user, ssh_key_path, repo_url):
    try:
        # Копирование скрипта
        scp = paramiko.Transport((vm_ip, 22))
        scp.connect(username=ssh_user, pkey=paramiko.RSAKey.from_private_key_file(ssh_key_path))
        sftp = paramiko.SFTPClient.from_transport(scp)
        sftp.put('setup_flask.sh', '/tmp/setup_flask.sh')
        sftp.close()

        # Запуск скрипта
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(vm_ip, username=ssh_user, key_filename=ssh_key_path)
        stdin, stdout, stderr = ssh.exec_command('chmod +x /tmp/setup_flask.sh && /tmp/setup_flask.sh')
        output = stdout.read().decode()
        error = stderr.read().decode()
        ssh.close()
        
        return True, f"Успешно!\n{output}"
    
    except Exception as e:
        return False, f"Ошибка: {str(e)}"