from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utls import reverse_lazy
from django.views import generic
# so that we can return 404 page
from django.http import Http404

from braces.views import SelectRelatedMixin

from . import momdels
from . import forms
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.

class PostList(generic.ListView,SelectRelatedMixin):
	model = models.Post
    select_related = ('user','group')

class UserPosts(generic.ListView):
    model = models.Post
    template_name = 'posts/user_post_list.html'

    def get_queryset(self):
        try:
            self.post.user = User.objects.prefetch_related('posts').get(username__iexact=self.kwargs.get('username'))
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['post_user'] = self.post_user
        return context

class PostDetail(generic.DetailView,SelectRelatedMixin):
	model = models.Post
    select_related = ('user','group')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user__username__iexact=self.kwargs.get('username'))

class CreatePost(generic.CreateView,LoginRequiredMixin,SelectRelatedMixin):
    fields = ('message','group')
	model = models.Post
	sucess_url = reverse_lazy('posts:list')

    def from_valid(self,form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

class DeletePost(generic.DeleteView,LoginRequiredMixin,SelectRelatedMixin):
	model = models.post
    select_related = ('user','group')
	success_url = reverse_lazy('posts:all')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id = self.request.user.id)

    def delete(self,*args,**kwargs):
        message.success(self.request,'Post Deleted')
        return super().delete(*args,**kwargs)
