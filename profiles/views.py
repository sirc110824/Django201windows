from django.contrib.auth.models import User
from django.views.generic import DetailView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseBadRequest
from followers.models import Follower
from django.shortcuts import render, redirect
from feed.models import Post
from .forms import ProfileUpdateForm

class ProfileDetailView(DetailView, View):
    http_method_names = ["get"]
    template_name = "profiles/detail.html"
    model = User
    context_object_name = "user" 
    slug_field = "username"
    slug_url_kwarg = "username"

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        user = self.get_object()
        context = super().get_context_data(**kwargs)
        context['total_post'] = Post.objects.filter(author=user).count()
        context['total_follower'] = Follower.objects.filter(following=user).count()
        context['total_following'] = Follower.objects.filter(followed_by=user).count()
        if self.request.user.is_authenticated:
            context['is_own_profile'] = self.request.user == user

            context['you_follow'] = Follower.objects.filter (following=user, followed_by=self.request.user).exists()
        return context

class FollowView (LoginRequiredMixin, View):
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        if "action" not in data or "username" not in data:
            return HttpResponseBadRequest("Missing data")
        try:
            other_user = User.objects.get(username=data ['username'])
        except User.DoesNotExist:
            return HttpResponseBadRequest("Missing user")
        
        if other_user == request.user:
            return HttpResponseBadRequest("You cannot follow yourself")
            
        if data['action'] == "follow":
            follower, created = Follower.objects.get_or_create (
                followed_by = request.user,
                following = other_user
            )
        else:

            try:
                follower = Follower.objects.get(
                    followed_by = request.user,
                    following = other_user,
                )

            except Follower.DoesNotExist:
                follower = None

            if follower:
                follower.delete()

        return JsonResponse ({
            'success': True,
            'wording': "Unfollow" if data ['action'] == "follow"
                else "Follow"
        })

class ProfileUpdateView(LoginRequiredMixin, View):

    def get(self, request):
        form = ProfileUpdateForm(
            instance=request.user.profile
        )

        return render(
            request,
            "profiles/edit_profile.html",
            {"form": form}
        )

    def post(self, request):
        form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user.profile
        )

        if form.is_valid():
            form.save()

            return redirect(
                "profile:detail",
                username=request.user.username
            )

        return render(
            request,
            "profiles/edit_profile.html",
            {"form": form}
        )