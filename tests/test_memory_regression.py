import tracemalloc
import unittest as ut

import defusedxml.ElementTree as defused_et

from taky.cot import models
from tests import XML_S


class TestMemoryRegression(ut.TestCase):
    def test_parser_no_memory_leak(self):
        """XML-05: Parse 10,000+ COT messages with stable memory footprint.

        Uses tracemalloc (stdlib) per D-02. Asserts total growth < 1 MB.
        This guards against the lxml C-heap leak regression and any future
        memory issues in the stdlib ET parse path.
        """
        tracemalloc.start()
        snapshot_before = tracemalloc.take_snapshot()

        for _ in range(10_000):
            elm = defused_et.fromstring(XML_S)
            models.Event.from_elm(elm)

        snapshot_after = tracemalloc.take_snapshot()
        total_growth = sum(
            stat.size_diff
            for stat in snapshot_after.compare_to(snapshot_before, "lineno")
        )
        tracemalloc.stop()

        self.assertLess(
            total_growth,
            1_000_000,
            f"Memory grew {total_growth} bytes over 10,000 parse cycles -- "
            "expected < 1 MB (possible leak regression)",
        )
