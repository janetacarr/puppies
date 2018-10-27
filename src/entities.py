from psycopg2 import connect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from functools import wraps
from hashlib import sha1

#TODO: these functions would probably benefit from having some static typing.

def dbsetup():
    conn = connect("dbname=puppies")
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    return cur, conn

def get_user_by_email(email):
    cur, conn = dbsetup()

    cur.execute("Select * from users where email = %s;", (str(email),))
    user = cur.fetchone()

    cur.close()
    conn.close()

    return user

def create_user(email, password, first_name, last_name):
    cur, conn = dbsetup()

    pw_hash = sha1(bytes(password, 'utf-8')).hexdigest()
    cur.execute("INSERT INTO users (email, password, first_name, last_name) values (%s, %s, %s, %s);", (email, pw_hash, first_name, last_name))

    cur.close()
    conn.close()

def create_post(user_id, description):
    cur, conn = dbsetup()

    cur.execute("INSERT INTO posts (user_id, description) values (%s, %s);", (user_id, description))

    cur.close()
    conn.close()

def get_last_post(user_id):
    cur, conn = dbsetup()

    cur.execute("SELECT post_id FROM posts WHERE user_id = %s ORDER BY post_id DESC;", (user_id,))
    post = cur.fetchone()

    cur.close()
    conn.close()

    return post[0]

def get_post_by_post_id_for_user_id(post_id, user_id):
    cur, conn = dbsetup()

    cur.execute("SELECT posts.post_id, posts.description, posts.ts, pictures.picture_data from posts, pictures where posts.post_id = pictures.post_id and posts.user_id = %s and posts.post_id = %s;", (user_id, post_id))
    post = cur.fetchone()

    cur.close()
    conn.close()

    return post

def get_posts():
    cur, conn = dbsetup()

    cur.execute("""
    select picture_posts.post_id, picture_posts.description, picture_posts.user_id, picture_posts.ts, picture_posts.picture_data, count(picture_posts.post_id) as number_of_likes from 
(SELECT posts.post_id, posts.user_id, posts.description, posts.ts, pictures.picture_data from posts, pictures where posts.post_id = pictures.post_id) as picture_posts, likes where picture_posts.post_id = likes.post_id group by picture_posts.post_id, picture_posts.description, picture_posts.user_id, picture_posts.ts, picture_posts.picture_data order by ts DESC;
    """)
    posts = cur.fetchall()

    cur.close()
    conn.close()

    return posts

def create_picture(post_id, picture_data):
    cur, conn = dbsetup()

    cur.execute("INSERT into pictures (post_id, picture_data) values (%s, %s);", (post_id, picture_data))

    cur.close()
    conn.close()

def create_like(post_id, user_id):
    cur, conn = dbsetup()

    cur.execute("INSERT into likes (post_id, user_id) values (%s, %s);", (post_id, user_id))

    cur.close()
    conn.close()