import json
import os
import argparse
from datetime import datetime

DATA_FILE = "data/logs.json"

def load_logs():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_logs(logs):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(logs, f, indent=4)

def add_log(entry, tags):
    logs = load_logs()
    log = {
        "timestamp": datetime.now().isoformat(),
        "entry": entry,
        "tags": tags
    }
    logs.append(log)
    save_logs(logs)
    print("✅ Log added.")

def view_logs(keyword=None, date=None):
    logs = load_logs()
    for log in logs:
        if (keyword and keyword.lower() not in log["entry"].lower()) or \
           (date and not log["timestamp"].startswith(date)):
            continue
        print(f"[{log['timestamp']}] {log['entry']} (Tags: {', '.join(log['tags'])})")

def main():
    parser = argparse.ArgumentParser(description="📝 DevLogger - Track your dev work.")
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add", help="Add a new log entry")
    add_parser.add_argument("entry", help="The activity description")
    add_parser.add_argument("--tags", nargs="*", default=[], help="Optional tags")

    view_parser = subparsers.add_parser("view", help="View log entries")
    view_parser.add_argument("--keyword", help="Search keyword")
    view_parser.add_argument("--date", help="Filter by date (YYYY-MM-DD)")

    args = parser.parse_args()
    if args.command == "add":
        add_log(args.entry, args.tags)
    elif args.command == "view":
        view_logs(args.keyword, args.date)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
