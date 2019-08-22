from flask import Flask, jsonify
from app.views import bp

app = Flask(__name__)
# app.secret_key = 'super secret string'  # Change this!

app.register_blueprint(bp, url_prefix='/api')

from app import views # noqa
