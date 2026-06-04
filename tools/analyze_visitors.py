import json
from collections import Counter

visitor_events = Counter()

with open(
    "data/events/generated_events.jsonl",
    "r",
    encoding="utf-8"
) as f:

    for line in f:

        event = json.loads(line)

        if event["event_type"] == "ENTRY":

            visitor_events[
                event["visitor_id"]
            ] += 1

print("\nVISITORS WITH MULTIPLE ENTRIES:\n")

for visitor, count in visitor_events.items():

    if count > 1:

        print(
            visitor,
            count
        )
        