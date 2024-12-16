"""This module interacts with the run.sh script from AIxCC challenge projects."""

import re
import subprocess
from pathlib import Path

from pydantic import BaseModel


class RunResult(BaseModel):
    """Result of run.sh"""

    stdout: str
    stderr: str
    return_code: int

    def scan_for_sanitizer(self, sanitizers: dict[str, str]) -> tuple[str, str, str] | tuple[None, None, None]:
        """
        Extract sanitizer id, name and corresponding output.
        """

        # let's figure out which sanitizer triggered
        for output in [self.stdout, self.stderr]:
            for sanitizer_id, sanitizer in sanitizers.items():
                if sanitizer in output:

                    return sanitizer_id, sanitizer, output

        return None, None, None


def invoke_run_sh(params: list[str], project_path: Path) -> RunResult:
    "Invoke the run.sh with the given arguments."

    result = subprocess.run(
        ["./run.sh", "-x", *params],
        check=False,
        capture_output=True,
        text=True,
        errors="ignore",
        cwd=project_path.as_posix(),
    )

    # Get the output path from the debug logs
    match = re.search(r"(?m)^<DEBUG> created output directory: (.*)$", result.stdout)

    # if output path is not known, use process output
    if not match:
        return RunResult(
            stdout=result.stdout,
            stderr=result.stderr,
            return_code=result.returncode,
        )

    output_path = match.group(1)

    return RunResult(
        stdout=(Path(output_path) / "stdout.log").read_text(),
        stderr=(Path(output_path) / "stderr.log").read_text(),
        return_code=int((Path(output_path) / "exitcode").read_text()),
    )
