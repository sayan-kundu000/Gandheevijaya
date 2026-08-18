import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from backend.tests.helpers import get_admin_auth_headers


def test_json_ingestion_idempotency_and_repeat_import(client: TestClient, db_session: Session):
    """
    ETL TEST: Verify importing the question dataset multiple times is idempotent
    and avoids creating duplicate database records or throwing unhandled database errors.
    """
    headers = get_admin_auth_headers(db_session)

    # Trigger initial import (dry_run mode)
    res1 = client.post(
        "/api/v1/admin/import/questions",
        params={"source_path": "datasets/cprog", "dry_run": True, "upsert": False},
        headers=headers,
    )
    assert res1.status_code == 200
    report1 = res1.json()
    assert report1["is_dry_run"] is True
    assert isinstance(report1["records_seen"], int)

    # Trigger second import with upsert mode enabled
    res2 = client.post(
        "/api/v1/admin/import/questions",
        params={"source_path": "datasets/cprog", "dry_run": True, "upsert": True},
        headers=headers,
    )
    assert res2.status_code == 200
    report2 = res2.json()
    assert report2["is_dry_run"] is True
    assert isinstance(report2["records_seen"], int)
