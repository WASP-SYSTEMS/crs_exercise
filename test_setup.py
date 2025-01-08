from pathlib import Path
from project.project import AixccProject

project = AixccProject(
    project_path=Path("mock-cp"),
    src_path_rel=Path("src/samples")
)

print("Testing setup")

print("Testing patch verification (takes some time)...", end=" ", flush=True)

out = project.verify_patch()

if not "AddressSanitizer: global-buffer-overflow" in out:
    print("Patch verification failed:\n" + out)
    exit()

print("OK")

print("Testing source code interaction...", end=" ", flush=True)

out = project.get_source_code()

if not "char items[3][10];" in out:
    print("Reading source code failed:\n" + out)
    exit()

project.write_source_code(out.replace(
    "char* buff;",
    "TEST_ME"
))

out = project.get_source_code()

if not "TEST_ME" in out:
    print("Writing source code failed")
    exit()

print("OK")

# reste source code
AixccProject(
    project_path=Path("mock-cp"),
    src_path_rel=Path("src/samples")
)