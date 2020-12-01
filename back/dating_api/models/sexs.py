from enum import Enum

class Sexs():
    class Gender(Enum):
        MALE = 0
        FEMALE = 0
        OTHER = 0

    class GenderType(Enum):
        CIS = 0
        TRANS = 1
        OTHER = 2

    available = {
        "cis-male": {
            "accepted": ["m", "h", "homme", "male", "mec", "guy", "pelo", "bite", "phallus", "penis"],
            "gender": Gender.MALE,
            "gender_type": GenderType.CIS,
        },
        "cis-female": {
            "accepted": ["f", "female", "femme", "meuf", "boobs", "chatte", "fouffe", "teucha"],
            "gender": Gender.FEMALE,
            "gender_type": GenderType.CIS,
        },
        "trans-male": {
            "accepted": ["transexuel", "trans male", "homme trans"],
            "gender": Gender.MALE,
            "gender_type": GenderType.TRANS,
        },
        "trans-female": {
            "accepted": ["transexuelle", "trans female", "shemale", "femme trans"],
            "gender": Gender.FEMALE,
            "gender_type": GenderType.TRANS,
        },
        "non-binary": {
            "accepted": ["non binaire", "non-binary", "ternary", "bien au contraire"],
            "gender": Gender.OTHER,
            "gender_type": GenderType.OTHER,
        },
        "other": {
            "accepted": ["autre", "other"],
            "gender": Gender.OTHER,
            "gender_type": GenderType.OTHER,
        }
    }
    
    @staticmethod
    def get():
        return Sexs.available.keys

    @staticmethod
    def same(name):
        res = []
        if name in Sexs.available.keys:
            gender = Sexs.available[name].gender_type
            for k in Sexs.available.keys:
                if Sexs.available[k].gender_type == gender:
                    res.append(k)
        if len(res) == 0:
            return [name]
        return res

    @staticmethod
    def opposite(name):
        res = []
        if name in Sexs.available.keys:
            gender = Sexs.available[name].gender_type
            for k in Sexs.available.keys:
                if Sexs.available[k].gender_type != gender:
                    res.append(k)
        if len(res) == 0:
            return [name]
        return res
