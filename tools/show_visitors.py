import json
from collections import defaultdict

events = defaultdict(list)

with open(
    "data/events/generated_events.jsonl",
    "r",
    encoding="utf-8"
) as f:

    for line in f:

        e = json.loads(line)

        events[
            e["visitor_id"]
        ].append(
            e["event_type"]
        )

for visitor in sorted(events):

    print(
        visitor,
        "->",
        events[visitor]
    )