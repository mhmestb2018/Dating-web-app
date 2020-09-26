import types

from .errors import InvalidData

def printable(fun):
    """
    printable decorator:
        1. raise exception if non printable parameter
    """

    def wrapper(val, **kwargs):
        if not val.isprintable():
            raise InvalidData(f"{fun.__name__}: caractères non-imprimables")
        return fun(val, **kwargs)

    if type(fun) is not types.FunctionType:
        raise ValueError()
    # To carry the name over and be able to register more than one route with this decorator
    wrapper.__name__ = fun.__name__
    return wrapper

class Validator():

    @staticmethod
    @printable
    def name(val, limit=32):
        if len(val) < 2:
            raise InvalidData(f"Le nom est trop court (< 2)")
        if len(val) > limit:
            raise InvalidData(f"Le nom est trop long (> {limit})")
        return val

    @staticmethod
    @printable
    def email(val):
        val = val.lower()
        tmp = val.split("@")
        if len(tmp) is not 2:
            raise InvalidData(f"{val} n'est pas un email valide ('@' manquant)")
        name = tmp[0].split("+")[0]
        provider = tmp[1]
        tmp = provider.split(".")
        if len(tmp) < 2:
            raise InvalidData(f"{val} n'est pas un email valide (extention manquante)")
        if len(tmp[-1]) > 4:
            raise InvalidData(f"{val} n'ets pas un email valide (extention '.{tmp[-1]}' trop longue)")
        if tmp[-2] is "gmail":
            name = "".join(name.split("."))
        return f"{name}@{provider}"

    @staticmethod
    @printable
    def orientation(val:str):
        val = val.lower()
        if val in ("straight", "hetero", "hétéro", "heterosexual", "heterosexuel", "hétérosexuel", "hétérosexuelle", "heterosexuelle"):
            return "heterosexual"
        if val in ("homosexual", "homosexuel", "homosexuelle", "gay", "lesbienne"):
            return "homosexual"
        if val in ("bisexuel", "bisexual"):
            return "bisexual"
        if val in ("asexual", "asexuel"):
            return "asexual"
        if val in ("autre", "other"):
            return "other"
        raise InvalidData(f"{val} is an uncommon sex")

    @staticmethod
    @printable
    def sex(val:str):
        val = val.lower()
        if val in ("m", "h", "homme", "male", "mec", "guy", "pelo", "bite", "phallus", "penis"):
            return "m"
        if val in ("f", "female", "femme", "meuf", "boobs", "chatte", "fouffe", "teucha"):
            return "f"
        if val in ("autre", "other"):
            return "other"
        raise InvalidData(f"{val} is an uncommon sex")

    @staticmethod
    @printable
    def bio(val, limit=4000):
        if len(val) <= limit:
            return val
        raise InvalidData(f"bio is too long (>{limit} chars)")

    @staticmethod
    @printable
    def password(val, limit=5):
        if len(val) >= limit:
            return val
        raise InvalidData(f"password is too short ({len(val)}<{limit} chars)")

    @staticmethod
    def path(val, limit=1024):
        if len(val.split('\x00')) > 1:
            raise InvalidData(f"image: adresse invalide")
        if len(val) > limit:
            raise InvalidData(f"path is too long ({len(val)}>{limit} chars)")
        return val
    
    picture_1 = picture_2 = picture_3 = picture_4 = picture_5 = path

    @staticmethod
    def first_name(val, limit=32):
        return Validator.name(val=val, limit=limit)

    @staticmethod
    def last_name(val, limit=32):
        return Validator.name(val=val, limit=limit)