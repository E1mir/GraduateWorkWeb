from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, _id):
        self.id = _id
        self.name = "Lol"
        self.type = "admin"


''' Very simple encryption functions'''


def encrypt_pass(normal_password):
    encrypted_password = ""
    for d_char in normal_password:
        d_ch_id = ord(d_char)
        enc_id = d_ch_id + 5
        e_char = chr(enc_id)
        encrypted_password += e_char
    return encrypted_password


def decrypt_pass(encrypted_password):
    decrypted_password = ""
    for e_char in encrypted_password:
        e_ch_id = ord(e_char)
        dec_id = e_ch_id - 5
        d_char = chr(dec_id)
        decrypted_password += d_char
    return decrypted_password


if __name__ == '__main__':
    password = "Hello World!"
    enc = encrypt_pass(password)
    print enc
    dec = decrypt_pass(enc)
    print dec
