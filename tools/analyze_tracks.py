import json
from collections import Counter

entries = Counter()
exits = Counter()

with open(
    "data/events/generated_events.jsonl",
    "r",
    encoding="utf-8"
) as f:

    for line in f:

        event = json.loads(line)

        visitor = event["visitor_id"]

        if event["event_type"] == "ENTRY":
            entries[visitor] += 1

        elif event["event_type"] == "EXIT":
            exits[visitor] += 1

print("\nENTRY COUNT:", len(entries))
print("EXIT COUNT :", len(exits))

missing = []

for visitor in entries:

    if visitor not in exits:
        missing.append(visitor)

print(
    "\nVISITORS WITHOUT EXIT:",
    len(missing)
)

print(
    "\nFIRST 20:"
)

for v in missing[:20]:
    print(v)