from django.urls import reverse_lazy
from django.views.generic import ListView
from blog.models import Post, Category, User
from django.utils import timezone
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import PostForm, UserForm, CommentForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from .constants import PAGINATE
from .mixins import CommentMixin
from .querysets import get_published_posts, get_all_posts


@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('blog:post_detail', pk=pk)


class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'page_obj'
    paginate_by = PAGINATE

    def get_queryset(self):
        return get_published_posts()


def post_detail(request, pk):
    post = get_object_or_404(get_all_posts(), pk=pk)
    if post.author != request.user:
        post = get_object_or_404(get_published_posts(), pk=pk)

    form = CommentForm(request.POST or None)

    comments = post.comments.all()
    return render(request,
                  'blog/detail.html',
                  {'post': post, 'comments': comments, 'form': form})


class CategoryPostsView(ListView):
    model = Post
    template_name = 'blog/category.html'
    context_object_name = 'page_obj'
    paginate_by = PAGINATE

    def get_queryset(self):
        category = get_object_or_404(Category,
                                     slug=self.kwargs['category_slug'],
                                     is_published=True)
        if category.is_published:
            return get_published_posts().filter(category=category)
        return Post.objects.none()


class ProfileView(ListView):
    model = Post
    template_name = 'blog/profile.html'
    context_object_name = 'page_obj'
    paginate_by = PAGINATE

    def get_queryset(self):
        queryset = get_all_posts().filter(
            author__username=self.kwargs['username'],
            pub_date__lte=timezone.now()
        )

        if self.request.user.is_authenticated:
            unpublished = get_all_posts().filter(
                author__username=self.kwargs['username'],
                author=self.request.user,
                pub_date__gt=timezone.now()
            )
            queryset = queryset | unpublished

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        var = self.kwargs['username']
        context['profile'] = get_object_or_404(User, username=var)
        return context


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'blog/user.html'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('blog:profile',
                            kwargs={'username': self.request.user.username})


class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.is_published = form.instance.pub_date <= timezone.now()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:profile',
                            kwargs={'username': self.request.user.username})


class EditPostView(LoginRequiredMixin,
                   UserPassesTestMixin,
                   UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def test_func(self):
        return self.get_object().author == self.request.user

    def handle_no_permission(self):
        post = self.get_object()
        return redirect('blog:post_detail', pk=post.pk)

    def get_success_url(self):
        return reverse_lazy('blog:post_detail',
                            kwargs={'pk': self.object.pk})


class PostDeleteView(LoginRequiredMixin,
                     UserPassesTestMixin,
                     DeleteView):
    model = Post
    template_name = 'blog/delete.html'
    success_url = reverse_lazy('blog:index')

    def test_func(self):
        return self.get_object().author == self.request.user


class EditCommentView(CommentMixin, UpdateView):
    form_class = CommentForm

    def form_valid(self, form):
        form.save(commit=False)
        return super().form_valid(form)


class CommentDeleteView(CommentMixin, DeleteView):
    pass
