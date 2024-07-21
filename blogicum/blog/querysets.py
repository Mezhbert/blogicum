from django.utils import timezone
from .models import Post


def get_all_posts():
    return Post.objects.select_related(
        'category',
        'author',
        'location'
    )


def get_published_posts():
    return get_all_posts().filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
        )
