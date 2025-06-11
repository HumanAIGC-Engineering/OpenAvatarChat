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
    echo "检测到 AvatarMusetalk 配置，开始安装相关依赖..."
    
    # 安装依赖
    echo "安装 setuptools 和 pip..."
    uv pip install setuptools pip
    
    echo "安装 chumpy==0.70..."
    uv pip install chumpy==0.70 --no-build-isolation
    
    echo "安装 mmcv==2.2.0..."
    uv pip install mmcv==2.2.0 -f https://download.openmmlab.com/mmcv/dist/cu121/torch2.4/index.html
    
    echo "AvatarMusetalk 依赖安装完成。"
else
    echo "配置文件中未发现 AvatarMusetalk 配置，跳过相关依赖安装。"
fi 