from flask import Flask, send_from_directory, request, jsonify, make_response
from middleware import requires_auth
import os
import entities
from werkzeug.utils import secure_filename
from base64 import b64encode

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app = Flask(__name__, static_folder='../../build')


@app.route('/users', methods=['POST'])
def user_handler():
    params = request.get_json()
    entities.create_user(params['email'], params['password'], params['first_name'], params['last_name'])
    return make_response("", 201)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/posts', methods=['GET', 'POST'])
@requires_auth
def posts_handler():
    auth = request.authorization
    params = request.get_json()
    user_id = entities.get_user_by_email(auth.username)[0]

    if request.method == 'POST':
        #HACK: should be in transaction to avoid data race
        entities.create_post(user_id, request.form['description'])
        post_id = entities.get_last_post(user_id)

        # check if the post request has the file part
        if 'file' not in request.files:
            return make_response("No file part", 400)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            print("here")
            return make_response("No selected file", 400)
        if file and allowed_file(file.filename):
            print("there")
            filename = secure_filename(file.filename)
            file_b = file.read()
            entities.create_picture(post_id, file_b)
        return make_response("", 201)

    #get individual post
    elif request.method == 'GET' and request.args.get('post_id') != None:
        post_id = request.args.get('post_id')
        full_post = entities.get_post_by_post_id_for_user_id(post_id, user_id)
        if full_post is None:
            return jsonify({})
        post_id = full_post[0]
        description = full_post[1]
        timestamp = full_post[2]
        picture = b64encode(bytes(full_post[3])).decode('utf-8')
        return jsonify({'post_id': post_id,
                        'description': description,
                        'date' : timestamp,
                        'picture_data': picture})
    #get all posts (user's feed)
    elif request.method == 'GET':
        posts = entities.get_posts()
        resp = []
        for post in posts:
            resp.append({'post_id': post[0],
                         'description': post[1],
                         'user_id': post[2],
                         'date': post[3],
                         'picture_data': b64encode(bytes(post[4])).decode('utf-8'),
                         'number_of_likes': post[5]})
        return jsonify(resp)
    else:
        return make_response("", 405)

@app.route('/likes', methods=['POST'])
@requires_auth
def likes_handler():
    if request.method == 'POST':
        auth = request.authorization
        post_id = request.args.get('post_id')
        user_id = entities.get_user_by_email(auth.username)[0]
        entities.create_like(post_id, user_id)

        return make_response("", 201)
    else:
        make_response("", 405)


if __name__ == '__main__':
    app.run(use_reloader=True, port=5000, threaded=True)