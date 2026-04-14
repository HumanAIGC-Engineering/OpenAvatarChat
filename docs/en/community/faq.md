# FAQ

Common issues and solutions.

> [!TIP]
> If your issue is not listed, please submit an [Issue](https://github.com/HumanAIGC-Engineering/OpenAvatarChat/issues).

## Installation

### Dependencies fail to install

Ensure git-lfs is installed and submodules updated:
```bash
sudo apt install git-lfs
git lfs install
git submodule update --init --recursive --depth 1
```

### CUDA version mismatch

This project requires NVIDIA driver supporting CUDA >= 12.8.

## Runtime

### Digital human won't load

1. Confirm all model dependencies are downloaded
2. Check SSL certificate configuration (required for non-localhost)
3. Verify TURN service configuration (required for public access)

### Connection stuck on "Waiting..."

This is typically a NAT traversal issue. Configure a TURN server. See [Deployment](/en/guide/deployment).
