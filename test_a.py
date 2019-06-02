import pytest
from flask import url_for


class TestApp:

    def test_fum(self, client):
        res = client.get(url_for('fum'))
        assert res.status_code == 200
        assert b"Fum" in res.data, "Problem!!!"

    def test_erase_db(self, client):
        res = client.get(url_for('eraseDB'))
        assert res.status_code == 200
        assert b"Erased" in res.data, "Problem in eraseDB; not returning 'Erased'"

    def test_seed_db(self, client):
        res = client.get(url_for('seedDB'))
        assert res.status_code == 200
        assert b"Seeded" in res.data, "Problem in seedDB; not returning 'Seeded'"

    def test_tinker(self, client):
        res = client.get(url_for('tinker'))
        assert res.status_code == 200
        assert b"Tinker" in res.data, "Problem in tinker; not returning 'Tinker'"

    def test_sql(self, client):
        res = client.get(url_for('sql'))
        assert res.status_code == 200
        assert b"Custom SQL" in res.data, "Problem in sql; not returning 'Custom SQL'"

    # this won't work if the test_erase and test_seed_db are out of sequence
    def test_all_books(self, client):
        res = client.get(url_for('books'))
        assert res.status_code == 200
        assert b"Frankenstein" in res.data, "Problem in All Books; not returning 'Frankenstein' "

    def test_new_book(self, client):
            res = client.get(url_for('addbook'))
            assert res.status_code == 200
            assert b"Description" in res.data, "Problem in New Book. Not returning 'Description'"

    def test_new_book(self, client):
            res = client.get(url_for('categories'))
            assert res.status_code == 200
            assert b"Horror" in res.data, "Problem in Categories. Not returning 'Horror'"
