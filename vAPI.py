"""
s API interacts with a user and token database.
The code is written to exemplify common API security vulnerabilities
1. No input validation
2. SQL queries are not parameterized
3. No real error handling
4. Errors that are handled give too much information
4. Tokens have an expiration date, but do not expire
5. Token string is generated with an md5 of the expire datetime string
6. Passwords are not hashed in the database
7. There is an *undocumented* GET that returns the user database
"""

import sqlite3
import json
import hashlib
import time
import os
import re
import xml.etree.ElementTree as ET
import logging
from lxml import etree
from bottle import route, run, request, debug
from bottle import hook
from bottle import abort
from bottle import response as resp
from paste import httpserver

logging.basicConfig(filename="vAPI.log",
                            filemode='a',
                            format='%(asctime)s.%(msecs)03d %(levelname)s %(message)s',
                            datefmt='%Y-%m-%dT%H:%M:%S',
                            level=logging.INFO)

logging.info("Starting vAPI")

logger = logging.getLogger('vAPI')

@route('/', method='GET')
def get_root():
    '''
    Give default message for a GET on root directory.
    '''
    src_ip=request.environ.get('HTTP_X_FORWARDED_FOR') or request.environ.get('REMOTE_ADDR')
    response = {'response':
                {
                    'application': 'vAPI',
                    'status': 'running'
                }
                }
    logging.info("app=vAPI: src_ip=%s action=success signature=\"API status request\"" % src_ip)
    return json.dumps(response, sort_keys=True, indent=2)


@route('/tokens', method='POST')
def get_token():
    '''
    User needs to get an auth token before actioning the database
    '''
    src_ip=request.environ.get('HTTP_X_FORWARDED_FOR') or request.environ.get('REMOTE_ADDR')
    content_type = request.headers.get('Content-type')
    if content_type == 'application/xml':
        try:
            # LXML is vulnerable to XXE, etree is vulnerable to Billion Laughs
            # So just have etree try to parse it just to watch it die
            ET.parse(request.body)
        except Exception:
            # But etree will throw an exception for XXE, so ignore that
            pass
        # force unsafe external entity parsing
        parser = etree.XMLParser(load_dtd=True, resolve_entities=True)
        data = etree.parse(request.body, parser)
        username = data.find('passwordCredentials').find('username').text
        password = data.find('passwordCredentials').find('password').text
    else:
        try:
            data = request.json if request.json!=None else {}
        except ValueError, e:
            abort(400, "Bad request")
        username = data.get('auth',{}).get('passwordCredentials',{}).get('username',"")
        password = data.get('auth',{}).get('passwordCredentials',{}).get('password',"")
    conn = sqlite3.connect('vAPI.db')
    c = conn.cursor()
    # no data validation
    # no sql parameterization
    user_query = "SELECT * FROM users WHERE username = '%s' AND password = '%s'" % (
        username, password)
    c.execute(user_query)
    user = c.fetchone()
    response = {}
    if user:
        response['access'] = {}
        response['access']['user'] = {'id': user[0], 'name': user[1]}
        # make sure to get most recent token in database, because we arent
        # removing them...
        token_query = "SELECT * FROM tokens WHERE userid = '%s' ORDER BY expires DESC" % (user[
                                                                                          0])
        c.execute(token_query)
        token_record = c.fetchone()
        if isinstance(token_record, tuple):
            if token_record[3] < int(time.time()):
                # token has expired. create new one that expires 5 minutes
                # after creation
                expire_stamp = int(time.time() + 300)
                expire_date = time.ctime(int(expire_stamp))
                token = hashlib.md5(expire_date).hexdigest()
                # we'll parameterize this one because we need this serious
                # functionality
                c.execute(
                    'INSERT INTO tokens (token, userid, expires) VALUES (?, ?, ?)',
                    (token,
                     user[0],
                        expire_stamp))
                conn.commit()
                response['access']['token'] = {
                    'id': token, 'expires': expire_date}
                logging.info("app=vAPI:tokens src_ip=%s user=%s action=success signature=\"Request token: authentication succeeded, found expired token in db\"" % (src_ip, username))
            else:
                # recent token hasn't expired. use same one.
                expire_date = time.ctime(int(token_record[3]))
                response['access']['token'] = {
                    'id': token_record[1], 'expires': expire_date}
                logging.info("app=vAPI:tokens src_ip=%s user=%s action=success signature=\"Request token: authentication succeeded, found recent token in db\"" % (src_ip, username))
        else:
            # no token exists. create one that expires in 5 minutes
            expire_stamp = int(time.time() + 300)
            expire_date = time.ctime(int(expire_stamp))
            token = hashlib.md5(expire_date).hexdigest()
            # we'll parameterize this one because we need this serious
            # functionality
            c.execute(
                'INSERT INTO tokens (token, userid, expires) VALUES (?, ?, ?)',
                (token,
                 user[0],
                    expire_stamp))
            conn.commit()
            response['access']['token'] = {'id': token, 'expires': expire_date}
            logging.info("app=vAPI:tokens src_ip=%s user=%s action=success signature=\"Request token: authentication succeeded, created new token in db\"" % (src_ip, username))
    else:
        # let's do another look up so we can return helpful info for failure
        # cases
        c.execute("SELECT * FROM users WHERE username = '%s'" % username)
        user = c.fetchone()
        if user:
            response['error'] = {'message': 'password does not match'}
            logging.info("app=vAPI:tokens src_ip=%s user=%s action=failure signature=\"Request token: authentication failed, wrong password\"" % (src_ip, username))
        else:
            logging.info("app=vAPI:tokens src_ip=%s user=%s action=failure signature=\"Request token: authentication failed, user unknown\"" % (src_ip, username))
            response['error'] = {
                'message': 'username ' + username + ' not found'}
    c.close()
    conn.close()

    return {json.dumps(response)}


