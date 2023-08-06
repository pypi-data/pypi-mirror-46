#!/usr/bin/python
# -*- coding: utf-8 -*-
# rdiffweb, A web interface to rdiff-backup repositories
# Copyright (C) 2018 rdiffweb contributors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import
from __future__ import unicode_literals

from builtins import bytes
import cherrypy
import logging

from rdiffweb import page_main
from rdiffweb.dispatch import poppath


# Define the logger
_logger = logging.getLogger(__name__)


@poppath()
class SettingsPage(page_main.MainPage):

    @cherrypy.expose
    def index(self, path=b""):
        self.assertIsInstance(path, bytes)

        _logger.debug("repo settings [%r]", path)

        # Check user permissions
        repo_obj = self.validate_user_path(path)[0]

        # Get page data.
        params = {
            'repo_name': repo_obj.display_name,
            'repo_path': repo_obj.path,
            'templates_content': [],
        }

        # Generate page.
        return self._compile_template("settings.html", **params)
