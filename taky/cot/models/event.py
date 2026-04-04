import xml.etree.ElementTree as etree
from dataclasses import dataclass, field
from datetime import datetime as dt

from dateutil.parser import isoparse

from taky.cot.models.detail import Detail
from taky.cot.models.errors import UnmarshalError
from taky.cot.models.geochat import GeoChat
from taky.cot.models.point import Point
from taky.cot.models.takuser import TAKUser


@dataclass(frozen=True, repr=False)
class Event:
    uid: str | None = None
    etype: str | None = None
    how: str | None = None
    time: dt | None = None
    start: dt | None = None
    stale: dt | None = None
    version: str = "2.0"
    point: Point = field(default_factory=Point)
    detail: Detail | GeoChat | TAKUser | None = None

    def __repr__(self):
        return '<Event uid="%s" etype="%s" time="%s">' % (
            self.uid,
            self.etype,
            self.time,
        )

    @property
    def persist_ttl(self):
        return round((self.stale - dt.utcnow()).total_seconds())

    @classmethod
    def from_elm(cls, elm):
        if elm.tag != "event":
            raise UnmarshalError("Cannot create Event from %s" % elm.tag)

        try:
            time = isoparse(elm.get("time")).replace(tzinfo=None)
            start = isoparse(elm.get("start")).replace(tzinfo=None)
            stale = isoparse(elm.get("stale")).replace(tzinfo=None)
        except (TypeError, ValueError) as exc:
            raise UnmarshalError("Date parsing error") from exc

        uid = elm.get("uid")
        etype = elm.get("type")

        if uid is None:
            raise UnmarshalError("Event must have 'uid' attribute")
        if etype is None:
            raise UnmarshalError("Event must have 'type' attribute")

        point = Point()
        detail = None
        child = None
        try:
            for child in list(elm):
                if child.tag == "point":
                    point = Point.from_elm(child)
                elif child.tag == "detail":
                    d_tags = set([d_elm.tag for d_elm in list(child)])
                    if TAKUser.is_type(d_tags):
                        detail = TAKUser.from_elm(child, uid=uid)
                    elif GeoChat.is_type(d_tags):
                        detail = GeoChat.from_elm(child)
                    else:
                        detail = Detail.from_elm(child)
        except (TypeError, ValueError, AttributeError) as exc:
            if child is not None:
                raise UnmarshalError(f"Issue parsing {child.tag}") from exc
            else:
                raise UnmarshalError("Issue parsing children") from exc

        return cls(
            version=elm.get("version"),
            uid=uid,
            etype=etype,
            how=elm.get("how"),
            time=time,
            start=start,
            stale=stale,
            point=point,
            detail=detail,
        )

    @property
    def as_element(self):
        ret = etree.Element("event")
        ret.set("version", self.version)
        ret.set("uid", self.uid)
        ret.set("type", self.etype)
        ret.set("how", self.how)
        ret.set("time", self.time.isoformat(timespec="milliseconds") + "Z")
        ret.set("start", self.start.isoformat(timespec="milliseconds") + "Z")
        ret.set("stale", self.stale.isoformat(timespec="milliseconds") + "Z")
        ret.append(self.point.as_element)
        if self.detail is not None:
            ret.append(self.detail.as_element)

        return ret
