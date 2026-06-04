with open(
    "data/events/generated_events.jsonl",
    "r",
    encoding="utf-8"
) as f:

    lines = f.readlines()

print("\nLAST 20 LINES:\n")

for line in lines[-20:]:

    print(line.strip())