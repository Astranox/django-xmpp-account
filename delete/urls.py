# -*- coding: utf-8 -*-
#
# This file is part of xmppregister (https://account.jabber.at/doc).
#
# xmppregister is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# xmppregister is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with xmppregister.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

from django.conf.urls import patterns
from django.conf.urls import url

from delete.views import DeleteView
from delete.views import DeleteThanksView
from delete.views import DeleteConfirmationView
from delete.views import DeleteConfirmationThanksView


urlpatterns = patterns('',
    url(r'^$', DeleteView.as_view(), name='Delete'),
    url(r'^thanks/$', DeleteThanksView.as_view(),
        name='DeleteThanks'),
    url(r'^confirm/(?P<key>\w+)/$', DeleteConfirmationView.as_view(),
        name='DeleteConfirmation'),
    url(r'^confirm-thanks/$', DeleteConfirmationThanksView.as_view(),
        name='DeleteConfirmationThanks'),
)
