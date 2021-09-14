from flask import Flask, request, jsonify
from marshmallow import validate
import requests
from flask_api import status
from webargs import fields
from webargs.flaskparser import use_args

from app import app, cache
import os
from werkzeug.datastructures import Range

CACHE_TIMEOUT = 30

MAX_INPUT_LENGTH = 40
MIN_INPUT_LENGTH = 1

@app.route("/dependencies", methods = ['GET'])
# Performing a very basic input validation, should be extended.
# For example: versioning has a specific format, need to address that, min/max length can vary between parameters 
@use_args({"package": fields.Str(required=True, validate=[validate.Length(min = MIN_INPUT_LENGTH, max=MAX_INPUT_LENGTH)]), 
           "version": fields.Str(required=True, validate=[validate.Length(min = MIN_INPUT_LENGTH, max=MAX_INPUT_LENGTH)])}, location="query")
@cache.cached(timeout=CACHE_TIMEOUT, query_string=True)
def get_dependencies(args):
    """ get depedencies
    ---
    get:
      parameters:
      - in: package
      - in: version
      responses:
        200:
          content:
            depencies tree json
        404:
          package not found
    """
    NPM_URL = "https://registry.npmjs.org/"
    npm_package_name = args.get('package')
    npm_package_version = args.get('version')
    result = requests.get(f"{NPM_URL}/{npm_package_name}/{npm_package_version}")
    if result.status_code == 404:
        return "Package not found", status.HTTP_404_NOT_FOUND
    npm_pacakge_json = result.json()
    depedency_tree = {}
    if 'dependencies' in npm_pacakge_json:
        depedency_tree['dependencies'] = npm_pacakge_json['dependencies']
    if 'optionalDependencies' in npm_pacakge_json:
        depedency_tree['optionalDependencies'] = npm_pacakge_json['optionalDependencies']
    if 'devDependencies' in npm_pacakge_json:
        depedency_tree['devlDependencies'] = npm_pacakge_json['devDependencies']
    return jsonify(depedency_tree), status.HTTP_200_OK
