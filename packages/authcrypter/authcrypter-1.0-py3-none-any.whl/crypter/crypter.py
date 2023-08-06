import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA

JWT_SECRET_KEY = 'a super secret code to test only'


class AESCipher(object):

    def __init__(self, key=JWT_SECRET_KEY):
        self.bs = 128
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, message):
        message = self._pad(message)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(message))

    def decrypt(self, message):
        message = base64.b64decode(message)
        iv = message[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(message[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s) - 1:])]


class AsymCipher:
    def __init__(self):
        pass

    def encrypt(self, public_key, message):
        key = RSA.importKey(public_key)
        cipher = PKCS1_OAEP.new(key)
        return cipher.encrypt(message.encode('latin1'))

    def decrypt(self, private_key, message):
        key = RSA.importKey(private_key)
        cipher = PKCS1_OAEP.new(key)
        return cipher.decrypt(message).decode('latin1')


if __name__ == '__main__':
    crypter = AESCipher()

    username = 'a user name to test'
    code = crypter.encrypt(username)
    print(code)

    decrypter = AESCipher()
    new_username = decrypter.decrypt(code)
    print(new_username)

    print(new_username == username, '\n')

    # Assymetric encryption
    public_key = '''-----BEGIN PUBLIC KEY-----
    MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCh9VhNMmTYVNEbNjzKKCdIcRoP
    ARH9T1bEtIFh4mvL4/758PD46DugEMcFYtrmNoIBeQ944ewu062sY+B6iZ1tPrtT
    JaO3MiSlEXPTiDor0hsW01PfvQHQXc6wNjIJgK/nQ9B22mq3sJCXLRVrj25O2TfD
    f2ZkobNKyYSzds/mQQIDAQAB
    -----END PUBLIC KEY-----'''
    asym_crypter = AsymCipher()
    encrypted = asym_crypter.encrypt(public_key, username)
    print(encrypted)

    private_key = '''-----BEGIN RSA PRIVATE KEY-----
MIICWwIBAAKBgQCh9VhNMmTYVNEbNjzKKCdIcRoPARH9T1bEtIFh4mvL4/758PD4
6DugEMcFYtrmNoIBeQ944ewu062sY+B6iZ1tPrtTJaO3MiSlEXPTiDor0hsW01Pf
vQHQXc6wNjIJgK/nQ9B22mq3sJCXLRVrj25O2TfDf2ZkobNKyYSzds/mQQIDAQAB
AoGASga9NJO7GlIyPbDdujz+L5NaqM8BbPnNnB0xIg9+2/O7QHzLd8mWL0Rb429a
xGzXoVq3IraI4KJqOGhyWy/5XxBuh6Hnu8E6xF4W4xYde5Nzg0JgYeJAem6kIsiD
aCYixTyZVC5m1NjcTc6qxz3nstOVyfdkvtgDRhtDb++iIk0CQQDrzAEtODaSdlLE
0B+mku63ldIixsZmxKtTXFp2NgFchISwMZgg+JgjKT3LAjtITAN3/xQVfs+YiXjf
XCMFJiA3AkEAr9XCEzngub4EAmE4e8ltCh6oOkaFymmCrhMv4FsPMh4TVWQmumCR
PGS4Q0LVi8tUwtJf34K8TIO7p+mev+lBRwJAehS+SzY+cugWBFYo/Oo39A76pAy8
LfsHJPq8z1U4sTjfJgYXWIK86f9xQcke/lh0t0z2jgaA3t3WGfavHvxVUwJAfvxf
Nsdb1oi2GInh4vQrPV26nKuFwBLG/7R3pQ3eQZGa4NZ9aaiH+xe6Q0knM9halICe
IKsoFhIlGjUMIwjvzQJAL4LR37cSJlbORfZnbOUHOoH4Kui0q2uB+yrlbs4qRCin
4CXAz9TmX3BZ+GY72XPwpf7v+EU5uzNkFvkzCmCtvQ==
-----END RSA PRIVATE KEY-----'''
    asym_decrypter = AsymCipher()
    decrypted = asym_decrypter.decrypt(private_key, encrypted)
    print(decrypted)
