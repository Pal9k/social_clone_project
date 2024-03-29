from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
# so that we can return 404 page
from django.http import Http404
from django.contrib import messages

from braces.views import SelectRelatedMixin

from . import models
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
            self.post_user = User.objects.prefetch_related('posts').get(username__iexact=self.kwargs.get('username'))
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
		print("----------------------------")
		queryset = super().get_queryset()
		print(self.kwargs.get("username"))
		# print(queryset.filter(user__username=self.kwargs.get("username"))
		un = self.kwargs.get("username")
		if(un=="delete"):
			print("yes")
		print(un)
		print("----------------------------")
		return queryset.filter(user__username__iexact=self.kwargs.get("username"))

class CreatePost(generic.CreateView,LoginRequiredMixin,SelectRelatedMixin):
	fields = ('message','group')
	model = models.Post
	sucess_url = reverse_lazy('groups:all')
	# sucess_url = reverse_lazy('posts:list')


	def form_valid(self,form):
		print("----------------------------------------------------")
		self.object = form.save(commit=False)
		self.object.user = self.request.user
		self.object.save()
		return super().form_valid(form)

class DeletePost(generic.DeleteView,LoginRequiredMixin,SelectRelatedMixin):
	model = models.Post
	select_related = ('user','group')
	success_url = reverse_lazy('posts:all')

	def get_queryset(self):
		queryset = super().get_queryset()
		return queryset.filter(user_id = self.request.user.id)

	def delete(self,*args,**kwargs):
		messages.success(self.request,'Post Deleted')
		return super().delete(*args,**kwargs)
