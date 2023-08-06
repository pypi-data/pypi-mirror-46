import os
import click
import paramiko


@click.command()
@click.option("-f", "--file", help="File path and name.", required=True)
@click.option("-h", "--host", help="Host address.", required=True)
@click.option("-p", "--port", help="Server's port.", required=True)
@click.option("-u", "--user", help="Username.", required=True)
@click.option("-pw", "--password", help="SSH Passwrd.", required=True)
def main(file, host, port, user, password):
    """Function to get executed through CLI"""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, port=port, username=user, password=password)
    sftp = client.open_sftp()  # open SFTP connection for file transfer
    file_name = file.split("/")[-1]  # take last element after split
    file_location = f"/tmp/{file_name}"
    sftp.put(file, file_location)  # transfer local file to SSH
    sftp.close()

    # execute command and loop through stdin
    stdout = client.exec_command(f"python {file_location}")[1]
    for line in stdout.read().splitlines():
        print(line)

    client.close()
