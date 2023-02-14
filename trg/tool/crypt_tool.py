
from cryptography.fernet import Fernet


class Crypt_Decrypt_Tool:
    # string translate to bytes,we can use str.encode(string) ----> bytes
    # bytes  translate to string,we can use bytes.decode()    ----> string
    def __init__(self,key=None):
        if not key:
            self.key = Fernet.generate_key()
        else:
            self.key = key                     # key must be same between use encrypted_pwd and decrypted_pwd

    def encrypt_pwd(self, passwd):              # passwd type must be bytes
        f = Fernet(self.key)
        encrypted_pwd =  f.encrypt(passwd)
        return encrypted_pwd                  # encrypted_pwd also bytes


    def decrypt_pwd(self, encrypted_pwd):      # encrypted_pwd must be bytes
        f = Fernet(self.key)
        decrypted_pwd = f.decrypt(encrypted_pwd)
        return decrypted_pwd                 # decrypted_pwd also bytes


    def get_key(self):
        return self.key