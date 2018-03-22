#!/usr/bin/env python3

import datetime
import time
from .data import getBoardDict
from . import CONFIG, app
from .parse import processEvent, parseData
from flask import request, render_template, make_response


def getEpoch():
    return time.mktime(datetime.datetime.now().timetuple())


@app.route('/', methods=['GET'])
def index():
    error = ""
    board = getBoardDict()
    resp = make_response(render_template('index.html', error=error,
                         board=board, teams=CONFIG['teams']))
    return resp


@app.route('/slack-events', methods=['POST'])
def slack_events():
    res = request.json
    if res.get('challenge', None):
        return request.json['challenge']

    # to get the 'channel' value right click on the channel and copy link
    # I.E C9PGYTYH5
    if res.get('event', None) and res.get('event')['channel'] == '':
        processEvent(res['event'])

    return ""


@app.route('/generic', methods=['POST'])
def genericEvent():
    req = request.get_json(force=True)
    if req.get('challenge', None):
        return req.json['challenge']
    data = {}
    # Type and IP are required
    if 'type' in req:
        data['type'] = req.get('type')
    else:
        return "Invalid data"
    if 'ip' in req:
        data['ip'] = req.get('ip')
    else:
        return "Invalid data"
    # Host and Session are not required
    data['host'] = None
    data['session'] = None
    # Time is calculated
    data['last_seen'] = getEpoch()
    parseData(data)
    return "Valid"
