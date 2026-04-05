import datetime

import pytest
import sqlalchemy.exc

from taky.models import CotHistory, IssuedCert, Package, User

STALE_TIME = datetime.datetime(2024, 1, 15, 12, 30, 0, tzinfo=datetime.timezone.utc)
CREATED_AT = datetime.datetime(2024, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)
UPLOAD_TS = datetime.datetime(2024, 6, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)
EXPIRY = datetime.datetime(2025, 1, 15, 12, 0, 0, tzinfo=datetime.timezone.utc)


async def test_cot_history_insert(db_session):
    record = CotHistory(
        uid="ANDROID-deadbeef",
        callsign="ALPHA",
        event_type="a-f-G-U-C",
        lat=38.8977,
        lon=-77.0365,
        stale_time=STALE_TIME,
    )
    db_session.add(record)
    await db_session.commit()

    assert record.id is not None
    assert record.uid == "ANDROID-deadbeef"
    assert record.lat == pytest.approx(38.8977)


async def test_issued_cert_insert(db_session):
    record = IssuedCert(
        subject="CN=alpha.tak.local",
        serial="AABBCCDD",
        expiry=EXPIRY,
        issuer="CN=takCA",
    )
    db_session.add(record)
    await db_session.commit()

    assert record.id is not None
    assert record.serial == "AABBCCDD"


async def test_package_insert(db_session):
    record = Package(
        hash="a" * 64,
        s3_key="packages/aaa.zip",
        uploader_dn="CN=alpha",
        upload_ts=UPLOAD_TS,
        size_bytes=1024,
        name="test.zip",
        keywords="test,demo",
        mime_type="application/zip",
        tool="public",
    )
    db_session.add(record)
    await db_session.commit()

    assert record.id is not None
    assert record.hash == "a" * 64
    assert record.keywords == "test,demo"


async def test_package_hash_unique(db_session):
    p1 = Package(
        hash="b" * 64,
        s3_key="packages/bbb1.zip",
        upload_ts=UPLOAD_TS,
        size_bytes=512,
        name="first.zip",
    )
    p2 = Package(
        hash="b" * 64,
        s3_key="packages/bbb2.zip",
        upload_ts=UPLOAD_TS,
        size_bytes=512,
        name="second.zip",
    )
    db_session.add(p1)
    await db_session.commit()

    db_session.add(p2)
    with pytest.raises(sqlalchemy.exc.IntegrityError):
        await db_session.commit()


async def test_user_insert(db_session):
    record = User(
        uid="test-uid-001",
        callsign="BRAVO",
        created_at=CREATED_AT,
        is_active=True,
        is_admin=False,
        last_seen_at=None,
    )
    db_session.add(record)
    await db_session.commit()

    assert record.id is not None
    assert record.last_seen_at is None
    assert record.is_active is True


async def test_user_uid_unique(db_session):
    u1 = User(
        uid="dup-uid",
        callsign="ALPHA",
        created_at=CREATED_AT,
        is_active=True,
        is_admin=False,
    )
    u2 = User(
        uid="dup-uid",
        callsign="BRAVO",
        created_at=CREATED_AT,
        is_active=True,
        is_admin=False,
    )
    db_session.add(u1)
    await db_session.commit()

    db_session.add(u2)
    with pytest.raises(sqlalchemy.exc.IntegrityError):
        await db_session.commit()


async def test_user_defaults(db_session):
    record = User(
        uid="default-test",
        callsign="CHARLIE",
        created_at=CREATED_AT,
    )
    db_session.add(record)
    await db_session.commit()

    assert record.is_active is True
    assert record.is_admin is False


async def test_session_expire_on_commit_false(db_session):
    record = CotHistory(
        uid="ANDROID-deadbeef",
        callsign="ALPHA",
        event_type="a-f-G-U-C",
        lat=38.8977,
        lon=-77.0365,
        stale_time=STALE_TIME,
    )
    db_session.add(record)
    await db_session.commit()

    # Accessing uid after commit should NOT raise DetachedInstanceError
    # because expire_on_commit=False is set in the fixture
    uid = record.uid
    assert uid == "ANDROID-deadbeef"
