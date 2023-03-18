from datetime import datetime, date
from dateutil.tz import UTC

import factory.fuzzy

from posts.models import Post, Comment
from users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    """Test class for User model"""

    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'user{n}')
    birthday = factory.fuzzy.FuzzyDate(
        date(1987, 1, 1),
        date(2001, 2, 18)
    )
    email = 'user@mail.ru'
    date_joined = factory.fuzzy.FuzzyDateTime(
        datetime(2008, 1, 1, tzinfo=UTC),
        datetime(2023, 2, 18, tzinfo=UTC)
    )
    date_updated = factory.fuzzy.FuzzyDateTime(
        datetime(2008, 1, 1, tzinfo=UTC),
        datetime(2023, 2, 18, tzinfo=UTC)
    )


class PostFactory(factory.django.DjangoModelFactory):
    """Test class for Post model."""

    class Meta:
        model = Post

    title = factory.fuzzy.FuzzyText(prefix='Title', length=150)
    text = factory.fuzzy.FuzzyText(prefix='Post', length=150)
    author = factory.SubFactory(UserFactory)
    created = factory.fuzzy.FuzzyDateTime(
        datetime(2008, 1, 1, tzinfo=UTC),
        datetime(2023, 2, 18, tzinfo=UTC)
    )
    updated = factory.fuzzy.FuzzyDateTime(
        datetime(2008, 1, 1, tzinfo=UTC),
        datetime(2023, 2, 18, tzinfo=UTC)
    )


class CommentFactory(factory.django.DjangoModelFactory):
    """Test class for Comment model."""

    class Meta:
        model = Comment

    post = factory.SubFactory(PostFactory)
    author = factory.SubFactory(UserFactory)
    text = factory.Sequence(lambda n: f'комментарий{n}')
    created = factory.fuzzy.FuzzyDateTime(
        datetime(2008, 1, 1, tzinfo=UTC),
        datetime(2023, 2, 18, tzinfo=UTC)
    )
    updated = factory.fuzzy.FuzzyDateTime(
        datetime(2008, 1, 1, tzinfo=UTC),
        datetime(2023, 2, 18, tzinfo=UTC)
    )