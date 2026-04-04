import xml.etree.ElementTree as etree
from dataclasses import dataclass

from .detail import Detail
from .errors import UnmarshalError
from .teams import Teams

TAKUSER_TAGS = set(["takv", "contact", "__group"])


@dataclass(frozen=True, repr=False)
class TAKDevice:
    os: str | None = None  # pylint: disable=invalid-name
    version: str | None = None
    device: str | None = None
    platform: str | None = None

    def __repr__(self):
        return "<TAKDevice %s (%s) on %s>" % (self.platform, self.version, self.device)

    @classmethod
    def from_elm(cls, elm):
        if elm.tag != "takv":
            raise UnmarshalError("Unable to load TAKDevice from %s" % elm.tag)

        return cls(
            os=elm.get("os"),
            device=elm.get("device"),
            version=elm.get("version"),
            platform=elm.get("platform"),
        )

    @property
    def as_element(self):
        ret = etree.Element("takv")
        ret.set("os", self.os or "")
        ret.set("device", self.device or "")
        ret.set("version", self.version or "")
        ret.set("platform", self.platform or "")
        return ret


class TAKUser(Detail):
    def __init__(self, elm):
        super().__init__(elm)

        self.uid = None
        self.callsign = None
        self.marker = None
        self.group = None
        self.role = None

        self.phone = None
        self.xmpp = None
        self.endpoint = None

        self.course = None
        self.speed = None

        self.battery = None
        self.device = TAKDevice()

    def __repr__(self):
        return f"<TAKUser callsign={self.callsign}, group={self.group}>"

    @staticmethod
    def is_type(tags):
        return TAKUSER_TAGS.issubset(tags)

    @staticmethod
    def from_elm(elm, uid):
        ret = TAKUser(elm)
        ret.uid = uid

        for d_elm in list(elm):
            if d_elm.tag == "takv":
                ret.device = TAKDevice.from_elm(d_elm)
            elif d_elm.tag == "contact":
                ret.callsign = d_elm.get("callsign")
                ret.phone = d_elm.get("phone")
                ret.endpoint = d_elm.get("endpoint")
            elif d_elm.tag == "__group":
                try:
                    ret.group = Teams(d_elm.get("name"))
                except ValueError:
                    ret.group = Teams.UNKNOWN
                ret.role = d_elm.get("role")
            elif d_elm.tag == "status":
                ret.battery = d_elm.get("battery")
            elif d_elm.tag == "track":
                ret.course = float(d_elm.get("course"))
                ret.speed = float(d_elm.get("speed"))

        return ret

    @property
    def as_element(self):
        if self.elm is not None:
            return self.elm

        if None in [self.device, self.callsign, self.group, self.role, self.endpoint]:
            raise ValueError("Missing fields, unable to convert to XML element")

        detail = etree.Element("detail")
        takv = self.device.as_element
        detail.append(takv)

        if self.battery:
            status = etree.Element(
                "status",
                attrib={
                    "battery": self.battery,
                },
            )
            detail.append(status)

        uid = etree.Element("uid", attrib={"Droid": self.callsign})
        detail.append(uid)

        contact = etree.Element(
            "contact",
            attrib={
                "callsign": self.callsign,
                "endpoint": self.endpoint,
            },
        )

        # TODO: What does empty phone look like?
        if self.phone:
            contact.set("phone", self.phone)
        if self.xmpp:
            contact.set("xmppUsername", self.xmpp)

        detail.append(contact)

        group = etree.Element(
            "__group",
            attrib={
                "role": self.role,
                "name": self.group.value,
            },
        )
        detail.append(group)

        if self.course and self.speed:
            track = etree.Element(
                "track",
                attrib={
                    "course": "%.1f" % self.course,
                    "speed": "%.1f" % self.speed,
                },
            )
            detail.append(track)

        return detail
