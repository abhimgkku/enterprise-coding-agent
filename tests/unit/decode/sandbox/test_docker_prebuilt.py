"""Tests for the transitional prebuilt Docker execution mode."""

from pathlib import Path

import pytest
from pydantic import SecretStr

from decode.config.settings import settings
from decode.sandbox import docker_backend
from decode.sandbox.docker_backend import DockerBackend


@pytest.fixture
def prebuilt_settings(monkeypatch):
    monkeypatch.setattr(settings, "sandbox_docker_prebuilt", True)
    monkeypatch.setattr(settings, "sandbox_docker_image", "test-sandbox:v1")
    monkeypatch.setattr(settings, "sandbox_git_token", None)
    monkeypatch.setattr(docker_backend.os, "getuid", lambda: 1000)
    monkeypatch.setattr(docker_backend.os, "getgid", lambda: 1000)


def test_prebuilt_worker_has_explicit_nonroot_identity(prebuilt_settings):
    args = DockerBackend()._run_args(Path("/ws"))

    assert args[args.index("--user") + 1] == "1000:1000"
    assert args[args.index("--cap-drop") + 1] == "ALL"
    assert args[args.index("--security-opt") + 1] == "no-new-privileges=true"
    assert "--pull=never" in args
    assert args[-3:] == ["test-sandbox:v1", "sleep", "infinity"]
    assert "-e" not in args


def test_prebuilt_worker_rejects_git_token(prebuilt_settings, monkeypatch):
    monkeypatch.setattr(
        settings,
        "sandbox_git_token",
        SecretStr("test-secret"),
    )

    with pytest.raises(RuntimeError, match="SANDBOX_GIT_TOKEN"):
        DockerBackend()._run_args(Path("/ws"))


@pytest.mark.parametrize(
    ("uid", "gid"),
    [(0, 1000), (1000, 0)],
)
def test_prebuilt_worker_rejects_root_identity(
    prebuilt_settings,
    monkeypatch,
    uid,
    gid,
):
    monkeypatch.setattr(docker_backend.os, "getuid", lambda: uid)
    monkeypatch.setattr(docker_backend.os, "getgid", lambda: gid)

    with pytest.raises(RuntimeError, match="non-root"):
        DockerBackend()._run_args(Path("/ws"))
