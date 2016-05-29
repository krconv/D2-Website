#! /home/krconverse/local/bin/python3.4
#-*- coding: iso-8859-1 -*-
# Copyright (C) 2006 Martin Glueck. All rights reserved
# 351 Bienterra Trail, #2, Rockford, IL, 61107, martin.glueck@insightbb.com
# ****************************************************************************
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the Free
# Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
# ****************************************************************************
#
#++
# Name
#    django.core.handlers.CGI
#
# Purpose
#    A CGI Handler for Django
#
# Revision Dates
#    14-Jul-2006 (MG) Creation
#    ««revision-date»»···
#--

import django
import sys
from   django                       import http
from   django.core.handlers.base    import BaseHandler
from   django.core                  import signals
from   django.dispatch              import dispatcher
from   django.utils                 import datastructures

__all__          = ["CGI_Handler"]

# See http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html
STATUS_CODE_TEXT = \
    { 100 : "CONTINUE"
    , 101 : "SWITCHING PROTOCOLS"
    , 200 : "OK"
    , 201 : "CREATED"
    , 202 : "ACCEPTED"
    , 203 : "NON-AUTHORITATIVE INFORMATION"
    , 204 : "NO CONTENT"
    , 205 : "RESET CONTENT"
    , 206 : "PARTIAL CONTENT"
    , 300 : "MULTIPLE CHOICES"
    , 301 : "MOVED PERMANENTLY"
    , 302 : "FOUND"
    , 303 : "SEE OTHER"
    , 304 : "NOT MODIFIED"
    , 305 : "USE PROXY"
    , 306 : "RESERVED"
    , 307 : "TEMPORARY REDIRECT"
    , 400 : "BAD REQUEST"
    , 401 : "UNAUTHORIZED"
    , 402 : "PAYMENT REQUIRED"
    , 403 : "FORBIDDEN"
    , 404 : "NOT FOUND"
    , 405 : "METHOD NOT ALLOWED"
    , 406 : "NOT ACCEPTABLE"
    , 407 : "PROXY AUTHENTICATION REQUIRED"
    , 408 : "REQUEST TIMEOUT"
    , 409 : "CONFLICT"
    , 410 : "GONE"
    , 411 : "LENGTH REQUIRED"
    , 412 : "PRECONDITION FAILED"
    , 413 : "REQUEST ENTITY TOO LARGE"
    , 414 : "REQUEST-URI TOO LONG"
    , 415 : "UNSUPPORTED MEDIA TYPE"
    , 416 : "REQUESTED RANGE NOT SATISFIABLE"
    , 417 : "EXPECTATION FAILED"
    , 500 : "INTERNAL SERVER ERROR"
    , 501 : "NOT IMPLEMENTED"
    , 502 : "BAD GATEWAY"
    , 503 : "SERVICE UNAVAILABLE"
    , 504 : "GATEWAY TIMEOUT"
    , 505 : "HTTP VERSION NOT SUPPORTED"
    }

class CGI_Request (http.HttpRequest) :
    """A Request from a normal CGI interface."""

    _request                = None
    _get                    = None
    _post                   = None
    _cookies                = None
    _files                  = None

    def __init__ (self, environ) :
        ### don't chain up, we set the dict's here as properties
        ### super (CGI_Request, self).__init__ (self, environ)
        self.environ   = environ
        self.path      = environ.get ("REDIRECT_URL", "/")
        self.META      = environ
        self.method    = environ.get ("REQUEST_METHOD", "GET").upper()
    # end def __init__

    def __repr__(self):
        return "\n".join \
            ( ( "<%s" % (self.__class__.__name__)
              , "  GET:  %r"    % (self.GET)
              , "  POST: %r"    % (self.POST)
              , "  COOKIES: %r" % (self.COOKIES)
              , "  META: %r"    % (self.META)
              , ">"
              )
            )
    # end def __repr__

    def get_full_path(self):
        return '%s%s' % \
            ( self.path
            ,            self.environ.get ("QUERY_STRING", "")
              and ("?" + self.environ     ["QUERY_STRING"])
              or ''
            )
    # end def get_full_path

    def _load_post_and_files(self):
        # Populates self._post and self._files
        if self.method == "POST" :
            if self.environ.get ("CONTENT_TYPE", "").startswith ("multipart") :
                header_dict = dict\
                    ( [ (k, v) for k, v in self.environ.iteritems ()
                                 if k.startswith('HTTP_')
                      ]
                    )
                header_dict ["Content-Type"] = self.environ.get \
                    ("CONTENT_TYPE", "")
                (self._post, self._files
                ) = http.parse_file_upload (header_dict, self.raw_post_data)
            else :
                self._post  = http.QueryDict (self.raw_post_data)
                self._files = datastructures.MultiValueDict ()
        else:
            self._post  = http.QueryDict                ("")
            self._files = datastructures.MultiValueDict ()
    # end def _load_post_and_files

    def _get_request(self):
        if self._request is None :
            self._request = datastructures.MergeDict (self.POST, self.GET)
        return self._request
    # end def _get_request

    def _get_get(self):
        if self._get is None :
            self._get = http.QueryDict (self.environ.get ("QUERY_STRING", ""))
        return self._get
    # end def _get_get

    def _set_get(self, get) :
        self._get = get
    # end def _set_get

    def _get_post(self):
        if self._post is None:
            self._load_post_and_files ()
        return self._post
    # end def _get_post

    def _set_post(self, post):
        self._post = post
    # end def _set_post

    def _get_cookies(self):
        if self._cookies is None :
            self._cookies = http.parse_cookie \
                (self.environ.get ("HTTP_COOKIE", ""))
        return self._cookies
    # end def _get_cookies

    def _set_cookies(self, cookies):
        self._cookies = cookies
    # end def _set_cookies

    def _get_files(self):
        if self._files is None :
            self._load_post_and_files ()
        return self._files
    # end def _get_files

    def _get_raw_post_data(self):
        try:
            return self._raw_post_data
        except AttributeError:
            self._raw_post_data = sys.stdin.read \
                (int (self.environ ["CONTENT_LENGTH"]))
            return self._raw_post_data
    # end def _get_raw_post_data

    GET           = property (_get_get,     _set_get)
    POST          = property (_get_post,    _set_post)
    COOKIES       = property (_get_cookies, _set_cookies)
    FILES         = property (_get_files)
    REQUEST       = property (_get_request)
    raw_post_data = property (_get_raw_post_data)

# end class CGI_Request

class CGI_Handler (BaseHandler) :
    """The handler for a CGI request."""

    def __call__ (self, environ, start_response) :
        from django.conf import settings

        # Set up middleware if needed. We couldn't do this earlier, because
        # settings weren't available.
        if self._request_middleware is None:
            self.load_middleware ()

        dispatcher.send (signal = signals.request_started)
        try:
            request  = CGI_Request       (environ)
            response = self.get_response (request.path, request)
            # Apply response middleware
            for middleware_method in self._response_middleware:
                response = middleware_method (request, response)
        finally:
            dispatcher.send (signal = signals.request_finished)

        status_text = STATUS_CODE_TEXT.get \
            (response.status_code, "UNKNOWN STATUS CODE")
        status           = '%s %s' % (response.status_code, status_text)
        response_headers = response.headers.items ()
        for c in response.cookies.values ():
            response_headers.append (('Set-Cookie', c.output(header='')))
        start_response (status, response_headers)
        return response.iterator
    # end def __call__

# end class CGI_Handler


### __END__ django.core.handerls.CGI

