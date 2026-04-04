import unittest as ut

import defusedxml.ElementTree as etree

from taky.cot import models

from . import elements_equal

XML_S = b'<event version="2.0" uid="TEST-deadbeef" type="a" how="m-g" time="2021-03-11T15:49:07.138Z" start="2021-03-11T15:49:07.138Z" stale="2021-03-12T15:49:07.138Z"><point lat="0.000000" lon="0.000000" hae="0.0" ce="9999999.0" le="9999999.0"/><detail><takv os="Android" version="10" device="Some Device" platform="python unittest"/><status battery="83"/><uid Droid="JENNY"/><contact callsign="JENNY" endpoint="*:-1:stcp" phone="800-867-5309"/><__group role="Team Member" name="Cyan"/><track course="90.1" speed="10.3"/></detail></event>'


class TAKUserTestcase(ut.TestCase):
    def setUp(self):
        elm = etree.fromstring(XML_S)
        self.answer = elm.find("detail")

    def test_as_element(self):
        tak_u = models.TAKUser(
            callsign="JENNY",
            marker="a",
            group=models.Teams.CYAN,
            role="Team Member",
            phone="800-867-5309",
            endpoint="*:-1:stcp",
            course=90.1,
            speed=10.3,
            battery="83",
            device=models.TAKDevice(
                os="Android", version="10", device="Some Device", platform="python unittest"
            ),
        )

        self.assertTrue(elements_equal(self.answer, tak_u.as_element))
