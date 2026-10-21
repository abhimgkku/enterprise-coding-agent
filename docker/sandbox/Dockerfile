# Supply a digest-pinned base image through --build-arg BASE_IMAGE.
ARG BASE_IMAGE
FROM ${BASE_IMAGE}

USER root

# Install tools once during the image build, not during every agent session.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        bash \
        ca-certificates \
        coreutils \
        curl \
        findutils \
        git \
        gh \
        grep \
        procps \
    && rm -rf /var/lib/apt/lists/*

# Match the local WSL user's IDs so bind-mounted files remain editable.
# These are build-time values for this local development image.
ARG SANDBOX_UID=1000
ARG SANDBOX_GID=1000

RUN test "${SANDBOX_UID}" -gt 0 \
    && test "${SANDBOX_GID}" -gt 0 \
    && groupadd --gid "${SANDBOX_GID}" sandbox \
    && useradd \
        --uid "${SANDBOX_UID}" \
        --gid "${SANDBOX_GID}" \
        --create-home \
        --shell /bin/bash \
        sandbox \
    && mkdir -p /workspace \
    && chown sandbox:sandbox /workspace

ENV HOME=/home/sandbox \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_CACHE_DIR=/home/sandbox/.cache/uv \
    UV_PYTHON_DOWNLOADS=never \
    UV_LINK_MODE=copy

WORKDIR /workspace

USER sandbox:sandbox

CMD ["sleep", "infinity"]