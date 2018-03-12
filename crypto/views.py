from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, HttpResponseRedirect, HttpResponse, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import FeedDetail, FeedUrl
from .scripts import feed_handler
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .forms import SignUpForm
from django.contrib.auth.models import User


def pag(a, request):
    paginator = Paginator(a, 30)
    page = request.GET.get('page')
    try:
        blog_post = paginator.page(page)
    except PageNotAnInteger:
        blog_post = paginator.page(1)
    except EmptyPage:
        blog_post = paginator.page(paginator.num_pages)
    return blog_post

# TODO: Check if caching works
# @csrf_exempt
# @cache_page(60 * 15)
@login_required(login_url=reverse_lazy('landing'))
def home(request):
    feed_list = FeedDetail.objects.filter(user_id=request.user.id).order_by('-pk')
    if request.method == 'POST' and 'refresh' in request.POST:
        user_id = User.objects.all().last().id # TODO: get id of current user...
        hit_list = feed_handler.get_urls(user_id)
        feed_handler.run_it(user_id, hit_list)
        feed_list = FeedDetail.objects.filter(user_id=request.user.id).order_by('-pk')
        return render(request, 'home.html', {'object_list': feed_list})
    return render(request, 'home.html', {'object_list': feed_list})


def landing(request):
    return render(request, 'landing.html')


def test():
    print('hello')


def signup(request): # TODO: need to async login and parsing feeds so its faster!
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.save()
            urls = form.cleaned_data.get('urls')
            if len(urls) > 0:
                user_id = User.objects.all().last().id
                feed_handler.run_it(user_id, urls)
                for url in urls:
                    b = FeedUrl.objects.create(user=user, url=url)
                    b.save()
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=user.username, password=raw_password)
                login(request, user)
                return redirect('home')
            else:
                form = SignUpForm()
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

# TODO: REMOVE DB AND NONSENSE FROM GIT AND ADD TO IGNORE, CHECK ALL FILES TO MAKE SURE NOTHING IMPT IN GITHUB!!
