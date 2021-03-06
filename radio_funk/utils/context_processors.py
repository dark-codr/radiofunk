import json
import operator
import datetime
from functools import reduce

from django.db.models import Q
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.gis.geoip2 import GeoIP2
from django.contrib.gis.db.models.functions import GeometryDistance
from django.contrib.gis.geos import Point

from radio_funk.tunes.models import Stations
from radio_funk.genre.models import Genre
from radio_funk.podcast.models import Podcast, Episodes
from radio_funk.mode.models import Mode

from radio_funk.utils.logger import LOGGER

User = get_user_model()

dt = datetime.datetime.now()

def context_data(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        if settings.PRODUCTION:
            ip = request.META.get('REMOTE_ADDR')
        else:
            ip = '8.8.8.8'

    if not Mode.objects.filter(ip=ip).exists():
        Mode.objects.create(ip=ip, theme="light")

    if request.user.is_authenticated:
        playlist = request.user.playlist_author.all().order_by("-modified")[:2]
    else:
        playlist = None

    device_type = ""
    browser_type = ""
    browser_version = ""
    os_type = ""
    os_version = ""

    if request.user_agent.is_mobile:
        device_type = "Mobile"
    if request.user_agent.is_tablet:
        device_type = "Tablet"
    if request.user_agent.is_pc:
        device_type = "PC"

    browser_type = request.user_agent.browser.family
    browser_version = request.user_agent.browser.version_string
    os_type = request.user_agent.os.family
    os_version = request.user_agent.os.version_string

    g = GeoIP2()
    location = g.city(ip)
    location_country = location["country_name"]
    location_country_code = location["country_code"]
    location_latitude = location["latitude"]
    location_longitude = location["longitude"]
    location_city = location["city"]

    current_loc = Point(location_longitude, location_latitude, srid=4326)


    new_podcasters = User.managers.latest()
    popular_podcasters = User.managers.popular()
    podcasters = User.managers.podcaster()

    bedtime_podcasts = Podcast.managers.published().filter(
        reduce(
            operator.or_, (
                Q(genre__name__icontains=x)
            for x in ["night", "sleep", "rest"]))
        ).filter(
        reduce(
            operator.or_, (
                Q(name__icontains=x)
            for x in ["night", "sleep", "rest"]))
        ).order_by("-created")[:20]
    moods_podcasts = Podcast.managers.published().filter(reduce(operator.or_, (Q(genre__name__icontains=x) for x in ["love", "romance", "erotic", "sexual", "sad", "happy", "emotional"]))).filter(reduce(operator.or_, (Q(name__icontains=x) for x in ["love", "romance", "erotic", "sexual", "sad", "happy", "emotional"]))).order_by("-created")[:20]
    podcast_documentary = Podcast.managers.published().search(query="documentary")[:20] if Podcast.managers.published().search(query="documentary").exists() else None

    all_radios = Stations.managers.closest(cur_loc=current_loc, dist=5000000000)
    other_radios = Stations.managers.closest(cur_loc=current_loc, dist=5000000000).other_radios(query=location_country)
    fiftykm_close_radios = Stations.managers.closest(cur_loc=current_loc, dist=5000000)[:25] if Stations.managers.closest(cur_loc=current_loc, dist=500000).exists() else None
    closest_radios = Stations.managers.closest(cur_loc=current_loc, dist=5000000)[:12] if Stations.managers.closest(cur_loc=current_loc, dist=500000).exists() else all_radios[:10]
    active_radios = Stations.managers.active().order_by("created")[:12] if Stations.managers.active().exists() else None
    popular_radios = Stations.managers.popular(cur_loc=current_loc, dist=50000000)[:25] if Stations.managers.popular(cur_loc=current_loc, dist=500000).exists() else all_radios[:10]
    radios_in_country = Stations.managers.closest(cur_loc=current_loc, dist=50000000).country(query=location_country)[:20] if Stations.managers.closest(cur_loc=current_loc, dist=50000000).country(query=location_country).exists() else None
    popular_radios_in_country = Stations.managers.popular(cur_loc=current_loc, dist=50000000).country(query=location_country)[:5] if Stations.managers.popular(cur_loc=current_loc, dist=50000000).country(query=location_country).exists() else all_radios[:10]
    radios_in_country_count = Stations.managers.closest(cur_loc=current_loc, dist=50000000).country(query=location_country).count() if Stations.managers.closest(cur_loc=current_loc, dist=50000000).country(query=location_country).exists() else 0
    # podcasts = Podcasts.objects.all().order_by("created")[:12]

    genres = Genre.objects.popular()[:20] if Genre.objects.popular().exists() else None

    if request.user.is_authenticated:
        favorites = request.user.podcast_likes.all()
    else:
        favorites = None

    sleep_episodes = Episodes.objects.filter(
        reduce(
            operator.or_, (
                Q(podcast__genre__name__icontains=x)
            for x in ["night", "sleep", "rest"]))
        ).filter(
        reduce(
            operator.or_, (
                Q(name__icontains=x)
            for x in ["night", "sleep", "rest"]))
        ).order_by("-created").order_by("-created")[:12]

    all_sleep_episodes = Episodes.objects.filter(
        reduce(
            operator.or_, (
                Q(podcast__genre__name__icontains=x)
            for x in ["night", "sleep", "rest"]))
        ).filter(
        reduce(
            operator.or_, (
                Q(name__icontains=x)
            for x in ["night", "sleep", "rest"]))
        ).order_by("-created")

    episodes = Episodes.objects.current()[:12] if Episodes.objects.current().exists() else None
    popular_episodes = Episodes.objects.popular()[:12] if Episodes.objects.popular().exists() else None

    moods = Episodes.objects.filter(reduce(operator.or_, (Q(podcast__genre__name__icontains=x) for x in ["love", "romance", "erotic", "sexual", "sad", "happy", "emotional"]))).filter(reduce(operator.or_, (Q(name__icontains=x) for x in ["love", "romance", "erotic", "sexual", "sad", "happy", "emotional"]))).order_by("-created")[:12]

    all_moods = Episodes.objects.filter(reduce(operator.or_, (Q(podcast__genre__name__icontains=x) for x in ["love", "romance", "erotic", "sexual", "sad", "happy", "emotional"]))).filter(reduce(operator.or_, (Q(name__icontains=x) for x in ["love", "romance", "erotic", "sexual", "sad", "happy", "emotional"]))).order_by("-created")

    documentary = Episodes.objects.search(query="documentary")[:12] if Episodes.objects.search(query="documentary").exists() else None

    all_documentary = Episodes.objects.search(query="documentary")


    if dt.hour >= 4 and dt.hour < 12:
        greeting = "Good Morning"
        sleep = False
    elif dt.hour >= 12 and dt.hour < 17:
        greeting = "Good Afternoon"
        sleep = False
    elif dt.hour >= 17 and dt.hour < 22:
        greeting = "Good Evening"
        sleep = False
    elif dt.hour >= 22 and dt.hour < 4:
        greeting = "Good Night"
        sleep = True
    else:
        greeting = "Welcome"
        sleep = False

    # if Mode.objects.filter(ip=ip, theme=Mode.DARK).exists():
    dark_mode = Mode.objects.filter(ip=ip, theme=Mode.DARK).exists()
    # else:
    #     dark_mode = False

    LOGGER.info(dark_mode)

    return {
        "new_podcasters": new_podcasters,
        "popular_podcasters": popular_podcasters,
        "podcasters": podcasters,
        "bedtime_podcasts": bedtime_podcasts,
        "moods_podcasts": moods_podcasts,
        'podcast_documentary': podcast_documentary,
        "favorites": favorites,

        'active_radios':active_radios,
        'c_radios':closest_radios,
        'closes_fifty': fiftykm_close_radios,
        'playlist': playlist,
        'all_radios': all_radios,
        'radios_in_country': radios_in_country,
        'popular_radios': popular_radios,
        'popular_radios_in_country': popular_radios_in_country,
        'radios_in_country_count': radios_in_country_count,
        'other_radios': other_radios,

        'episodes': episodes,
        'popular_episodes': popular_episodes,
        'documentary': documentary,
        'moods': moods,
        'all_documentary': all_documentary,
        'all_moods': all_moods,
        # 'podcasts':podcasts,
        'genres':genres,
        'sleep_episodes': sleep_episodes,
        'all_sleep_episodes': all_sleep_episodes,

        # IP informations
        'browser_type': browser_type,
        'os_type': os_type,
        'os_version': os_version,
        'user_ip': ip,
        'location_country': location_country,
        'location_country_code': location_country_code,
        'location_latitude': location_latitude,
        'location_longitude': location_longitude,
        'location_city': location_city,

        # Time greeting
        'greeting': greeting,
        'sleep_time': sleep,

        # Device
        'device': device_type,

        # themedate_joined
        'dark': dark_mode,

        "ACCOUNT_ALLOW_REGISTRATION": settings.ACCOUNT_ALLOW_REGISTRATION,
        "settings": settings
    }


