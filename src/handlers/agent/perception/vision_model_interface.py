"""
视觉模型抽象接口

定义视觉模型需要实现的接口，支持后续替换不同模型
"""
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor, Future
from typing import Any, Callable, Dict, List, Optional
import base64
import os
import re
import threading
import time

import cv2
from loguru import logger
import numpy as np

from handlers.agent.agent_data_models import PerceptionData, EnvironmentEvent


class AsyncPerceptionManager:
    """
    异步感知任务管理器
    
    使用线程池并发处理 LLM 请求，采用"最新优先"策略：
    - 如果有更新的轮次已经发送，则跳过旧轮次（避免阻塞）
    - 结果立即发送，不等待前序轮次
    """
    
    def __init__(
        self,
        vision_model: "VisionModelInterface",
        max_workers: int = 3,
        on_result_callback: Optional[Callable[[int, Optional[PerceptionData]], None]] = None,
    ):
        """
        初始化异步管理器
        
        Args:
            vision_model: 视觉模型实例
            max_workers: 最大并发工作线程数
            on_result_callback: 结果回调函数，参数为 (round_id, perception_data)
        """
        self.vision_model = vision_model
        self.max_workers = max_workers
        self.on_result_callback = on_result_callback
        
        # 线程池
        self.executor = ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix="perception_worker")
        
        # 最新优先策略：记录已发送的最大轮次
        self.last_sent_round: int = 0  # 已发送的最大 round_id
        self.send_lock = threading.Lock()
        
        # 正在进行的任务
        self.pending_futures: Dict[int, Future] = {}
        self.pending_lock = threading.Lock()
        
        # 统计信息
        self.total_submitted: int = 0
        self.total_completed: int = 0
        self.total_skipped: int = 0
        self.total_outdated: int = 0  # 因过时而跳过的轮次
        
        # 运行状态
        self._running = True
        
        logger.info(f"[AsyncPerceptionManager] 初始化完成: max_workers={max_workers}, 策略: 最新优先")
    
    @property
    def current_pending_count(self) -> int:
        """当前正在进行的任务数"""
        with self.pending_lock:
            return len(self.pending_futures)
    
    def submit_task(self, round_id: int, frames: List[np.ndarray]) -> bool:
        """
        提交异步感知任务
        
        Args:
            round_id: 感知轮次 ID
            frames: 视频帧列表
            
        Returns:
            bool: 是否成功提交（如果达到并发上限则返回 False）
        """
        if not self._running:
            logger.warning(f"[AsyncPerceptionManager] [Round-{round_id}] 管理器已停止，拒绝提交任务")
            return False
        
        with self.pending_lock:
            pending_count = len(self.pending_futures)
            
            # 检查并发上限
            if pending_count >= self.max_workers:
                logger.warning(
                    f"[AsyncPerceptionManager] [Round-{round_id}] ⚠️ 达到并发上限 ({pending_count}/{self.max_workers})，跳过本轮"
                )
                self.total_skipped += 1
                return False
            
            # 提交任务到线程池
            future = self.executor.submit(self._worker, round_id, frames)
            self.pending_futures[round_id] = future
            self.total_submitted += 1
            
            logger.info(
                f"[AsyncPerceptionManager] [Round-{round_id}] 📤 提交异步任务 "
                f"(当前并发: {pending_count + 1}/{self.max_workers}, 帧数: {len(frames)})"
            )
            
            # 添加完成回调
            future.add_done_callback(lambda f: self._on_future_done(round_id, f))
            
            return True
    
    def _worker(self, round_id: int, frames: List[np.ndarray]) -> Optional[PerceptionData]:
        """
        工作线程：执行 API 调用
        
        Args:
            round_id: 感知轮次 ID
            frames: 视频帧列表
            
        Returns:
            Optional[PerceptionData]: 感知数据或 None
        """
        try:
            logger.debug(f"[AsyncPerceptionManager] [Round-{round_id}] 工作线程开始执行")
            result = self.vision_model.generate_perception(frames, round_id=round_id)
            return result
        except Exception as e:
            logger.error(f"[AsyncPerceptionManager] [Round-{round_id}] 工作线程异常: {e}")
            return None
    
    def _on_future_done(self, round_id: int, future: Future):
        """
        Future 完成回调
        
        Args:
            round_id: 感知轮次 ID
            future: 完成的 Future 对象
        """
        # 从 pending 中移除
        with self.pending_lock:
            self.pending_futures.pop(round_id, None)
        
        # 获取结果
        try:
            result = future.result()
        except Exception as e:
            logger.error(f"[AsyncPerceptionManager] [Round-{round_id}] 获取结果异常: {e}")
            result = None
        
        self.total_completed += 1
        
        # 处理结果（最新优先策略）
        self._handle_result(round_id, result)
    
    def _handle_result(self, round_id: int, result: Optional[PerceptionData]):
        """
        处理结果：最新优先策略
        
        - 如果 round_id <= last_sent_round：跳过（已有更新的结果发送）
        - 否则：立即发送并更新 last_sent_round
        
        Args:
            round_id: 感知轮次 ID
            result: 感知数据
        """
        with self.send_lock:
            # 检查是否已过时
            if round_id <= self.last_sent_round:
                self.total_outdated += 1
                logger.info(
                    f"[AsyncPerceptionManager] [Round-{round_id}] ⏭️ 跳过过时结果 "
                    f"(已发送: Round-{self.last_sent_round})"
                )
                return
            
            # 结果为空也需要更新 last_sent_round，防止旧轮次覆盖
            if result is None:
                logger.info(f"[AsyncPerceptionManager] [Round-{round_id}] ⚠️ 结果为空，但更新轮次标记")
                self.last_sent_round = round_id
                return
            
            # 立即发送结果
            logger.info(
                f"[AsyncPerceptionManager] [Round-{round_id}] ✅ API 完成，"
                f"上次发送: Round-{self.last_sent_round}"
            )
            
            if self.on_result_callback:
                try:
                    logger.info(f"[AsyncPerceptionManager] [Round-{round_id}] 📤 立即发送结果到 Manager")
                    self.on_result_callback(round_id, result)
                except Exception as e:
                    logger.error(f"[AsyncPerceptionManager] [Round-{round_id}] 回调执行异常: {e}")
            
            # 更新已发送的最大轮次
            self.last_sent_round = round_id
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        with self.pending_lock:
            pending = len(self.pending_futures)
        
        return {
            "total_submitted": self.total_submitted,
            "total_completed": self.total_completed,
            "total_skipped": self.total_skipped,
            "total_outdated": self.total_outdated,
            "current_pending": pending,
            "last_sent_round": self.last_sent_round,
        }
    
    def shutdown(self, wait: bool = True, timeout: float = 5.0):
        """
        关闭管理器
        
        Args:
            wait: 是否等待所有任务完成
            timeout: 等待超时时间（秒），超时后强制取消
        """
        self._running = False
        
        stats = self.get_stats()
        logger.info(
            f"[AsyncPerceptionManager] 关闭中... "
            f"(submitted: {stats['total_submitted']}, "
            f"completed: {stats['total_completed']}, "
            f"skipped: {stats['total_skipped']}, "
            f"outdated: {stats['total_outdated']}, "
            f"pending: {stats['current_pending']})"
        )
        
        # 取消所有挂起的任务
        with self.pending_lock:
            for round_id, future in list(self.pending_futures.items()):
                if not future.done():
                    future.cancel()
                    logger.debug(f"[AsyncPerceptionManager] 取消挂起任务: Round-{round_id}")
        
        # 不等待，直接关闭（避免卡住）
        self.executor.shutdown(wait=False, cancel_futures=True)
        logger.info("[AsyncPerceptionManager] 已关闭")


