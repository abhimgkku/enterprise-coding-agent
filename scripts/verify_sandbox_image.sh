#!/usr/bin/env bash
set -euo pipefail

image="${1:-decode-sandbox:local-v1}"

# Use an existing image only. Verification must not silently pull another one.
docker image inspect "$image" >/dev/null

workspace="$(mktemp -d)"
container_name="decode-image-check-$(cat /proc/sys/kernel/random/uuid)"

cleanup() {
    # Target only this verification container.
    docker rm -f "$container_name" >/dev/null 2>&1 || true
    rm -rf -- "$workspace"
}
trap cleanup EXIT

host_uid="$(id -u)"
host_gid="$(id -g)"

echo "Verifying image: $image"

docker run --rm \
    --pull=never \
    --name "$container_name" \
    --network none \
    --cap-drop ALL \
    --security-opt no-new-privileges=true \
    --cpus 1 \
    --memory 512m \
    --memory-swap 512m \
    --pids-limit 64 \
    --mount "type=bind,src=$workspace,dst=/workspace" \
    --env EXPECTED_UID="$host_uid" \
    --env EXPECTED_GID="$host_gid" \
    "$image" \
    bash -euo pipefail -c '
        echo "Checking non-root identity..."
        test "$(id -u)" -ne 0
        test "$(id -u)" = "$EXPECTED_UID"
        test "$(id -g)" = "$EXPECTED_GID"

        echo "Checking preinstalled tools..."
        python --version
        uv --version
        git --version
        gh --version

        echo "Checking workspace writes..."
        printf "sandbox write succeeded\n" > /workspace/probe.txt

        echo "Checking home-directory writes..."
        printf "home write succeeded\n" > "$HOME/probe.txt"

        echo "Checking protected-directory permissions..."
        if touch /usr/local/bin/decode-permission-probe 2>/dev/null; then
            echo "FAIL: sandbox user can modify /usr/local/bin"
            exit 1
        fi

        echo "Checking local Git operations..."
        git init -q /workspace/repo
        git -C /workspace/repo config user.name "Sandbox Verification"
        git -C /workspace/repo config user.email "sandbox@example.invalid"

        printf "verification\n" > /workspace/repo/README.md
        git -C /workspace/repo add README.md
        git -C /workspace/repo commit -qm "Verify sandbox Git operations"

        echo "PASS: in-container verification completed."
    '

echo "Checking host ownership..."
test "$(stat -c %u "$workspace/probe.txt")" = "$host_uid"
test "$(stat -c %g "$workspace/probe.txt")" = "$host_gid"

echo "Checking that the host user can edit the generated file..."
printf "host write succeeded\n" >> "$workspace/probe.txt"

echo "PASS: non-root execution, offline tools, Git operations, and file ownership."