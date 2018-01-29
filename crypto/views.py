from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, HttpResponseRedirect, HttpResponse, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import FeedUrl, FeedDetail
from .scripts import feed_handler


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
    feed_list = FeedDetail.objects.all().order_by('-pk')
    if request.method == 'POST' and 'refresh' in request.POST:
        feed_handler.run_it()
        return render(request, 'home.html', {'object_list': feed_list})
    return render(request, 'home.html', {'object_list': feed_list})
