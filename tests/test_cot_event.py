import unittest as ut

import defusedxml.ElementTree as etree

from taky.cot import models

from . import XML_S, elements_equal


class COTTestcase(ut.TestCase):
    def setUp(self):
        self.elm = etree.fromstring(XML_S)

    def test_unmarshall(self):
        event = models.Event.from_elm(self.elm)

        # Event
        self.assertEqual(event.version, "2.0")
        self.assertEqual(event.uid, "ANDROID-deadbeef")
        self.assertEqual(event.etype, "a-f-G-U-C")
        self.assertEqual(event.how, "m-g")
        self.assertEqual(event.time, event.start)

        # Point
        self.assertAlmostEqual(event.point.lat, 1.234567, places=6)
        self.assertAlmostEqual(event.point.lon, -3.141592, places=6)
        self.assertAlmostEqual(event.point.hae, -25.7, places=1)
        self.assertAlmostEqual(event.point.ce, 9.9, places=1)
        self.assertAlmostEqual(event.point.le, 9999999.0, places=1)

        self.assertIsInstance(event.detail, models.TAKUser)
        self.assertFalse(isinstance(event.detail, models.Detail))

    def test_marshall(self):
        event = models.Event.from_elm(self.elm)

        # TAKUser.as_element produces a canonical detail; unknown sub-elements
        # (precisionlocation), unknown contact attributes (xmppUsername), and
        # full-precision track values are not preserved on round-trip.
        canonical_xml = (
            b'<event version="2.0" uid="ANDROID-deadbeef" type="a-f-G-U-C" how="m-g"'
            b' time="2021-02-27T20:32:24.771Z" start="2021-02-27T20:32:24.771Z"'
            b' stale="2021-02-27T20:38:39.771Z">'
            b'<point lat="1.234567" lon="-3.141592" hae="-25.7" ce="9.9" le="9999999.0"/>'
            b"<detail>"
            b'<takv os="29" version="4.0.0.0 (deadbeef).1234567890-CIV"'
            b' device="Some Android Device" platform="ATAK-CIV"/>'
            b'<status battery="78"/>'
            b'<uid Droid="JENNY"/>'
            b'<contact callsign="JENNY" endpoint="*:-1:stcp"/>'
            b'<__group role="Team Member" name="Cyan"/>'
            b'<track course="80.2" speed="0.0"/>'
            b"</detail>"
            b"</event>"
        )
        self.assertTrue(
            elements_equal(etree.fromstring(canonical_xml), event.as_element)
        )

    def test_marshall_err_tagname(self):
        self.elm.tag = "xxx"
        self.assertRaises(models.UnmarshalError, models.Event.from_elm, self.elm)

    def test_marshall_err_ts_failure(self):
        self.elm.set("start", "xxx")
        self.assertRaises(models.UnmarshalError, models.Event.from_elm, self.elm)

    def test_marshall_err_invalid_point(self):
        self.elm[0].set("lat", "xxx")
        self.assertRaises(models.UnmarshalError, models.Event.from_elm, self.elm)

    def test_marshall_err_no_uid(self):
        self.elm.attrib.pop("uid")
        self.assertRaises(models.UnmarshalError, models.Event.from_elm, self.elm)

    def test_marshall_err_no_type(self):
        # An element with no type
        self.elm.attrib.pop("type")
        self.assertRaises(models.UnmarshalError, models.Event.from_elm, self.elm)

    def test_marti_exceptions(self):
        # An element with no detail/marti
        del self.elm[1]
        evt = models.Event.from_elm(self.elm)
        self.assertTrue(evt.detail is None)
