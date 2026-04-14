#!/usr/bin/env python3
"""
JWT Token 生成工具

用于生成用于 API 认证的 JWT token。

使用方式:
    # 使用环境变量中的密钥生成 token
    python scripts/generate_jwt.py
    
    # 指定过期时间（小时）
    python scripts/generate_jwt.py --expire 72
    
    # 指定主题和自定义声明
    python scripts/generate_jwt.py --subject "user_123" --claim "role=admin" --claim "name=张三"
    
    # 使用指定的密钥
    python scripts/generate_jwt.py --secret "your-secret-key"
    
    # 生成新的随机密钥
    python scripts/generate_jwt.py --generate-secret

环境变量:
    AVATAR_CHAT_JWT_SECRET: JWT 签名密钥
"""

import argparse
import os
import secrets
import sys
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

from dotenv import load_dotenv

# 添加项目路径
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root / "src"))

# 加载项目根目录下的 .env（若存在）
load_dotenv(dotenv_path=project_root / ".env")

try:
    import jwt
except ImportError:
    print("错误: 请先安装 PyJWT 库")
    print("运行: pip install PyJWT")
    sys.exit(1)


def generate_secret(length: int = 32) -> str:
    """生成随机密钥"""
    return secrets.token_hex(length)


def generate_token(
    secret: str,
    algorithm: str = "HS256",
    subject: str = "api_access",
    issuer: str = "avatar-chat",
    expire_hours: int = 24,
    extra_claims: dict = None,
    include_jti: bool = True,
) -> str:
    """
    生成 JWT token
    
    Args:
        secret: 签名密钥
        algorithm: 签名算法
        subject: token 主题
        issuer: 签发者
        expire_hours: 过期时间（小时）
        extra_claims: 额外的声明
        include_jti: 是否包含唯一标识符
        
    Returns:
        str: JWT token
    """
    now = datetime.now(timezone.utc)
    expire = now + timedelta(hours=expire_hours)
    
    payload = {
        "sub": subject,
        "iss": issuer,
        "iat": now,
        "exp": expire,
        "nbf": now,
    }
    
    # 添加唯一标识符（可用于 token 吊销追踪）
    if include_jti:
        payload["jti"] = str(uuid.uuid4())
    
    if extra_claims:
        payload.update(extra_claims)
    
    return jwt.encode(payload, secret, algorithm=algorithm)


def decode_token(token: str, secret: str, algorithm: str = "HS256") -> dict:
    """
    解码 JWT token（用于验证）
    
    Args:
        token: JWT token
        secret: 签名密钥
        algorithm: 签名算法
        
    Returns:
        dict: payload
    """
    return jwt.decode(
        token,
        secret,
        algorithms=[algorithm],
        options={"verify_exp": True},
    )


def parse_claims(claim_strings: list) -> dict:
    """解析命令行中的 claim 参数"""
    claims = {}
    for claim in claim_strings:
        if "=" in claim:
            key, value = claim.split("=", 1)
            # 尝试转换数字
            try:
                value = int(value)
            except ValueError:
                try:
                    value = float(value)
                except ValueError:
                    # 保持字符串
                    pass
            claims[key.strip()] = value
    return claims


