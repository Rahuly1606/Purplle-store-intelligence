import json

file_path = "verification_events.jsonl"

print("\nFIRST 20 EVENTS:\n")

with open(file_path, "r", encoding="utf-8") as f:

    for i, line in enumerate(f):

        event = json.loads(line)

        print(event)

        if i >= 19:
            break