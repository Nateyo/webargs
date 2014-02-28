# -*- coding: utf-8 -*-
"""Flask request argument parsing module.

Example: ::

    from flask import Flask
    from webargs import Arg
    from webargs.flaskparser import use_args

    app = Flask(__name__)

    hello_args = {
        'name': Arg(str, required=True)
    }

    @app.route('/')
    @use_args(hello_args)
    def index(args):
        return 'Hello ' + args['name']
"""
from flask import request
from flask import abort as flask_abort
from werkzeug.exceptions import HTTPException

from webargs import core

def abort(http_status_code, **kwargs):
    """Raise a HTTPException for the given http_status_code. Attach any keyword
    arguments to the exception for later processing.

    From Flask-Restful. See NOTICE file for license information.
    """
    try:
        flask_abort(http_status_code)
    except HTTPException as err:
        if len(kwargs):
            err.data = kwargs
        raise err


class FlaskParser(core.Parser):
    """Flask request argument parser."""

    def parse_json(self, req, name, arg):
        """Pull a json value from the request."""
        try:
            return self._get_value(req.json, name, arg.multiple)
        except AttributeError:
            return None

    def parse_querystring(self, req, name, arg):
        """Pull a querystring value from the request."""
        return self._get_value(req.args, name, arg.multiple)

    def parse_form(self, req, name, arg):
        """Pull a form value from the request."""
        try:
            return self._get_value(req.form, name, arg.multiple)
        except AttributeError:
            return None

    def parse_headers(self, req, name, arg):
        """Pull a value from the header data."""
        return self._get_value(req.headers, name, arg.multiple)

    def parse_cookies(self, req, name, arg):
        """Pull a value from the cookiejar."""
        return self._get_value(req.cookies, name, arg.multiple)

    def parse_files(self, req, name, arg):
        """Pull a file from the request."""
        return self._get_value(req.files, name, arg.multiple)

    def _get_value(self, d, name, multiple):
        if multiple:
            if hasattr(d, 'getlist'):
                return d.getlist(name)
            else:
                return [d.get(name)]
        return d.get(name)

    def handle_error(self, error):
        """Handles errors during parsing. Aborts the current HTTP request and
        responds with a 400 error.
        """
        abort(400, message=error)

    def parse(self, argmap, req=None, *args, **kwargs):
        """Parses the request using the given arguments map.
        Uses Flask's context-local request object if req=None.
        """
        req_obj = req or request  # Default to context-local request
        return super(FlaskParser, self).parse(argmap, req_obj, *args, **kwargs)


use_args = FlaskParser().use_args
