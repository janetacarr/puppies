from functools import wraps
from flask import request, Response
from hashlib import sha1
import entities


def check_auth(email, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    stored_pw = entities.get_user_by_email(email)[2]
    return stored_pw == sha1(bytes(password, 'utf-8')).hexdigest()

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

#HACK: Ideally, would we be returning a jwt for login instead of basic auth, and asserting against claims.
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated