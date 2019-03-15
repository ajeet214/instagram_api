import pytest
from modules.emailNumberChecker import EmailChecker


def search(query):
    obj = EmailChecker()
    result = obj.checker(query)
    return result


@pytest.mark.parametrize("id", ['austinpaul134@outlook.com', '919416284225'])
def test_id_checker(id):
    result1 = search(id)
    assert type(result1['profileExists']) == bool


