"""Тест контента."""
import pytest

from django.conf import settings
from django.urls import reverse

from news.forms import CommentForm


@pytest.mark.django_db
def test_news_count(client, create_many_news):
    """Тест кол-ва новостей на домашней странице."""
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context['object_list']
    news_count = object_list.count()
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_order(client, create_many_news):
    """Проверка сортировки записей на домашней странице."""
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


@pytest.mark.django_db
def test_comments_order(client, pk_news_for_args, create_many_comments):
    """Тест сортировки комментарий по дате."""
    url = reverse('news:detail', args=pk_news_for_args)
    response = client.get(url)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    sorted_timestamps = sorted(all_timestamps)
    assert all_timestamps == sorted_timestamps


@pytest.mark.django_db
def test_anonymous_client_has_no_form(client, pk_news_for_args):
    """Тест отсутствия Формы для анонимного пользователя."""
    url = reverse('news:detail', args=pk_news_for_args)
    response = client.get(url)
    assert 'form' not in response.context


def test_authorized_client_has_form(not_author_client, pk_news_for_args):
    """Тест присутствия Формы для авторизированного пользователя."""
    url = reverse('news:detail', args=pk_news_for_args)
    response = not_author_client.get(url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)
