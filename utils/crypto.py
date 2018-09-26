from base64 import b64encode
import hashlib

SALT = 'luckyyou'


def string2md5(s, salt=SALT):
    h1 = hashlib.md5()
    h1.update((s+salt).encode(encoding='utf-8'))
    return h1.hexdigest()


def string2base64withsalt(s, salt=SALT):
    salt_int = int(b64encode(salt.encode('utf-8')).decode('utf-8'), 16)
    s_int = int(b64encode(s), 16)
    return hex(salt_int + s_int)[2:]
