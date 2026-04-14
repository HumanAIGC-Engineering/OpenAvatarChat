import weakref
import time
from dataclasses import dataclass
from typing import Dict, Tuple, Optional, List, Callable, Union, Any

import numpy as np
from loguru import logger

from chat_engine.contexts.session_clock import SessionClock

from chat_engine.data_models.internal.handler_definition_data import ChatDataConsumeMode, HandlerDataInfo

from chat_engine.data_models.runtime_data.data_bundle import DataBundleDefinition, DataBundle
from chat_engine.data_models.chat_data.chat_data_model import ChatData, StreamableData
from chat_engine.data_models.chat_data_type import ChatDataType
from chat_engine.data_models.chat_signal import ChatSignal
from chat_engine.data_models.chat_signal_type import ChatSignalType
from chat_engine.data_models.chat_stream import ChatStreamIdentity, StreamKey
from chat_engine.data_models.chat_stream_config import ChatStreamConfig
from chat_engine.data_models.chat_stream_status import ChatStreamStatus
from chat_engine.core.signal_manager import SignalEmitter, SignalManager


@dataclass
class StreamDebugConfig:
    """Global configuration for stream lifecycle debug logging."""
    enabled: bool = False

    # Visual symbols for different events
    SYMBOLS = {
        'create': '🆕',
        'start': '▶️',
        'finish': '✅',
        'cancel': '❌',
        'recycle': '🗑️',
        'ref_add': '🔗',
        'ref_remove': '💔',
        'cancel_chain': '⛓️',
        'arrow': '→',
        'tree_branch': '├──',
        'tree_last': '└──',
        'tree_vertical': '│  ',
    }

    def log(self, message: str):
        if self.enabled:
            logger.info(message)

    def log_create(self, stream: "ChatStream"):
        """Log stream creation with visual dependency tree."""
        if not self.enabled:
            return
        sym = self.SYMBOLS
        lines = [
            f"{sym['create']} STREAM CREATED: {stream.identity}",
            f"   ┌─ cancelable: {stream.config.cancelable}",
        ]
        
        # Parents section
        parents = list(stream.source_streams.values())
        if parents:
            lines.append(f"   ├─ parents ({len(parents)}):")
            for i, p in enumerate(parents):
                prefix = sym['tree_last'] if i == len(parents) - 1 else sym['tree_branch']
                lines.append(f"   │  {prefix} {p}")
        else:
            lines.append(f"   ├─ parents: (none)")
        
        # Ancestors section (excluding parents)
        ancestors_only = [a for a in stream.ancestor_streams if a.key not in stream.source_streams]
        if ancestors_only:
            lines.append(f"   ├─ ancestors ({len(ancestors_only)}):")
            for i, a in enumerate(ancestors_only):
                prefix = sym['tree_last'] if i == len(ancestors_only) - 1 else sym['tree_branch']
                lines.append(f"   │  {prefix} {a}")
        
        # Cancelable ancestors section
        if stream.cancelable_ancestors:
            lines.append(f"   └─ cancelable chain ({len(stream.cancelable_ancestors)}):")
            for i, c in enumerate(stream.cancelable_ancestors):
                prefix = sym['tree_last'] if i == len(stream.cancelable_ancestors) - 1 else sym['tree_branch']
                lines.append(f"      {prefix} {c}")
        else:
            lines.append(f"   └─ cancelable chain: (none)")
        
        logger.info("\n".join(lines))

    def log_start(self, stream: "ChatStream", timestamp):
        """Log stream start."""
        if not self.enabled:
            return
        logger.info(f"{self.SYMBOLS['start']} STREAM STARTED: {stream.identity} @ {timestamp}")

    def log_finish(self, stream: "ChatStream", prev_status, ref_by_list: list):
        """Log stream finish."""
        if not self.enabled:
            return
        ref_info = f"ref_by=[{', '.join(ref_by_list)}]" if ref_by_list else "ref_by=(none)"
        logger.info(
            f"{self.SYMBOLS['finish']} STREAM FINISHED: {stream.identity} | "
            f"{prev_status.name} {self.SYMBOLS['arrow']} ENDED | {ref_info}"
        )

    def log_cancel(self, stream: "ChatStream", prev_status, ref_by_list: list):
        """Log stream cancel."""
        if not self.enabled:
            return
        ref_info = f"ref_by=[{', '.join(ref_by_list)}]" if ref_by_list else "ref_by=(none)"
        logger.warning(
            f"{self.SYMBOLS['cancel']} STREAM CANCELLED: {stream.identity} | "
            f"{prev_status.name} {self.SYMBOLS['arrow']} CANCELLED | {ref_info}"
        )

    def log_recycle(self, stream: "ChatStream", ttl: float):
        """Log stream recycle."""
        if not self.enabled:
            return
        logger.info(
            f"{self.SYMBOLS['recycle']} STREAM RECYCLED: {stream.identity} | "
            f"status={stream.status.name} | lived {ttl}s after finish"
        )

    def log_ref_add(self, refer_by, refer_to, ref_count: int):
        """Log reference added."""
        if not self.enabled:
            return
        logger.info(
            f"{self.SYMBOLS['ref_add']} REF ADD: {refer_by} {self.SYMBOLS['arrow']} {refer_to} | "
            f"ref_count={ref_count}"
        )

    def log_ref_remove(self, refer_by, refer_to, ref_count: int):
        """Log reference removed."""
        if not self.enabled:
            return
        logger.info(
            f"{self.SYMBOLS['ref_remove']} REF REMOVE: {refer_by} {self.SYMBOLS['arrow']} {refer_to} | "
            f"ref_count={ref_count}"
        )

    def log_cancel_chain_start(self, stream: "ChatStream"):
        """Log cancel chain start."""
        if not self.enabled:
            return
        sym = self.SYMBOLS
        lines = [
            f"{sym['cancel_chain']} CANCEL CHAIN INITIATED from: {stream.identity}",
        ]
        if stream.cancelable_ancestors:
            lines.append(f"   targets ({len(stream.cancelable_ancestors)}):")
            for i, c in enumerate(stream.cancelable_ancestors):
                prefix = sym['tree_last'] if i == len(stream.cancelable_ancestors) - 1 else sym['tree_branch']
                lines.append(f"   {prefix} {c}")
        else:
            lines.append(f"   targets: (none)")
        logger.info("\n".join(lines))

    def log_cancel_chain_complete(self, cancelled: list):
        """Log cancel chain completion."""
        if not self.enabled:
            return
        sym = self.SYMBOLS
        if cancelled:
            cancelled_str = ", ".join(str(c) for c in cancelled)
            logger.info(f"{sym['cancel_chain']} CANCEL CHAIN COMPLETE: cancelled {len(cancelled)} streams [{cancelled_str}]")
        else:
            logger.info(f"{sym['cancel_chain']} CANCEL CHAIN COMPLETE: no streams cancelled")


