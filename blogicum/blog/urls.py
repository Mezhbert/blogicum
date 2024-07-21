from django.urls import path
from django.contrib import admin
from .views import (
    IndexView,
    CreatePostView,
    EditPostView,
    CategoryPostsView,
    ProfileView,
    EditProfileView,
    EditCommentView,
)
from . import views

app_name = 'blog'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('posts/create/',
         CreatePostView.as_view(),
         name='create_post'),
    path('posts/<int:pk>/',
         views.post_detail,
         name='post_detail'),
    path('posts/<int:pk>/edit/',
         EditPostView.as_view(),
         name='edit_post'),
    path('category/<slug:category_slug>/',
         CategoryPostsView.as_view(),
         name='category_posts'),
    path('admin/', admin.site.urls),
    path('profile/<str:username>/',
         ProfileView.as_view(),
         name='profile'),
    path('edit_profile/',
         EditProfileView.as_view(),
         name='edit_profile'),
    path('<int:pk>/comment/',
         views.add_comment,
         name='add_comment'),
    path('posts/<int:pk>/delete/',
         views.PostDeleteView.as_view(),
         name='delete_post'),
    path('posts/<int:post_pk>/delete_comment/<int:pk_comment>/',
         views.CommentDeleteView.as_view(),
         name='delete_comment'),
    path('posts/<int:pk>/edit_comment/<int:pk_comment>/',
         EditCommentView.as_view(),
         name='edit_comment'),
]
