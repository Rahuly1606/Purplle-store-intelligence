import json
from collections import Counter

entry_counter = Counter()
exit_counter = Counter()

with open(
    "data/events/generated_events.jsonl",
    "r",
    encoding="utf-8"
) as f:

    for line in f:

        event = json.loads(line)

        visitor = event["visitor_id"]

        if event["event_type"] == "ENTRY":

            entry_counter[visitor] += 1

        elif event["event_type"] == "EXIT":

            exit_counter[visitor] += 1


print("\nDUPLICATE ENTRIES:\n")

for visitor, count in entry_counter.items():

    if count > 1:

        print(
            visitor,
            count
        )

print("\nDUPLICATE EXITS:\n")

for visitor, count in exit_counter.items():

    if count > 1:

        print(
            visitor,
            count
        )