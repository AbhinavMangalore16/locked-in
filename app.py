import os
import ast
from os import environ as env
from dotenv import load_dotenv
import pymongo
import pandas as pd
import numpy as np
from urllib.parse import quote_plus, urlencode
import logging
import json
import utils
import utils.data_utils
from authlib.integrations.flask_client import OAuth # type: ignore
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, session, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash


utils.logs_utils.setup_logging("LOGS/data_export.log")
logger = logging.getLogger(__name__)

load_dotenv()

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['APP_SECRET_KEY']

db = utils.data_utils.connect_db()

utils.logs_utils.setup_logging("LOGS/app.log")
logger = logging.getLogger(__name__)

oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)

@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )

@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )

@app.route("/")
def home():
    if session.get('user'):
        # print(session.get('user'), json.dumps(session.get('user')))
        # print(ast.literal_eval(json.dumps(session.get('user')))['email'])
        print(ast.literal_eval(str(session.get('user'))))
        return render_template("home.html", session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))
    
    else:
        return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=env.get("PORT", 3000))