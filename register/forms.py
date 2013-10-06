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

from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

_fieldattrs = {'class': 'form-control', 'maxlength': 30, }
_emailattrs = _fieldattrs.copy()
_emailattrs['type'] = 'email'
_textwidget = forms.TextInput(attrs=_fieldattrs)
_passwidget = forms.PasswordInput(attrs=_fieldattrs)
_mailwidget = forms.TextInput(attrs=_emailattrs)

class RegistrationForm(forms.Form):
    username = forms.CharField(
        label=_("Username"), max_length=30, widget=_textwidget,
        error_messages={
            'invalid': _("This value may contain only letters, numbers and "
                         "@/./+/-/_ characters.")}
    )
    email = forms.EmailField(
        max_length=30, widget=_mailwidget,
        help_text=_(
            'Required, a confirmation email will be sent to this address.')
    )

    password1 = forms.CharField(label=_("Password"),
                                widget=_passwidget)
    password2 = forms.CharField(label=_("Confirm"),
        widget=_passwidget,
        help_text=_("Enter the same password as above, for verification."))

    # server field is only present if configured for multiple hosts
    server = forms.ChoiceField(
        choices=tuple([(host, host) for host in settings.XMPP_HOSTS]),
    )