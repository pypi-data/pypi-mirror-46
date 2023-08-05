import os
import getpass
from cryptography.fernet import Fernet


homedir_path = os.getenv('HOME')
folder_path = homedir_path + '/.ezissue/'
hub_path = folder_path + 'hub'
lab_path = folder_path + 'lab'


def create_secure_key():
    check_folder_structure(folder_path)
    path = folder_path + 'key.key'

    if os.path.isfile(path):        # this can be bugged
        return False
    else:
        key = Fernet.generate_key()
        file = open(path, 'wb+')
        file.write(key)
        file.close()
        return True


def get_key():
    file = open(folder_path + 'key.key', 'rb')
    k = file.readline()
    return k


def check_folder_structure(full_path):
    if not os.path.exists(full_path):
        os.makedirs(full_path)


def encrypt(line):
    k = get_key()
    f = Fernet(k)
    return f.encrypt(line)


def decrypt_token(encrypted_line):
    k = get_key()
    f = Fernet(k)
    return f.decrypt(encrypted_line)


def write_tokens(github_key, gitlab_key):
    fp = hub_path
    fp2 = lab_path

    check_folder_structure(folder_path)

    enc_gh = encrypt(github_key.encode())
    enc_gl = encrypt(gitlab_key.encode())

    try:
        file = open(fp, "wb+")
        file2 = open(fp2, "wb+")
        file.write(enc_gh)
        file2.write(enc_gl)
    finally:
        file.close()
        file2.close()

    return (os.path.isfile(fp) and os.path.isfile(fp2))


def get_token(repo_manager):
    if repo_manager == 'github':
        file = open(hub_path, 'rb')
        enc = file.read()
        token = decrypt_token(enc)
        return token.decode()
    elif repo_manager == 'gitlab':
        file = open(lab_path, 'rb')
        enc = file.read()
        token = decrypt_token(enc)
        return token.decode()
    # else:
        # it would be nice to raise an exception here btw
