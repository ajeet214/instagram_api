import pytest
from modules.instagram_profile_fetcher import ProfileFetcher


@pytest.mark.parametrize("id", ['harrypotterfans', 'thisisbillgates'])
def test_profile_fetcher(id):
    obj = ProfileFetcher()
    res = obj.profile_fetcher(id)

    assert type(res['following']) == int

    assert type(res['followers']) == int

    assert type(res['posts']) == int

    try:
        assert type(res['linked_url']) == str
        assert res['linked_url'].startswith('http')
        assert res['linked_url'] != ""

    except AssertionError:
        assert res['linked_url'] is None

    try:
        assert type(res['business_email']) == str
        assert res['business_email'].find('http')
        assert res['business_email'] != ""
    except AssertionError:
        assert res['business_email'] is None

    try:
        assert type(res['business_category_name']) == str
        assert res['business_category_name'] != ""
    except AssertionError:
        assert res['business_category_name'] is None

    try:
        assert type(res['description']) == str
        assert res['description'] != ""
    except AssertionError:
        assert res['description'] is None

    try:
        assert type(res['business_address_json']) == str
        assert res['business_address_json'] != ""
    except AssertionError:
        assert res['business_address_json'] is None

    try:
        assert type(res['name']) == str
        assert res['name'] != ""
    except AssertionError:
        assert res['name'] is None

    assert type(res['verified']) == bool
    assert type(res['is_business_account']) == bool
    assert type(res['is_joined_recently']) == bool
    assert res['url'].startswith('http')
    assert res['image'].startswith('http')
    assert type(res['userid']) == str
    assert res['userid'] != ""

    try:
        assert type(res['business_phone_number']) == str
        assert res['business_phone_number'] != ""
    except AssertionError:
        assert res['business_phone_number'] is None

    assert res['type'] is 'identity'