class VisionModelInterface(ABC):
    """
    视觉模型抽象接口
    
    子类需要实现具体的视觉理解能力
    """
    
    @abstractmethod
    def generate_perception(self, frames: List[np.ndarray], round_id: int = 0) -> Optional[PerceptionData]:
        """
        生成分层视觉感知数据
        
        Args:
            frames: 视频帧列表 (BGR 格式)
            round_id: 感知轮次 ID，用于日志追踪
            
        Returns:
            PerceptionData: 成功时返回分层视觉上下文
            None: 失败时返回 None
        """
        pass
    
    @abstractmethod
    def detect_events(self, frame: np.ndarray, 
                     previous_frame: Optional[np.ndarray] = None) -> List[EnvironmentEvent]:
        """
        检测环境事件
        
        Args:
            frame: 当前帧 (BGR 格式)
            previous_frame: 上一帧 (用于检测变化)
            
        Returns:
            List[EnvironmentEvent]: 检测到的事件列表
        """
        pass
    
    def warmup(self):
        """预热模型 (可选)"""
        pass
    
    def cleanup(self):
        """清理资源 (可选)"""
        pass


class MockVisionModel(VisionModelInterface):
    """
    Mock 视觉模型，用于测试
    
    返回固定的感知数据，不进行实际的视觉理解
    """
    
    def __init__(self):
        self._frame_count = 0
    
    def generate_perception(self, frames: List[np.ndarray], round_id: int = 0) -> PerceptionData:
        """返回 mock 感知数据"""
        import time
        from handlers.agent.agent_data_models import SceneStructure, UserState
        
        self._frame_count += len(frames)
        logger.info(f"[MockVisionModel] [Round-{round_id}] 生成 Mock 感知数据 (帧数: {len(frames)})")
        
        return PerceptionData(
            scene_summary="我看到用户正坐在电脑前",
            scene_structure=SceneStructure(
                location="办公室",
                people=["用户"],
                objects=["电脑", "键盘", "鼠标"],
                activities=["工作"],
            ),
            user_state=UserState(
                emotion="neutral",
                gaze="screen",
                posture="sitting",
                action="typing",
            ),
            timestamp=time.time(),
        )
    
    def detect_events(self, frame: np.ndarray,
                     previous_frame: Optional[np.ndarray] = None) -> List[EnvironmentEvent]:
        """Mock 事件检测，不返回任何事件"""
        return []


