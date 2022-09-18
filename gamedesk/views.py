from django.shortcuts import render, redirect

from .models import *
from django.views.generic import *
from .forms import *
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
#from .utils.permissions import IsAuthorMixin, NotIsAuthorMixin
from django.contrib import messages

class PostList(ListView):
    model = Post
    context_object_name = 'post_list'
    queryset = Post.objects.order_by('-dateCreation')

class PostDetail(DetailView):
    model = Post
    context_object_name = 'post_detail'
    template_name = 'gamedesk/post_detail.html'

class PostCreate(LoginRequiredMixin, CreateView):
    template_name = 'gamedesk/post_create.html'
    form_class = PostForm
    context_object_name = 'post_create'
    model = Post
    permission_required = ('post.post_create', )

    def get_absolute_url(self):
        return reverse('post_list', args=[str(self.id)])

class PostUpdate(LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'gamedesk/post_create.html'
    permission_required = ('post.post_create',)
    success_url = '/gamedesk/'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'gamedesk/post_delete.html'
    success_url = '/gamedesk/'
    queryset = Post.objects.all()
    permission_required = ('post.post_delete',)

class CommentList(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        post_pk = kwargs['post_pk']
        post = Post.objects.get(pk=post_pk)
        qs = Comment.objects.order_by('-dateCreation').filter(post=post)

        context = {
            'comments': qs,
            'post': post
        }

        return render(request, 'gamedesk/comment_list.html', context)


class CommentCreate(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        form = CommentCreateForm(request.POST or None)
        post = Post.objects.get(pk=kwargs['post_pk'])

        context = {
            'form': form,
            'post': post
        }

        return render(request, 'gamedesk/comment_create.html', context)

    def post(self, request, *args, **kwargs):
        form = CommentCreateForm(request.POST)
        user = request.user
        post_pk = kwargs['post_pk']

        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = user
            comment.post = Post.objects.get(pk=post_pk)
            comment.save()

        return redirect('/gamedesk/')

class CommentDelete(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'gamedesk/comment_delete.html'
    success_url = '/gamedesk/'
    permission_required = ('gamedesk.comment_delete')
    context_object_name = 'comment'

    def get_object(self, **kwargs ):
        comment_id = self.kwargs.get('comment_pk')
        comment = Comment.objects.get(pk=comment_id)
        return comment

class CommentAccept(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        comment_pk = kwargs['comment_pk']

        comment = Comment.objects.get(pk=comment_pk)
        comment.approved = True
        comment.save()

        return redirect(request.META['HTTP_REFERER'])


class CommentReject(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        comment_pk = kwargs['comment_pk']

        comment = Comment.objects.get(pk=comment_pk)
        comment.approved = False
        comment.save()

        return redirect(request.META['HTTP_REFERER'])

class ByAuthorView(ListView):
    def get(self, request, *args, **kwargs):
      author = User.objects.get(username=kwargs['name'])
      qs = Post.objects.order_by('dateCreation').filter(author = author)

      context = {
          'author': author,
          'posts': qs,
      }

      return render(request, 'by_author.html', context)


