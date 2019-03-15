from flask import Flask, jsonify, request
from modules.instagram_search_db import ProfileSearch
from modules.instagram_post import InstaPost
from modules.instagram_db import ProfileExistence
from modules.instagram_profile_fetcher import ProfileFetcher
from modules.instagram_profile_posts import ProfilePosts
from raven.contrib.flask import Sentry

app = Flask(__name__)
sentry = Sentry(app)


@app.route('/api/v1/search/profile')
def search():
    query = request.args.get('q')
    obj1 = ProfileSearch()
    return jsonify(obj1.db_check(query))


@app.route('/api/v1/search/post')
def post_search():
    query = request.args.get('q')
    obj2 = InstaPost()
    result = obj2.instagram_post(query)
    return jsonify(result)


# @app.route('/api/v1/search/id')
# def emailChecker():
#     email = request.args.get('q')
#     # obj = EmailChecker()
#     obj1 = Profile_existance()
#     data = obj1.db_check(email)
#     return jsonify({'data': data})

@app.route('/api/v1/search/id')
def email_checker():
    email = request.args.get('q')
    obj = ProfileExistence()

    data = obj.db_check(email)
    return jsonify({'data': {'availability': data['profileExists']}})


@app.route('/api/v1/profile')
def profile_fetch():
    query = request.args.get('id')
    obj1 = ProfileFetcher()
    return jsonify(obj1.profile_fetcher(query))


@app.route('/api/v1/profile/posts')
def profile_posts():
    query = request.args.get('id')
    obj1 = ProfilePosts()
    return jsonify(obj1.profile_posts(query))


if __name__ == '__main__':
    app.run(port=5004)
