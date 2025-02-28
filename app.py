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
from utils.gemini_utils import get_career_roadmap
import utils.pdf_utils


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
        user_data = utils.data_utils.exist_user(ast.literal_eval(str(session.get('user'))))

        return render_template("home.html", name=user_data['name'], email=user_data['email'], user_data=user_data)
    
    else:
        return render_template("navbar.html")

@app.route("/predict", methods=["POST"])
def profile():
    data = request.form

    user_input = {
        "name": data['name'],
        "email": data['email'],
        "age_group": data['age_group'],
        "current_role": data['current_role'],
        "industry": data['industry'],
        "experience": data['experience'],
        "career_goal": data['career_goal'],
        "new_career": data['new_career'],
        "career_switch": data['career_switch'],
        "skills": data['skills'],
        "learning_style": data['learning_style'],
        "time_commitment": data['time_commitment'],
        "budget": data['budget']
    }

    utils.data_utils.insert_or_update_user(user_input)

    profile = utils.data_utils.find_user_by_email(user_input['email'])

    output = get_career_roadmap(profile)

    return render_template("output.html", prediction=output)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'pdf_file' not in request.files:
        return "No file part", 400

    file = request.files['pdf_file']
    goal = request.form['goal']

    if file.filename == '':
        return "No selected file", 400

    if file and file.filename.endswith('.pdf'):
        file.save(file.filename)
        # return f"File successfully uploaded to {file.filename}", 200

        resume_text = utils.pdf_utils.extract_text_from_pdf(file.filename)

    data = {'resume': resume_text, 'goal': goal}

    return render_template("output.html", prediction=get_career_roadmap(data))

    # return "Invalid file format. Please upload a PDF.", 400
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=env.get("PORT", 3000))