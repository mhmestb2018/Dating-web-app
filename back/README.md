# Flask Backend
### Using Flask and MariaDB

The backend is accessible on port 5000 on your machine ([link](http://0.0.0.0:5000)).

This API uses `POST` request to communicate and HTTP [response codes](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes) to indenticate status and errors. All responses come in standard JSON. All requests must include a `content-type` of `application/json` and the body must be valid JSON.

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
Server: Werkzeug/1.0.1 Python/3.7.9
Content-Type: application/json
Content-Length: xy
{
    "error": "Vous n'êtes pas connecté",
}
```

## Signup
**You send:**  Your basic information.  
**You get:** An email is sent with a validation link (http://hostname/validation/<validation_id>).

**Request:**
```json
POST /signup HTTP/1.1
Accept: application/json
Content-Type: application/json
Content-Length: xy
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
Server: Werkzeug/1.0.1 Python/3.7.9
Content-Type: application/json
Content-Length: xy
{
    "pcachin": "true",
}
```

## Email validation (link from mail) TO DO
**You send:**  Your new `password`.  
**You get:** A success message.

**Request:**
```json
POST /validate HTTP/1.1
Accept: application/json
Content-Type: application/json
Content-Length: xy
{
    "validation_id": "AE16F5D0438CA",
}
```
**Successful Response:**
```json
HTTP/1.1 200 OK
Server: Werkzeug/1.0.1 Python/3.7.9
Content-Type: application/json
Content-Length: xy
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
Accept: application/json
Content-Type: application/json
Content-Length: xy
{
    "username": "foo",
    "password": "1234567" 
}
```
**Successful Response:**
```json
HTTP/1.1 200 OK
Server: Werkzeug/1.0.1 Python/3.7.9
Set-Cookie: session=eyJfcGVybWFuZW50Ijp0cnVlLCJ1c2VyIjoxfQ.X1Uwog.BBHCto1CAuJj_9RLJ0g5kPHgtbU
Content-Type: application/json
Content-Length: xy
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
    "validated": 1
}
```

## Logout
**You send:**  Your `session` cookie.  
**You get:** Disconnected.

**Request:**
```json
POST /logout HTTP/1.1
```
**Successful Response:**
```json
HTTP/1.1 200 OK
Server: Werkzeug/1.0.1 Python/3.7.9
Content-Type: application/json
Content-Length: xy
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
Accept: application/json
Cookie: session=eyJfcGVybWFuZW50Ijp0cnVlLCJ1c2VyIjoxfQ.X1Uwog.BBHCto1CAuJj_9RLJ0g5kPHgtbU
Content-Type: application/json
Content-Length: xy
{
    "first_name": "updated" 
}
```
**Successful Response:**
```json
HTTP/1.1 200 OK
Server: Werkzeug/1.0.1 Python/3.7.9
Content-Type: application/json
Content-Length: xy
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
    "validated": 1
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
Server: Werkzeug/1.0.1 Python/3.7.9
Content-Type: application/json
Content-Length: xy
{
    "bio": "",
    "first_name": "roger",
    "orientation": null,
    "pictures": [],
    "score": 0.0,
    "sex": "m"
}
```

## Password lost TO DO
**You send:**  Your `email` address.  
**You get:** A mail is sent with a reset link (http://hostname/reset/<reset_id>).

**Request:**
```json
POST /reset_password HTTP/1.1
Accept: application/json
Content-Type: application/json
Content-Length: xy
{
    "email": "foo@bar.xy",
}
```
**Successful Response:**
```json
HTTP/1.1 200 OK
Server: Werkzeug/1.0.1 Python/3.7.9
Content-Type: application/json
Content-Length: xy
{
    "pcachin": "true",
}
```

## Password reset (link from mail) TO DO
**You send:**  Your `reset_id` and  new `password`.  
**You get:** A success message.

**Request:**
```json
POST /reset_password HTTP/1.1
Accept: application/json
Content-Type: application/json
Content-Length: xy
{
    "reset_id": "AE148F34643CD40",
    "password": "S€cUr1ty",
}
```
**Successful Response:**
```json
HTTP/1.1 200 OK
Server: Werkzeug/1.0.1 Python/3.7.9
Content-Type: application/json
Content-Length: xy
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
Server: Werkzeug/1.0.1 Python/3.7.9
Content-Type: application/json
Content-Length: xy
{
    "bio": "",
    "first_name": "roger",
    "orientation": null,
    "pictures": [],
    "score": 0.0,
    "sex": "m"
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
Server: Werkzeug/1.0.1 Python/3.7.9
Content-Type: application/json
Content-Length: xy
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
    "sex": "m"
}
```

## Actions
**You send:**  Your `session` cookie and the json encoded action (`like` or `block`) with it's boolean setting.  
**You get:** The full JSON encoded profile of the connected user.

**Request:**
```json
POST /users/<user_id> HTTP/1.1
Accept: application/json
Cookie: session=eyJfcGVybWFuZW50Ijp0cnVlLCJ1c2VyIjoxfQ.X1Uwog.BBHCto1CAuJj_9RLJ0g5kPHgtbU
Content-Type: application/json
Content-Length: xy
{
    "like": false,
}
```
**Successful Response:**
```json
HTTP/1.1 200 OK
Server: Werkzeug/1.0.1 Python/3.7.9
Content-Type: application/json
Content-Length: xy
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
Server: Werkzeug/1.0.1 Python/3.7.9
Content-Type: application/json
Content-Length: xy
{
    "matches": [
        {
            "bio": "J'aime manger des pommes",
            "blocked": false,
            "first_name": "roger",
            "id": 2,
            "liked": true,
            "matches": true,
            "orientation": "heterosexual",
            "pictures": [],
            "score": 42.101,
            "sex": "m"
        },
        {
            "bio": "Je pète au lit",
            "blocked": false,
            "first_name": "bertrand",
            "id": 7,
            "liked": true,
            "matches": true,
            "orientation": "bisexual",
            "pictures": [],
            "score": 101.42,
            "sex": "m"
        }
    ],
}
```

## List users
**You send:**  Your `session` cookie and optional search parameters.  
**You get:** A JSON encoded list of validated unmatched users

(count is not yet enforced)

**Request:**
```json
GET /users HTTP/1.1
Accept: application/json
Cookie: session=eyJfcGVybWFuZW50Ijp0cnVlLCJ1c2VyIjoxfQ.X1Uwog.BBHCto1CAuJj_9RLJ0g5kPHgtbU
Content-Type: application/json
Content-Length: xy
{
    "count": 2,
    "sex": "m", 
}
```
**Successful Response:**
```json
HTTP/1.1 200 OK
Server: Werkzeug/1.0.1 Python/3.7.9
Content-Type: application/json
Content-Length: xy
{
    "users":  [
        {
            "bio": "J'aime manger des pommes",
            "blocked": false,
            "first_name": "roger",
            "id": 2,
            "liked": true,
            "matches": false,
            "orientation": "heterosexual",
            "pictures": [],
            "score": 0,
            "sex": "m"
        },
        {
            "bio": "Je pète au lit",
            "blocked": false,
            "first_name": "bertrand",
            "id": 7,
            "liked": false,
            "matches": false,
            "orientation": "bisexual",
            "pictures": [],
            "score": 0,
            "sex": "m"
        }
    ],
}
```

## Author
* **Kevin Azoulay** @ 42 Lyon