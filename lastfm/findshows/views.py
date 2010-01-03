"""Views for viewing upcoming show for favorite lastfm bands"""

from django.shortcuts import render_to_response
from lastfm.findshows.forms.forms import ShowsForm

import datetime

import pylast
import eventful

API_KEY = "2465572f9a20dc3775129665207edfcf"
API_SECRET = "ed9ccfacd5df88cf05c0d58fb546481c"


def home(request):
    """Show base form to view upcoming shows"""

    if request.method == 'GET':
        form = ShowsForm()
        return render_to_response('home.html', {'form': form})


def myshows(request):
    """Handle request for upcoming shows"""

    if request.method == 'POST':
        form = ShowsForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['username']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            shows = __find_shows(user, city, state)
            return render_to_response('myshows.html', {'myshows': shows,
                                      'user': user})

    return render_to_response('home.html')


def __find_shows(lastfm_user, city, state):
    """Look up top bands for lastfm user and check eventful for shows"""

    user = pylast.User(user_name=lastfm_user, api_key=API_KEY,
                       api_secret=API_SECRET, session_key=None)
    api = eventful.API(app_key="hdpzLJWDRbFWFsLf")

    try:
        bands = user.get_top_artists()
    except pylast.ServiceException:
        return None

    shows = {}

    for band in bands[:20]:
        bname = band.get_item().get_name().encode('utf-8')
        per = 'performer:"%s"' % (bname)
        loc = "%s, %s" % (city, state)
        res = api.call(method="events/search", location=loc, keywords=per)

        if int(res['total_items']) > 0:
            shows[bname] = []
            for show in res['events']['event']:
                time = datetime.datetime.strptime(show['start_time'],
                                                  '%Y-%m-%d %H:%M:%S')
                shows[bname].append({'venue': show['venue_name'],
                                       'time': time})
    return shows