# Global debug config instance - can be enabled/disabled at runtime
stream_debug = StreamDebugConfig()


@dataclass
class InputStreamStats:
    stream_id: ChatStreamIdentity
    start_time: Optional[Tuple[int, int]] = None
    # Keep track of when the upstream stream ended so we can retain it briefly
    # for downstream ref_streams discovery.
    end_mark: Optional[float] = None


class ChatStream:
    def __init__(self, identity: ChatStreamIdentity,
                 storage: "StreamStorage",
                 config: ChatStreamConfig,
                 source_streams: Optional[List[ChatStreamIdentity]] = None,
                 remove_callback: Optional[Callable[["ChatStream"], None]] = None,
                 signal_emitter: Optional[SignalEmitter] = None):
        self.config: ChatStreamConfig = config
        self.identity: ChatStreamIdentity = identity
        self.status: ChatStreamStatus = ChatStreamStatus.NOT_STARTED
        self.start_time: Optional[Tuple[int, int]] = None
        self.end_time: Optional[Tuple[int, int]] = None
        # Direct parent streams (immediate sources) - dict for fast lookup
        self.source_streams: Dict[StreamKey, ChatStreamIdentity] = {}
        # All ancestor streams in dependency order (parents first, then grandparents, etc.)
        # This is an ordered list for proper interrupt propagation
        self.ancestor_streams: List[ChatStreamIdentity] = []
        # Cancelable ancestors (excludes non-cancelable streams like client audio/video input)
        # Determined at creation time, static and ordered (parents first)
        self.cancelable_ancestors: List[ChatStreamIdentity] = []
        self.ref_by: Dict[StreamKey, ChatStreamIdentity] = {}
        self.weak_storage: weakref.ReferenceType["StreamStorage"] = weakref.ref(storage)
        self.remove_callback: Optional[Callable[["ChatStream"], None]] = remove_callback
        self._signal_emitter = signal_emitter
        self._metadata: Dict[str, Any] = {}
        self._inheritable_metadata: Dict[str, Any] = {}  # Metadata that will be inherited by child streams
        self._should_cancel_on_create: bool = False  # Flag for deferred cancel
        if source_streams is not None:
            seen_keys = set()
            for source_stream in source_streams:
                stream_key = source_stream.key
                if stream_key in seen_keys:
                    continue
                seen_keys.add(stream_key)
                self.source_streams[stream_key] = source_stream
                self.ancestor_streams.append(source_stream)
                # Check if parent is cancelled - if so, we should cancel ourselves
                parent_valid = storage.ref_stream(self.identity, source_stream)
                if not parent_valid:
                    self._should_cancel_on_create = True
            # Collect ancestors from parent streams and build cancelable list
            self._collect_ancestors_and_cancelable(storage, seen_keys)
            # Inherit inheritable metadata from parent streams
            self._inherit_metadata_from_parents(storage)
        
        # Debug logging for stream creation
        self._log_creation()
        
        # If any parent was cancelled, cancel this stream immediately after creation
        if self._should_cancel_on_create and self.config.cancelable:
            logger.info(f"Auto-cancelling stream {self.identity} due to cancelled parent")
            self.cancel(storage)

    def _log_creation(self):
        """Log stream creation with dependency information."""
        stream_debug.log_create(self)

    def _collect_ancestors_and_cancelable(self, storage: "StreamStorage", seen_keys: set):
        """
        Collect all ancestor streams from parent streams and build the cancelable ancestors list.
        Both lists maintain dependency order: direct parents first, then their ancestors.
        """
        # First, add ancestors from all parent streams (in order)
        for source_id in list(self.source_streams.values()):
            parent_stream = storage.find_stream(source_id)
            if parent_stream is None:
                continue
            # Add parent's ancestors (already ordered in parent)
            for ancestor_id in parent_stream.ancestor_streams:
                if ancestor_id.key not in seen_keys:
                    seen_keys.add(ancestor_id.key)
                    self.ancestor_streams.append(ancestor_id)

        # Now build cancelable_ancestors from ancestor_streams (preserving order)
        for ancestor_id in self.ancestor_streams:
            ancestor_stream = storage.find_stream(ancestor_id)
            if ancestor_stream is not None and ancestor_stream.config.cancelable:
                self.cancelable_ancestors.append(ancestor_id)

    def _inherit_metadata_from_parents(self, storage: "StreamStorage"):
        """
        Inherit inheritable metadata from parent streams.
        If multiple parents have the same inheritable metadata key, the first parent's value takes precedence.
        """
        for source_id in list(self.source_streams.values()):
            parent_stream = storage.find_stream(source_id)
            if parent_stream is None:
                continue
            # Inherit from parent's inheritable_metadata
            for key, value in parent_stream._inheritable_metadata.items():
                if key not in self._inheritable_metadata:
                    # Only inherit if not already set (first parent wins)
                    self._inheritable_metadata[key] = value
                    # Also add to regular metadata for easy access
                    self._metadata[key] = value

    def cancel_with_ancestors(self, storage: "StreamStorage") -> List[ChatStreamIdentity]:
        """
        Cancel this stream and all its cancelable ancestors.
        Returns list of cancelled stream identities.
        Cancels from root to leaf order for cleaner signal propagation.
        """
        stream_debug.log_cancel_chain_start(self)
        cancelled = []
        # Cancel ancestors from root to leaf (reverse of dependency order)
        for ancestor_id in reversed(self.cancelable_ancestors):
            ancestor_stream = storage.find_stream(ancestor_id)
            if ancestor_stream is not None:
                if ancestor_stream.status in (ChatStreamStatus.NOT_STARTED, ChatStreamStatus.STARTED):
                    if ancestor_stream.cancel(storage):
                        cancelled.append(ancestor_id)
        # Cancel self if cancelable
        if self.config.cancelable:
            if self.cancel(storage):
                cancelled.append(self.identity)
        stream_debug.log_cancel_chain_complete(cancelled)
        return cancelled

    def __del__(self):
        storage = self.weak_storage()
        if storage is None:
            return
        for source_stream in self.source_streams.values():
            storage.unref_stream(self.identity, source_stream)

    def cancel(self, storage: "StreamStorage"):
        # 已经 cancel 的不能重复 cancel
        if self.status == ChatStreamStatus.CANCELLED:
            return False
        # 允许 cancel 任何非 CANCELLED 状态的 stream
        # 即使 ENDED 且无下游引用，也需要发送 STREAM_CANCEL 信号
        # 因为可能有 handler 正在处理这个 stream（如 LLM 正在处理 HUMAN_TEXT）
        prev_status = self.status
        self.status = ChatStreamStatus.CANCELLED
        ref_by_list = [str(sid) for sid in self.ref_by.values()]
        stream_debug.log_cancel(self, prev_status, ref_by_list)
        stream_cancel_signal = ChatSignal(
            type=ChatSignalType.STREAM_CANCEL,
            source_type=self.config.source_type,
            related_stream=self.identity,
        )
        self._signal_emitter.emit(stream_cancel_signal)
        if self.config.forward_cancel_signal:
            for referer_id in self.ref_by.values():
                referer_stream = storage.find_stream(referer_id)
                if referer_stream is not None:
                    referer_stream.cancel(storage)
        storage.check_stream_status(self)
        if self.remove_callback is not None:
            self.remove_callback(self)
        return True

    def finish(self, storage: "StreamStorage"):
        if self.status not in (ChatStreamStatus.NOT_STARTED, ChatStreamStatus.STARTED):
            return False
        prev_status = self.status
        self.status = ChatStreamStatus.ENDED
        ref_by_list = [str(sid) for sid in self.ref_by.values()]
        stream_debug.log_finish(self, prev_status, ref_by_list)
        stream_end_signal = ChatSignal(
            type=ChatSignalType.STREAM_END,
            source_type=self.config.source_type,
            related_stream=self.identity,
        )
        self._signal_emitter.emit(stream_end_signal)
        storage.check_stream_status(self)
        if self.remove_callback is not None:
            self.remove_callback(self)
        return True

    @property
    def metadata(self) -> Dict[str, Any]:
        """
        Get merged metadata (regular + inheritable).
        Inheritable metadata takes precedence if there are key conflicts.
        This ensures downstream handlers can access inheritable metadata.
        """
        merged = self._metadata.copy()
        merged.update(self._inheritable_metadata)  # Inheritable takes precedence
        return merged

    def update_metadata(self, metadata: Dict[str, Any]):
        """Update regular metadata (not inheritable by child streams)."""
        self._metadata.update(metadata)

    def update_inheritable_metadata(self, metadata: Dict[str, Any], inherit: bool = True):
        """
        Update inheritable metadata that will be automatically inherited by child streams.
        
        Args:
            metadata: Dictionary of metadata to set
            inherit: If True, mark these metadata as inheritable. If False, remove from inheritable.
        """
        if inherit:
            # Add to inheritable_metadata and regular metadata
            self._inheritable_metadata.update(metadata)
            self._metadata.update(metadata)
        else:
            # Remove from inheritable_metadata (but keep in regular metadata)
            for key in metadata.keys():
                self._inheritable_metadata.pop(key, None)


