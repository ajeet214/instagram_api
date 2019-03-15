import pytest
from modules.instagram_profile_posts import ProfilePosts


@pytest.mark.parametrize("id", ['thisisbillgates', 'william_asher'])
def test_profile_posts(id):
    obj = ProfilePosts()
    res = obj.profile_posts(id)

    for i in res:

        assert isinstance(i['datetime'], int)
        assert isinstance(i['comments'], int)
        assert isinstance(i['likes'], int)
        assert type(i['is_video']) == bool

        try:
            assert type(i['country']) == str
            assert i['country'] != ""
        except AssertionError:
            assert i['country'] is None

        try:
            assert type(i['content']) == str
            assert i['content'] != ""
        except AssertionError:
            assert i['content'] is None

        try:
            assert type(i['location']) == str
            assert i['location'] != ""
        except AssertionError:
            assert i['location'] is None

        try:
            assert type(i['thumbnail']) == str
            assert i['thumbnail'].startswith('http')
            assert i['thumbnail'] != ""
        except AssertionError:
            assert i['thumbnail'] is None

        try:
            assert type(i['url']) == str
            assert i['url'].startswith('http')
            assert i['url'] != ""
        except AssertionError:
            assert i['url'] is None

        try:
            assert type(i['country_code']) == str
            assert i['country_code'] != ""
            assert len(i['country_code']) is 2
        except AssertionError:
            assert i['country_code'] is None

        # checking for non-empty and non-space string
        try:
            assert type(i['author_userid']) == str
            assert i['author_userid'] != ""
            assert ' ' not in i['author_userid']
        except AssertionError:
            assert i['author_userid'] is None

        try:
            assert type(i['postid']) == str
            assert i['postid'] != ""
            assert ' ' not in i['postid']
        except AssertionError:
            assert i['postid'] is None

        # checking for non-empty string
        try:
            assert type(i['author_name']) == str
            assert i['author_name'] != ""
        except AssertionError:
            assert i['author_name'] is None

        # checking for url
        try:
            assert type(i['author_image']) == str
            assert i['author_image'].startswith('http')
            assert i['author_image'] != ""
        except AssertionError:
            assert i['author_image'] is None

        try:
            assert i['type'] is 'image'
        except AssertionError:
            assert i['type'] is 'video'
