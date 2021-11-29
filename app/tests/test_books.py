import json
from fastapi.testclient import TestClient

from app.services.books import update
from ..main import app
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

client = TestClient(app)


def test_create_book():
    logger.info(">>> Testing create book...")
    body = {
        "title": "Título Teste Um",
        "author": "Autor Teste Um",
        "teacher": "Professor Teste Um"
    }
    response = client.post("/books/", json=body)

    assert response.status_code == 201
    assert body.get("title") == response.json().get("title")
    assert body.get("author") == response.json().get("author")
    assert body.get("teacher") == response.json().get("teacher")


def test_get_all_books():
    logger.info(">>> Testing Get All Books...")
    response = client.get("/books/")
    assert response.status_code == 200


def test_get_book_by_magic_code():
    logger.info(">>> Testing Get Book By Magic Code...")
    books = client.get('/books/').json().get("books")
    for book in books:
        response = client.get(f'/books/{book.get("magic_code")}')
        assert response.status_code == 200
    response_book = client.get('/books/ABCDEFG/')
    assert response_book.status_code == 404


def test_update_book():
    logger.info(">>> Testing Update Book")
    books = client.get('/books/').json().get("books")

    for book in books:
        update_body = {
            "title": f'Atualizado {book.get("id")}',
            "author": f'Atualizado {book.get("id")}',
            "teacher": f'Atualizado {book.get("id")}'
        }

        response = client.put(f'/books/{book.get("id")}', json=update_body)
        assert response.status_code == 200
        assert response.json().get("title") == update_body.get("title")
        assert response.json().get("author") == update_body.get("author")
        assert response.json().get("teacher") == update_body.get("teacher")

    response_fail = client.put(f'/books/0', json=update_body)
    assert response_fail.status_code == 404


def test_delete_book():
    logger.info(">>> Testing Delete Book")
    books = client.get('/books/').json().get("books")

    for book in books:
        response = client.delete(f'/books/{book.get("id")}')
        assert response.status_code == 200

    response = client.get('/books/')
    assert response.status_code == 404

    response = client.delete(f'/books/1')
    assert response.status_code == 404