class StreamStorage:
    def __init__(self, 
                 recycle_ttl: float = 10.0,
                 cleanup_interval: float = 1.0):
        """
        Initialize stream storage with configurable lifecycle parameters.
        
        Args:
            recycle_ttl: Time in seconds to keep finished streams alive after ending,
                        even without references. This allows downstream handlers
                        enough time to establish dependencies.
            cleanup_interval: Interval in seconds between periodic cleanup checks.
        """
        self.streams: Dict[StreamKey, ChatStream] = {}
        # recycle pool: keep finished streams for a grace period to avoid
        # dangling ref_stream lookups right after upstream finishes.
        self._finished_at: Dict[StreamKey, float] = {}
        self._recycle_ttl = recycle_ttl
        self._cleanup_interval = cleanup_interval
        self._last_cleanup = time.monotonic()

    def set_recycle_ttl(self, ttl: float):
        """Set the time-to-live for finished streams before recycling."""
        self._recycle_ttl = ttl

    def set_cleanup_interval(self, interval: float):
        """Set the interval between periodic cleanup checks."""
        self._cleanup_interval = interval

    def _cleanup_recycle(self, force: bool = False):
        """
        Periodic cleanup of expired finished streams.
        
        Args:
            force: If True, run cleanup regardless of interval.
        """
        now = time.monotonic()
        if not force and now - self._last_cleanup < self._cleanup_interval:
            return
        self._last_cleanup = now
        expired_keys = [
            key for key, ts in self._finished_at.items()
            if now - ts >= self._recycle_ttl
        ]
        for key in expired_keys:
            stream = self.streams.get(key)
            if stream is not None and len(stream.ref_by) == 0 and stream.status in (
                ChatStreamStatus.ENDED, ChatStreamStatus.CANCELLED
            ):
                stream_debug.log_recycle(stream, self._recycle_ttl)
                self.streams.pop(key, None)
            self._finished_at.pop(key, None)

    def add_stream(self, key: StreamKey, stream: ChatStream):
        self._cleanup_recycle()
        if key in self.streams:
            raise ValueError(f"Stream {key} already exists")
        self.streams[key] = stream

    def find_stream(self, stream_id: ChatStreamIdentity) -> Optional[ChatStream]:
        self._cleanup_recycle()
        key = stream_id.key
        result = self.streams.get(key, None)
        return result

    def ref_stream(self, refer_by: ChatStreamIdentity, refer_to: ChatStreamIdentity) -> bool:
        """
        Add a reference from refer_by to refer_to.
        
        Returns:
            bool: True if the target stream is in a valid state (not cancelled),
                  False if the target stream is cancelled (caller should cancel itself)
        """
        self._cleanup_recycle()
        target_stream = self.find_stream(refer_to)
        if target_stream is None:
            logger.error(f"Stream {refer_to} not found")
            return False
        
        referrer_key = refer_by.key
        if referrer_key not in target_stream.ref_by:
            target_stream.ref_by[referrer_key] = refer_by
            stream_debug.log_ref_add(refer_by, refer_to, len(target_stream.ref_by))
        # once referenced again, remove from recycle tracking
        self._finished_at.pop(target_stream.identity.key, None)
        
        # If target stream is already cancelled, the referrer should also be cancelled
        if target_stream.status == ChatStreamStatus.CANCELLED:
            logger.warning(f"Stream {refer_by} references cancelled stream {refer_to}, will propagate cancel")
            return False
        return True

    def unref_stream(self, refer_by: ChatStreamIdentity, refer_to: ChatStreamIdentity):
        self._cleanup_recycle()
        target_stream = self.find_stream(refer_to)
        if target_stream is None:
            logger.error(f"Stream {refer_to} not found")
        else:
            target_stream.ref_by.pop(refer_by.key, None)
            stream_debug.log_ref_remove(refer_by, refer_to, len(target_stream.ref_by))
            self._check_lifespan_(target_stream)

    def check_stream_status(self, stream: ChatStream):
        self._check_lifespan_(stream)

    def _check_lifespan_(self, stream: ChatStream):
        key = stream.identity.key
        # mark finished streams; actual removal deferred to recycle cleanup
        if len(stream.ref_by) == 0 and stream.status in (
            ChatStreamStatus.ENDED, ChatStreamStatus.CANCELLED
        ):
            self._finished_at.setdefault(key, time.monotonic())
        else:
            # still referenced; ensure not in recycle list
            self._finished_at.pop(key, None)
        self._cleanup_recycle()

    def get_all_active_streams(self) -> List[ChatStream]:
        """Get all streams that are currently active (not ended or cancelled)."""
        self._cleanup_recycle()
        return [
            stream for stream in self.streams.values()
            if stream.status in (ChatStreamStatus.NOT_STARTED, ChatStreamStatus.STARTED)
        ]

    def cancel_stream_with_ancestors(self, stream_id: ChatStreamIdentity) -> List[ChatStreamIdentity]:
        """
        Cancel a stream and all its cancelable ancestor streams.
        Used for interrupt functionality.
        
        Args:
            stream_id: Identity of the stream to cancel (typically the leaf/latest stream)
            
        Returns:
            List of cancelled stream identities
        """
        stream = self.find_stream(stream_id)
        if stream is None:
            logger.warning(f"Cannot cancel stream {stream_id}: not found")
            return []
        return stream.cancel_with_ancestors(self)

    def get_stream_ancestry(self, stream_id: ChatStreamIdentity) -> Dict[str, List[ChatStreamIdentity]]:
        """
        Get the complete ancestry information of a stream.
        
        Returns:
            Dict with:
            - 'parents': direct source streams
            - 'ancestors': all ancestors in dependency order (parents first)
            - 'cancelable': cancelable ancestors in dependency order
        """
        stream = self.find_stream(stream_id)
        if stream is None:
            return {'parents': [], 'ancestors': [], 'cancelable': []}
        return {
            'parents': list(stream.source_streams.values()),
            'ancestors': stream.ancestor_streams.copy(),
            'cancelable': stream.cancelable_ancestors.copy()
        }

