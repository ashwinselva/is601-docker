import shutil
import subprocess
import time
import pytest


docker_cli = shutil.which("docker")


@pytest.mark.skipif(docker_cli is None, reason="docker CLI not available")
def test_docker_build():
    """Attempt to build the project's Docker image locally.

    This test will be skipped if the `docker` CLI is not found on PATH
    or if the Docker daemon does not respond to `docker info`.
    """
    # Quick check that the daemon is reachable
    info = subprocess.run([docker_cli, "info"], capture_output=True, text=True)
    if info.returncode != 0:
        pytest.skip("docker daemon not available or not responding")

    tag = f"module7_is601:test_{int(time.time())}"
    # Run docker build in repository root (assumes tests are executed from project root)
    res = subprocess.run([docker_cli, "build", "-t", tag, "."], capture_output=True, text=True)
    print(res.stdout)
    print(res.stderr)

    assert res.returncode == 0, f"Docker build failed: {res.stderr}"

    # Cleanup: remove the test image (best-effort)
    subprocess.run([docker_cli, "rmi", "-f", tag], capture_output=True)
