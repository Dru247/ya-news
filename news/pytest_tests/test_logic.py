"""Django pytest тесты бизнес логики."""
from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertFormError, assertRedirects
from pytils.translit import slugify

# from notes.forms import WARNING
from news.models import Comment


def test_user_can_create_note(
        author_client, form_data, pk_news_for_args):
    """Тест пользователь может создать запись."""
    url = reverse('news:detail', args=pk_news_for_args)
    response = author_client.post(url, data=form_data)
    assertRedirects(response, url + '#comments')
    assert Comment.objects.count() == 1
    new_note = Comment.objects.get()
    assert new_note.text == form_data['text']
