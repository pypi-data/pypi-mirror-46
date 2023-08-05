import nacl.pwhash
import nacl.secret
import nacl.utils


def kdf(password):
    salt = b'PASSPASSWHEELEEE'
    return nacl.pwhash.argon2i.kdf(
        nacl.secret.SecretBox.KEY_SIZE,
        password,
        salt,
        opslimit=nacl.pwhash.argon2i.OPSLIMIT_SENSITIVE,
        memlimit=nacl.pwhash.argon2i.MEMLIMIT_SENSITIVE,
    )


def encrypt(password, message):
    key = kdf(password)
    box = nacl.secret.SecretBox(key)
    return box.encrypt(message)


def decrypt(password, message):
    key = kdf(password)
    box = nacl.secret.SecretBox(key)
    return box.decrypt(message)
