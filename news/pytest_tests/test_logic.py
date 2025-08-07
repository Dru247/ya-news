"""Django pytest тесты бизнес логики."""
from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertFormError, assertRedirects
from pytils.translit import slugify

# from notes.forms import WARNING
from news.models import Comment


def test_user_can_create_comment(
    author_client, form_data, pk_news_for_args
):
    """Тест пользователь может создать комментарий."""
    url = reverse('news:detail', args=pk_news_for_args)
    response = author_client.post(url, data=form_data)
    assertRedirects(response, url + '#comments')
    assert Comment.objects.count() == 1
    new_note = Comment.objects.get()
    assert new_note.text == form_data['text']


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(
    client, form_data, pk_news_for_args
):
    """Тест анонимный пользователь не может создать комментарий."""
    url = reverse('news:detail', args=pk_news_for_args)
    response = client.post(url, data=form_data)
    login_url = reverse('users:login')
    expected_url = f'{login_url}?next={url}'
    assertRedirects(response, expected_url)
    assert Comment.objects.count() == 0


def test_author_can_edit_comment(
    author_client, comment, form_data, pk_comment_for_args
):
    """Тест автор может изменить комментарий."""
    url = reverse('news:edit', args=pk_comment_for_args)
    response = author_client.post(url, form_data)
    assertRedirects(
        response,
        reverse('news:detail', args=(comment.news.pk,)) + '#comments'
    )
    # Обновляем объект заметки note: получаем обновлённые данные из БД:
    comment.refresh_from_db()
    assert comment.text == form_data['text']


def test_other_user_cant_edit_comment(
    not_author_client, form_data, comment, pk_comment_for_args
):
    """Тест не автор не может изменить комментарий."""
    url = reverse('news:edit', args=pk_comment_for_args)
    response = not_author_client.post(url, form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    # Получаем новый объект запросом из БД.
    note_from_db = Comment.objects.get(id=comment.id)
    assert comment.text == note_from_db.text


def test_author_can_delete_comment(author_client, pk_comment_for_args):
    """Тест автор может удалять комментарий."""
    url = reverse('news:delete', args=pk_comment_for_args)
    response = author_client.post(url)
    assertRedirects(
        response,
        reverse('news:detail', args=pk_comment_for_args) + '#comments'
    )
    assert Comment.objects.count() == 0


def test_other_user_cant_delete_comment(
    not_author_client, pk_comment_for_args, pk_news_for_args
):
    """Тест не автор не может удалять комментарий."""
    url = reverse('news:delete', args=pk_comment_for_args)
    response = not_author_client.post(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 1
