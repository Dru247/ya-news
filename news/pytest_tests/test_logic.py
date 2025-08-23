"""Django pytest тесты бизнес логики."""
from http import HTTPStatus as Status

import pytest
from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment

pytestmark = pytest.mark.django_db

FORM_DATA = {'text': 'Новый текст комментария'}


def test_user_can_create_comment(author, news, author_client, get_urls):
    """Тест пользователь может создать комментарий."""
    Comment.objects.all().delete()
    url = get_urls['news_detail']
    response = author_client.post(url, data=FORM_DATA)
    assertRedirects(response, url + '#comments')
    assert Comment.objects.count() == 1
    new_note = Comment.objects.get()
    assert new_note.text == FORM_DATA['text']
    assert new_note.author == author
    assert new_note.news == news


def test_anonymous_user_cant_create_comment(client, get_urls):
    """Тест анонимный пользователь не может создать комментарий."""
    first_comment_count = Comment.objects.count()
    url = get_urls['news_detail']
    response = client.post(url, data=FORM_DATA)
    expected_url = f'{get_urls['users_login']}?next={url}'
    assertRedirects(response, expected_url)
    second_comment_count = Comment.objects.count()
    assert first_comment_count == second_comment_count


def test_author_can_edit_comment(
        author, author_client, news, get_urls, comment
):
    """Тест автор может изменить комментарий."""
    response = author_client.post(get_urls['comment_edit'], FORM_DATA)
    assertRedirects(
        response,
        get_urls['news_detail'] + '#comments'
    )
    edit_comment = Comment.objects.get(pk=comment.pk)
    assert edit_comment.text == FORM_DATA['text']
    assert edit_comment.author == author
    assert edit_comment.news == news


def test_other_user_cant_edit_comment(
        author, not_author_client, news, comment, get_urls
):
    """Тест не автор не может изменить комментарий."""
    response = not_author_client.post(get_urls['comment_edit'], FORM_DATA)
    assert response.status_code == Status.NOT_FOUND
    edit_comment = Comment.objects.get(pk=comment.pk)
    assert edit_comment.text == comment.text
    assert edit_comment.author == author
    assert edit_comment.news == news


def test_author_can_delete_comment(author_client, get_urls):
    """Тест автор может удалять комментарий."""
    first_comment_count = Comment.objects.count()
    response = author_client.post(get_urls['comment_delete'])
    assertRedirects(
        response,
        get_urls['news_detail'] + '#comments'
    )
    second_comment_count = Comment.objects.count()
    assert first_comment_count - second_comment_count == 1


def test_other_user_cant_delete_comment(not_author_client, get_urls):
    """Тест не автор не может удалять комментарий."""
    first_comment_count = Comment.objects.count()
    response = not_author_client.post(get_urls['comment_delete'])
    assert response.status_code == Status.NOT_FOUND
    second_comment_count = Comment.objects.count()
    assert first_comment_count == second_comment_count


def test_user_cant_use_bad_words(author_client, get_urls):
    """Вывоз исключения при наличии запрещённых слов в комментарии."""
    first_comment_count = Comment.objects.count()
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    response = author_client.post(
        get_urls['news_detail'],
        data=bad_words_data
    )
    second_comment_count = Comment.objects.count()
    assert first_comment_count == second_comment_count
    form = response.context['form']
    assertFormError(
        form=form,
        field='text',
        errors=WARNING
    )
