import mariadb, datetime
from flask import jsonify
from werkzeug.security import check_password_hash

from .. import db
from ..utils import Validator
from .tag import Tag
from ..utils.errors import InvalidData

class User():
    __fields__ = (
        "id", "first_name", "last_name", "email", "password", "sex",
        "orientation", "bio", "views_count", "likes_count",
        "picture_1", "picture_2", "picture_3", "picture_4", "picture_5",
        "validated", "banned", "last_seen", "age", "lat", "lon")
    __restricted_fields__ = ("id", "validated", "views_count", "likes_count", "last_seen")
    __private_fields__ = ("last_seen", "banned")

    def list_users(self):
        query = """
            SELECT
                *
            FROM
                users
                LEFT OUTER JOIN (likes a
                    INNER JOIN likes b
                        ON a.user_id = b.liked
                        AND a.liked = b.user_id
                        AND b.user_id=?)
                    ON users.id = a.user_id
                LEFT OUTER JOIN blocks
                    ON users.id = blocks.user_id
                    AND blocks.blocked=?
            WHERE
                blocks.user_id IS NULL
                AND b.user_id IS NULL
                AND users.validated=1
                AND users.id != ?
            """
        rows = db.fetch(query, (self.id, self.id, self.id))

        return [User.build_from_db_tuple(t).intro_as(self) for t in rows]

    @staticmethod
    def build_from_db_tuple(values):
        values = zip(User.__fields__, values)
        user = User(empty=True)
        for f, v in values:
            if "picture" in f:
                if v:
                    user.pictures.append(v)
            elif "count" in f:
                tmp = None
                if "views" in f:
                    tmp = v
                elif "likes" in f and tmp is not None:
                    user.score = float(v) / max(tmp, 1E-7)
            else:
                setattr(user, f, v)
        return user

    @staticmethod
    def get_user(**kwargs):
        rows = []
        if "email" in kwargs:
            email = Validator.email(kwargs['email'])
            query = "SELECT * FROM users WHERE email=?"
            rows = db.fetch(query, (email,))
        elif "user_id" in kwargs:
            query = "SELECT * FROM users WHERE id=?"
            rows = db.fetch(query, (kwargs['user_id'],))
        else:
            return None

        if len(rows) is 0:
            return None
    
        return User.build_from_db_tuple(rows[0])

    def __init__(self, user_id=None, first_name=None, last_name=None, email=None, password=None, empty=False):
        self.pictures = []
        self.orientation = None
        self.sex = None
        self.bio = None
        self.score = 0.0
        self.validated = 0
        self.lon = 0
        self.lat = 0
        self.last_seen = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        if not empty:
            self.first_name = Validator.name(first_name)
            self.last_name = Validator.name(last_name)
            self.email = Validator.email(email)
            self.password = Validator.password(password)
            self.id = user_id

    @staticmethod
    def create_user(first_name, last_name, email, hashed_password, validation_id):

        user = User(0, first_name, last_name, email, hashed_password)
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (?, ?, ?, ?)"
        user.id = db.exec(query, (first_name, last_name, email, hashed_password))

        query = "INSERT INTO validations (user_id, validation_id) VALUES (?, ?)"
        db.exec(query, (user.id, validation_id))

        return user

    def update(self, new_values:dict, force=False):
        reqs = []
        params = []

        new_values = dict(new_values)
        # Unpack pictures array:
        if "pictures" in new_values:
            pictures = []
            # print(new_values["pictures"])
            pictures += new_values["pictures"]
            # print(pictures, flush=True)
            self.pictures = []
            for i, path in enumerate(pictures):
                path = Validator.path(path)
                new_values[f"picture_{i+1}"] = path
                self.pictures.append(path)
            del new_values["pictures"]
        if "tags" in new_values:
            if len(new_values["tags"]) > 0:
                self.update_tags(new_values["tags"])
            del new_values["tags"]

        for k in new_values.keys():
            if k not in User.__fields__ or (k in User.__restricted_fields__ and not force):
                raise KeyError(f"field {k} doesn't exist")
            reqs += [f"{k}=?"]
        if len(reqs) > 0:
            req = ", ".join(reqs)
            query = "UPDATE users SET " + req + " WHERE id=" + str(self.id)
            for (k, v) in new_values.items():
                if "picture" in k:
                    continue
                checker = getattr(Validator, k)
                setattr(self, k, checker(v))
            db.exec(query, tuple(new_values.values()))
        return True

    @staticmethod
    def validate(validation_id):
        query = """
            SELECT
                u.*
            FROM users u
                INNER JOIN validations v
                    ON v.user_id = u.id
                    AND v.validation_id = ?
            """
        rows = db.fetch(query, (validation_id,))
        if len(rows) is 0:
            return False
        db.exec("UPDATE users SET validated=1 WHERE id=?", (rows[0][0],))
        db.exec("DELETE FROM validations WHERE user_id=?", (rows[0][0],))
        return True

    def delete(self):
        query = "DELETE FROM users WHERE id=" + str(self.id)
        db.exec(query)
        return True

    def like(self, user):
        query = "SELECT * FROM likes WHERE user_id=? AND liked=?"
        rows = db.fetch(query, (self.id, user.id))

        if len(rows) is not 0:
            return False
        query = "INSERT INTO likes (user_id, liked) VALUES (?, ?)"
        db.exec(query, (self.id, user.id))
        return True

    def report(self, user):
        query = "SELECT * FROM reports WHERE user_id=? AND reported=?"
        rows = db.fetch(query, (self.id, user.id))
        if len(rows) is not 0:
            return False
        query = "INSERT INTO reports (user_id, reported) VALUES (?, ?)"
        db.exec(query, (self.id, user.id))


        query = "SELECT COUNT(*) FROM visits WHERE visited=?"
        rows = db.fetch(query, (user.id,))
        if len(rows) is not 0:
            visits = float(rows[0][0])
        visits = max(1.0, visits)

        query = "SELECT COUNT(*) FROM reports WHERE reported=?"
        rows = db.fetch(query, (user.id,))
        reports = 0
        if len(rows) is not 0:
            reports = float(rows[0][0])
        if reports / visits > 0.3:
            query = "UPDATE users SET banned=1 WHERE id=?"
            db.exec(query, (user.id,))

        return True

    def visit(self, user):
        query = "SELECT * FROM visits WHERE user_id=? AND visited=?"
        rows = db.fetch(query, (self.id, user.id))
        if len(rows) is not 0:
            query = "UPDATE visits SET date=? WHERE user_id=? AND visited=?"
            db.exec(query, (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"), self.id, user.id))
        else:
            query = "INSERT INTO visits (user_id, visited) VALUES (?, ?)"
            db.exec(query, (self.id, user.id))
        return True

    def unlike(self, user):
        query = "SELECT * FROM likes WHERE user_id=? AND liked=?"
        rows = db.fetch(query, (self.id, user.id))

        if len(rows) is 0:
            return False
        query = "DELETE FROM likes WHERE user_id=? AND liked=?"
        db.exec(query, (self.id, user.id))
        return True

    def liked(self, user):
        query = "SELECT * FROM likes WHERE user_id=? AND liked=?"
        like = db.fetch(query, (self.id, user.id))
        if len(like) is 0:
            return False
        return True

    def matches_with(self, user):
        if self.liked(user) and user.liked(self):
            return True
        return False

    def block(self, user):
        query = "SELECT * FROM blocks WHERE user_id=? AND blocked=?"
        rows = db.fetch(query, (self.id, user.id))
        if len(rows) is not 0:
            return False
        query = "INSERT INTO blocks (user_id, blocked) VALUES (?, ?)"
        db.exec(query, (self.id, user.id))
        return True

    def unblock(self, user):
        query = "SELECT * FROM blocks WHERE user_id=? AND blocked=?"
        rows = db.fetch(query, (self.id, user.id))
        if len(rows) is 0:
            return False
        query = "DELETE FROM blocks WHERE user_id=? AND blocked=?"
        db.exec(query, (self.id, user.id))
        return True

    @property
    def blocklist(self):
        query = "SELECT blocked FROM blocks WHERE user_id=?"
        values = db.fetch(query, (self.id,))
        return [int(i[0]) for i in values]
    
    @property
    def matchlist(self):
        query = """
            SELECT
                u.*
            FROM users u
            INNER JOIN(likes a
                INNER JOIN likes b
                    ON a.user_id = b.liked
                    AND a.liked = b.user_id
                    AND b.user_id = ?)
                ON
                    u.id = a.user_id
            """
        rows = db.fetch(query, (self.id,))
        return [User.build_from_db_tuple(t).intro_as(self) for t in rows]
    
    @property
    def liked_by_list(self):
        query = """
            SELECT
                *
            FROM users
            INNER JOIN likes
            ON users.id = likes.user_id
                AND likes.liked = ?
            """
        rows = db.fetch(query, (self.id,))
        return [User.build_from_db_tuple(t).intro_as(self) for t in rows]
    
    # @property
    # def liked_list(self):
    #     query = """
    #         SELECT
    #             *
    #         FROM users
    #         INNER JOIN likes
    #         ON users.id = likes.user_id
    #             AND likes.liked = ?
    #         """
    #     rows = db.fetch(query, (self.id,))
    #     return [User.build_from_db_tuple(t).intro_as(self) for t in rows]
    
    @property
    def visits_list(self):
        query = """
            SELECT
                u.*
            FROM users u
            INNER JOIN visits v
            ON u.id = v.user_id
                AND v.visited = ?
            ORDER BY v.date DESC;
            """
        rows = db.fetch(query, (self.id,))
        return [User.build_from_db_tuple(t).intro_as(self) for t in rows]

    @property
    def blocked_list(self):
        query = """
            SELECT
                u.*
            FROM users u
            INNER JOIN blocks b
                ON b.user_id = ?
            ORDER BY v.date DESC;
            """
        rows = db.fetch(query, (self.id,))
        return [User.build_from_db_tuple(t).intro_as(self) for t in rows]
    
    @property
    def tags_list(self):
        query = """
            SELECT
                t.name
            FROM user_tags ut
            INNER JOIN tags t
                ON ut.tag_id = t.id
            WHERE
                ut.user_id=?
            """
        rows = db.fetch(query, (self.id,))
        return [str(t[0]) for t in rows]

    @property
    def blocked_by(self):
        query = "SELECT user_id FROM blocks WHERE blocked=?"
        rows = db.fetch(query, (self.id,))

        return [int(i[0]) for i in rows]

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __str__(self):
        return str(vars(self))

    def __repr__(self):
        return self.__str__()

    @property
    def dict(self):
        d = vars(self)
        d["tags"] = self.tags_list
        return d

    def public_as(self, user):
        d = self.public
        d["liked"] = user.liked(self)
        d["matches"] = user.matches_with(self)
        d["blocked"] = self.id in user.blocklist 
        return d

    def intro_as(self, user):
        d = self.intro
        d["liked"] = user.liked(self)
        d["matches"] = user.matches_with(self)
        d["blocked"] = self.id in user.blocklist 
        return d

    @property
    def public(self):
        return {
            "first_name": self.first_name,
            "id": self.id,
            "pictures": self.pictures,
            "orientation": self.orientation,
            "bio": self.bio,
            "age": self.age,
            "score": self.score,
            "sex": self.sex,
            "lon": self.lon,
            "lat": self.lat,
            "last_seen": self.last_seen,
            "tags": self.tags_list
        }

    @property
    def intro(self):
        return {
            "first_name": self.first_name,
            "id": self.id,
            "pictures": self.pictures,
            "age": self.age,
            "sex": self.sex,
            "last_seen": self.last_seen
        }

    def save_reset_id(self, reset_id):
        query = "INSERT INTO resets (user_id, reset_id) VALUES (?, ?)"
        db.exec(query, (self.id, reset_id))

    @property
    def reset_id(self):
        query = "SELECT reset_id FROM resets WHERE user_id=?"
        rows = db.fetch(query, (self.id,))
        if len(rows) is 0:
            return False
        return rows[0]

    def clear_resets(self):
        query = "DELETE from resets WHERE user_id=?"
        db.exec(query, (self.id,))

    def clear_reports(self):
        query = "DELETE from reports WHERE user_id=? OR reported=?"
        db.exec(query, (self.id, self.id))

    def clear_blocks(self):
        query = "DELETE from blocks WHERE user_id=? or blocked=?"
        db.exec(query, (self.id, self.id))

    def clear_likes(self):
        query = "DELETE from likes WHERE user_id=? or liked=?"
        db.exec(query, (self.id, self.id))

    def clear_tags(self):
        query = "DELETE from user_tags WHERE user_id=?"
        db.exec(query, (self.id,))
        
    def update_tags(self, tags):
        if type(tags) is not list or type(tags[0]) is not str:
            raise InvalidData(f"{tags} is not a list of strings")
        tags = [Tag(t) for t in tags]
        self.clear_tags()
        query = f"""
            INSERT INTO `user_tags` (user_id, tag_id) VALUES {", ".join(["(?, ?)"] * len(tags))};
        """
        params = zip([self.id] * len(tags), [t.id for t in tags])
        params = tuple(i for t in params for i in t)
        # print(params, [t.name for t in tags])
        db.exec(query, params)

    def search(self, payload):
        age_min = 18
        age_max = 99
        score_min = 0
        score_max = 100
        distance_max = 50000 # km
        tags = []
        if type(payload) is dict:
            if "age" in payload:
                age_min = payload["age"]["min"]
                age_max = payload["age"]["max"]
            if "score" in payload:
                score_min = payload["score"]["min"] / 100.0
                score_max = payload["score"]["max"] / 100.0
            if "distance" in payload:
                distance_max = payload["distance"]
            if "tags" in payload:
                tags = payload["tags"]

        query = """
            SELECT DISTINCT
                u.*
            FROM
                users u
                LEFT OUTER JOIN (likes a
                    INNER JOIN likes b
                        ON a.user_id = b.liked
                        AND a.liked = b.user_id
                        AND b.user_id=?)
                    ON u.id = a.user_id
                LEFT OUTER JOIN blocks
                    ON u.id = blocks.user_id
                    AND blocks.blocked=?
                LEFT JOIN user_tags ut
                    ON ut.user_id = u.id
                LEFT JOIN tags t
                    ON t.id = ut.tag_id
            WHERE
                blocks.user_id IS NULL
                AND b.user_id IS NULL
                AND u.validated=1
                AND u.id != ?
                AND u.age >= ?
                AND u.age <= ?
                AND u.validated=1
                AND st_distance(POINT(u.lat, u.lon), POINT(?, ?)) * 111 <= ?
                AND u.likes_count / (0.5 * ((u.views_count + 1) + ABS(u.views_count - 1))) >= ?
                AND u.likes_count / (0.5 * ((u.views_count + 1) + ABS(u.views_count - 1))) <= ?
            """
        if len(tags) > 0:
            tags_query = []
            junc = " "
            for t in tags:
                tags_query.append("t.name=?")
            if len(tags) > 1:
                junc = " OR "
            query += " AND (" + junc.join(tags_query) + ")"


        rows = db.fetch(query, (self.id, self.id, self.id, age_min, age_max, self.lat, self.lon, distance_max, score_min, score_max, *tags))

        return [User.build_from_db_tuple(t).intro_as(self) for t in rows]
        
    @property
    def conversations(self):
        query = """
            SELECT DISTINCT
                u.*
            FROM
                users u
                -- boilerplate start
                LEFT OUTER JOIN (likes a
                    INNER JOIN likes b
                        ON a.user_id = b.liked
                        AND a.liked = b.user_id
                        AND b.user_id=?)
                    ON u.id = a.user_id
                LEFT OUTER JOIN blocks
                    ON u.id = blocks.user_id
                    AND blocks.blocked=?
                -- boilerplate end
                INNER JOIN messages m
                ON (m.from_id=u.id OR m.to_id=u.id)
            WHERE
                u.id != ? 
        """
        rows = db.fetch(query, (self.id, self.id, self.id,))
        return [User.build_from_db_tuple(t).intro_as(self) for t in rows]