class ChatStreamer:
    @dataclass
    class StreamHolder:
        stream: Optional[ChatStream] = None

    def __init__(self, storage: StreamStorage, session_clock: SessionClock,
                 data_info: HandlerDataInfo,
                 data_sinks,
                 signal_emitter: SignalEmitter,
                 producer_name: str,
                 data_name: Optional[str] = None,
                 config: Optional[ChatStreamConfig] = None):
        self._input_stream_ids: Dict[StreamKey, InputStreamStats] = {}
        self._streamer_id: int = -1
        self._session_clock: SessionClock = session_clock
        self._data_sinks = data_sinks
        self._producer_name: str = producer_name
        self._data_name: Optional[str] = data_name
        self._data_type: ChatDataType = data_info.type
        self._data_definition: Optional[DataBundleDefinition] = data_info.definition
        self._signal_emitter = signal_emitter
        self._storage = storage
        self._next_id = 0
        self._current_stream = self.StreamHolder()
        self._default_config: ChatStreamConfig = ChatStreamConfig() if config is None else config
        # Keep ended upstream streams for a short grace period so downstream
        # outputs (e.g., HUMAN_TEXT) can still reference them for ref_streams.
        self._ended_input_retention = 3.0  # seconds

    @property
    def data_type(self):
        return self._data_type

    @property
    def data_name(self):
        return self._data_name

    @property
    def producer_name(self):
        return self._producer_name

    @property
    def auto_link_input(self):
        return self._default_config.auto_link_input

    @property
    def current_stream(self):
        if self._current_stream.stream is None:
            return None
        if self._current_stream.stream.status not in (ChatStreamStatus.NOT_STARTED, ChatStreamStatus.STARTED):
            self._current_stream.stream = None
        return self._current_stream.stream

    @property
    def data_definition(self):
        return self._data_definition

    def update_input_stream(self, chat_data: ChatData):
        self._cleanup_input_streams()
        if chat_data.stream_id is None:
            return
        stream_key = chat_data.stream_id.key
        stream_stats = self._input_stream_ids.setdefault(
            stream_key,
            InputStreamStats(stream_id=chat_data.stream_id)
        )
        if chat_data.is_last_data:
            stream_stats.end_mark = time.monotonic()
        if stream_stats.start_time is None:
            stream_stats.start_time = self._session_clock.get_timestamp()

    def _cleanup_input_streams(self):
        if not self._input_stream_ids:
            return
        now = time.monotonic()
        to_remove = []
        for key, stats in self._input_stream_ids.items():
            # Remove expired streams (ended and past retention period)
            if (stats.end_mark is not None
                and now - stats.end_mark >= self._ended_input_retention):
                to_remove.append(key)
                continue
            # Remove cancelled streams
            stream = self._storage.find_stream(stats.stream_id)
            if stream is not None and stream.status == ChatStreamStatus.CANCELLED:
                to_remove.append(key)
        for key in to_remove:
            self._input_stream_ids.pop(key, None)

    def find_stream(self, stream_id: ChatStreamIdentity):
        return self._storage.find_stream(stream_id)

    def new_stream(self, sources: List[ChatStreamIdentity],
                   name: Optional[str] = None, config: Optional[ChatStreamConfig] = None):
        if self._current_stream.stream is not None:
            self.finish_current()
        new_stream_config = self._default_config
        if config is not None:
            new_stream_config = ChatStreamConfig(**{**new_stream_config.model_dump(), **config.model_dump(exclude_unset=True)})
        new_stream_id = ChatStreamIdentity(
            data_type=self._data_type,
            builder_id=self._streamer_id,
            stream_id=self._next_id,
            name=name,
            producer_name=self._producer_name
        )
        stream_holder = self._current_stream
        def stream_remove_callback(stream):
            if (id(stream) == id(stream_holder.stream)
                and stream.status in (ChatStreamStatus.NOT_STARTED, ChatStreamStatus.STARTED)):
                stream_holder.stream = None

        new_stream = ChatStream(
            config=new_stream_config,
            identity=new_stream_id,
            storage=self._storage,
            source_streams=sources,
            remove_callback=stream_remove_callback,
            signal_emitter=self._signal_emitter,
        )
        key = new_stream.identity.key
        self._storage.add_stream(key, new_stream)
        self._next_id += 1
        self._current_stream.stream = new_stream
        return new_stream_id

    def new_stream_from_input(
        self,
        input_stream: ChatStreamIdentity,
        name: Optional[str] = None,
        config: Optional[ChatStreamConfig] = None
    ) -> ChatStreamIdentity:
        """
        Create a new output stream strictly associated with a single input stream.
        
        Unlike new_stream() which auto-associates with all active input streams,
        this method creates an output stream that only references the specified
        input stream. This is useful for handlers that need strict 1:1 input-output
        stream association (e.g., ASR in duplex mode where each audio segment
        must produce a corresponding text segment).
        
        Args:
            input_stream: The specific input stream to associate with
            name: Optional name for the stream
            config: Optional stream configuration override
            
        Returns:
            The identity of the newly created stream
        """
        return self.new_stream(
            sources=[input_stream],
            name=name,
            config=config
        )

    def open_stream(
        self,
        sources: Optional[List[ChatStreamIdentity]] = None,
        name: Optional[str] = None,
        config: Optional[ChatStreamConfig] = None,
        meta: Optional[Dict[str, Any]] = None,
    ) -> Optional[ChatStreamIdentity]:
        """
        Create and immediately start a lifecycle-only stream (no data distribution).
        Emits STREAM_BEGIN signal. Use finish_current() to close it (emits STREAM_END).

        Unlike stream_data(), this does not require data sinks or actual data.
        Useful for virtual streams (e.g., CLIENT_PLAYBACK) that only track lifecycle.

        Args:
            sources: Parent stream identities. If None, uses current active input streams.
            name: Optional stream name.
            config: Optional stream config override.
            meta: Optional metadata to attach to the stream.

        Returns:
            The identity of the newly created and started stream, or None if creation failed.
        """
        if sources is None:
            self._cleanup_input_streams()
            sources = [v.stream_id for v in self._input_stream_ids.values()]
        stream_id = self.new_stream(sources, name, config)
        stream = self.current_stream
        if stream is None:
            return None
        if meta:
            stream.update_metadata(meta)
        timestamp = self._session_clock.get_timestamp()
        stream.start_time = timestamp
        stream.status = ChatStreamStatus.STARTED
        stream_debug.log_start(stream, timestamp)
        stream_begin_signal = ChatSignal(
            type=ChatSignalType.STREAM_BEGIN,
            source_type=stream.config.source_type,
            related_stream=stream.identity,
        )
        self._signal_emitter.emit(stream_begin_signal)
        return stream_id

    def _packet_chat_data(self, data: StreamableData):
        if data is None:
            return None
        timestamp = self._session_clock.get_timestamp()
        if isinstance(data, ChatData):
            if data.type != self._data_type:
                raise ValueError(f"Data type mismatch: {data.type} != {self._data_type}")
            chat_data = data
        elif isinstance(data, DataBundle):
            chat_data = ChatData(
                data=data,
                type=self._data_type,
                timestamp=timestamp,
            )
        elif isinstance(data, np.ndarray):
            data_bundle = DataBundle(definition=self._data_definition)
            data_bundle.set_main_data(data)
            chat_data = ChatData(
                data=data_bundle,
                type=self._data_type,
                timestamp=timestamp,
            )
        else:
            raise TypeError(f"Unsupported data type: {type(data)}")
        if not chat_data.is_timestamp_valid():
            chat_data.timestamp = timestamp
        chat_data.source = self._producer_name
        return chat_data

    @classmethod
    def _distribute_chat_data(cls, data: ChatData, sinks):
        for sink in sinks:
            if sink.owner == data.source:
                continue
            sink.sink_queue.put(data)
            if sink.consume_info.input_consume_mode == ChatDataConsumeMode.ONCE:
                break

    def stream_data(self, data: StreamableData,
                    missing_stream_callback: Optional[Callable[[ChatData], ChatStream]] = None,
                    finish_stream: Optional[bool] = None,
                    stream_meta: Optional[Dict] = None):
        self._cleanup_input_streams()
        if self.current_stream is None:
            if missing_stream_callback is not None:
                self._current_stream.stream = missing_stream_callback(data)
            else:
                source_streams = [value.stream_id for value in self._input_stream_ids.values()]
                self.new_stream(source_streams)
        stream = self.current_stream
        if stream is None:
            raise ValueError("No current stream")
        if stream_meta is not None:
            stream.update_metadata(stream_meta)
        sinks = self._data_sinks.get(self._data_type, [])
        if len(sinks) == 0:
            if finish_stream:
                self.finish_current()  # Still need to finish the stream even without sinks
            return
        chat_data = self._packet_chat_data(data)
        if isinstance(finish_stream, bool):
            chat_data.is_last_data = finish_stream
        if chat_data is None:
            return
        if stream.status == ChatStreamStatus.NOT_STARTED:
            stream.start_time = chat_data.timestamp
            stream.status = ChatStreamStatus.STARTED
            chat_data.is_first_data = True
            stream_debug.log_start(stream, chat_data.timestamp)
            stream_begin_signal = ChatSignal(
                type=ChatSignalType.STREAM_BEGIN,
                source_type=stream.config.source_type,
                related_stream=stream.identity,
            )
            self._signal_emitter.emit(stream_begin_signal)
        # Production-side cancel guard: check status right before distribution
        # to minimize the TOCTOU window. GIL ensures atomic status read, and the
        # consumer-side guard in _pumper_func catches anything that slips through.
        if stream.status == ChatStreamStatus.CANCELLED:
            return
        chat_data.stream_id = stream.identity
        # Always copy inheritable metadata to ChatData so downstream handlers can access it
        # Regular metadata is only copied on first/last data for performance
        if chat_data.data is not None:
            # Always include inheritable metadata (for POST_END reconnection detection, etc.)
            chat_data.data.metadata.update(stream._inheritable_metadata)
            # Include regular metadata on first/last data
            if chat_data.is_first_data or chat_data.is_last_data:
                chat_data.data.metadata.update(stream._metadata)
        if stream_meta is not None:
            chat_data.data.metadata.update(stream_meta)
        self._distribute_chat_data(chat_data, sinks)
        if chat_data.is_last_data:
            self.finish_current()

    def cancel_current(self):
        stream = self.current_stream
        if stream is None:
            return
        stream.cancel(self._storage)

    def cancel_stream(self, stream_id: ChatStreamIdentity) -> bool:
        """Cancel a specific stream by its identity.
        
        Unlike cancel_current(), this can cancel any stream including:
        - Currently active streams
        - Already finished streams (if they still have downstream dependencies)
        
        Args:
            stream_id: Identity of the stream to cancel
            
        Returns:
            True if the stream was cancelled, False otherwise
        """
        stream = self._storage.find_stream(stream_id)
        if stream is None:
            return False
        return stream.cancel(self._storage)

    def finish_current(self):
        stream = self.current_stream
        if stream is None:
            return
        stream.finish(self._storage)


