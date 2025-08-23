"""Тесты маршрутизации."""
from http import HTTPStatus as Status

import pytest
from pytest_django.asserts import assertRedirects
from pytest_lazy_fixtures import lf

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'reverse_url, parametrized_client, status',
    (
        ('news_home', lf('client'), Status.OK),
        ('news_detail', lf('client'), Status.OK),
        ('users_login', lf('client'), Status.OK),
        ('users_signup', lf('client'), Status.OK),
        ('comment_edit', lf('not_author_client'), Status.NOT_FOUND),
        ('comment_delete', lf('not_author_client'), Status.NOT_FOUND),
        ('comment_edit', lf('author_client'), Status.OK),
        ('comment_delete', lf('author_client'), Status.OK)
    )
)
def test_pages_availability_for_different_users(
    reverse_url, parametrized_client, status, get_urls
):
    """Тест доступности страниц для пользователей."""
    response = parametrized_client.get(get_urls[reverse_url])
    assert response.status_code == status


def test_logout_availability_for_anonymous_user(client, get_urls):
    """Тест доступности страницы logout для анонимного ползователя."""
    response = client.post(get_urls['users_logout'])
    assert response.status_code == Status.OK


@pytest.mark.parametrize(
    'url',
    ('comment_edit', 'comment_delete')
)
def test_redirects(client, url, get_urls):
    """Тест редиректа."""
    expected_url = f'{get_urls['users_login']}?next={get_urls[url]}'
    response = client.get(get_urls[url])
    assertRedirects(response, expected_url)
