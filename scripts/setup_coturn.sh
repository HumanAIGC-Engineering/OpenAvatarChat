#!/bin/bash

# 检查是否以root权限运行
if [ "$EUID" -ne 0 ]; then 
    echo "请使用sudo运行此脚本"
    exit 1
fi

# 安装coturn
echo "正在安装coturn..."
if command -v apt-get &> /dev/null; then
    apt-get update
    apt-get install -y coturn
elif command -v yum &> /dev/null; then
    yum install -y coturn
elif command -v brew &> /dev/null; then
    brew install coturn
else
    echo "未找到包管理器，请手动安装coturn"
    exit 1
fi

# 获取内网IP地址
PRIVATE_IP=$(ip addr | grep 'inet ' | grep -v '127.0.0.1' | grep -v 'docker' | awk '{print $2}' | cut -d/ -f1 | head -n 1)
if [ -z "$PRIVATE_IP" ]; then
    PRIVATE_IP=$(ifconfig | grep 'inet ' | grep -v '127.0.0.1' | grep -v 'docker' | awk '{print $2}' | head -n 1)
fi

# 获取公网IP地址
PUBLIC_IP=$(curl -s ifconfig.me)
if [ -z "$PUBLIC_IP" ]; then
    PUBLIC_IP=$(curl -s ipinfo.io/ip)
fi

# 生成一个基于公网IP的realm标识符
REALM="turn.${PUBLIC_IP//./-}.turnserver"

echo "检测到内网IP地址: $PRIVATE_IP"
echo "检测到公网IP地址: $PUBLIC_IP"
echo "生成的realm标识符: $REALM"

# 配置coturn
echo "正在配置coturn..."
CONFIG_FILE="/etc/turnserver.conf"
MIN_PORT=49152
MAX_PORT=65535

# 备份原始配置文件
if [ -f "$CONFIG_FILE" ]; then
    cp "$CONFIG_FILE" "${CONFIG_FILE}.bak"
fi

# 写入新的配置
cat > "$CONFIG_FILE" << EOF
listening-port=3478
tls-listening-port=5349
listening-ip=0.0.0.0
relay-ip=$PRIVATE_IP
external-ip=$PUBLIC_IP
min-port=$MIN_PORT
max-port=$MAX_PORT
verbose
fingerprint
lt-cred-mech
user=username:password
realm=$REALM
EOF

# 启用coturn服务
echo "正在启用coturn服务..."
if command -v systemctl &> /dev/null; then
    systemctl enable coturn
    systemctl restart coturn
elif command -v service &> /dev/null; then
    service coturn restart
else
    echo "无法自动重启coturn服务，请手动重启"
fi

echo "coturn安装和配置完成！"
echo "请确保以下端口已开放："
echo "- UDP 3478"
echo "- TCP 3478"
echo "- UDP 5349"
echo "- TCP 5349"
echo "- UDP $MIN_PORT:$MAX_PORT"
