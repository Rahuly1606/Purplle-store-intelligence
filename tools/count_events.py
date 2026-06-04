import json

count = 0

with open(
    "data/events/generated_events.jsonl",
    "r",
    encoding="utf-8"
) as f:

    for line in f:

        count += 1

print(
    "TOTAL EVENTS:",
    count
)