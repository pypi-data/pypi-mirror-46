import datetime
import pytz

from django.conf import settings
from django.shortcuts import redirect
from django.utils.timezone import now


def CoverPageMiddleware(get_response):
    def middleware(request):
        # get settings
        config = getattr(settings, 'WEBSITE_COVERPAGE', {})
        active = config.get('active', True)
        url = config.get('url', '/coverpage/')
        cookiename = config.get('cookiename', 'coverpage')

        # do redirect if applicable
        if active and \
           cookiename not in request.COOKIES and \
           request.method == 'GET' and \
           not request.is_ajax() and \
           request.path != url:
                do_redirect = True

                # check files to ignore
                ignore_files = config.get('ignore_files', [
                    '/favicon.ico',
                    '/robots.txt'
                ])
                for ig in ignore_files:
                    if request.path.startswith(ig):
                        do_redirect = False
                        break

                # check urls to ignore
                if do_redirect:
                    ignore_urls = config.get('ignore_urls', [])
                    for ig in ignore_urls:
                        if request.path.startswith(ig):
                            do_redirect = False
                            break

                # ignore common bots
                # yes, we should use something like
                if do_redirect:
                    ua = request.META.get('HTTP_USER_AGENT', '').lower()
                    bots = [
                        'apachebench', # not a bot, but it can go here

                        '360spider',
                        'adsbot-google',
                        'ahrefs',
                        'archive.org',
                        'baiduspider',
                        'bingbot',
                        'bingpreview',
                        'dotbot',
                        'duckduckgo',
                        'duckduckbot',
                        'exabot',
                        'facebook',
                        'feedfetcher-google',
                        'googlebot',
                        'googleimageproxy',
                        'ia_archiver',
                        'mediapartners-google',
                        'mj12bot',
                        'msnbot',
                        'panscient.com',
                        'pinterest',
                        'slackbot',
                        'slurp',
                        'sogou',
                        'surveybot',
                        'twitterbot',
                        'voilabot',
                        'yahoo-mmcrawler',
                        'yahoomailproxy',
                        'yandexbot'
                    ]
                    for bot in bots:
                        if bot in ua:
                            do_redirect = False
                            break

                # check start time
                if do_redirect:
                    dt_from = config.get('start', None)
                    if dt_from is not None:
                        tz = pytz.timezone(settings.TIME_ZONE) if settings.USE_TZ else None
                        dt_from = datetime.datetime(*dt_from, tzinfo=tz)
                        if now() < dt_from:
                            do_redirect = False

                # check end time
                if do_redirect:
                    dt_to = config.get('end', None)
                    if dt_to is not None:
                        tz = pytz.timezone(settings.TIME_ZONE) if settings.USE_TZ else None
                        dt_to = datetime.datetime(*dt_to, tzinfo=tz)
                        if now() > dt_to:
                            do_redirect = False

                if do_redirect:
                    response = redirect(url)
                    response.set_cookie(
                        '%s_referrer' % cookiename,
                        request.path
                    )
                    return response

        # nothing to do
        response = get_response(request)
        return response

    return middleware
