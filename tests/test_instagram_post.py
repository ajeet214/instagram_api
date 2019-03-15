import pytest
from modules.instagram_post import InstaPost


def Object(query):
    obj = InstaPost()
    result = obj.instagram_post(query)
    return result


@pytest.mark.parametrize("name", ['walker', 'Nguyễn Xuân Phúc', 'Pedro Sánchez'])
def test_post_search(name):
    result1 = Object(name)
    for i in result1['data']:
        assert type(i['likes']) == int

        assert type(i['comments']) == int

        assert type(i['datetime']) == int

        assert type(i['polarity']) == str
        assert i['polarity'] != ""

        assert i['thumbnail'].startswith('http')
        assert i['thumbnail'] != ""

        assert i['url'].startswith('http')
        assert i['url'] != ""

        assert type(i['content']) == str
        assert i['content'] != ""

        assert type(i['postid']) == str
        assert i['postid'] != ""

        try:
            assert i['type'] is 'image'
        except AssertionError:
            assert i['type'] is 'video'

