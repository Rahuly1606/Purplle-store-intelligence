import json
from pathlib import Path


class EventEmitter:

    def __init__(self, output_file):

        self.output_file = Path(output_file)

        self.output_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

    def emit(self, event):

        with open(
            self.output_file,
            "a",
            encoding="utf-8"
        ) as f:

            f.write(
                json.dumps(event)
            )

            f.write("\n")