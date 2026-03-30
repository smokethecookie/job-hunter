import json
import subprocess
from pathlib import Path
from datetime import datetime, timedelta

DATA_DIR = Path(__file__).parent.parent / "data"
APPLICATIONS_FILE = DATA_DIR / "applications.json"
DAYS_THRESHOLD = 7


def get_stale_applications():
    """Find applications that need follow-up."""
    if not APPLICATIONS_FILE.exists():
        return []
    
    applications = json.loads(APPLICATIONS_FILE.read_text())
    stale = []
    
    now = datetime.now()
    for app in applications:
        if app["status"] != "applied":
            continue
        
        applied_date = datetime.fromisoformat(app["created_at"])
        days_since = (now - applied_date).days
        
        if days_since >= DAYS_THRESHOLD:
            app["days_since"] = days_since
            stale.append(app)
    
    return stale


def send_notification(title: str, message: str, actions: list[str] = None) -> str:
    """Send macOS notification and get response."""
    
    script = f'''
    set theActions to {{{", ".join(f'"{a}"' for a in actions)}}}
    
    display dialog "{message}" with title "{title}" buttons theActions default button 3
    set theResponse to button returned of result
    return theResponse
    '''
    
    result = subprocess.run(
        ["osascript", "-e", script],
        capture_output=True,
        text=True
    )
    
    return result.stdout.strip()


def update_application(app_id: int, new_status: str):
    """Update application status."""
    applications = json.loads(APPLICATIONS_FILE.read_text())
    
    for app in applications:
        if app["id"] == app_id:
            app["status"] = new_status
            app["updated_at"] = datetime.now().isoformat()
            break
    
    APPLICATIONS_FILE.write_text(json.dumps(applications, indent=2))


def main():
    stale = get_stale_applications()
    
    if not stale:
        print("No applications need follow-up.")
        return
    
    for app in stale:
        message = f"You applied to {app['company']} ({app['role']}) {app['days_since']} days ago. Any update?"
        
        response = send_notification(
            title="Job Hunter Reminder",
            message=message,
            actions=["Rejected", "Interviewing", "Snooze"]
        )
        
        if response == "Rejected":
            update_application(app["id"], "rejected")
            print(f"Marked {app['company']} as rejected")
        
        elif response == "Interviewing":
            update_application(app["id"], "interviewing")
            print(f"Marked {app['company']} as interviewing")
        
        elif response == "Snooze":
            print(f"Snoozed {app['company']}")


if __name__ == "__main__":
    main()