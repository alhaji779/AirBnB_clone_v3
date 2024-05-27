#!/usr/bin/python3
""" app file for rest-api
"""
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """ teardown function"""
    storage.close()


@app.errorhandler(404)
def 404_page(e):
    return jsonify({"error": "Not found"})


if __name__ == "__main__":
    apiHOST = getenv("HBNB_API_HOST", default="0.0.0.0")
    apiPORT = getenv("HBNB_API_PORT", default=5000)
    app.run(host=apiHOST, port=int(apiPORT), threaded=True)
