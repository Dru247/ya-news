"""Фиктуры тестов."""
from datetime import datetime, timedelta

import pytest
from django.conf import settings
from django.test.client import Client

from news.models import Comment, News


@pytest.fixture
def author(django_user_model):
    """Создаёт и возвращает пользователя-автора."""
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    """Создаёт и возвращает пользователя-читателя."""
    return django_user_model.objects.create(username='Читатель')


@pytest.fixture
def author_client(author):
    """Авторизирует и возвращает пользователя-автора."""
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    """Авторизирует и возвращает пользователя-читателя."""
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def news():
    """Создаёт и возвращает объект новости."""
    news = News.objects.create(
        title='Заголовок новости',
        text='Текст новости'
    )
    return news


@pytest.fixture
def pk_news_for_args(news):
    """Возващает PK новости для аргуумента."""
    return (news.id,)


@pytest.fixture
def comment(news, author):
    """Создаёт и возвращает объект комментария."""
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария'
    )
    return comment


@pytest.fixture
def pk_comment_for_args(comment):
    """Возващает PK комментария для аргуумента."""
    return (comment.id,)


@pytest.fixture
def create_many_news():
    """Создаёт несколько объектов News."""
    today = datetime.today()
    News.objects.bulk_create(
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=today - timedelta(days=index)
        ) for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    )


@pytest.fixture
def create_many_comments(news, author):
    """Создаёт несколько объектов Comment."""
    number_comments = 10
    today = datetime.today()
    Comment.objects.bulk_create(
        Comment(
            news=news,
            author=author,
            text='Просто текст.',
            created=today - timedelta(days=index)
        ) for index in range(number_comments)
    )


@pytest.fixture
def form_data():
    return {'text': 'Тест текст'}
