from django.shortcuts import render, redirect
from django.views import generic
from django.http import HttpResponse

from .scrapper import format_url, get_torrents, download_torrent


class HomePage(generic.TemplateView):
    template_name = 'torrents/index.html'


def search(request):
    search_key = request.GET['q']
    url = format_url(search_key)
    return render(
        request,
        'torrents/torrents_list.html',
        context={
            'torrents': get_torrents(url),
            'search_key': search_key
        }
    )


def download(request):
    download_torrent(request.GET['link'])
    return redirect(request.META['HTTP_REFERER'])
