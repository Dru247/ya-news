"""Тесты контента."""
import pytest
from django.conf import settings

from news.forms import CommentForm

pytestmark = pytest.mark.django_db


def test_news_count(client, get_urls, create_many_news):
    """Тест кол-ва новостей на домашней странице."""
    url = get_urls['news_home']
    response = client.get(url)
    news_count = response.context['object_list'].count()
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order(client, get_urls, create_many_news):
    """Проверка сортировки записей на домашней странице."""
    url = get_urls['news_home']
    response = client.get(url)
    all_dates = [news.date for news in response.context['object_list']]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


def test_comments_order(client, get_urls, create_many_comments):
    """Тест сортировки комментарий по дате."""
    url = get_urls['news_detail']
    response = client.get(url)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    sorted_timestamps = sorted(all_timestamps)
    assert all_timestamps == sorted_timestamps


def test_anonymous_client_has_no_form(client, get_urls):
    """Тест отсутствия Формы для анонимного пользователя."""
    url = get_urls['news_detail']
    response = client.get(url)
    assert 'form' not in response.context


def test_authorized_client_has_form(not_author_client, get_urls):
    """Тест присутствия Формы для авторизированного пользователя."""
    url = get_urls['news_detail']
    response = not_author_client.get(url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)
