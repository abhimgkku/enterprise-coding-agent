]633;E;printf '# Sandbox image verification\\n\\n';799289be-a74e-442e-bc92-3cd08df77145]633;C# Sandbox image verification

- Verification: passed
- Image: decode-sandbox:local-v1
- Local UID: 1000
- Local GID: 1000
- Base image: ghcr.io/astral-sh/uv@sha256:e5b65587bce7de595f299855d7385fe7fca39b8a74baa261ba1b7147afa78e58
- Built image ID: sha256:fe251cf3758e36ec0f8556ab922d699761ccfc9004617365ea783a40c0ce2cf5

Verified non-root execution, offline tool availability, local Git commits,
workspace ownership, and rejection of a protected-directory write.

Backend integration and runtime installation removal remain pending.
