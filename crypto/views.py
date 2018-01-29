from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, HttpResponseRedirect, HttpResponse, get_object_or_404, redirect
from .models import Feeds
from .scripts.feed_handler import run_it
from django.views.decorators.csrf import csrf_exempt
from sklearn.feature_extraction.text import TfidfVectorizer


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


@csrf_exempt
def home(request):
    feed_list = Feeds.objects.all().order_by('-pk')
    if request.method == 'POST' and 'refresh' in request.POST:
        run_it()
        return render(request, 'home.html', {'object_list': feed_list})
    return render(request, 'home.html', {'object_list': feed_list})

