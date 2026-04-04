import pytest
import xml.etree.ElementTree as ET

from taky.util.stream_framer import StreamFramer

# ---------------------------------------------------------------------------
# Ported from tests/test_xmldeclstrip.py (D-07)
# ---------------------------------------------------------------------------


def test_single_message_with_decl():
    """Port of test_valid_xml: single <?xml?> + <event/> yields 1 frame."""
    framer = StreamFramer()
    frames = framer.feed(b"<?xml version='1.0' encoding='utf-8'?>")
    frames += framer.feed(b'<event data="stuff here" />')

    assert len(frames) == 1
    elm = ET.fromstring(frames[0])
    assert elm.tag == "event"
    assert elm.get("data") == "stuff here"
    assert not frames[0].startswith(b"<?xml")


def test_split_decl_mid_tag():
    """Port of test_split_decl: declaration split mid-<?xml across two feeds."""
    framer = StreamFramer()
    frames = framer.feed(b"<?xm")
    frames += framer.feed(b"l version='1.0' encoding='utf-8'?>")
    frames += framer.feed(b'<event data="stuff here" />')

    assert len(frames) == 1
    elm = ET.fromstring(frames[0])
    assert elm.tag == "event"


def test_split_decl_before_close():
    """Port of test_split_decl2: declaration split just before ?> close."""
    framer = StreamFramer()
    frames = framer.feed(b"<?xml version='1.0' encoding='utf-8'?")
    frames += framer.feed(b">")
    frames += framer.feed(b'<event data="stuff here" />')

    assert len(frames) == 1
    elm = ET.fromstring(frames[0])
    assert elm.tag == "event"


def test_two_messages_batched():
    """Port of test_split_decl3: two messages with declarations in batched feeds yield 2 frames."""
    framer = StreamFramer()
    frames = framer.feed(b"<?xml version='1.0' encoding='utf-8'?>")
    frames += framer.feed(b'<event data="stuff here" /><')
    frames += framer.feed(b"?xml version='1.0' encoding='utf-8'?>")
    frames += framer.feed(b'<event data="stuff here" />')

    assert len(frames) == 2
    for frame in frames:
        elm = ET.fromstring(frame)
        assert elm.tag == "event"


def test_split_message_body():
    """Port of test_split_data: message body split across two feeds yields 1 frame."""
    framer = StreamFramer()
    frames = framer.feed(b"<?xml version='1.0' encoding='utf-8'?>")
    frames += framer.feed(b'<event data="stuff')
    frames += framer.feed(b' here" />')

    assert len(frames) == 1
    elm = ET.fromstring(frames[0])
    assert elm.tag == "event"
    assert elm.get("data") == "stuff here"


# ---------------------------------------------------------------------------
# New STRM-02 through STRM-05 scenarios
# ---------------------------------------------------------------------------


def test_well_formed_single():
    """STRM-05: a well-formed single <event>...</event> yields exactly 1 frame."""
    framer = StreamFramer()
    data = (
        b'<event uid="ANDROID-abc" type="a-f-G">'
        b'<point lat="0" lon="0" hae="0" ce="0" le="0"/>'
        b"</event>"
    )
    frames = framer.feed(data)

    assert len(frames) == 1
    elm = ET.fromstring(frames[0])
    assert elm.tag == "event"
    assert elm.get("uid") == "ANDROID-abc"


def test_multi_message_batch():
    """STRM-05: two concatenated events in one feed call yield 2 frames."""
    framer = StreamFramer()
    msg = b'<event uid="ANDROID-1" type="a-f-G"><point/></event>'
    frames = framer.feed(msg + msg)

    assert len(frames) == 2
    for frame in frames:
        elm = ET.fromstring(frame)
        assert elm.tag == "event"


