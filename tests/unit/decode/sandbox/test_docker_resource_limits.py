"""Regression tests for Docker sandbox resource constraints."""

from pathlib import Path

import pytest

from decode.config.settings import settings
from decode.sandbox.docker_backend import DockerBackend


@pytest.mark.parametrize(
    ("cpus", "memory_mb", "pids_limit"),
    [
        (1.0, 2048, 256),
        (0.5, 512, 64),
    ],
)
def test_container_receives_resource_limits(
    monkeypatch,
    tmp_path: Path,
    cpus: float,
    memory_mb: int,
    pids_limit: int,
) -> None:
    monkeypatch.setattr(settings, "sandbox_docker_cpus", cpus)
    monkeypatch.setattr(settings, "sandbox_docker_memory_mb", memory_mb)
    monkeypatch.setattr(settings, "sandbox_docker_pids_limit", pids_limit)
    monkeypatch.setattr(settings, "sandbox_git_token", None)

    args = DockerBackend()._run_args(tmp_path)

    def argument_value(flag: str) -> str:
        assert args.count(flag) == 1
        return args[args.index(flag) + 1]

    assert argument_value("--cpus") == str(cpus)
    assert argument_value("--memory") == f"{memory_mb}m"
    assert argument_value("--memory-swap") == f"{memory_mb}m"
    assert argument_value("--pids-limit") == str(pids_limit)
    assert argument_value("-v") == f"{tmp_path}:/workspace"
    assert argument_value("-w") == "/workspace"


@pytest.mark.parametrize(
    ("field_name", "invalid_value"),
    [
        ("sandbox_docker_cpus", 0),
        ("sandbox_docker_cpus", -1),
        ("sandbox_docker_cpus", float("inf")),
        ("sandbox_docker_memory_mb", 0),
        ("sandbox_docker_pids_limit", -1),
    ],
)
def test_invalid_resource_settings_are_rejected(
    field_name: str,
    invalid_value: float | int,
) -> None:
    from pydantic import ValidationError

    # Validate a complete copy without loading additional environment settings.
    values = settings.model_dump()
    values[field_name] = invalid_value

    with pytest.raises(ValidationError):
        type(settings).model_validate(values)
