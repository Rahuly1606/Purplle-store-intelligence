import json
from pathlib import Path


class FinalReportGenerator:

    def generate(
        self,
        metrics,
        output_file
    ):

        Path(
            output_file
        ).parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                metrics,
                f,
                indent=2
            )