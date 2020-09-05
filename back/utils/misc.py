from flask import jsonify

def error(msg):
    return jsonify({"error": msg})

def success():
    return jsonify({"pcachin": True})

# def generate_token(user):
#     m = hashlib.sha256()
#     m.update(f"{user.password}{user.email}{time.time()}".encode('utf-8'))
#     return str(m.digest())