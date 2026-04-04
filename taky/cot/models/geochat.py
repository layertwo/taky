import enum
import xml.etree.ElementTree as etree
from dataclasses import dataclass
from datetime import datetime

from dateutil.parser import isoparse

from taky.cot.models.errors import UnmarshalError
from taky.cot.models.teams import Teams

ALL_CHAT_ROOMS = "All Chat Rooms"
GEOCHAT_TAGS = set(["__chat", "remarks", "link"])


class ChatParents(enum.Enum):
    ROOT = "RootContactGroup"
    TEAM = "TeamGroups"


@dataclass(frozen=True, repr=False)
class GeoChat:
    """
    Class representing a GeoChat message

    The GeoChat messages sent from Android are a bit difficult to
    parse. Many fields are redundant, or conflicting in type. This class
    attempts to unify the field names and meanings.
    """

    chatroom: str | None = None
    chat_parent: str | None = None
    group_owner: bool = False
    src_uid: str | None = None
    src_cs: str | None = None
    src_marker: str | None = None
    message: str | None = None
    message_ts: datetime | None = None
    dst_uid: str | None = None
    dst_team: Teams | None = None

    def __repr__(self):
        if self.broadcast:
            return '<GeoChat src="%s", dst="%s", msg="%s">' % (
                self.src_cs,
                ALL_CHAT_ROOMS,
                self.message,
            )

        if self.dst_team:
            return '<GeoChat src="%s", dst="%s", msg="%s">' % (
                self.src_cs,
                self.dst_team,
                self.message,
            )

        return '<GeoChat src="%s", dst_uid="%s", msg="%s">' % (
            self.src_cs,
            self.dst_uid,
            self.message,
        )

    @property
    def broadcast(self):
        """Returns true if message is sent to all chat rooms"""
        return self.chatroom == ALL_CHAT_ROOMS

    @staticmethod
    def is_type(tags):
        return GEOCHAT_TAGS.issubset(tags)

    @classmethod
    def from_elm(cls, elm):
        if elm.tag != "detail":
            raise UnmarshalError("Cannot create GeoChat from %s" % elm.tag)

        chat = elm.find("__chat")
        chatgrp = None
        if chat is not None:
            chatgrp = chat.find("chatgrp")
        remarks = elm.find("remarks")
        link = elm.find("link")

        if None in [chat, chatgrp, remarks, link]:
            raise UnmarshalError("Detail does not contain GeoChat")

        chatroom = chat.get("chatroom")
        chat_parent = chat.get("parent")
        dst_uid = None
        dst_team = None
        if chat_parent == ChatParents.TEAM.value:
            dst_team = Teams(chatroom)
        elif chatroom != ALL_CHAT_ROOMS:
            dst_uid = chat.get("id")

        return cls(
            chatroom=chatroom,
            chat_parent=chat_parent,
            group_owner=chat.get("groupOwner") == "true",
            src_uid=link.get("uid"),
            src_cs=chat.get("senderCallsign"),
            src_marker=link.get("type"),
            message=remarks.text,
            message_ts=isoparse(remarks.get("time")).replace(tzinfo=None),
            dst_uid=dst_uid,
            dst_team=dst_team,
        )

    @property
    def as_element(self):
        if self.broadcast:
            dst_uid = ALL_CHAT_ROOMS
        elif self.dst_team:
            dst_uid = self.dst_team.value
        else:
            dst_uid = self.dst_uid

        detail = etree.Element("detail")
        chat = etree.Element(
            "__chat",
            attrib={
                "parent": self.chat_parent,
                "groupOwner": "true" if self.group_owner else "false",
                "chatroom": self.chatroom,
                "id": dst_uid,
                "senderCallsign": self.src_cs,
            },
        )
        chatgroup = etree.Element(
            "chatgrp", attrib={"uid0": self.src_uid, "uid1": dst_uid, "id": dst_uid}
        )
        chat.append(chatgroup)
        detail.append(chat)

        link = etree.Element(
            "link",
            attrib={"uid": self.src_uid, "type": self.src_marker, "relation": "p-p"},
        )
        detail.append(link)

        rmk_src = f"BAO.F.ATAK.{self.src_uid}"
        remarks = etree.Element(
            "remarks",
            attrib={
                "source": rmk_src,
                "to": dst_uid,
                "time": self.message_ts.isoformat(timespec="milliseconds") + "Z",
            },
        )
        remarks.text = self.message
        detail.append(remarks)

        return detail
