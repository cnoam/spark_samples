# test ssh command to the spark cluster
#
# pip install ssh2-python
import socket

from ssh2.session import Session


def ssh2_ssh(host, port, user, password, command):
    # Make socket, connect
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    # Initialise
    session = Session()
    session.handshake(sock)

    session.userauth_password(user, password)

    # Public key blob available as identities[0].blob

    # Channel initialise, exec and wait for end
    channel = session.open_session()
    channel.execute(command)
    channel.wait_eof()
    channel.close()
    channel.wait_closed()

    # Print output
    output = b''
    size, data = channel.read()
    while size > 0:
        output += data
        size, data = channel.read()

    # Get exit status
    output = output.decode("utf-8").strip()
    print(f'{host}, {output}, {channel.get_exit_status()}')
    return output

if __name__ == "__main__":
    #o = ssh2_ssh("noam-c3-ssh.azurehdinsight.net", port=22, user="sshuser", password="%Qq12345678", command="yarn top")
    o = ssh2_ssh("localhost", port=22, user="cnoam", password=None, command="ls")
    #print(o)
    

