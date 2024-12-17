import random
import uuid
from http import HTTPStatus

import pytest
from faker import Faker

from init_db import author_uuids, book_uuids, user_uuids, borrow_uuids1, borrow_uuids2

faker = Faker('ru_RU')


@pytest.mark.usefixtures('create_tables')
@pytest.mark.asyncio
async def test_create_author(client):
    params = dict(
        name=faker.first_name(),
        surname=faker.last_name(),
        birthdate='2012-10-10'
    )
    response = await client.post('api/v1/authors/', json=params)

    assert response.status_code == HTTPStatus.CREATED


@pytest.mark.usefixtures('create_tables')
@pytest.mark.asyncio
async def test_get_authors(client):
    params = {'page_number': 0, 'page_size': 20}
    response = await client.get('api/v1/authors/', params=params)

    assert response.status_code == HTTPStatus.OK


@pytest.mark.usefixtures('create_tables')
@pytest.mark.asyncio
async def test_find_author(client):
    author_id = random.choice(author_uuids)
    response = await client.get(f'api/v1/authors/{author_id}')
    assert response.status_code == HTTPStatus.OK


@pytest.mark.usefixtures('create_tables')
@pytest.mark.asyncio
async def test_update_author(client):
    id = random.choice(author_uuids)
    data = {
        'name': str(uuid.uuid4()),
        'surname': 'Mike',
        'birthdate': '2024-12-17'
    }
    response = await client.put(f'api/v1/authors/{id}', json=data)

    assert response.status_code == HTTPStatus.OK


@pytest.mark.usefixtures('create_tables')
@pytest.mark.asyncio
async def test_remove_author(client):
    id = str(random.choice(author_uuids))
    response = await client.delete(f'api/v1/authors/{id}')
    assert response.status_code == HTTPStatus.NO_CONTENT

    response = await client.delete(f'api/v1/authors/{id}')
    assert response.status_code == HTTPStatus.NOT_FOUND



@pytest.mark.usefixtures('create_tables')
@pytest.mark.asyncio
async def test_add_book(client):
    data = {
        'title': 'some title',
        'description': 'some descr',
        'author_id': str(random.choice(author_uuids)),
        'quantity': 20
    }
    response = await client.post('api/v1/books/', json=data)
    assert response.status_code == HTTPStatus.CREATED


@pytest.mark.usefixtures('create_tables')
@pytest.mark.asyncio
async def test_get_books(client):
    response = await client.get(f'api/v1/books/')
    assert response.status_code == HTTPStatus.OK


@pytest.mark.usefixtures('create_tables')
@pytest.mark.asyncio
async def test_get_book_info(client):
    id = random.choice(book_uuids)
    response = await client.get(f'api/v1/books/{id}')
    assert response.status_code == HTTPStatus.OK


@pytest.mark.usefixtures('create_tables')
@pytest.mark.asyncio
async def test_update_book_info(client):
    id = str(random.choice(book_uuids))
    data = {
        'title': 'new title',
        'description': 'new descr',
        'author_id': str(random.choice(author_uuids)),
        'quantity': 3,
    }
    response = await client.put(f'api/v1/books/{id}', json=data)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.usefixtures('create_tables')
@pytest.mark.asyncio
async def test_del_book_info(client):
    id = str(random.choice(book_uuids))

    response = await client.delete(f'api/v1/books/{id}')
    assert response.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.usefixtures('create_tables')
@pytest.mark.asyncio
async def test_create_borrow(client):
    params = {
        'book_id': random.choice(book_uuids),
        'user_id': random.choice(user_uuids)
    }
    response = await client.post('api/v1/borrow/', json=params)

    assert response.status_code == HTTPStatus.CREATED


@pytest.mark.usefixtures('create_tables')
@pytest.mark.asyncio
async def test_create_borrow(client):
    response = await client.get('api/v1/borrow/')

    assert response.status_code == HTTPStatus.OK


@pytest.mark.usefixtures('create_tables')
@pytest.mark.asyncio
async def test_create_borrow(client):
    params = {'id': random.choice(borrow_uuids1)}
    response = await client.get('api/v1/borrow/', params=params)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.usefixtures('create_tables')
@pytest.mark.asyncio
async def test_return_book(client):
    id = str(random.choice(borrow_uuids2))
    response = await client.patch(f'api/v1/borrow/{id}/return')

    assert response.status_code == HTTPStatus.OK