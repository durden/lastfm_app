# Create your views here.
from django.shortcuts import render_to_response
from lastfm.findshows.forms.forms import ShowsForm

import datetime

import pylast
import eventful

API_KEY = "2465572f9a20dc3775129665207edfcf"
API_SECRET = "ed9ccfacd5df88cf05c0d58fb546481c"

def home(request):
    form = ShowsForm()
    return render_to_response('home.html', {'form' : form})

def myshows(request):
    if request.method == 'POST':
        form = ShowsForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['username']
            shows = __find_shows__(user)
            return render_to_response('myshows.html', {'myshows' : shows,
                                      'user' : user})

def __find_shows__(lastfm_user):
    user = pylast.User(user_name=lastfm_user, api_key=API_KEY,
                       api_secret=API_SECRET, session_key=None)
    api = eventful.API(app_key="hdpzLJWDRbFWFsLf")

    try:
        bands = user.get_top_artists()
    except pylast.ServiceException:
        return None

    myshows = {}

    for band in bands[:20]:
        bname = band.get_item().get_name().encode('utf-8')
        per = 'performer:"%s"' % (bname)
        shows = api.call(method="events/search", location="Houston, Tx",
                         keywords=per)

        if int(shows['total_items']) > 0:
            myshows[bname] = []
            for show in shows['events']['event']:
                time = datetime.datetime.strptime('2009-07-22 19:30:00',
                                                  '%Y-%m-%d %H:%M:%S')
                myshows[bname].append({'venue' : show['venue_name'],
                                       'time' : time})
    return myshows