def test_truncated_recovery():
    """STRM-05: first half of event, then second half + complete second event yields 2 frames."""
    framer = StreamFramer()
    msg1 = b'<event uid="ANDROID-1" type="a-f-G"><point/></event>'
    msg2 = b'<event uid="ANDROID-2" type="a-f-G"><point/></event>'

    half = len(msg1) // 2
    frames = framer.feed(msg1[:half])
    assert len(frames) == 0  # incomplete frame — not yet yielded

    frames += framer.feed(msg1[half:] + msg2)
    assert len(frames) == 2

    elm0 = ET.fromstring(frames[0])
    elm1 = ET.fromstring(frames[1])
    assert elm0.get("uid") == "ANDROID-1"
    assert elm1.get("uid") == "ANDROID-2"


def test_attribute_value_false_boundary():
    """STRM-02: </event> inside an attribute value must not trigger a false frame split.

    Note: The payload uses a literal '<' inside an attribute value which is not
    well-formed XML (requires &lt; encoding). The framer must not split on the
    '</event>' substring inside the quoted value — it must wait for the real
    closing tag at depth 0. We verify framing correctness only (no XML parse).
    """
    framer = StreamFramer()
    # The </event> embedded in the uid attribute (between double quotes) must
    # NOT cause a frame boundary — the framer must suppress < and > inside quotes.
    data = b'<event uid="</event>"><point/></event>'
    frames = framer.feed(data)

    assert len(frames) == 1, f"Expected 1 frame, got {len(frames)}"
    # Verify the full raw bytes are in the one frame (not truncated)
    assert b"</event>" in frames[0]
    assert frames[0].endswith(b"</event>")


def test_oversized_frame_guard():
    """STRM-04/STRM-05: buffer exceeding 64 KB without a frame boundary is reset with a warning."""
    framer = StreamFramer()
    # Build a payload that starts an element but never closes it, exceeding 64 KB
    oversized = b'<event uid="x">' + b"A" * 65536
    frames = framer.feed(oversized)

    # No frame should be yielded — buffer is reset
    assert len(frames) == 0

    # After reset, a well-formed message should be framed correctly
    frames = framer.feed(b'<event uid="ok"/>')
    assert len(frames) == 1
    elm = ET.fromstring(frames[0])
    assert elm.get("uid") == "ok"


def test_self_closing_event():
    """A self-closing <event .../> root element yields exactly 1 frame."""
    framer = StreamFramer()
    frames = framer.feed(b'<event uid="takPing" type="t-x-c-t" />')

    assert len(frames) == 1
    elm = ET.fromstring(frames[0])
    assert elm.tag == "event"
    assert elm.get("uid") == "takPing"


def test_xml_decl_stripped():
    """STRM-03: yielded frames must NOT start with <?xml."""
    framer = StreamFramer()
    frames = framer.feed(b"<?xml version='1.0' encoding='UTF-8'?><event uid='x'/>")

    assert len(frames) == 1
    assert (
        not frames[0].strip().startswith(b"<?xml")
    ), "XML declaration must be stripped"
    # Frame must still be parseable
    elm = ET.fromstring(frames[0])
    assert elm.tag == "event"


def test_whitespace_between_events():
    """Whitespace between events is discarded; both events are yielded as separate frames."""
    framer = StreamFramer()
    frames = framer.feed(b"<event/>\n  \t\n<event/>")

    assert len(frames) == 2
    for frame in frames:
        elm = ET.fromstring(frame)
        assert elm.tag == "event"


def test_multiple_sequential_feeds_accumulate():
    """State persists correctly across multiple feed() calls on the same framer instance."""
    framer = StreamFramer()
    # Split a multi-child event across 5 separate feeds
    frames = framer.feed(b"<event")
    frames += framer.feed(b' uid="multi"')
    frames += framer.feed(b">")
    frames += framer.feed(b"<detail/>")
    frames += framer.feed(b"</event>")

    assert len(frames) == 1
    elm = ET.fromstring(frames[0])
    assert elm.get("uid") == "multi"
