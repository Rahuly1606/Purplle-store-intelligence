import json
from collections import Counter

event_types = Counter()

with open(
    "data/events/generated_events.jsonl",
    "r",
    encoding="utf-8"
) as f:

    for line in f:

        event = json.loads(line)

        event_types[
            event["event_type"]
        ] += 1

print("\nEVENT COUNTS:\n")

for k, v in event_types.items():
    print(k, ":", v)