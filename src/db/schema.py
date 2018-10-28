from psycopg2 import connect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def build_users_table(cur):
    cur.execute('CREATE TABLE users (user_id serial primary key, email text unique not null, password text not null, first_name text not null, last_name text not null);')

def build_posts_table(cur):
    cur.execute('CREATE TABLE posts (post_id serial primary key, user_id integer references users(user_id), description text, ts timestamp default current_timestamp);')

def build_pictures_table(cur):
    cur.execute('CREATE TABLE pictures (picture_id serial primary key, post_id integer references posts(post_id), picture_data bytea);')

def build_likes_table(cur):
    cur.execute('CREATE TABLE likes (like_id serial primary key, user_id integer references users(user_id), post_id integer references posts(post_id));')

def build_db(cur, dbname):
    cur.execute('CREATE DATABASE ' + dbname)


def build_schema(dbname):
    #create our db
    conn = connect("dbname=postgres")
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    build_db(cur, dbname)

    cur.close()
    conn.close()

    #db table schema
    conn = connect("dbname=" + dbname)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    build_users_table(cur)
    build_posts_table(cur)
    build_pictures_table(cur)
    build_likes_table(cur)

    cur.close()
    conn.close()


if __name__ == '__main__':
    build_schema('puppies')