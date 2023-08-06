#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 Maxime “pep” Buquet <pep@bouah.net>
#
# Distributed under terms of the zlib license.

"""
Usage
-----

Rot13 encryption plugin.

This plugin also respects security guidelines listed in XEP-0419.

.. glossary::
    /rot13
        **Usage:** ``/rot13``

        This command enables encryption of outgoing messages for the current
        tab.
"""

from typing import Union

import codecs
from slixmpp import InvalidJID, JID, Message

from poezio import tabs
from poezio.plugin import BasePlugin

import logging
log = logging.getLogger(__name__)


ROT13_NS = 'urn:xmpps:rot13:0'

ChatTabs = Union[
    tabs.MucTab,
    tabs.DynamicConversationTab,
    tabs.PrivateTab,
]

class Plugin(BasePlugin):
    def init(self):
        self.api.add_event_handler('muc_msg', self.decode)
        self.api.add_event_handler('muc_say', self.encode)
        self.api.add_event_handler('conversation_msg', self.decode)
        self.api.add_event_handler('conversation_say', self.encode)
        self.api.add_event_handler('private_msg', self.decode)
        self.api.add_event_handler('private_say', self.encode)

        self._enabled_tabs = set()

        for tab_t in (tabs.DynamicConversationTab, tabs.PrivateTab, tabs.MucTab):
            self.api.add_tab_command(
                tab_t,
                'rot13',
                self.toggle,
                usage='',
                short='Toggle rot13 encryption for tab.',
                help='Toggle automatic rot13 encryption for tab.',
            )

        tabs.ConversationTab.add_information_element('rot13', self.display_encryption_status)
        tabs.MucTab.add_information_element('rot13', self.display_encryption_status)
        tabs.PrivateTab.add_information_element('rot13', self.display_encryption_status)

    def cleanup(self):
        tabs.ConversationTab.remove_information_element('rot13')
        tabs.MucTab.remove_information_element('rot13')
        tabs.PrivateTab.remove_information_element('rot13')

    def display_encryption_status(self, jid_s: str) -> str:
        """
            Return information to display in the infobar if ROT13 is enabled
            for the JID.
        """

        try:
            jid = JID(jid_s)
        except InvalidJID:
            return ""

        if jid in self._enabled_tabs:
            return " ROT13"
        return ""

    def toggle(self, _input: str) -> None:
        jid = self.api.current_tab().jid  # type: JID

        if jid in self._enabled_tabs:
            self._enabled_tabs.remove(jid)
            self.api.information('Rot13 encryption disabled for %r' % jid, 'Info')
        else:
            self._enabled_tabs.add(jid)
            self.api.information('Rot13 encryption enabled for %r' % jid, 'Info')

    def encode(self, message: Message, tab: ChatTabs) -> None:
        """
            Encode to rot13
        """
        self.api.information('Sending rot13 message: %r' % message['body'], 'Info')

        jid = tab.jid
        if jid not in self._enabled_tabs:
            return None

        # TODO: Stop using <body/> for this. Put the encoded payload in another element.
        body = message['body']
        message['body'] = codecs.encode(body, "rot13")
        message['eme']['namespace'] = ROT13_NS
        message['eme']['name'] = 'rot13'

    def decode(self, message: Message, _tab: tabs.DynamicConversationTab) -> None:
        """
            Decode rot13
        """
        if message['eme'] is None:
            return None

        if message['eme']['namespace'] != ROT13_NS:
            return None

        self.api.information('Received rot13 message: %r' % message['body'], 'Info')

        body = message['body']
        message['body'] = codecs.decode(body, "rot13")

