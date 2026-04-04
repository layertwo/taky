import logging
import re

MAX_FRAME_BYTES = 64 * 1024  # 64 KB per STRM-04

# Strip <?xml ...?> processing instructions from completed frames (STRM-03).
_XML_DECL_RE = re.compile(rb"<\?xml[^?]*\?>", re.IGNORECASE)


class StreamFramer:
    """
    Byte-level stream framer for COT XML messages.

    Accumulates TCP stream bytes and yields complete <event>...</event> frames
    using depth-tracking (not </event> string matching). Strips <?xml ...?>
    declarations from yielded frames. Resets buffer with a warning on frames
    exceeding MAX_FRAME_BYTES.

    Attributes:
        lgr: Logger instance named after the class.
    """

    def __init__(self):
        self.lgr = logging.getLogger(self.__class__.__name__)
        self._buf = bytearray()
        self._depth = 0
        # Quote-aware tag scanning state
        self._in_tag = False  # inside <...> (between < and >)
        self._in_double_quote = False  # inside "..." within a tag
        self._in_single_quote = False  # inside '...' within a tag
        self._tag_is_close = False  # current tag started with </
        self._tag_is_pi = False  # current tag is <?...?>
        self._saw_slash = False  # saw / just before > (self-closing)
        self._tag_byte_idx = 0  # byte index within current tag (0=the '<' itself)

    def _reset_tag_state(self):
        """Reset per-tag scanning flags after a '>' is processed."""
        self._in_tag = False
        self._in_double_quote = False
        self._in_single_quote = False
        self._tag_is_close = False
        self._tag_is_pi = False
        self._saw_slash = False
        self._tag_byte_idx = 0

    def _reset_frame_state(self):
        """Reset full framer state (used after buffer overflow or frame completion)."""
        self._buf = bytearray()
        self._depth = 0
        self._reset_tag_state()

    def feed(self, data: bytes) -> list:
        """
        Feed a chunk of raw TCP bytes into the framer.

        Returns a list of complete raw XML frame byte strings.  Each returned
        frame has its leading <?xml ...?> declaration stripped and is a valid
        standalone XML document fragment starting with <event>.

        Args:
            data: Raw bytes received from the TCP stream.

        Returns:
            A list of bytes objects, one per complete frame detected.
        """
        frames = []

        for byte in data:
            ch = chr(byte)

            # ------------------------------------------------------------------
            # OVERFLOW GUARD — check before every byte append (STRM-04)
            # ------------------------------------------------------------------
            if len(self._buf) >= MAX_FRAME_BYTES:
                self.lgr.warning(
                    "Frame exceeded %d byte buffer limit -- resetting", MAX_FRAME_BYTES
                )
                self._reset_frame_state()
                # Fall through: process the current byte in the fresh state.

            # ------------------------------------------------------------------
            # OUTSIDE any element (depth == 0, not in a tag)
            # ------------------------------------------------------------------
            if self._depth == 0 and not self._in_tag:
                if ch == "<":
                    self._buf.append(byte)
                    self._in_tag = True
                    self._tag_byte_idx = 0  # '<' is index 0
                # Bytes outside any element at depth 0 are discarded (whitespace/junk)
                continue

            # ------------------------------------------------------------------
            # INSIDE a tag (<...>): quote-aware scanning
            # ------------------------------------------------------------------
            if self._in_tag:
                # Always accumulate bytes while inside a tag
                self._buf.append(byte)
                self._tag_byte_idx += 1  # 1 = first byte after '<'

                if self._in_double_quote:
                    if ch == '"':
                        self._in_double_quote = False
                    continue

                if self._in_single_quote:
                    if ch == "'":
                        self._in_single_quote = False
                    continue

                # Not in quotes — inspect the character
                if ch == '"':
                    self._in_double_quote = True
                    self._saw_slash = False
                elif ch == "'":
                    self._in_single_quote = True
                    self._saw_slash = False
                elif ch == "?" and self._tag_byte_idx == 1:
                    # First byte after '<' is '?' — this is a processing instruction
                    self._tag_is_pi = True
                    self._saw_slash = False
                elif ch == "/" and self._tag_byte_idx == 1:
                    # First byte after '<' is '/' — this is a closing tag </tag>
                    self._tag_is_close = True
                    self._saw_slash = False
                elif ch == "/":
                    # '/' mid-tag (not first byte) means potential self-close />
                    self._saw_slash = True
                elif ch == ">":
                    # Tag closes here
                    if self._tag_is_pi:
                        # Processing instruction (<?xml ...?>) — ignore for depth
                        pass
                    elif self._tag_is_close:
                        # Closing tag </tag> — only decrement if already inside
                        if self._depth > 0:
                            self._depth -= 1
                        else:
                            # Closing tag at depth 0 is malformed — discard and reset
                            self.lgr.debug(
                                "Unexpected closing tag at depth 0 -- discarding"
                            )
                            self._reset_frame_state()
                            continue
                    elif self._saw_slash:
                        # Self-closing tag <tag ... />
                        if self._depth == 0:
                            # Root self-closing: open to 1, close back to 0 → yields frame
                            self._depth += 1
                            self._depth -= 1
                        # else: child self-closing — no net depth change (already inside)
                    else:
                        # Opening tag
                        self._depth += 1

                    self._reset_tag_state()

                    # ----------------------------------------------------------
                    # Frame complete: depth returned to 0
                    # ----------------------------------------------------------
                    if self._depth == 0 and len(self._buf) > 0:
                        raw = bytes(self._buf)
                        self._buf = bytearray()
                        # Strip XML declarations (STRM-03)
                        frame = _XML_DECL_RE.sub(b"", raw, count=1).lstrip()
                        if frame:
                            frames.append(frame)
                else:
                    # Any other character resets the saw_slash flag
                    self._saw_slash = False

                continue

            # ------------------------------------------------------------------
            # INSIDE element content (depth > 0, not in a tag)
            # ------------------------------------------------------------------
            self._buf.append(byte)
            if ch == "<":
                self._in_tag = True
                self._tag_byte_idx = 0  # '<' itself counts as index 0
                # Note: the next byte appended will set tag_byte_idx to 1

        return frames
