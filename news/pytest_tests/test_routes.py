"""Тесты маршрутизации."""
from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects
from pytest_lazy_fixtures import lf


@pytest.mark.parametrize(
    'name, args',
    (
        ('news:home', None),
        ('news:detail', lf('pk_news_for_args')),
        ('users:login', None),
        ('users:logout', None),
        ('users:signup', None)
    )
)
def test_pages_availability_for_anonymous_user(client, name, args):
    """Тест доступности страниц для анонимного ползователя."""
    url = reverse(name, args=args)
    if name == 'users:logout':
        response = client.post(url)
    else:
        response = client.get(url)
    assert response.status_code == HTTPStatus.OK
