#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 Maxime “pep” Buquet <pep@bouah.net>
#
# Distributed under terms of the zlib license. See the COPYING file.

"""
    Display MUC Config diffs when changed.
"""

from poezio.plugin import BasePlugin
from poezio.fixes import get_room_form
from poezio.tabs.muctab import NS_MUC_USER


class Plugin(BasePlugin):
    def init(self):
        self.mucs = {}

        self.api.add_event_handler('muc_join', self.on_join)
        self.api.add_event_handler('muc_part', self.on_part)
        self.api.add_event_handler(
            'groupchat_config_status',
            self.on_config_change,
        )

    def diff_config_fields(self, jid, old_fields, new_fields):
        if old_fields == new_fields:
            return

        self.api.information('MUC Config for %s updated.' % jid, 'info')

        for field in new_fields:
            if field in old_fields and new_fields[field] != old_fields[field]:
                self.api.information(
                    '%s: %s -> %s' %
                    (field, old_fields[field], new_fields[field]),
                    'info',
                )
            elif field not in old_fields:
                self.api.information(
                    '%s: %s' % (field, new_fields[field]),
                    'info',
                )

    def fetch_room_config(self, jid):
        def inner(form):
            fields = {}
            if form is not None:
                fields = {
                    field['var']: field['value']
                    for field in form['fields']
                    if field['var'] and field['var'].startswith('muc#')
                }
            if jid in self.mucs:
                self.diff_config_fields(jid, self.mucs[jid], fields)
            self.mucs[jid] = fields
        return inner

    def on_join(self, presence, _tab):
        jid = presence['from'].bare
        if jid in self.mucs:
            return
        get_room_form(self.core.xmpp, jid, self.fetch_room_config(jid))

    def on_part(self, presence, _tab):
        jid = presence['from'].bare
        if jid in self.mucs:
            del self.mucs[jid]

    def on_config_change(self, message):
        jid = message['from'].bare

        config_codes = {102, 103, 104, 170, 171, 172, 173, 174}
        status_codes = {
            int(s.attrib['code'])
            for s in message.xml.findall('{%s}x/{%s}status' % (
                NS_MUC_USER, NS_MUC_USER,
            ))
        }

        if status_codes and not (status_codes - config_codes):
            get_room_form(self.core.xmpp, jid, self.fetch_room_config(jid))