class StreamManager:
    def __init__(self, signal_manager: SignalManager,
                 recycle_ttl: float = 10.0,
                 cleanup_interval: float = 1.0):
        """
        Initialize stream manager.
        
        Args:
            signal_manager: Signal manager for emitting stream signals
            recycle_ttl: Time in seconds to keep finished streams alive.
                        This gives downstream handlers time to establish dependencies.
            cleanup_interval: Interval in seconds between periodic cleanup checks.
        """
        self._signal_manager = signal_manager
        self._stream_storage = StreamStorage(
            recycle_ttl=recycle_ttl,
            cleanup_interval=cleanup_interval
        )
        # Use time-based unique base value to ensure stream keys don't conflict
        # across sessions (e.g., when client reconnects and creates a new session).
        # This prevents the issue where a new stream reuses a stream_key that was
        # previously interrupted, causing the client to incorrectly discard audio.
        self._next_streamer_id = int(time.monotonic() * 1000) % 10000000

    def create_streamer(self,
                        data_info: HandlerDataInfo,
                        data_sinks,
                        producer_name: str,
                        data_name: Optional[str] = None,
                        config: Optional[ChatStreamConfig] = None):
        signal_emitter = self._signal_manager.get_emitter(producer_name)
        builder = ChatStreamer(
            storage=self._stream_storage,
            session_clock=self._signal_manager.get_clock(),
            data_info=data_info,
            data_sinks=data_sinks,
            signal_emitter=signal_emitter,
            producer_name=producer_name,
            data_name=data_name,
            config=config
        )
        builder._streamer_id = self._next_streamer_id
        self._next_streamer_id += 1
        return builder

    def create_lifecycle_streamer(
        self,
        data_type: ChatDataType,
        producer_name: str,
        config: Optional[ChatStreamConfig] = None,
    ) -> "ChatStreamer":
        """
        Create a streamer for lifecycle-only streams (no data sinks needed).

        The returned streamer uses open_stream() / finish_current() to manage
        stream lifecycle and emit STREAM_BEGIN / STREAM_END signals without
        distributing any data.

        Args:
            data_type: The data type for the lifecycle stream (e.g., CLIENT_PLAYBACK).
            producer_name: Name of the producer handler.
            config: Optional stream configuration.

        Returns:
            A ChatStreamer configured for lifecycle-only use.
        """
        data_info = HandlerDataInfo(type=data_type)
        return self.create_streamer(
            data_info=data_info,
            data_sinks={},
            producer_name=producer_name,
            config=config,
        )

    def find_stream(self, stream_id: ChatStreamIdentity):
        if stream_id is None:
            return None
        return self._stream_storage.find_stream(stream_id)

    def set_recycle_ttl(self, ttl: float):
        """Set the time-to-live for finished streams before recycling."""
        self._stream_storage.set_recycle_ttl(ttl)

    def set_cleanup_interval(self, interval: float):
        """Set the interval between periodic cleanup checks."""
        self._stream_storage.set_cleanup_interval(interval)

    def cancel_stream_chain(self, stream_id: ChatStreamIdentity) -> List[ChatStreamIdentity]:
        """
        Cancel a stream and all its cancelable ancestor streams.
        Used for interrupt functionality - cancels the entire processing chain.
        The target stream itself is always cancelled regardless of its cancelable flag.
        
        Args:
            stream_id: Identity of the stream to cancel (typically the leaf/latest stream)
            
        Returns:
            List of cancelled stream identities
        """
        cancelled = self._stream_storage.cancel_stream_with_ancestors(stream_id)
        if stream_id not in cancelled:
            stream = self._stream_storage.find_stream(stream_id)
            if stream is not None and stream.cancel(self._stream_storage):
                cancelled.append(stream_id)
        return cancelled

    def get_stream_ancestry(self, stream_id: ChatStreamIdentity) -> Dict[str, List[ChatStreamIdentity]]:
        """
        Get the complete ancestry information of a stream.
        
        Returns:
            Dict with:
            - 'parents': direct source streams
            - 'ancestors': all ancestors in dependency order (parents first)
            - 'cancelable': cancelable ancestors in dependency order
        """
        return self._stream_storage.get_stream_ancestry(stream_id)

    def get_active_streams(self) -> List[ChatStream]:
        """Get all streams that are currently active (not ended or cancelled)."""
        return self._stream_storage.get_all_active_streams()

    def cancel_streams_by_type(self, data_type: "ChatDataType") -> List[ChatStreamIdentity]:
        """
        Cancel all active streams of the given data type and their cancelable ancestor chains.

        This is the engine-level API for interrupt: call with CLIENT_PLAYBACK to cancel
        all active playback streams and trace back through AVATAR_AUDIO → TTS → LLM.
        Each cancelled stream emits STREAM_CANCEL; forward_cancel_signal cascades
        to downstream referrers.

        Args:
            data_type: The data type of streams to cancel (e.g., ChatDataType.CLIENT_PLAYBACK)

        Returns:
            Deduplicated list of all cancelled stream identities
        """
        active = self.get_active_streams()
        targets = [s for s in active if s.identity.data_type == data_type]
        if not targets:
            return []
        cancelled_set = set()
        cancelled_list = []
        for stream in targets:
            result = self.cancel_stream_chain(stream.identity)
            for sid in result:
                if sid.key not in cancelled_set:
                    cancelled_set.add(sid.key)
                    cancelled_list.append(sid)
        return cancelled_list

    @staticmethod
    def enable_debug_logging(enabled: bool = True):
        """
        Enable or disable stream lifecycle debug logging.
        
        Args:
            enabled: True to enable debug logging, False to disable.
        """
        stream_debug.enabled = enabled
        logger.info(f"Stream debug logging {'enabled' if enabled else 'disabled'}")

    @staticmethod
    def is_debug_logging_enabled() -> bool:
        """Check if stream debug logging is enabled."""
        return stream_debug.enabled


