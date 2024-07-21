from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from blog.models import Comment
from django.urls import reverse_lazy


class CommentMixin(LoginRequiredMixin):
    model = Comment
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'pk_comment'

    def get_success_url(self):
        return reverse_lazy('blog:post_detail',
                            kwargs={'pk': self.object.post.pk})

    def get_comment_object(self):
        pk_comment = self.kwargs.get(self.pk_url_kwarg)
        return get_object_or_404(Comment, pk=pk_comment)

    def check_if_author(self, comment):
        if comment.author != self.request.user:
            raise PermissionDenied

    def dispatch(self, request, *args, **kwargs):
        instance = self.get_comment_object()
        self.check_if_author(comment=instance)
        return super().dispatch(request, *args, **kwargs)
