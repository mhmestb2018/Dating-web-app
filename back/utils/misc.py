def error(msg, status=500):
    return {"error": msg}, status

def success(body={"pcachin": True}, status=200):
    return body, status

# def generate_token(user):
#     m = hashlib.sha256()
#     m.update(f"{user.password}{user.email}{time.time()}".encode('utf-8'))
#     return str(m.digest())