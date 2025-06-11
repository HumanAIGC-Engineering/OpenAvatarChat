#!/usr/bin/env bash

# 初始化变量
CONFIG_FILE=""

# 解析参数的循环
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --config )
            CONFIG_FILE="$2"
            shift 2 # 跳过当前参数及后一个参数
            ;;
        * )
            shift # 跳过未知参数
            ;;
    esac
done

if [[ -z "$CONFIG_FILE" ]]; then
    echo "错误：未指定配置文件。请使用 --config 参数指定配置文件路径。"
    exit 1
fi

if [[ ! -f "$CONFIG_FILE" ]]; then
    echo "错误：配置文件 $CONFIG_FILE 不存在。"
    exit 1
fi

echo "解析配置文件: $CONFIG_FILE"

# 使用 grep 检查配置文件中是否包含 AvatarMusetalk 配置
if grep -q "AvatarMusetalk:" "$CONFIG_FILE"; then
    echo "检测到 AvatarMusetalk 配置，开始执行后续配置..."
    
    # 1. 修改 mmdet 的 __init__.py 文件中的 mmcv_maximum_version
    MMDET_INIT_FILE=".venv/lib/python3.11/site-packages/mmdet/__init__.py"
    
    if [[ -f "$MMDET_INIT_FILE" ]]; then
        echo "修改 mmdet/__init__.py 中的 mmcv_maximum_version..."
        sed -i "s/mmcv_maximum_version = '[^']*'/mmcv_maximum_version = '2.2.1'/g" "$MMDET_INIT_FILE"
        echo "mmcv_maximum_version 已更新为 2.2.1"
    else
        echo "警告：未找到 $MMDET_INIT_FILE 文件"
    fi
    
    # 2. 设置 LD_LIBRARY_PATH 环境变量
    echo "设置 NVIDIA 库路径到 LD_LIBRARY_PATH..."
    
    # 查找 .venv 中的 nvidia 库路径
    VENV_PATH=".venv"
    NVIDIA_PATHS=""
    
    # 检查常见的 nvidia 库路径
    NVIDIA_LIBS=(
        "cuda_runtime/lib"
        "cublas/lib" 
        "cudnn/lib"
        "cufft/lib"
        "curand/lib"
        "cusolver/lib"
        "cusparse/lib"
        "nccl/lib"
        "nvjpeg/lib"
        "nvtx/lib"
    )
    
    for lib in "${NVIDIA_LIBS[@]}"; do
        LIB_PATH="$VENV_PATH/lib/python3.11/site-packages/nvidia/$lib"
        if [[ -d "$LIB_PATH" ]]; then
            if [[ -z "$NVIDIA_PATHS" ]]; then
                NVIDIA_PATHS="$LIB_PATH"
            else
                NVIDIA_PATHS="$NVIDIA_PATHS:$LIB_PATH"
            fi
            echo "找到 NVIDIA 库路径: $LIB_PATH"
        fi
    done
    
    if [[ -n "$NVIDIA_PATHS" ]]; then
        # 将环境变量设置写入到一个脚本文件中，供后续使用
        echo "#!/bin/bash" > /tmp/set_nvidia_env.sh
        echo "export LD_LIBRARY_PATH=\"$NVIDIA_PATHS:\$LD_LIBRARY_PATH\"" >> /tmp/set_nvidia_env.sh
        echo "echo \"LD_LIBRARY_PATH 已设置为: \$LD_LIBRARY_PATH\"" >> /tmp/set_nvidia_env.sh
        chmod +x /tmp/set_nvidia_env.sh
        
        # 执行环境变量设置
        source /tmp/set_nvidia_env.sh
        rm -f /tmp/set_nvidia_env.sh
        
        echo "NVIDIA 库路径已添加到 LD_LIBRARY_PATH"
    else
        echo "警告：未找到任何 NVIDIA 库路径"
    fi
    
    echo "AvatarMusetalk 后续配置完成。"
else
    echo "配置文件中未发现 AvatarMusetalk 配置，跳过后续配置。"
fi 