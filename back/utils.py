import hashlib, time

def salt(param):
    b = (f"pcachin{param}").encode('utf-8')
    m = hashlib.sha256()
    m.update(b)
    return str(m.digest())

def generate_token(email, password):
    m = hashlib.sha256()
    m.update(f"{password}{email}{time.now()}".encode('utf-8'))
    return str(m.digest())