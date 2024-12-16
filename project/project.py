"""Project definition."""

from functools import cached_property
from pathlib import Path

from git import Repo

from .project_yaml import ProjectYaml
from .runsh import RunResult
from .runsh import invoke_run_sh


class BaseProject:
    """Project base class"""

    def __init__(self, project_path: Path, src_path_rel: Path) -> None:
        self.cp_path = project_path
        self.src_path = project_path / src_path_rel

        # check out target refs
        for src, src_val in self.yaml.cp_sources.items():
            r = Repo(self.cp_path / "src" / src)
            r.git.checkout(src_val.ref, force=True)

    @cached_property
    def yaml(self) -> ProjectYaml:
        "The project.yaml file of this challenge project"
        return ProjectYaml.from_cp_path(self.cp_path)

    @property
    def repo(self) -> Repo:
        "Return a src repository."

        return Repo(self.src_path)


class AixccProject(BaseProject):
    "Class for aixcc based projects."

    POV_INPUT_PATH = Path("exemplar_only/cpv_1/blobs/sample_solve.bin")

    def __init__(self, project_path: Path, src_path_rel: Path) -> None:
        super().__init__(project_path, src_path_rel)
    
    def get_source_code(self) -> str:
        """Get the source code of the project."""

        return (self.src_path / "mock_vp.c").read_text()
    
    def write_source_code(self, code: str) -> str:
        """Get the source code of the project."""

        return (self.src_path / "mock_vp.c").write_text(code)
    
    def verify_patch(self) -> str:
        """
        Verify the patch and get feedback about what went wrong or if the patch is ok.

        Returns compilation errors, crash report if the patch did not work.
        """

        # rebuild the project
        output = self._build()
        if output.return_code != 0:
            return f"Compilation error:\n```\n{output.stderr}\n```\n"
        
        # execute pov
        output = self._run_pov(self.POV_INPUT_PATH, self.yaml.harnesses["id_1"].name)

         # check if pov crashed
        san_id, _, crash_output = output.scan_for_sanitizer(self.yaml.sanitizers)

        if san_id is not None:
            assert crash_output is not None
            return f"The vulnerabilty still persists. Here is the crash report:\n```\n{crash_output}\n```\n"
        
        if output.return_code != 0:
            return f"Ooops something went wrong: \n ```json\n{output.model_dump_json()}\n```\n"

        # run tests if program did not crash
        test_out = self._run_tests()
        # 0 indicates all tests passed. 1 indicates an internal error,
        # which has nothing to do with the patch
        if test_out.return_code == 0:
            return "The vulnerabilty is fixed. Yeaaahh :)"
        
        if 1 < test_out.return_code < 125:
            return (
                "The program did not crash, but"
                f"the tests failed:\n ```json\n{test_out.model_dump_json()}\n```\n"
            )
        
        return f"Ooops something went wrong: \n ```json\n{test_out.model_dump_json()}\n```\n"

    def _build(self) -> RunResult:
        "Build the CP"

        return invoke_run_sh(["build"], self.cp_path)
    
    def _run_pov(self, input_path: Path, harness_name: str) -> RunResult:
        "Run a pov blob against a harness"

        return invoke_run_sh(["run_pov", input_path.as_posix(), harness_name], self.cp_path)

    def _run_tests(self) -> RunResult:
        """
        Run the functionality tests.
        0 indicates all tests passed. 1 indicates an internal error.
        """

        return invoke_run_sh(["run_tests"], self.cp_path)
