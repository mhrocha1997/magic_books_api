import json
from fastapi.testclient import TestClient

from app.services.books import update
from ..main import app
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

client = TestClient(app)


def test_create_page():
    logger.info(">>> Testing create page...")

    book_body = {
        "title": "Título Teste Página",
        "author": "Autor Teste Página",
        "teacher": "Professor Teste Página"
    }
    book_response = client.post("/books/", json=book_body)
    book_id = book_response.json().get('id')

    text = f"Lorem ipsum dolor sit amet, consectetur adipiscing elit." \
        f" Etiam eget ligula eu lectus lobortis condimentum." \
        f"Aliquam nonummy auctor massa. Pellentesque habitant" \
        f" morbi tristique senectus et netus et malesuada fames ac " \
        f"turpis egestas. Nulla at risus. Quisque purus magna, auctor et,"\
        f" sagittis ac, posuere eu, lectus. Nam mattis, felis ut adipiscing."
    image = "data:image/png;base64,example"

    body = {
        "text": text,
        "image": image,
    }

    for _ in range(6):
        response = client.post(f"/pages/book/{book_id}", json=body)

        assert response.status_code == 201
        assert body.get("text") == response.json().get("text")
        assert body.get("image") == response.json().get("image")
        assert book_id == response.json().get('book_id')

    response = client.post(f"/pages/book/{book_id}", json=body)
    assert response.status_code == 400

    response = client.post(f"/pages/book/0", json=body)
    assert response.status_code == 404


def test_get_page_by_id():
    logger.info(">>> Testing Get Page By Id...")
    books = client.get("/books/").json().get("books")

    for book in books:
        response_book = client.get(f'/books/{book.get("magic_code")}')
        pages = response_book.json().get("pages")
        for page in pages:
            response = client.get(f'pages/{page.get("id")}')
            assert response.status_code == 200
    response = client.get(f'pages/0')
    assert response.status_code == 404


def test_update_page():
    logger.info(">>> Testing Update Page...")
    books = client.get("/books/").json().get("books")
    update_body = {
        "text": "Atualizado",
                "image": "data:image/png;base64,atualizado"
    }
    for book in books:
        response_book = client.get(f'/books/{book.get("magic_code")}')
        pages = response_book.json().get("pages")
        for page in pages:
            response = client.put(f'pages/{page.get("id")}', json=update_body)

            assert response.status_code == 200
            assert response.json().get("text") == update_body.get("text")
            assert response.json().get("image") == update_body.get("image")

    response = client.put(f'pages/0', json=update_body)
    assert response.status_code == 404


def test_delete_page():
    logger.info(">>> Testing Delete Page")
    books = client.get("/books/").json().get("books")

    for book in books:
        response_book = client.get(f'/books/{book.get("magic_code")}')
        pages = response_book.json().get("pages")
        for page in pages:
            response = client.delete(f'/pages/{page.get("id")}')
            assert response.status_code == 200
    response = client.delete(f'/pages/0')
    assert response.status_code == 404
