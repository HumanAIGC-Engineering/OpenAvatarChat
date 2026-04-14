"""WebSocket Client Handler 集成测试"""
import asyncio
import json
import ssl
import wave
from typing import Any, Callable, Optional
from uuid import uuid4

import pytest
import websockets

from .ws_test_utils import (
    load_test_audio_bytes,
    parse_jbin_motion_data,
    generate_test_image,
    wait_for_message,
)

# 测试服务器地址（注意：服务器使用 HTTPS，所以用 wss://）
BASE_URL = "wss://localhost:8283"
SESSION_ENDPOINT = "/ws/session/{session_id}"

# SSL 上下文（禁用证书验证，因为使用自签名证书）
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE


async def initialize_session(ws) -> None:
    """向会话连接发送初始化消息并等待确认"""
    init_msg = {
        "header": {"name": "InitializeAvatarSession", "request_id": str(uuid4())},
        "payload": {"audio": {"format": "PCM", "sample_rate": 16000, "channels": 1}},
    }
    await ws.send(json.dumps(init_msg))
    response = await wait_for_message(ws, "AvatarSessionInitialized", timeout=5.0)
    assert response is not None, "未收到 AvatarSessionInitialized"


async def wait_for_condition(
    ws,
    predicate: Callable[[Any], Optional[Any]],
    timeout: float = 30.0,
) -> Optional[Any]:
    """等待满足条件的消息，predicate 返回非 None 表示命中"""
    try:
        async with asyncio.timeout(timeout):
            while True:
                message = await ws.recv()
                result = predicate(message)
                if result is not None:
                    return result
    except asyncio.TimeoutError:
        return None


async def wait_for_binary(ws, timeout: float = 30.0) -> Optional[bytes]:
    """等待下一条二进制消息"""
    return await wait_for_condition(
        ws,
        lambda msg: msg if isinstance(msg, bytes) else None,
        timeout=timeout,
    )


async def wait_for_json(ws, name: str, timeout: float = 30.0) -> Optional[dict]:
    """等待指定类型的 JSON 消息"""
    def _predicate(message: Any) -> Optional[dict]:
        if isinstance(message, str):
            data = json.loads(message)
            if data.get("header", {}).get("name") == name:
                return data
        return None

    return await wait_for_condition(ws, _predicate, timeout=timeout)


async def send_text(
    ws,
    text: str,
    *,
    speech_id: Optional[str] = None,
    mode: str = "full_text",
    end_of_speech: bool = True,
) -> str:
    """发送文本输入"""
    speech_id = speech_id or str(uuid4())
    text_msg = {
        "header": {"name": "SendHumanText", "request_id": str(uuid4())},
        "payload": {
            "speech_id": speech_id,
            "mode": mode,
            "text": text,
            "end_of_speech": end_of_speech,
        },
    }
    await ws.send(json.dumps(text_msg))
    return speech_id