class ChatDataSubmitter:
    def __init__(self, auto_update_input_stream: bool = True):
        self.streamers: Dict[ChatDataType, List[ChatStreamer]] = {}
        self.streamer_name_map: Dict[str, ChatStreamer] = {}
        self.auto_update_input_stream = auto_update_input_stream
        # Type mapping for override support: original_type -> actual_type
        self._output_type_mapping: Dict[ChatDataType, ChatDataType] = {}

    def set_output_type_mapping(self, mapping: Dict[ChatDataType, ChatDataType]):
        """
        Set the output type mapping for type_override support.
        This allows handler code to use original type names while the framework
        automatically maps to the actual (overridden) types.
        
        Args:
            mapping: Dict mapping original types to actual types
        """
        self._output_type_mapping = mapping

    def _resolve_type(self, data_type: ChatDataType) -> ChatDataType:
        """Resolve original type to actual type using mapping."""
        return self._output_type_mapping.get(data_type, data_type)

    def update_input_stream(self, chat_data: ChatData):
        if not self.auto_update_input_stream:
            return
        for streamer_list in self.streamers.values():
            for streamer in streamer_list:
                if not streamer.auto_link_input:
                    continue
                streamer.update_input_stream(chat_data)

    def register_streamer(self, streamer: ChatStreamer):
        streamer_list = self.streamers.setdefault(streamer.data_type, [])
        streamer_list.append(streamer)
        if streamer.data_name is not None:
            self.streamer_name_map[streamer.data_name] = streamer

    def get_streamers(self, data_type: ChatDataType):
        actual_type = self._resolve_type(data_type)
        return self.streamers.get(actual_type, [])

    def get_streamer(self, data_type: ChatDataType):
        streamers = self.get_streamers(data_type)
        if len(streamers) == 0:
            return None
        if len(streamers) > 1:
            logger.warning(f"More than one streamer for data type {data_type}, using the first one.")
        return streamers[0]

    def get_streamer_by_name(self, name: str):
        return self.streamer_name_map.get(name, None)

    def submit(self, data: Union[StreamableData, Tuple[ChatDataType, StreamableData]],
               finish_stream: Optional[bool] = None):
        if data is None:
            return
        data_type = None
        streamers = None
        stream_data = data  # 实际要流式传输的数据
        if len(self.streamers) == 1:
            data_type = list(self.streamers.keys())[0]
            streamers = self.get_streamers(data_type)
        if isinstance(data, ChatData):
            data_type = data.type
            streamers = self.get_streamers(data_type)
        elif isinstance(data, (DataBundle, np.ndarray)):
            if data_type is None:
                msg = f"Bare DataBundle is supported only if handler outputs single chat data type."
                raise ValueError(msg)
        elif isinstance(data, tuple) and len(data) == 2:
            chat_data_type, raw_data = data
            if not isinstance(chat_data_type, ChatDataType) or not isinstance(raw_data, (DataBundle, np.ndarray)):
                msg = f"Unsupported handler output type {type(data)}"
                raise ValueError(msg)
            if chat_data_type not in self.streamers:
                msg = f"Handler output type {chat_data_type} is not configured."
                raise ValueError(msg)
            data_type = chat_data_type
            streamers = self.get_streamers(data_type)
            stream_data = raw_data  # 使用提取的原始数据
        else:
            msg = f"Unsupported chat data with type {type(data)}"
            raise ValueError(msg)
        if streamers is None or len(streamers) == 0:
            logger.warning(f"No streamer for data type {data_type}")
            return
        for streamer in streamers:
            streamer.stream_data(stream_data, finish_stream=finish_stream)
