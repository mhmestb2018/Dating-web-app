# Flask Backend
### Using Flask and MariaDB

The backend is accessible on port 5000 on your machine ([link](http://0.0.0.0:5000)).

This API uses `POST` request to communicate and HTTP [response codes](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes) to indenticate status and errors. All responses come in standard JSON. All requests must include a `content-type` of `application/json` and the body must be valid JSON.

![Tests](https://github.com/Karocyt/Dating-web-app/workflows/Tests_back/badge.svg)

## Response Codes 
### Response Codes
```
200: Success
201: Ressource created
400: Bad request
401: Unauthorized
404: Cannot be found
405: Method not allowed 
418: I'm a teapot
50X: Server Error
```

### Example Error Message
```json
HTTP/1.1 403 FORBIDDEN
Content-Type: application/json
{
    "error": "Vous n'êtes pas connecté",
}
```

## Signup
**You send:**  Your basic information.  
**You get:** An email is sent with a validation link (http://hostname/validate/<validation_id>). If email is not set up, returns the `validation_id`.

**Request:**
```json
POST /signup HTTP/1.1
Content-Type: application/json
{
    "email": "foo@bar.xy",
    "password": "1234567",
    "first_name": "roger",
    "last_name": "moore",
}
```
**Successful Response:**
```json
HTTP/1.1 201 CREATED
Content-Type: application/json
{
    "pcachin": "true",
}
```

## Email validation (link from mail)
**You send:** Nothing  
**You get:** A success message.

**Request:**
```json
POST /validate/<validation_id> HTTP/1.1
```
**Successful Response:**
```json
HTTP/1.1 200 OK
Content-Type: application/json
{
    "pcachin": "true",
}
```

## Login
**You send:**  Your login credentials.  
**You get:** A cookie with a `session` token valid for 31 days with wich you can make further actions.

**Request:**
```json
POST /login HTTP/1.1
Content-Type: application/json
{
    "email": "foo@bar.fr",
    "password": "1234567",
    "remember_me: true 
}
```
**Successful Response:**
```json
HTTP/1.1 200 OK
Set-Cookie: session=eyJfcGVybWFuZW50Ijp0cnVlLCJ1c2VyIjoxfQ.X1Uwog.BBHCto1CAuJj_9RLJ0g5kPHgtbU
Content-Type: application/json
{
    "bio": "Je suis caché",
    "email": "pcachin@gmail.com",
    "first_name": "phillipe",
    "id": 1,
    "last_name": "cachin",
    "orientation": null,
    "pictures": [
        "/data/pcachin.jpg",
        "/data/gikghks.jpg",
    ],
    "score": 42.0,
    "sex": "m",
    "validated": 1,
    "last_seen": "Tue, 29 Sep 2020 00:00:00 GMT",
    "lon": 45.454646545,
    "lat": 12.135456464,
    "age": 21
}
```

## Logout
**You send:**  Your `session` cookie.  
**You get:** Disconnected.

**Request:**
```json
POST /logout HTTP/1.1
Cookie: session=eyJfcGVybWFuZW50Ijp0cnVlLCJ1c2VyIjoxfQ.X1Uwog.BBHCto1CAuJj_9RLJ0g5kPHgtbU
```
**Successful Response:**
```json
HTTP/1.1 200 OK
Content-Type: application/json
{
    "pcachin": true,
}
```

## Update
**You send:**  Your `session` cookie and all the json encoded fields to edit.  
**You get:** The full JSON encoded profile of the connected user.

If `email` is changed, this call will unvalidate the user and send a new validation link. (TO DO)

**Request:**
```json
PUT /profile HTTP/1.1
Cookie: session=eyJfcGVybWFuZW50Ijp0cnVlLCJ1c2VyIjoxfQ.X1Uwog.BBHCto1CAuJj_9RLJ0g5kPHgtbU
Content-Type: application/json
{
    "first_name": "updated" 
}
```
**Successful Response:**
```json
HTTP/1.1 200 OK
Content-Type: application/json
{
    "bio": "Je suis caché",
    "email": "pcachin@gmail.com",
    "first_name": "updated",
    "id": 1,
    "last_name": "cachin",
    "orientation": null,
    "pictures": [
        "/data/pcachin.jpg",
        "/data/gikghks.jpg",
    ],
    "score": 42.0,
    "sex": "m",
    "validated": 1,
    "last_seen": "Tue, 29 Sep 2020 00:00:00 GMT",
    "lon": 45.454646545,
    "lat": 12.135456464,
    "age": 21
}
```

## Delete
**You send:**  Your `session` cookie.  
**You get:** The user public profile, for the last time.

**Request:**
```json
DELETE /profile HTTP/1.1
Cookie: session=eyJfcGVybWFuZW50Ijp0cnVlLCJ1c2VyIjoxfQ.X1Uwog.BBHCto1CAuJj_9RLJ0g5kPHgtbU
```
**Successful Response:**
```json
HTTP/1.1 200 OK
Content-Type: application/json
{
    "bio": "",
    "first_name": "roger",
    "orientation": null,
    "pictures": [],
    "score": 0.0,
    "sex": "m",
    "last_seen": "Tue, 29 Sep 2020 00:00:00 GMT",
    "lon": 45.454646545,
    "lat": 12.135456464,
    "age": 21
}
```

## Password lost
**You send:**  Your `email` address  
**You get:** If applicable, a mail is sent with a reset link (http://hostname/reset/<user_id>/<reset_id>), otherwise, you get the `reset_id`.

**Request:**
```json
POST /reset HTTP/1.1
Content-Type: application/json
{
    "email": "foo@bar.fr",
}
```
**Successful Response:**
```json
HTTP/1.1 200 OK
Content-Type: application/json
{
    "pcachin": "true",
}
```

## Password reset (link from mail)
**You send:**  Your `new_password`.  
**You get:** A success message.

**Request:**
```json
POST /reset/<user_id>/<reset_id> HTTP/1.1
Content-Type: application/json
{
    "new_password": "passW0rd",
}
```
**Successful Response:**
```json
HTTP/1.1 200 OK
Content-Type: application/json
{
    "pcachin": "true",
}
```

## Get current user
**You send:**  Your `session` cookie.  
**You get:** The connected user full JSON encoded profile.

**Request:**
```json
GET /profile HTTP/1.1
Cookie: session=eyJfcGVybWFuZW50Ijp0cnVlLCJ1c2VyIjoxfQ.X1Uwog.BBHCto1CAuJj_9RLJ0g5kPHgtbU
```
**Successful Response:**
```json
HTTP/1.1 200 OK
Content-Type: application/json
{
    "bio": "",
    "first_name": "roger",
    "orientation": null,
    "pictures": [],
    "score": 0.0,
    "sex": "m",
    "last_seen": "Tue, 29 Sep 2020 00:00:00 GMT",
    "lon": 45.454646545,
    "lat": 12.135456464,
    "age": 21
}
```

## Get a public profile
**You send:**  Your `session` cookie.  
**You get:** The user JSON encoded public profile.

**Request:**
```json
GET /users/<user_id> HTTP/1.1
Cookie: session=eyJfcGVybWFuZW50Ijp0cnVlLCJ1c2VyIjoxfQ.X1Uwog.BBHCto1CAuJj_9RLJ0g5kPHgtbU
```
**Successful Response:**
```json
HTTP/1.1 200 OK
Content-Type: application/json
{
    "bio": "J'aime manger des pommes",
    "blocked": false,
    "first_name": "roger",
    "id": 2,
    "liked": true,
    "matches": false,
    "orientation": "asexual",
    "pictures": [],
    "score": 0.0,
    "sex": "m",
    "last_seen": "Tue, 29 Sep 2020 00:00:00 GMT",
    "lon": 45.454646545,
    "lat": 12.135456464,
    "age": 21
}
```

## Actions
**You send:**  Your `session` cookie and the json encoded action (`like`, `block` or `report`) with its boolean setting.  
**You get:** The match status with the user.

**Request:**
```json
POST /users/<user_id> HTTP/1.1
Cookie: session=eyJfcGVybWFuZW50Ijp0cnVlLCJ1c2VyIjoxfQ.X1Uwog.BBHCto1CAuJj_9RLJ0g5kPHgtbU
Content-Type: application/json
{
    "like": false,
}
```
**Successful Response:**
```json
HTTP/1.1 200 OK
Content-Type: application/json
{
    "match": false,
}
```

## Matches
**You send:**  Your `session` cookie.  
**You get:** A JSON encoded list of users

**Request:**
```json
GET /matches HTTP/1.1
Cookie: session=eyJfcGVybWFuZW50Ijp0cnVlLCJ1c2VyIjoxfQ.X1Uwog.BBHCto1CAuJj_9RLJ0g5kPHgtbU
```
**Successful Response:**
```json
HTTP/1.1 200 OK
Content-Type: application/json
{
    "matches": [
        {
            "blocked": false,
            "first_name": "roger",
            "id": 2,
            "liked": true,
            "matches": true,
            "pictures": [],
            "last_seen": "Tue, 29 Sep 2020 00:00:00 GMT",
            "age": 21
        },
        {
            "blocked": false,
            "first_name": "bertrand",
            "id": 7,
            "liked": true,
            "matches": true,
            "pictures": [],
            "last_seen": "Tue, 29 Sep 2020 00:00:00 GMT",
            "age": 21
        }
    ],
}
```

## Liked by
**You send:**  Your `session` cookie.  
**You get:** A JSON encoded list of users who like you (including matches)

**Request:**
```json
GET /liked_by HTTP/1.1
Cookie: session=eyJfcGVybWFuZW50Ijp0cnVlLCJ1c2VyIjoxfQ.X1Uwog.BBHCto1CAuJj_9RLJ0g5kPHgtbU
```
**Successful Response:**
```json
HTTP/1.1 200 OK
Content-Type: application/json
{
    "users": [
        {
            "blocked": false,
            "first_name": "roger",
            "id": 2,
            "liked": true,
            "matches": true,
            "pictures": [],
            "last_seen": "Tue, 29 Sep 2020 00:00:00 GMT",
            "age": 21
        },
        {
            "blocked": false,
            "first_name": "bertrand",
            "id": 7,
            "liked": false,
            "matches": false,
            "pictures": [],
            "last_seen": "Tue, 29 Sep 2020 00:00:00 GMT",
            "age": 21
        }
    ],
}
```

## Visits

**You send:**  Your `session` cookie and optional search parameters.  
**You get:** A list of users who visited you, sorted by last visit date

**Request:**
```json
GET /visits HTTP/1.1
Cookie: session=eyJfcGVybWFuZW50Ijp0cnVlLCJ1c2VyIjoxfQ.X1Uwog.BBHCto1CAuJj_9RLJ0g5kPHgtbU
Content-Type: application/json
```
**Successful Response:**
```json
HTTP/1.1 200 OK
Content-Type: application/json
{
    "users":  [...],
}
```

## List users

**You send:**  Your `session` cookie 
**You get:** A JSON encoded list of validated unmatched users

**Request:**
```json
GET /users HTTP/1.1
Cookie: session=eyJfcGVybWFuZW50Ijp0cnVlLCJ1c2VyIjoxfQ.X1Uwog.BBHCto1CAuJj_9RLJ0g5kPHgtbU
Content-Type: application/json
```
**Successful Response:**
```json
HTTP/1.1 200 OK
Content-Type: application/json
{
    "users":  [
        {
            "blocked": false,
            "first_name": "roger",
            "id": 2,
            "liked": true,
            "matches": false,
            "pictures": [],
            "sex": "m",
            "last_seen": "Tue, 29 Sep 2020 00:00:00 GMT",
            "age": 21
        },
        {
            "blocked": false,
            "first_name": "bertrand",
            "id": 7,
            "liked": false,
            "matches": false,
            "pictures": [],
            "sex": "m",
            "last_seen": "Tue, 29 Sep 2020 00:00:00 GMT",
            "age": 21
        }
    ],
}
```

## Search users # TO DO

**You send:**  Your `session` cookie 
**You get:** A JSON encoded list of validated unmatched users

**Request:**
```json
POST /users HTTP/1.1
Cookie: session=eyJfcGVybWFuZW50Ijp0cnVlLCJ1c2VyIjoxfQ.X1Uwog.BBHCto1CAuJj_9RLJ0g5kPHgtbU
Content-Type: application/json
{
    "count": 2,
    "sex": "m", 
}
```
**Successful Response:**
```json
HTTP/1.1 200 OK
Content-Type: application/json
{
    "users":  [
        {
            "blocked": false,
            "first_name": "roger",
            "id": 2,
            "liked": true,
            "matches": false,
            "pictures": [],
            "sex": "m",
            "last_seen": "Tue, 29 Sep 2020 00:00:00 GMT",
            "age": 21
        },
        {
            "blocked": false,
            "first_name": "bertrand",
            "id": 7,
            "liked": false,
            "matches": false,
            "pictures": [],
            "sex": "m",
            "last_seen": "Tue, 29 Sep 2020 00:00:00 GMT",
            "age": 21
        }
    ],
}
```

## Author
* **Kevin Azoulay** @ 42 Lyon
