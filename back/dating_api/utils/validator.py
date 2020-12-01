import types

from .errors import InvalidData
from ..models.sexs import Sexs
from ..models.orientations import Orientations

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
            raise InvalidData(f"Le nom {val} est trop court (< 2)")
        if len(val) > limit:
            raise InvalidData(f"Le nom {val} est trop long (> {limit})")
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
        if len(tmp) < 2 or len(tmp[0]) < 2 or len(tmp[-1]) < 2 or len(name) < 2:
            raise InvalidData(f"{val} n'est pas un email valide")
        if len(tmp[-1]) > 4:
            raise InvalidData(f"{val} n'est pas un email valide (extention '.{tmp[-1]}' trop longue)")
        if tmp[-2] is "gmail":
            name = "".join(name.split("."))
        return f"{name}@{provider}"

    @staticmethod
    @printable
    def orientation(val:str):
        val = val.lower()

        for k in Orientations.available:
            if val in Orientations.available[k]["accepted"]:
                return k

        raise InvalidData(f'{val} is an uncommon orientation, please use "other" if nothing else fits')

    @staticmethod
    @printable
    def sex(val:str):
        val = val.lower()

        for k in Sexs.available:
            if val in Sexs.available[k]["accepted"]:
                return k

        raise InvalidData(f'{val} is an uncommon sex, please use "other" if nothing else fits')

    @staticmethod
    @printable
    def bio(val, limit=4000):
        if len(val) <= limit:
            return val
        raise InvalidData(f"bio is too long (>{limit} chars)")

    @staticmethod
    @printable
    def password(val):
        return val

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

    @staticmethod
    def last_seen(val):
        return val

    @staticmethod
    def coord(val):
        val = float(val)
        if val < -180.0 or val > 180.0:
            raise InvalidData(f"Coordonnées géographiques incorrects")
        return float(val)

    @staticmethod
    def lat(val):
        return Validator.coord(val)

    @staticmethod
    def lon(val):
        return Validator.coord(val)

    @staticmethod
    def age(val):
        val = int(val)
        if val < 18:
            raise InvalidData(f"Il y a trop de pédophiles ici pour toi")
        elif val > 120:
            raise InvalidData(f"Jeanne Calment, elle a plus mal au dents...")
        return val

    @staticmethod
    def tag(val):
        return Validator.name(val, limit=99).lower()
