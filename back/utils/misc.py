from mariadb import Error as AnyDatabaseError

def error(msg, status=500):
    return {"error": msg}, status

def success(body={"pcachin": False}, status=200):
    return body, status

def retry_on_db_error(exc):
    if isinstance(exc, AnyDatabaseError):
        from .. import db
        print(f"Retrying after db error: {exc}", flush=True)
        db.connect()
        return True
    return False

# def generate_token(user):
#     m = hashlib.sha256()
#     m.update(f"{user.password}{user.email}{time.time()}".encode('utf-8'))
#     return str(m.digest())