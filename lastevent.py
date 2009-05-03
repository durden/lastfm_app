#!/usr/bin/env python

import pylast
import eventful

user = pylast.User(user_name="durden2.0",
                   api_key="2465572f9a20dc3775129665207edfcf",
                   api_secret="ed9ccfacd5df88cf05c0d58fb546481c",
                   session_key=None)

api = eventful.API(app_key="hdpzLJWDRbFWFsLf")
bands = user.get_top_artists()

for band in bands[:20]:
    bname = band.get_item().get_name().encode('utf-8')
    per = 'performer:"%s"' % (bname)
    print "Searching for", bname
    shows = api.call(method="events/search", location="Houston, Tx",
                     keywords=per)

    if int(shows['total_items']) > 0:
        for show in shows['events']['event']:
            print "%s playing at %s on %s" % (bname, show['venue_name'],
                                              show['start_time'])
