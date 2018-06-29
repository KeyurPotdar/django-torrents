import os
import re
import requests
import subprocess
import sys
from bs4 import BeautifulSoup

WEBSITE_NAME = 'https://piratepirate.eu'
WEBSITE_PREFIX = '/s/?q='
WEBSITE_SPACE = '+'
WEBSITE_SUFFIX = '&page=0&orderby=99'

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}


def format_episode(season, episode):
    return 's{:02d}e{:02d}'.format(season, episode)


def format_url(name, season=None, episode=None):
    """
    Usage:
    (1): format_url('the office', 4, 11)
    (2): format_url('the office', 's04e11')
    (3): format_url('the office s04e11')
    """
    if season is None and episode is None:
        return WEBSITE_NAME + WEBSITE_PREFIX + name.replace(' ', WEBSITE_SPACE) + WEBSITE_SUFFIX
    if episode:
        episode = format_episode(season, episode)
    else:
        episode = season
    return WEBSITE_NAME + WEBSITE_PREFIX + name.replace(' ', WEBSITE_SPACE) + WEBSITE_SPACE + episode + WEBSITE_SUFFIX


def download_torrent(link):
    r = requests.get(link, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    magnet = soup.find('a', {'title': 'Get this torrent'}).get('href')

    if sys.platform.startswith('linux'):
        subprocess.Popen(['xdg-open', magnet], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    elif sys.platform.startswith('win32'):
        os.startfile(magnet)
    elif sys.platform.startswith('cygwin'):
        os.startfile(magnet)
    elif sys.platform.startswith('darwin'):
        subprocess.Popen(['open', magnet], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        subprocess.Popen(['xdg-open', magnet], stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def get_torrents(url):
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')

    torrents_list = []
    for tr in soup.select('#searchResult tr')[1:]:
        try:
            det_link = tr.find('a', {'class': 'detLink'})
            name = det_link.text
            href = det_link.get('href')
            seeders, leechers = [x.text for x in tr.find_all('td', {'align': 'right'})]
            info_regex = re.compile(r'Uploaded (.*), Size (.*), ULed by (.*)')
            uploaded, size, uploader = info_regex.search(tr.find('font', {'class': 'detDesc'}).text).groups()
            torrents_list.append({
                'name': name,
                'seeders': seeders,
                'leechers': leechers,
                'uploaded': uploaded,
                'size': size,
                'uploader': uploader,
                'link': WEBSITE_NAME + href,
            })
        except AttributeError:
            continue

    return torrents_list
