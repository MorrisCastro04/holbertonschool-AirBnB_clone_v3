#!/usr/bin/python3
""""""
from api.v1.views.index import app_views
from flask import app, jsonify


app.route('/status', methods=['GET'], strict_slashes=False)
def status():
    return jsonify({"status": "OK"})