class TestWSClientIntegration:
    """WebSocket Client Handler 集成测试"""

    @pytest.mark.asyncio
    async def test_01_session_initialization(self):
        session_id = str(uuid4())
        async with websockets.connect(
            f"{BASE_URL}{SESSION_ENDPOINT.format(session_id=session_id)}",
            ssl=ssl_context,
        ) as ws:
            await initialize_session(ws)
            print(f"✓ 会话初始化成功: {session_id}")

    @pytest.mark.asyncio
    async def test_02_motion_welcome_single_port(self):
        session_id = str(uuid4())
        async with websockets.connect(
            f"{BASE_URL}{SESSION_ENDPOINT.format(session_id=session_id)}",
            ssl=ssl_context,
        ) as ws:
            await initialize_session(ws)
            await send_text(ws, "你好")

            # 先等待 Welcome Message 的 JSON 文本帧
            welcome_json = await wait_for_json(ws, "MotionDataWelcome", timeout=30.0)
            assert welcome_json is not None, "未收到 Welcome Message JSON"
            
            # 然后等待二进制数据
            welcome_payload = await wait_for_binary(ws, timeout=30.0)
            assert welcome_payload is not None, "未收到 Welcome Message 二进制"
            parsed = parse_jbin_motion_data(welcome_payload)
            assert parsed["type"] == "container"
            assert "channel_names" in parsed["description"]["data_records"]["arkit_face"]
            print("✓ 单端口收到 Welcome Message")

    @pytest.mark.asyncio
    async def test_03_audio_streaming_binary(self):
        session_id = str(uuid4())
        async with websockets.connect(
            f"{BASE_URL}{SESSION_ENDPOINT.format(session_id=session_id)}",
            ssl=ssl_context,
        ) as ws:
            await initialize_session(ws)

            audio_bytes = load_test_audio_bytes()
            audio_msg = {
                "header": {"name": "SendHumanAudio", "request_id": str(uuid4())},
                "payload": {
                    "transport": "binary",
                    "binary_size": len(audio_bytes),
                    "segment_num": 1,
                },
            }
            await ws.send(json.dumps(audio_msg))
            await ws.send(audio_bytes)
            print(f"✓ 成功发送音频二进制，大小 {len(audio_bytes)} 字节")

            for _ in range(2):
                echo = await wait_for_json(ws, "EchoHumanText", timeout=30.0)
                if echo:
                    text = echo.get("payload", {}).get("text")
                    print(f"ASR EchoHumanText: {text}, end_of_speech: {echo.get('payload', {}).get('end_of_speech')}")

    @pytest.mark.asyncio
    async def test_04_video_upload_binary(self):
        session_id = str(uuid4())
        async with websockets.connect(
            f"{BASE_URL}{SESSION_ENDPOINT.format(session_id=session_id)}",
            ssl=ssl_context,
        ) as ws:
            await initialize_session(ws)

            image_data = generate_test_image(640, 480)
            video_msg = {
                "header": {"name": "SendHumanVideo", "request_id": str(uuid4())},
                "payload": {
                    "width": 640,
                    "height": 480,
                    "format": "JPEG",
                    "transport": "binary",
                    "binary_size": len(image_data),
                    "segment_num": 1,
                },
            }
            await ws.send(json.dumps(video_msg))
            await ws.send(image_data)
            print(f"✓ 成功上传视频帧，大小 {len(image_data)} 字节")

    @pytest.mark.asyncio
    async def test_05_text_input_and_echo(self):
        session_id = str(uuid4())
        async with websockets.connect(
            f"{BASE_URL}{SESSION_ENDPOINT.format(session_id=session_id)}",
            ssl=ssl_context,
        ) as ws:
            await initialize_session(ws)
            await send_text(ws, "测试文本")

            response = await wait_for_json(ws, "EchoAvatarText", timeout=30.0)
            assert response is not None, "未收到 Avatar 文本回显"
            print(f"✓ 收到 Avatar 文本: {response['payload']['text'][:50]}")

    @pytest.mark.asyncio
    async def test_06_motion_data_output(self):
        session_id = str(uuid4())
        async with websockets.connect(
            f"{BASE_URL}{SESSION_ENDPOINT.format(session_id=session_id)}",
            ssl=ssl_context,
        ) as ws:
            await initialize_session(ws)
            await send_text(ws, "你好")

            # Welcome Message JSON
            welcome_json = await wait_for_json(ws, "MotionDataWelcome", timeout=30.0)
            assert welcome_json is not None, "未收到 Welcome Message JSON"
            
            # Welcome Message 二进制
            welcome_payload = await wait_for_binary(ws, timeout=30.0)
            assert welcome_payload is not None, "未收到 Welcome Message 二进制"
            welcome_parsed = parse_jbin_motion_data(welcome_payload)
            assert welcome_parsed["type"] == "container"

            # MotionData JSON
            motion_json = await wait_for_json(ws, "MotionData", timeout=30.0)
            assert motion_json is not None, "未收到 MotionData JSON"
            print(f"✓ 收到 MotionData JSON: speech_id={motion_json['payload']['speech_id']}")

            # 读取对应的二进制分段（现在分包没有头部，只是纯二进制数据）
            segment_num = motion_json["payload"]["motion_data"]["segment_num"]
            for _ in range(segment_num):
                packet = await wait_for_binary(ws, timeout=5.0)
                assert packet is not None, "未收到 MotionData 二进制"
                assert len(packet) > 0, "MotionData 二进制分段为空"
            print(f"✓ MotionData 二进制分段 {segment_num} 个已接收")

    @pytest.mark.asyncio
    async def test_07_end_speech_handling(self):
        session_id = str(uuid4())
        async with websockets.connect(
            f"{BASE_URL}{SESSION_ENDPOINT.format(session_id=session_id)}",
            ssl=ssl_context,
        ) as ws:
            await initialize_session(ws)
            await send_text(ws, "测试 EndSpeech 流程")

            await wait_for_json(ws, "MotionDataWelcome", timeout=30.0)  # Welcome JSON
            await wait_for_binary(ws, timeout=30.0)  # Welcome 二进制
            motion_json = await wait_for_json(ws, "MotionData", timeout=30.0)
            assert motion_json is not None, "未收到 MotionData JSON"
            speech_id = motion_json["payload"]["speech_id"]

            # 消耗对应二进制分段
            segment_num = motion_json["payload"]["motion_data"]["segment_num"]
            for _ in range(segment_num):
                await wait_for_binary(ws, timeout=5.0)

            end_speech_msg = {
                "header": {"name": "EndSpeech", "request_id": str(uuid4())},
                "payload": {"speech_id": speech_id},
            }
            await ws.send(json.dumps(end_speech_msg))
            print(f"✓ 发送 EndSpeech: {speech_id}")

    @pytest.mark.asyncio
    async def test_08_heartbeat_mechanism(self):
        session_id = str(uuid4())
        async with websockets.connect(
            f"{BASE_URL}{SESSION_ENDPOINT.format(session_id=session_id)}",
            ssl=ssl_context,
        ) as ws:
            await initialize_session(ws)

            heartbeat_msg = {
                "header": {"name": "TriggerHeartbeat", "request_id": str(uuid4())},
            }
            await ws.send(json.dumps(heartbeat_msg))

            response = await wait_for_json(ws, "AvatarHeartbeat", timeout=5.0)
            assert response is not None, "未收到心跳响应"
            print("✓ 心跳机制正常")

    @pytest.mark.asyncio
    async def test_09_interrupt_signal(self):
        session_id = str(uuid4())
        async with websockets.connect(
            f"{BASE_URL}{SESSION_ENDPOINT.format(session_id=session_id)}",
            ssl=ssl_context,
        ) as ws:
            await initialize_session(ws)

            interrupt_msg = {
                "header": {"name": "Interrupt", "request_id": str(uuid4())},
            }
            await ws.send(json.dumps(interrupt_msg))

            response = await wait_for_json(ws, "InterruptAccepted", timeout=5.0)
            assert response is not None, "未收到打断确认"
            print("✓ 打断信号处理正常")

    @pytest.mark.asyncio
    async def test_10_motion_data_audio_capture(self, tmp_path):
        """等待完整 MotionData 并保存音频片段"""
        session_id = str(uuid4())
        async with websockets.connect(
            f"{BASE_URL}{SESSION_ENDPOINT.format(session_id=session_id)}",
            ssl=ssl_context,
        ) as ws:
            await initialize_session(ws)
            await send_text(ws, "测试一次完整的 motion data 音频抓取")

            # Welcome Message JSON
            welcome_json = await wait_for_json(ws, "MotionDataWelcome", timeout=30.0)
            assert welcome_json is not None, "未收到 Welcome Message JSON"
            
            # Welcome Message 二进制
            welcome_payload = await wait_for_binary(ws, timeout=30.0)
            assert welcome_payload is not None, "未收到 Welcome Message 二进制"
            welcome_parsed = parse_jbin_motion_data(welcome_payload)
            assert welcome_parsed["type"] == "container"

            collected_audio_chunks: list[bytes] = []
            finished = False

            while not finished:
                motion_json = await wait_for_json(ws, "MotionData", timeout=30.0)
                assert motion_json is not None, "未收到 MotionData JSON"
                payload = motion_json["payload"]
                segment_meta = payload["motion_data"]
                segment_num = segment_meta["segment_num"]

                # 现在分包没有头部，只是纯二进制数据，按接收顺序组装
                partial_segments: list[bytes] = []
                for _ in range(segment_num):
                    packet = await wait_for_binary(ws, timeout=5.0)
                    assert packet is not None, "未收到 MotionData 二进制"
                    assert len(packet) > 0, "MotionData 二进制分段为空"
                    partial_segments.append(packet)

                if not partial_segments:
                    continue

                # 直接按顺序拼接所有分段
                container_bytes = b"".join(partial_segments)
                container_parsed = parse_jbin_motion_data(container_bytes)
                assert container_parsed["type"] == "container"

                description = container_parsed["description"]["data_records"]
                audio_meta = description.get("audio")
                if audio_meta:
                    offset = audio_meta["data_offset"]
                    samples = audio_meta["shape"][1]
                    bytes_per_sample = 2  # int16
                    audio_chunk = container_parsed["binary_data"][offset: offset + samples * bytes_per_sample]
                    collected_audio_chunks.append(audio_chunk)

                finished = payload.get("end_of_speech", False)

            assert collected_audio_chunks, "未收集到音频数据"

            audio_bytes = b"".join(collected_audio_chunks)
            output_path = tmp_path / "motion_audio.wav"
            with wave.open(str(output_path), "wb") as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(24000)
                wf.writeframes(audio_bytes)

            print(f"✓ MotionData 音频已保存: {output_path}")

    @pytest.mark.asyncio
    async def test_11_multi_connection_broadcast(self):
        """验证监听连接能够收到主连接的回传"""
        session_id = str(uuid4())
        async with websockets.connect(
            f"{BASE_URL}{SESSION_ENDPOINT.format(session_id=session_id)}",
            ssl=ssl_context,
        ) as primary_ws:
            await initialize_session(primary_ws)

            async with websockets.connect(
                f"{BASE_URL}{SESSION_ENDPOINT.format(session_id=session_id)}",
                ssl=ssl_context,
            ) as listener_ws:
                await initialize_session(listener_ws)

                await send_text(primary_ws, "多连接广播测试")

                primary_task = asyncio.create_task(
                    wait_for_json(primary_ws, "EchoAvatarText", timeout=30.0)
                )
                listener_task = asyncio.create_task(
                    wait_for_json(listener_ws, "EchoAvatarText", timeout=30.0)
                )

                primary_msg, listener_msg = await asyncio.gather(primary_task, listener_task)
                assert primary_msg is not None, "主连接未收到 EchoAvatarText"
                assert listener_msg is not None, "监听连接未收到 EchoAvatarText"
                assert (
                    primary_msg["payload"]["speech_id"] == listener_msg["payload"]["speech_id"]
                ), "广播消息 speech_id 不一致"
                print("✓ 监听连接成功收到广播文本")

    @pytest.mark.asyncio
    async def test_12_listener_input_restrictions(self):
        """监听连接只能心跳，发送输入应得到 Error"""
        session_id = str(uuid4())
        async with websockets.connect(
            f"{BASE_URL}{SESSION_ENDPOINT.format(session_id=session_id)}",
            ssl=ssl_context,
        ) as primary_ws:
            await initialize_session(primary_ws)

            async with websockets.connect(
                f"{BASE_URL}{SESSION_ENDPOINT.format(session_id=session_id)}",
                ssl=ssl_context,
            ) as listener_ws:
                await initialize_session(listener_ws)

                # 监听者发送心跳应当得到响应
                heartbeat_msg = {
                    "header": {"name": "TriggerHeartbeat", "request_id": str(uuid4())},
                }
                await listener_ws.send(json.dumps(heartbeat_msg))
                heartbeat_resp = await wait_for_json(listener_ws, "AvatarHeartbeat", timeout=5.0)
                assert heartbeat_resp is not None, "监听者心跳未得到响应"

                # 监听者发送文本应被拒绝
                speech_id = str(uuid4())
                listener_text_msg = {
                    "header": {"name": "SendHumanText", "request_id": str(uuid4())},
                    "payload": {
                        "speech_id": speech_id,
                        "mode": "full_text",
                        "text": "监听者不允许发送",
                        "end_of_speech": True,
                    },
                }
                await listener_ws.send(json.dumps(listener_text_msg))

                error_resp = await wait_for_json(listener_ws, "Error", timeout=5.0)
                assert error_resp is not None, "监听者发送输入未收到错误"
                assert (
                    error_resp.get("payload", {}).get("code") == "INVALID_MESSAGE"
                ), "监听者输入错误码不正确"
                print("✓ 监听连接输入受限逻辑正常")

    @pytest.mark.asyncio
    async def test_13_listener_motion_audio_capture(self, tmp_path):
        """监听连接保存 MotionData 音频片段"""
        session_id = str(uuid4())
        async with websockets.connect(
            f"{BASE_URL}{SESSION_ENDPOINT.format(session_id=session_id)}",
            ssl=ssl_context,
        ) as primary_ws:
            await initialize_session(primary_ws)

            async with websockets.connect(
                f"{BASE_URL}{SESSION_ENDPOINT.format(session_id=session_id)}",
                ssl=ssl_context,
            ) as listener_ws:
                await initialize_session(listener_ws)

                await send_text(primary_ws, "监听者抓取 MotionData 音频")

                # Welcome Message JSON
                welcome_json = await wait_for_json(listener_ws, "MotionDataWelcome", timeout=30.0)
                assert welcome_json is not None, "监听者未收到 Welcome Message JSON"
                
                # Welcome Message 二进制
                welcome_payload = await wait_for_binary(listener_ws, timeout=30.0)
                assert welcome_payload is not None, "监听者未收到 Welcome Message 二进制"
                welcome_parsed = parse_jbin_motion_data(welcome_payload)
                assert welcome_parsed["type"] == "container"

                collected_audio_chunks: list[bytes] = []
                finished = False

                while not finished:
                    motion_json = await wait_for_json(listener_ws, "MotionData", timeout=30.0)
                    assert motion_json is not None, "监听者未收到 MotionData JSON"
                    payload = motion_json["payload"]
                    segment_meta = payload["motion_data"]
                    segment_num = segment_meta["segment_num"]

                    # 现在分包没有头部，只是纯二进制数据，按接收顺序组装
                    partial_segments: list[bytes] = []
                    for _ in range(segment_num):
                        packet = await wait_for_binary(listener_ws, timeout=5.0)
                        assert packet is not None, "监听者未收到 MotionData 二进制"
                        assert len(packet) > 0, "MotionData 二进制分段为空"
                        partial_segments.append(packet)

                    if not partial_segments:
                        continue

                    # 直接按顺序拼接所有分段
                    container_bytes = b"".join(partial_segments)
                    container_parsed = parse_jbin_motion_data(container_bytes)
                    assert container_parsed["type"] == "container"

                    description = container_parsed["description"]["data_records"]
                    audio_meta = description.get("audio")
                    if audio_meta:
                        offset = audio_meta["data_offset"]
                        samples = audio_meta["shape"][1]
                        bytes_per_sample = 2  # int16
                        audio_chunk = container_parsed["binary_data"][offset: offset + samples * bytes_per_sample]
                        collected_audio_chunks.append(audio_chunk)

                    finished = payload.get("end_of_speech", False)

                assert collected_audio_chunks, "监听者未收集到音频数据"

                audio_bytes = b"".join(collected_audio_chunks)
                output_path = tmp_path / "listener_motion_audio.wav"
                with wave.open(str(output_path), "wb") as wf:
                    wf.setnchannels(1)
                    wf.setsampwidth(2)
                    wf.setframerate(24000)
                    wf.writeframes(audio_bytes)

                print(f"✓ 监听者 MotionData 音频已保存: {output_path}")
