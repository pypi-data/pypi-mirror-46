# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import re
from functools import partial

from telethon import events
from telethon.tl.functions.messages import EditMessageRequest
from telethon.extensions.markdown import (
    DEFAULT_URL_RE, _add_surrogate, _del_surrogate
)
from telethon.tl.types import (
    MessageEntityBold, MessageEntityItalic, MessageEntityCode,
    MessageEntityPre, MessageEntityTextUrl
)


def parse_url_match(m):
    entity = MessageEntityTextUrl(
        offset=m.start(),
        length=len(m.group(1)),
        url=_del_surrogate(m.group(2))
    )
    return m.group(1), entity


def get_tag_parser(tag, entity):
    # TODO unescape escaped tags?
    def tag_parser(m):
        return m.group(1), entity(offset=m.start(), length=len(m.group(1)))
    tag = re.escape(tag)
    return re.compile(tag + r'(.+?)' + tag, re.DOTALL), tag_parser


def parse_subreddit(m):
    text = '/' + m.group(3)
    entity = MessageEntityTextUrl(
        offset=m.start(2),
        length=len(text),
        url=f'reddit.com{text}'
    )
    return m.group(1) + text, entity


def parse_snip(m):
    try:
        name = m.group(1)[1:]
        snip = borg._plugins['snip'].storage.snips[name]
        if snip['type'] == borg._plugins['snip'].TYPE_TEXT:
            return snip['text'], None
    except KeyError:
        pass
    return m.group(1), None


PARSED_ENTITIES = (
    MessageEntityBold, MessageEntityItalic, MessageEntityCode,
    MessageEntityPre, MessageEntityTextUrl
)
# a matcher is a tuple of (regex pattern, parse function)
# where the parse function takes the match and returns (text, entity)
MATCHERS = [
    (DEFAULT_URL_RE, parse_url_match),
    (get_tag_parser('**', MessageEntityBold)),
    (get_tag_parser('__', MessageEntityItalic)),
    (get_tag_parser('```', partial(MessageEntityPre, language=''))),
    (get_tag_parser('`', MessageEntityCode)),
    (re.compile(r'([^/\w]|^)(/?(r/\w+))'), parse_subreddit),
    (re.compile(r'(!\w+)'), parse_snip)
]


def parse(message):
    entities = []

    i = 0
    message = _add_surrogate(message)
    while i < len(message):
        # find the first pattern that matches
        for pattern, parser in MATCHERS:
            match = pattern.match(message, pos=i)
            if match:
                break
        else:
            i += 1
            continue

        text, entity = parser(match)
        # replace whole match with text from parser
        message = ''.join((
            message[:match.start()],
            text,
            message[match.end():]
        ))

        # append entity if we got one
        if entity:
            entities.append(entity)

        # skip past the match
        i += len(text)

    return _del_surrogate(message), entities


@borg.on(events.MessageEdited(outgoing=True))
@borg.on(events.NewMessage(outgoing=True))
async def reparse(event):
    message, msg_entities = await borg._parse_message_text(event.text, parse)
    # filter out entities that we don't generate
    old_entities = []
    for entity in event.message.entities or []:
        if isinstance(entity, PARSED_ENTITIES):
            old_entities.append(entity)

    if len(old_entities) == len(msg_entities) and event.raw_text == message:
        return

    await borg(EditMessageRequest(
        peer=await event.input_chat,
        id=event.message.id,
        message=message,
        no_webpage=not bool(event.message.media),
        entities=msg_entities
    ))
    raise events.StopPropagation