@route('/tokens', method='GET')
def get_get_token():
    '''
    this is an undocumented request. EASTER EGG
    /tokens is only supposed to accept a POST! Are you checking the other verbs?
    '''
    src_ip=request.environ.get('HTTP_X_FORWARDED_FOR') or request.environ.get('REMOTE_ADDR')
    conn = sqlite3.connect('vAPI.db')
    c = conn.cursor()
    query = "SELECT * FROM users"
    c.execute(query)
    users = c.fetchall()
    c.close()
    conn.close()
    return {'response': users}


@route('/user/<user:re:.*>', method='GET')
def get_user(user):
    '''
    Expects a user id to return that user's data.
    X-Auth-Token is also expected
    '''
    src_ip=request.environ.get('HTTP_X_FORWARDED_FOR') or request.environ.get('REMOTE_ADDR')
    token = request.headers.get('X-Auth-Token')
    conn = sqlite3.connect('vAPI.db')
    c = conn.cursor()
    user_query = "SELECT * FROM users WHERE id = '%s'" % (user)
    c.execute(user_query)
    user_record = c.fetchone()
    token_query = "SELECT * FROM tokens WHERE token = '%s'" % (str(token))
    c.execute(token_query)
    token_record = c.fetchone()
    c.close()
    response = {}
    # you'll notice we don't actually check the token expiration date
    if isinstance(token_record, tuple):
        if isinstance(user_record, tuple):
            if token_record[2] == user_record[0]:
                response['user'] = {}
                response['user']['id'] = user_record[0]
                response['user']['name'] = user_record[1]
                response['user']['password'] = user_record[2]
                logging.info("app=vAPI:user src_ip=%s user=%s action=success signature=\"Requesting user record: success for user record %s\"" % (src_ip, token_record.get(2,""), user))
            else:
                response['error'] = {
                    'message': 'the token and user do not match!'}
                logging.info("app=vAPI:user src_ip=%s user=%s action=failure signature=\"Requesting user record: no permission to show user=%s\"" % (src_ip, token_record.get(2,""), user))
        else:
            response['error'] = {'message': 'user id ' + user + ' not found'}
            logging.info("app=vAPI:user src_ip=%s user=%s action=failure signature=\"Requesting user record: failed for unknown user %s\"" % (src_ip, token_record(2,""), user))
    else:
        response['error'] = {
            'message': 'token id ' + str(token) + ' not found'}
        logging.info("app=vAPI:user src_ip=%s user=%s action=failure \"Requesting user record: authentication failed for user %s\"" % (src_ip, "" , user))
    conn.close()

    return {'response': response}