def main():
    parser = argparse.ArgumentParser(
        description="JWT Token 生成工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 基本用法（使用环境变量 AVATAR_CHAT_JWT_SECRET）
  python scripts/generate_jwt.py

  # 指定过期时间为 7 天
  python scripts/generate_jwt.py --expire 168

  # 添加自定义声明
  python scripts/generate_jwt.py --subject "service_a" --claim "role=admin"

  # 生成新密钥
  python scripts/generate_jwt.py --generate-secret
        """
    )
    
    parser.add_argument(
        "--secret",
        type=str,
        help="JWT 签名密钥（默认从环境变量 AVATAR_CHAT_JWT_SECRET 获取）"
    )
    parser.add_argument(
        "--algorithm",
        type=str,
        default="HS256",
        help="签名算法（默认: HS256）"
    )
    parser.add_argument(
        "--subject",
        type=str,
        default="api_access",
        help="Token 主题（默认: api_access）"
    )
    parser.add_argument(
        "--issuer",
        type=str,
        default="avatar-chat",
        help="签发者（默认: avatar-chat）"
    )
    parser.add_argument(
        "--expire",
        type=int,
        default=24,
        help="过期时间，单位小时（默认: 24）"
    )
    parser.add_argument(
        "--claim",
        action="append",
        default=[],
        help="额外的声明，格式: key=value（可多次使用）"
    )
    parser.add_argument(
        "--generate-secret",
        action="store_true",
        help="生成新的随机密钥并退出"
    )
    parser.add_argument(
        "--secret-length",
        type=int,
        default=32,
        help="生成密钥的长度（默认: 32 字节）"
    )
    parser.add_argument(
        "--verify",
        type=str,
        help="验证指定的 token"
    )
    parser.add_argument(
        "--env-key",
        type=str,
        default="AVATAR_CHAT_JWT_SECRET",
        help="密钥环境变量名称（默认: AVATAR_CHAT_JWT_SECRET）"
    )
    
    args = parser.parse_args()
    
    # 生成新密钥模式
    if args.generate_secret:
        new_secret = generate_secret(args.secret_length)
        print("=" * 60)
        print("生成的 JWT 密钥（请妥善保管）:")
        print("=" * 60)
        print(f"\n{new_secret}\n")
        print("=" * 60)
        print(f"\n设置环境变量:")
        print(f"  export {args.env_key}=\"{new_secret}\"")
        print()
        return
    
    # 获取密钥
    secret = args.secret or os.environ.get(args.env_key, "")
    
    if not secret:
        print(f"错误: 未提供 JWT 密钥")
        print(f"请通过以下方式之一提供密钥:")
        print(f"  1. 设置环境变量: export {args.env_key}=\"your-secret\"")
        print(f"  2. 使用命令行参数: --secret \"your-secret\"")
        print(f"  3. 生成新密钥: --generate-secret")
        sys.exit(1)
    
    # 验证 token 模式
    if args.verify:
        print("=" * 60)
        print("验证 JWT Token")
        print("=" * 60)
        try:
            payload = decode_token(args.verify, secret, args.algorithm)
            print("\n✅ Token 有效\n")
            print("Payload 内容:")
            for key, value in payload.items():
                if key in ("iat", "exp", "nbf"):
                    # 转换时间戳
                    dt = datetime.fromtimestamp(value, tz=timezone.utc)
                    print(f"  {key}: {value} ({dt.strftime('%Y-%m-%d %H:%M:%S UTC')})")
                else:
                    print(f"  {key}: {value}")
            
            # 计算剩余有效期
            exp = payload.get("exp")
            if exp:
                remaining = datetime.fromtimestamp(exp, tz=timezone.utc) - datetime.now(timezone.utc)
                if remaining.total_seconds() > 0:
                    hours = remaining.total_seconds() / 3600
                    print(f"\n剩余有效期: {hours:.1f} 小时")
                else:
                    print("\n⚠️ Token 已过期")
        except jwt.ExpiredSignatureError:
            print("\n❌ Token 已过期")
            sys.exit(1)
        except jwt.InvalidTokenError as e:
            print(f"\n❌ Token 无效: {e}")
            sys.exit(1)
        return
    
    # 生成 token
    extra_claims = parse_claims(args.claim)
    
    token = generate_token(
        secret=secret,
        algorithm=args.algorithm,
        subject=args.subject,
        issuer=args.issuer,
        expire_hours=args.expire,
        extra_claims=extra_claims,
    )
    
    # 计算过期时间
    expire_time = datetime.now(timezone.utc) + timedelta(hours=args.expire)
    
    print("=" * 60)
    print("JWT Token 生成成功")
    print("=" * 60)
    print(f"\n主题 (sub): {args.subject}")
    print(f"签发者 (iss): {args.issuer}")
    print(f"算法: {args.algorithm}")
    print(f"有效期: {args.expire} 小时")
    print(f"过期时间: {expire_time.strftime('%Y-%m-%d %H:%M:%S UTC')}")
    
    if extra_claims:
        print(f"额外声明: {extra_claims}")
    
    print("\n" + "=" * 60)
    print("Token:")
    print("=" * 60)
    print(f"\n{token}\n")
    print("=" * 60)
    
    print("\n使用方式:")
    print("  HTTP Header: Authorization: Bearer <token>")
    print(f"\n  curl -H \"Authorization: Bearer {token[:50]}...\" http://localhost:8282/api/endpoint")
    print()


if __name__ == "__main__":
    main()

