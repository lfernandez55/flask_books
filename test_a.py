import pytest
from flask import url_for


class TestApp:

    def test_fum(self, client):
        res = client.get(url_for('fum'))
        assert res.status_code == 200
        assert b"Fum" in res.data, "Problem!!!"

    def test_bar(self, client):
        res = client.get(url_for('bar'))
        assert res.status_code == 200
        # assert res.json == {'ping': 'pong'}

    def test_books(self, client):
        res = client.get(url_for('books'))
        assert res.status_code == 200
        assert b"Frankenstein" in res.data, "Problem in test_books!!!"

    # def test_ping_false_positive(self, client):
    #     res = client.get(url_for('ping'))
    #     assert res.status_code == 400, 'Request ping did not result in a 400 error'

    # def test_home_page(self, client):
    #     res = client.get(url_for('tinker_json'))
    #     assert res.status_code == 200
