import json
from datetime import datetime, timedelta

import reminder
import server


def test_save_and_list_application(data_dir):
    msg = server.save_application("Acme", "Junior Engineer", "https://acme.example/jobs/1")
    assert "#1" in msg

    listing = server.list_applications()
    assert "Junior Engineer at Acme" in listing
    assert "researching" in listing


def test_ids_increment(data_dir):
    server.save_application("A", "Role A", "https://a.example")
    msg = server.save_application("B", "Role B", "https://b.example")
    assert "#2" in msg


def test_list_filters_by_status(data_dir):
    server.save_application("A", "Role A", "https://a.example", status="applied")
    server.save_application("B", "Role B", "https://b.example", status="rejected")

    applied = server.list_applications("applied")
    assert "Role A" in applied
    assert "Role B" not in applied


def test_list_when_empty(data_dir):
    assert server.list_applications() == "No applications tracked yet."


def test_stale_applications(data_dir):
    old = (datetime.now() - timedelta(days=10)).isoformat()
    new = datetime.now().isoformat()
    apps = [
        {"id": 1, "company": "Old", "role": "R", "status": "applied", "created_at": old},
        {"id": 2, "company": "New", "role": "R", "status": "applied", "created_at": new},
        {"id": 3, "company": "Done", "role": "R", "status": "rejected", "created_at": old},
    ]
    (data_dir / "applications.json").write_text(json.dumps(apps))

    stale = reminder.get_stale_applications()
    assert [a["company"] for a in stale] == ["Old"]


def test_update_application_status(data_dir):
    server.save_application("Acme", "Engineer", "https://acme.example", status="applied")
    reminder.update_application(1, "interviewing")

    apps = json.loads((data_dir / "applications.json").read_text())
    assert apps[0]["status"] == "interviewing"
