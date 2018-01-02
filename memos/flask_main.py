"""
Flask web app connects to Mongo database.
Keep a simple list of dated memoranda.

Representation conventions for dates: 
   - We use Arrow objects when we want to manipulate dates, but for all
     storage in database, in session or g objects, or anything else that
     needs a text representation, we use ISO date strings.  These sort in the
     order as arrow date objects, and they are easy to convert to and from
     arrow date objects.  (For display on screen, we use the 'humanize' filter
     below.) A time zone offset will 
   - User input/output is in local (to the server) time.  
"""
import json
import flask
from flask import g
from flask import render_template
from flask import request
from flask import url_for

import json
import logging

import sys

# Date handling
import arrow
from dateutil import tz  # For interpreting local times

# Mongo database
import model

import config
CONFIG = config.configuration()

###
# Globals
###

app = flask.Flask(__name__)
app.secret_key = CONFIG.SECRET_KEY

####
# Database connection per server process
###
DBCONFIG = model.DB_config(CONFIG.DB_USER,
                           CONFIG.DB_USER_PW,
                           CONFIG.DB_HOST,
                           CONFIG.DB_PORT,
                           CONFIG.DB)
DB = model.DB(DBCONFIG)
DB.set_collection("dated")
###
# Pages
###


@app.route('/zippologin', methods=['GET', 'POST'])
def login():
  error = None
  if request.method == 'POST':
    if request.form['username'] != CONFIG.ADMIN or request.form['password'] != CONFIG.ADMIN_PSW:
      error = 'Invalid Credentials. Please try again.'
    else:
      flask.session["SessionLoginProof"] = CONFIG.ADMIN
      return flask.redirect(url_for('index'))
  return render_template('login.html', error=error)


@app.route("/")
@app.route("/index")
def index():
  app.logger.debug("Main page entry")
  if flask.session.get("SessionLoginProof") == CONFIG.ADMIN:
    flask.g.LoginProof = True
  '''
  g.memos = get_memos()
  for memo in g.memos:
    app.logger.debug("Memo: " + str(memo))
  '''
  return flask.render_template('index.html')


# We don't have an interface for creating memos yet
# @app.route("/create")
# def create():
#     app.logger.debug("Create")
#     return flask.render_template('create.html')


@app.errorhandler(404)
def page_not_found(error):
  app.logger.debug("Page not found")
  return flask.render_template('page_not_found.html',
                               badurl=request.base_url,
                               linkback=url_for("index")), 404

#################
#
# Functions used within the templates
#
#################


@app.route("/_getmemos")
def _get_memos():
  """
  Returns all memos in the database, in a form that
  can be inserted directly in the 'session' object.
  """
  app.logger.debug("Begin loading all the memo from database")
  rslt = {"memos": DB.get_all()}
  return flask.jsonify(result=rslt)

@app.route("/_getDetailedMemo")
def _get_detail():
  """
  Returns all memos in the database, in a form that
  can be inserted directly in the 'session' object.
  """
  app.logger.debug("Begin loading the detail of a memo from database")
  date_time = request.args.get("date_time")
  title = request.args.get("memo_title")
  date_time = str(arrow.get(date_time).timestamp)
  #rslt = {}
  rslt = {"memos": DB.get({'date': date_time}, title)}
  print(rslt)
  return flask.jsonify(result=rslt)

@app.route("/_delmemos", methods=['GET', 'POST'])
def _del_memos():
  if flask.session.get("SessionLoginProof") == CONFIG.ADMIN:
    memos = request.get_json()
    for date in memos:
      print(model.record(date, memos[date]))
      DB.delete_memos(model.record(date, memos[date]))
  return flask.jsonify(success=True, data=memos)


@app.route("/_sendmemo")
def _set_memo():
  if flask.session.get("SessionLoginProof") == CONFIG.ADMIN:
    app.logger.debug("Got a memo input request")
    date_time = request.args.get("date_time", type=str)
    title = request.args.get("title", type=str)
    memo = request.args.get("memo", type=str)
    app.logger.debug("They are " + date_time + " with title " + title)

    DB.insert(model.record(date_time, title, memo))
  rslt = {}
  return flask.jsonify(result=rslt)


#############
#
# Functions available to the page code above
#
##############


if __name__ == "__main__":
  app.debug = CONFIG.DEBUG
  app.logger.setLevel(logging.DEBUG)
  app.run(port=CONFIG.PORT, host="0.0.0.0")