class OpenAIVisionModel(VisionModelInterface):
    """
    OpenAI 兼容接口视觉模型 (如 qwen-plus-vl)
    """

    DEFAULT_SYSTEM_PROMPT = """你是一个具身智能体的视觉感知系统。你正在通过摄像头实时观察用户。

重要视角说明：
- 你的视角是摄像头视角，用户正面对着你
- 你收到的是一段实时视频流的关键帧序列，展示了最近几秒内用户的状态变化
- 当你看到一个人举着手机对着画面时，这表示用户正在向你展示手机，而不是在自拍
- 当你看到一个人做某个动作时，描述为"用户正在做..."，而不是"视频中有人在做..."
- 请综合分析整段视频，描述用户当前的状态和正在进行的活动

请以第一人称视角描述你观察到的内容，严格使用以下 XML 标签格式输出（只输出标签，不要输出任何其他内容）：

<scene_summary>一句话描述你当前观察到的场景（使用"我看到用户..."的表述）</scene_summary>
<location>场景位置（办公室/家/户外等）</location>
<people>可见的人物，逗号分隔（如：用户, 背景中的同事）</people>
<objects>可见的物品，逗号分隔（如：笔记本电脑, 手机, 水杯）</objects>
<activities>正在进行的活动，逗号分隔（如：用户在打字, 同事在讨论）</activities>
<emotion>用户情绪（focused/happy/confused/sad/angry/surprised/neutral）</emotion>
<gaze>用户视线方向（looking_at_camera/looking_away/looking_down/looking_at_screen）</gaze>
<posture>用户姿态（sitting/standing/leaning/lying）</posture>
<action>用户当前动作（speaking/typing/holding_phone/gesturing/idle/reading）</action>
<events></events>

交互事件检测规则（events 标签）：
- 仅当检测到用户有明确的交互意图时才在 events 内输出事件，否则保持 <events></events> 为空
- 有事件时的格式：
<events>
<event type="事件类型" confidence="0.8">事件描述</event>
</events>
- confidence 取值 0.0-1.0，只有 >= 0.7 的事件才会被处理
- 事件类型说明：
  * waving: 用户举手挥动，表示打招呼或想吸引你的注意
  * showing_object: 用户主动将某物品举向摄像头展示
  * asking_for_attention: 用户做出明显想引起注意的动作（如敲桌子、招手、大幅度挥手）
  * leaving: 用户正在离开画面
  * arriving: 有新的人进入画面

重要提示：
- 普通的手部动作（如打字、摸脸）不算 waving
- 只有用户明显向摄像头方向挥手时才算 waving
- 如果没有检测到任何交互事件，events 标签应为空：<events></events>"""

    def __init__(
        self,
        model_name: str = "qwen-plus-vl",
        api_key: Optional[str] = None,
        api_url: Optional[str] = None,
        max_frames: int = 4,
        system_prompt: Optional[str] = None,
    ):
        self.model_name = model_name
        self.api_key = api_key or os.getenv("DASHSCOPE_API_KEY")
        self.api_url = api_url
        self.max_frames = max_frames
        self._system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT

        self._client = None
        # API 调用超时时间（秒）
        self.api_timeout = 6.0
        try:
            from openai import OpenAI
            import httpx

            # 设置 API 超时 (连接超时 5s, 读取超时 6s)
            self._client = OpenAI(
                api_key=self.api_key,
                base_url=self.api_url,
                timeout=httpx.Timeout(self.api_timeout, connect=5.0),
            )
        except Exception:
            self._client = None

    # 视频模式最少需要的帧数 (阿里云 qwen-vl 要求 4-2000 帧)
    MIN_VIDEO_FRAMES = 4

    def generate_perception(self, frames: List[np.ndarray], round_id: int = 0, debug_save: bool = True) -> Optional[PerceptionData]:
        """
        生成感知数据
        
        Args:
            frames: 视频帧列表
            round_id: 感知轮次 ID，用于日志追踪
            debug_save: 是否保存调试图片
            
        Returns:
            PerceptionData: 成功时返回感知数据
            None: 失败时返回 None，调用方应保留之前的缓存
        """
        round_tag = f"[Round-{round_id}]"
        
        if not frames:
            logger.warning(f"[OpenAI Vision Model] {round_tag} No frames provided")
            return None

        if self._client is None:
            logger.warning(f"[OpenAI Vision Model] {round_tag} Client is None")
            return None

        selected_frames = self._select_frames(frames, self.max_frames)
        
        messages, valid_images = self._build_messages(selected_frames, round_id=round_id, debug_save=debug_save)
        if valid_images == 0:
            logger.warning(f"[OpenAI Vision Model] {round_tag} No valid images to send after processing")
            return None

        try:
            time_start = time.time()
            logger.info(f"[OpenAI Vision Model] {round_tag} 🚀 开始 API 调用 (超时: {self.api_timeout}s)...")
            response = self._client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                stream=False,
                max_tokens=600,
                timeout=self.api_timeout,
            )
            time_end = time.time()
            logger.info(f"[OpenAI Vision Model] {round_tag} ✅ API 调用完成，耗时: {time_end - time_start:.2f}s")
        except Exception as exc:
            time_end = time.time()
            elapsed = time_end - time_start
            if elapsed >= self.api_timeout - 0.5:
                logger.warning(f"[OpenAI Vision Model] {round_tag} ⏱️ API 调用超时 ({elapsed:.2f}s >= {self.api_timeout}s)，跳过本轮")
            else:
                logger.warning(f"[OpenAI Vision Model] {round_tag} API call failed ({elapsed:.2f}s): {exc}")
            return None

        content = ""
        if response and response.choices:
            raw_content = response.choices[0].message.content
            if isinstance(raw_content, list):
                parts = []
                for item in raw_content:
                    if isinstance(item, dict):
                        parts.append(str(item.get("text", "")))
                    else:
                        parts.append(str(item))
                content = "".join(parts).strip()
            else:
                content = (raw_content or "").strip()

        logger.info(f"[OpenAI Vision Model] {round_tag} 📝 Response: {content}")
        parsed = self._parse_xml_response(content)
        if not parsed or not parsed.get("scene_summary"):
            logger.warning(f"[OpenAI Vision Model] {round_tag} Empty/invalid XML response, returning None")
            return None
        parsed["timestamp"] = time.time()
        return PerceptionData.from_dict(parsed)
    def detect_events(self, frame: np.ndarray,
                     previous_frame: Optional[np.ndarray] = None) -> List[EnvironmentEvent]:
        return []

    def _select_frames(self, frames: List[np.ndarray], max_frames: int) -> List[np.ndarray]:
        if max_frames <= 0 or len(frames) <= max_frames:
            return frames
        step = max(1, len(frames) // max_frames)
        selected = frames[::step][:max_frames]
        return selected

    def _build_messages(self, frames: List[np.ndarray], round_id: int = 0, debug_save: bool = False) -> tuple[List[Dict[str, Any]], int]:
        round_tag = f"[Round-{round_id}]"
        
        system_prompt = self._system_prompt

        # 收集所有有效帧的 data URL
        video_frames: List[str] = []
        for frame in frames:
            data_url = self._frame_to_data_url(frame, debug_save_path=None)
            if data_url:
                video_frames.append(data_url)
        
        original_count = len(video_frames)
        
        if original_count == 0:
            logger.warning(f"[OpenAI Vision Model] {round_tag} No valid frames to build video content")
            return [], 0
        
        # 视频模式要求至少 MIN_VIDEO_FRAMES 帧，不足时通过重复帧来补足
        if original_count < self.MIN_VIDEO_FRAMES:
            logger.info(f"[OpenAI Vision Model] {round_tag} Padding frames: {original_count} -> {self.MIN_VIDEO_FRAMES} (repeating frames)")
            # 循环重复帧直到达到最小数量
            while len(video_frames) < self.MIN_VIDEO_FRAMES:
                video_frames.append(video_frames[len(video_frames) % original_count])
        
        valid_images = len(video_frames)
        
        # 使用视频格式：将图片列表作为视频传入
        content: List[Dict[str, Any]] = [
            {
                "type": "video",
                "video": video_frames,
            },
            {
                "type": "text",
                "text": "请根据这段实时摄像头视频，描述你观察到的用户状态和场景。"
            }
        ]
        
        logger.info(f"[OpenAI Vision Model] {round_tag} 📹 构建视频消息: {valid_images} 帧 (原始: {original_count})")

        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": content},
        ], valid_images

    def _frame_to_data_url(self, frame: np.ndarray, debug_save_path: Optional[str] = None) -> Optional[str]:
        """
        将视频帧转换为 data URL (直接使用项目的 ImageUtils)
        """
        try:
            from engine_utils.media_utils import ImageUtils
            
            if not isinstance(frame, np.ndarray):
                logger.warning(f"[OpenAI Vision Model] Frame is not np.ndarray, type: {type(frame)}")
                return None
            
            if frame.size == 0:
                logger.warning("[OpenAI Vision Model] Frame size is 0")
                return None
            
            # 调试：保存处理后的图片到本地
            if debug_save_path:
                try:
                    debug_dir = os.path.dirname(debug_save_path)
                    if debug_dir:
                        os.makedirs(debug_dir, exist_ok=True)
                    # 使用 ImageUtils 的方式保存
                    data_url = ImageUtils.format_image(frame)
                    ImageUtils.save_base64_image(data_url, debug_save_path)
                    logger.info(f"[OpenAI Vision Model] Debug: saved frame to {debug_save_path}")
                except Exception as save_exc:
                    logger.warning(f"[OpenAI Vision Model] Failed to save debug frame: {save_exc}")

            # 直接使用 ImageUtils.format_image，与 llm_handler_openai_compatible 一致
            return ImageUtils.format_image(frame)
            
        except Exception as exc:
            logger.warning(f"Failed to encode frame: {exc}")
            import traceback
            logger.warning(traceback.format_exc())
            return None

    def _parse_xml_response(self, content: str) -> Dict[str, Any]:
        """从 XML 标签化的 VLM 输出中提取感知数据。

        每个标签只取第一次出现，天然容错：即使 LLM 重复生成某个标签，
        后续重复内容会被忽略。
        """
        if not content:
            return {}

        def _extract_tag(text: str, tag: str) -> str:
            m = re.search(rf'<{tag}[^>]*>(.*?)</{tag}>', text, re.DOTALL)
            return m.group(1).strip() if m else ""

        def _extract_list(text: str, tag: str) -> List[str]:
            raw = _extract_tag(text, tag)
            if not raw:
                return []
            return [item.strip() for item in raw.split(",") if item.strip()]

        scene_summary = _extract_tag(content, "scene_summary")
        if not scene_summary:
            return {}

        detected_events: List[Dict[str, Any]] = []
        events_block = _extract_tag(content, "events")
        if events_block:
            for m in re.finditer(
                r'<event\s+type="([^"]*?)"\s+confidence="([^"]*?)">(.*?)</event>',
                events_block, re.DOTALL,
            ):
                try:
                    conf = float(m.group(2))
                except (ValueError, TypeError):
                    conf = 0.0
                detected_events.append({
                    "event_type": m.group(1),
                    "confidence": conf,
                    "description": m.group(3).strip(),
                })

        return {
            "scene_summary": scene_summary,
            "scene_structure": {
                "location": _extract_tag(content, "location"),
                "people": _extract_list(content, "people"),
                "objects": _extract_list(content, "objects"),
                "activities": _extract_list(content, "activities"),
            },
            "user_state": {
                "emotion": _extract_tag(content, "emotion"),
                "gaze": _extract_tag(content, "gaze"),
                "posture": _extract_tag(content, "posture"),
                "action": _extract_tag(content, "action"),
            },
            "detected_events": detected_events,
        }