@route('/user', method='POST')
def create_user():
    src_ip=request.environ.get('HTTP_X_FORWARDED_FOR') or request.environ.get('REMOTE_ADDR')
    token = request.headers.get('X-Auth-Token')
    conn = sqlite3.connect('vAPI.db')
    c = conn.cursor()
    token_query = "SELECT * FROM tokens WHERE token = '%s' AND userid = 10" % (
        str(token))
    c.execute(token_query)
    token_record = c.fetchone()
    response = {}
    if isinstance(token_record, tuple):
        try:
            data = request.json if request.json!=None else {}
        except ValueError, e:
            abort(400, "Bad request")
        name = data['user']['username']
        password = data['user']['password']
        # catastrophically bad regex
        match = "([a-z]+)*[0-9]"
        m = re.search(match, name)
        if m:
            user_query = "SELECT * FROM users WHERE username = '%s'" % (name)
            c.execute(user_query)
            user_record = c.fetchone()
            if isinstance(user_record, tuple):
                response['error'] = {
                    "message": "User %s already exists!" %
                    name}
                logging.info("app=vAPI:user src_ip=%s user=%s action=failure signature=\"Create new user: already existing user %s\"" % (src_ip, token_record[2], name))
            else:
                c.execute(
                    "INSERT INTO users (username, password) VALUES (?, ?)", (name, password))
                conn.commit()
                response['user'] = {"username": name, "password": password}
                logging.info("app=vAPI:user src_ip=%s user=%s action=success signature=\"Create new user: %s\"" % (src_ip, token_record[2], name))
        else:
            response['error'] = {
                "message": "username {0} invalid format, check documentation!".format(name)}
            logging.info("app=vAPI:user src_ip=%s user=%s action=failure signature=\"Create new user: invalid name %s\"" % (src_ip, token_record[2], name))
    else:
        response['error'] = {"message": "must provide valid admin token"}
        logging.info("app=vAPI:user src_ip=%s action=failure signature=\"Create new user: authentication failed, invalid token\"" % src_ip)

    c.close()
    conn.close()
    return{'response': response}


@route('/uptime', method='GET')
@route('/uptime/<flag>', method='GET')
def display_uptime(flag=None):
    src_ip=request.environ.get('HTTP_X_FORWARDED_FOR') or request.environ.get('REMOTE_ADDR')
    if flag:
        command = "uptime -" + flag
        logging.info("app=vAPI:uptime src_ip=%s action=success signature=\"Uptime request: flag=%s\"" % (src_ip, flag))
    else:
        command = "uptime" 
        logging.info("app=vAPI:uptime src_ip=%s action=success signature=\"Uptime request\"" % src_ip) 
    output = os.popen(command).read() 
    response = {'response':
        {
              'Command': command,
              'Output': output
        }}
    return json.dumps(response, sort_keys=True, indent=2)

@route('/widget', method='POST')
def create_widget_reservation():
    src_ip=request.environ.get('HTTP_X_FORWARDED_FOR') or request.environ.get('REMOTE_ADDR')
    token = request.headers.get('X-Auth-Token')
    conn = sqlite3.connect('vAPI.db')
    c = conn.cursor()
    token_query = "SELECT * FROM tokens WHERE token = '%s'" % (
        str(token))
    c.execute(token_query)
    token_record = c.fetchone()
    response = {}
    try:
        data = request.json if request.json!=None else {}
    except ValueError, e:
        abort(400, "Bad request")
    name = data.get('widget', {}).get('name',{})
    if isinstance(token_record, tuple):
        # catastrophically bad regex
        match = "([a-z]+)*[0-9]"
        m = re.search(match, str(name))
        if m:
            response = {"message": "created reservation for widget %s" % name}
            logging.info("app=vAPI:widget src_ip=%s user=%s action=success signature=\"Create reservation: widget=%s\"" % (src_ip, token_record[2], name))
        else:
            response['error'] = {"message": "illegal widget name"}
            logging.info("app=vAPI:widget src_ip=%s user=%s action=failure signature=\"Create reservation: illegal name widget=%s\"" % (src_ip, token_record[2], name))
    else:
        response['error'] = {"message": "must provide valid token"}
        logging.info("app=vAPI:widget src_ip=%s action=failure signature=\"Create reservation: authentication failure widget=%s\"" % (src_ip, name))

    c.close()
    conn.close()
    return{'response': response}

@hook('after_request')
def enable_cors():
    '''
    Method to enable cross origin resource sharing headers
    for all requests.
    '''
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = '*'
    resp.headers['Access-Control-Allow-Headers'] = '*'

debug(True)
run(server='paste', host='0.0.0.0', port=8081, reloader=True)
