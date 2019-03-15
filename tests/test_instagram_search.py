import pytest
from modules.instagram_search import Instagram


def search(query):
    obj = Instagram()
    result = obj.search_api(query)
    return result


@pytest.mark.parametrize("name", ['bill gates', 'Nguyễn Xuân Phúc'])
def test_profile_search(name):
    result1 = search(name)
    for i in result1:
        assert type(i['following']) == int

        assert type(i['followers']) == int

        assert type(i['posts']) == int

        try:
            assert type(i['business_phone_number']) == str
            assert i['business_phone_number'] != ""
        except AssertionError:
            assert i['business_phone_number'] is None

        assert type(i['verified']) == bool
        assert type(i['is_business_account']) == bool
        assert type(i['is_joined_recently']) == bool
        assert i['url'].startswith('http')
        assert i['image'].startswith('http')
        assert type(i['userid']) == str
        assert i['userid'] != ""

        try:
            assert type(i['linked_url']) == str
            assert i['linked_url'].startswith('http')
            assert i['linked_url'] != ""

        except AssertionError:
            assert i['linked_url'] is None

        try:
            assert type(i['business_email']) == str
            assert i['business_email'].find('http')
            assert i['business_email'] != ""
        except AssertionError:
            assert i['business_email'] is None

        try:
            assert type(i['business_category_name']) == str
            assert i['business_category_name'] != ""
        except AssertionError:
            assert i['business_category_name'] is None

        try:
            assert type(i['description']) == str
            assert i['description'] != ""
        except AssertionError:
            assert i['description'] is None

        try:
            assert type(i['business_address_json']) == str
            assert i['business_address_json'] != ""
        except AssertionError:
            assert i['business_address_json'] is None

        try:
            assert type(i['name']) == str
            assert i['name'] != ""
        except AssertionError:
            assert i['name'] is None

        assert i['type'] is 'identity'

