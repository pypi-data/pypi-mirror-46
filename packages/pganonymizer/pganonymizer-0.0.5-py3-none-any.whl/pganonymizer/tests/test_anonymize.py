from pganonymizer.anonymize import loadcsj, hashRecord, run_anonymizer
from pganonymizer.helper import TypeMismatchedException
import pytest
import asyncio
import asyncpg

pytestmark = pytest.mark.asyncio

async def test_load_config(event_loop):
    config = await loadcsj("schema.csj")
    assert config != None

async def test_anonymize_data(event_loop):
    data = "RANDOM"
    anonymized_data = await hashRecord(data, "hash")
    assert data != anonymized_data and len(anonymized_data) == 16

async def test_anonymize_date(event_loop):
    date = "1995-05-12"
    anonymized_date = await hashRecord(date, "date")
    assert anonymized_date != date and anonymized_date[:4] == date[:4]

async def test_anonymize_phoneno(event_loop):
    phoneno = "+669587413"
    anonymized_phoneno = await hashRecord(phoneno, "phone")
    assert anonymized_phoneno != phoneno and len(anonymized_phoneno) == len(phoneno)

async def test_invalid_date_anonymizer(event_loop):
    dsn = "postgresql://"
    with pytest.raises(TypeMismatchedException):
        error = await run_anonymizer(dsn, "invalid_date_schema.csj")

async def test_invalid_phone_anonymizer(event_loop):
    dsn = "postgresql://"
    with pytest.raises(TypeMismatchedException):
        error = await run_anonymizer(dsn, "invalid_phone_schema.csj")

async def test_anonymizer(event_loop):
    dsn = "postgresql://"
    await run_anonymizer(dsn, "schema.csj")
    conn = await asyncpg.connect(dsn)
    records = await conn.fetch("SELECT * FROM customer")
    for each_record in records:
        assert len(each_record.get('name')) == 16


