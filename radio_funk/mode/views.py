from django.shortcuts import render
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse, HttpRequest, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_http_methods
from django.db import transaction

from radio_funk.utils.logger import LOGGER

from radio_funk.mode.models import Mode

# @require_http_methods(['GET', 'POST', 'PUT'])
def enable_dark_mode(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        if settings.PRODUCTION:
            ip = request.META.get('REMOTE_ADDR')
        else:
            ip = '8.8.8.8'

    LOGGER.info(f"IP Address: {ip}")

    Mode.objects.filter(ip=ip, theme='light').update(theme='dark')

    # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponse("""
        <button :class="{'hidden':dark === true, '':dark === false}" x-on:click="dark = true, iziToast.success({'message':'Dark Mode Activated', 'id':'alert-success', 'color':'green', 'title':'DARK MODE', 'timeout': 5000, 'resetOnHover': true, 'balloon': true})" hx-post="/dark_mode/" hx-trigger="click" hx-swap="outerHTML" class="block" type="button">
            <svg class="w-6 h-6 text-font-darker dark:text-primary" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
              <path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z"></path>
            </svg>
        </button>
    """)


@require_http_methods(['PUT'])
def enable_light_mode(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
        return str(ip)
    else:
        if settings.PRODUCTION:
            ip = str(request.META.get('REMOTE_ADDR'))
        else:
            ip = '8.8.8.8'

    Mode.objects.filter(ip=ip, theme="dark").update(theme="light")
    # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponse("""
        <button :class="{'':dark === true, 'hidden':dark === false}" x-on:click="dark = false, iziToast.error({'message':'Dark Mode Deactivated', 'id':'alert-error', 'color':'red', 'title':'DARK MODE', 'timeout': 5000, 'resetOnHover': true, 'balloon': true,})" hx-put="/light_mode/" hx-trigger="click" hx-swap="outerHTML" class="block" type="button">
            <svg class="w-6 h-6 text-font-darker dark:text-primary" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                <path fill-rule="evenodd" d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z" clip-rule="evenodd"></path>
            </svg>
        </button>
    """)
