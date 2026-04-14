"""
Session History Module for Full-Duplex Conversation

This module provides a global timeline for recording all conversation events within a session,
including VAD events, ASR transcriptions, LLM outputs, TTS audio, and client playback states.

Key features:
- Uses monotonic clock for real-time event ordering
- Reuses ChatDataType and ChatSignalType for event classification
- Supports owner-based logical revocation (not physical deletion)
- Event-level relationship tracking (independent of stream lifecycle)
- Configurable retention policies (by count or time)
- Extension points for persistence and LLM summarization
"""

from typing import Optional, List, Any, Dict
from dataclasses import dataclass, field
from enum import Enum
import time
import uuid

from chat_engine.data_models.chat_data_type import ChatDataType
from chat_engine.data_models.chat_signal_type import ChatSignalType


class HistoryRetentionMode(str, Enum):
    """History retention mode"""
    BY_COUNT = "by_count"      # Retain by event count
    BY_TIME = "by_time"        # Retain by time window
    BY_BOTH = "by_both"        # Both count and time limits


@dataclass
class HistoryEvent:
    """
    A single history event record.
    
    Events can represent data flow (ASR text, LLM output) or signals
    (stream begin/end, interrupts). The combination of data_type and
    signal_type determines the event semantics.
    """
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    
    # Timestamp: monotonic real-time clock (seconds)
    timestamp: float = field(default_factory=time.monotonic)
    
    # Event classification using existing type system
    data_type: Optional[ChatDataType] = None      # Data modality
    signal_type: Optional[ChatSignalType] = None  # Signal type
    
    # Event payload
    data: Any = None  # Text content or metadata dict
    
    # Owner for revocation (handler name or "client")
    owner: Optional[str] = None
    
    # Event relationships (independent of stream lifecycle)
    related_event_ids: List[str] = field(default_factory=list)  # Related event IDs
    parent_event_id: Optional[str] = None  # Parent event (e.g., STREAM_END -> STREAM_BEGIN)
    
    # Original stream info (snapshot, stream may have expired)
    source_stream_key: Optional[str] = None  # Stream key snapshot (format: "stream_{builder_id}_{stream_id}")
    
    # Revocation state
    revoked: bool = False
    revoked_at: Optional[float] = None


@dataclass 
class HistoryConfig:
    """History module configuration"""
    retention_mode: HistoryRetentionMode = HistoryRetentionMode.BY_BOTH
    max_events: int = 1000                    # Maximum event count
    max_age_seconds: float = 3600.0           # Maximum retention time (seconds)
    cleanup_interval_seconds: float = 60.0   # Cleanup check interval
    
    # Extension placeholders
    enable_persistence: bool = False          # Enable persistence (future)
    enable_summary: bool = False              # Enable LLM summary (future)


class SessionHistory:
    """
    Session-level global history timeline.
    
    Provides methods to:
    - Add and query events
    - Revoke events by owner
    - Track avatar speaking state for interrupt detection
    - Link related events
    - Manage retention and cleanup
    - Accumulate streaming text data
    """
    
    def __init__(self, config: Optional[HistoryConfig] = None):
        self.config = config or HistoryConfig()
        self._events: List[HistoryEvent] = []
        self._event_index: Dict[str, HistoryEvent] = {}  # event_id -> event
        self._last_cleanup_time: float = time.monotonic()
        # Stream data accumulator: stream_key -> accumulated text
        self._stream_accumulators: Dict[str, str] = {}
        # Dedup tracker: stream_key -> set of (chunk_hash) to prevent duplicate accumulation
        self._stream_chunk_hashes: Dict[str, set] = {}
        # Lock for thread-safe accumulation
        import threading
        self._accumulator_lock = threading.Lock()
    
    def accumulate_stream_data(self, stream_key: str, text: str, chunk_id: Optional[str] = None) -> bool:
        """
        Accumulate text data for a streaming source.
        
        This is used for incremental streams like AVATAR_TEXT where data
        arrives in multiple chunks. Uses hash-based deduplication to prevent
        duplicate accumulation when multiple handlers process the same stream.
        
        Args:
            stream_key: The stream key to accumulate for
            text: Text to append
            chunk_id: Optional unique chunk identifier for deduplication
            
        Returns:
            True if data was accumulated, False if skipped (duplicate)
        """
        if not text:
            return False
        
        with self._accumulator_lock:
            if stream_key not in self._stream_accumulators:
                self._stream_accumulators[stream_key] = ""
                self._stream_chunk_hashes[stream_key] = set()
            
            # Generate chunk identifier for deduplication
            # Use provided chunk_id or generate from content + current position
            current_pos = len(self._stream_accumulators[stream_key])
            dedup_key = chunk_id if chunk_id else f"{current_pos}:{hash(text)}"
            
            # Check if this chunk was already accumulated
            if dedup_key in self._stream_chunk_hashes[stream_key]:
                return False  # Duplicate, skip
            
            # Accumulate and mark as processed
            self._stream_accumulators[stream_key] += text
            self._stream_chunk_hashes[stream_key].add(dedup_key)
            return True
    
    def get_accumulated_data(self, stream_key: str) -> Optional[str]:
        """
        Get accumulated data for a stream.
        
        Args:
            stream_key: The stream key
            
        Returns:
            Accumulated text, or None if no data
        """
        with self._accumulator_lock:
            return self._stream_accumulators.get(stream_key)
    
    def finalize_stream_accumulator(self, stream_key: str) -> Optional[str]:
        """
        Get and remove accumulated data for a finished stream.
        
        Args:
            stream_key: The stream key
            
        Returns:
            Final accumulated text, or None if no data
        """
        with self._accumulator_lock:
            self._stream_chunk_hashes.pop(stream_key, None)
            return self._stream_accumulators.pop(stream_key, None)
    
    def add_event(self, event: HistoryEvent) -> str:
        """
        Add an event to history.
        
        Args:
            event: The event to add
            
        Returns:
            The event_id of the added event
        """
        self._maybe_cleanup()
        self._events.append(event)
        self._event_index[event.event_id] = event
        return event.event_id
    
    def create_and_add_event(
        self,
        data_type: Optional[ChatDataType] = None,
        signal_type: Optional[ChatSignalType] = None,
        data: Any = None,
        owner: Optional[str] = None,
        related_event_ids: Optional[List[str]] = None,
        parent_event_id: Optional[str] = None,
        source_stream_key: Optional[str] = None,
    ) -> str:
        """
        Convenience method to create and add an event in one call.
        
        Returns:
            The event_id of the created event
        """
        event = HistoryEvent(
            timestamp=time.monotonic(),
            data_type=data_type,
            signal_type=signal_type,
            data=data,
            owner=owner,
            related_event_ids=related_event_ids or [],
            parent_event_id=parent_event_id,
            source_stream_key=source_stream_key,
        )
        return self.add_event(event)
    
    def revoke_event(self, event_id: str, owner: str) -> bool:
        """
        Revoke an event (logical revocation, excluded from queries).
        
        Only the event's owner can revoke it.
        
        Args:
            event_id: ID of the event to revoke
            owner: Must match the event's owner
            
        Returns:
            True if revoked, False otherwise
        """
        event = self._event_index.get(event_id)
        if event is None:
            return False
        if event.owner != owner:
            return False  # Only owner can revoke
        event.revoked = True
        event.revoked_at = time.monotonic()
        return True
    
    def revoke_by_owner(self, owner: str, since_timestamp: Optional[float] = None) -> int:
        """
        Revoke all events from a specific owner.
        
        Args:
            owner: Owner whose events to revoke
            since_timestamp: Only revoke events after this timestamp (optional)
            
        Returns:
            Number of events revoked
        """
        count = 0
        for event in self._events:
            if event.owner == owner and not event.revoked:
                if since_timestamp is None or event.timestamp >= since_timestamp:
                    event.revoked = True
                    event.revoked_at = time.monotonic()
                    count += 1
        return count
    
    def get_event(self, event_id: str, include_revoked: bool = False) -> Optional[HistoryEvent]:
        """Get a specific event by ID."""
        event = self._event_index.get(event_id)
        if event and (include_revoked or not event.revoked):
            return event
        return None
    
    def get_recent_events(
        self, 
        data_types: Optional[List[ChatDataType]] = None,
        signal_types: Optional[List[ChatSignalType]] = None,
        owners: Optional[List[str]] = None,
        max_count: int = 20,
        since_timestamp: Optional[float] = None,
        include_revoked: bool = False
    ) -> List[HistoryEvent]:
        """
        Query recent events with filters.
        
        Args:
            data_types: Filter by data types (OR logic)
            signal_types: Filter by signal types (OR logic)
            owners: Filter by owners (OR logic)
            max_count: Maximum number of events to return
            since_timestamp: Only events after this timestamp
            include_revoked: Include revoked events
            
        Returns:
            Events in chronological order (oldest first)
        """
        results = []
        for event in reversed(self._events):
            # Filter revoked
            if event.revoked and not include_revoked:
                continue
            # Filter by timestamp
            if since_timestamp and event.timestamp < since_timestamp:
                continue
            # Filter by data_type
            if data_types and event.data_type not in data_types:
                continue
            # Filter by signal_type
            if signal_types and event.signal_type not in signal_types:
                continue
            # Filter by owner
            if owners and event.owner not in owners:
                continue
            
            results.append(event)
            if len(results) >= max_count:
                break
        
        return list(reversed(results))  # Return in chronological order
    
    def get_recent_dialog(self, max_turns: int = 5) -> List[HistoryEvent]:
        """
        Get recent dialog turns (HUMAN_TEXT + AVATAR_TEXT).
        
        This method aggregates text content for each stream and deduplicates
        consecutive identical messages.
        
        Args:
            max_turns: Maximum number of turns (each turn = human + avatar)
            
        Returns:
            Deduplicated dialog events in chronological order
        """
        # Get all text events (both BEGIN and END) to aggregate content
        all_events = self.get_recent_events(
            data_types=[ChatDataType.HUMAN_TEXT, ChatDataType.AVATAR_TEXT],
            max_count=max_turns * 4,  # Get more to handle aggregation
        )
        
        # Group events by stream and aggregate text content
        # Use source_stream_key or event_id to identify streams
        stream_texts: Dict[str, str] = {}  # stream_key -> aggregated text
        stream_types: Dict[str, ChatDataType] = {}  # stream_key -> data type
        stream_order: List[str] = []  # Track order of streams
        
        for event in all_events:
            key = event.source_stream_key or event.event_id
            if key not in stream_texts:
                stream_texts[key] = ""
                stream_types[key] = event.data_type
                stream_order.append(key)
            
            # Aggregate text content (skip None/empty)
            if event.data:
                text = str(event.data).strip()
                if text and text != stream_texts[key]:  # Avoid duplicate appends
                    if stream_texts[key]:
                        stream_texts[key] += " " + text
                    else:
                        stream_texts[key] = text
        
        # Build deduplicated dialog list
        result: List[HistoryEvent] = []
        last_text = None
        
        for key in stream_order:
            text = stream_texts[key]
            data_type = stream_types[key]
            
            # Skip if same as last message (dedup consecutive identical)
            if text == last_text and text:
                continue
            
            # Create a synthetic event with aggregated text
            result.append(HistoryEvent(
                data_type=data_type,
                signal_type=ChatSignalType.STREAM_END,
                data=text if text else None,
                source_stream_key=key,
            ))
            last_text = text
        
        # Return only the last N turns
        return result[-(max_turns * 2):]
    
    def is_avatar_speaking(self) -> bool:
        """Check if avatar is currently speaking."""
        return self.get_active_avatar_stream() is not None
    
    def get_stream_start_time(
        self,
        data_type: ChatDataType,
        source_stream_key: Optional[str] = None,
        most_recent: bool = True
    ) -> Optional[float]:
        """
        Get the monotonic timestamp of when a stream started.
        
        This is useful for getting the actual time when user started speaking
        (from HUMAN_DUPLEX_AUDIO STREAM_BEGIN) rather than when ASR result arrived.
        
        Args:
            data_type: Data type to search for
            source_stream_key: Optional specific stream key to match
            most_recent: If True, return the most recent stream; otherwise the first match
            
        Returns:
            Monotonic timestamp of the stream start, or None if not found
        """
        events = list(reversed(self._events)) if most_recent else self._events
        
        for event in events:
            if event.revoked:
                continue
            if (event.data_type == data_type 
                and event.signal_type == ChatSignalType.STREAM_BEGIN):
                if source_stream_key is None or event.source_stream_key == source_stream_key:
                    return event.timestamp
        
        return None
    
    @staticmethod
    def _is_playback_begin(event: "HistoryEvent") -> bool:
        return (event.data_type == ChatDataType.CLIENT_PLAYBACK
                and event.signal_type == ChatSignalType.STREAM_BEGIN)

    @staticmethod
    def _is_playback_end(event: "HistoryEvent") -> bool:
        return (event.data_type == ChatDataType.CLIENT_PLAYBACK
                and event.signal_type in (ChatSignalType.STREAM_END, ChatSignalType.STREAM_CANCEL))

    def was_avatar_speaking_at(self, timestamp: float) -> bool:
        """
        Check if avatar was speaking at a specific timestamp.
        
        This is useful for interrupt detection: we need to check if avatar
        was speaking when the user STARTED speaking, not when ASR result arrives.
        
        Avatar is considered "speaking" while a CLIENT_PLAYBACK stream is active
        (from STREAM_BEGIN until STREAM_END/STREAM_CANCEL).
        Multiple playback endpoints may each create their own CLIENT_PLAYBACK streams.
        
        Args:
            timestamp: The monotonic timestamp to check
            
        Returns:
            True if avatar was speaking at that timestamp
        """
        ended_stream_keys: Dict[str, float] = {}
        for event in self._events:
            if event.revoked:
                continue
            if self._is_playback_end(event) and event.source_stream_key:
                ended_stream_keys[event.source_stream_key] = event.timestamp

        for event in self._events:
            if event.revoked:
                continue
            if self._is_playback_begin(event):
                begin_ts = event.timestamp
                stream_key = event.source_stream_key
                end_ts = ended_stream_keys.get(stream_key) if stream_key else None
                if begin_ts <= timestamp:
                    if end_ts is None or timestamp < end_ts:
                        return True
        
        return False
    
    def get_active_avatar_stream(self) -> Optional[HistoryEvent]:
        """
        Get the STREAM_BEGIN event of the currently active CLIENT_PLAYBACK stream.
        
        Avatar is considered "speaking" while a CLIENT_PLAYBACK stream is active.
        A stream is ended when STREAM_END or STREAM_CANCEL matches its source_stream_key.
        
        Returns:
            The STREAM_BEGIN event if avatar is speaking, None otherwise.
            Contains source_stream_key for stream association.
        """
        ended_stream_keys = set()
        for event in self._events:
            if event.revoked:
                continue
            if self._is_playback_end(event) and event.source_stream_key:
                ended_stream_keys.add(event.source_stream_key)
        
        for event in reversed(self._events):
            if event.revoked:
                continue
            if self._is_playback_begin(event):
                if event.source_stream_key and event.source_stream_key in ended_stream_keys:
                    continue
                return event
        
        return None
    
    def get_active_avatar_streams(self) -> List[HistoryEvent]:
        """
        Get all currently active CLIENT_PLAYBACK streams (may have multiple in parallel).
        
        A stream is active if no STREAM_END/STREAM_CANCEL with matching source_stream_key
        exists. Multiple playback endpoints may each create their own CLIENT_PLAYBACK streams.
        
        Returns:
            List of STREAM_BEGIN events for active CLIENT_PLAYBACK streams, newest first.
        """
        active_streams = []
        
        ended_stream_keys = set()
        for event in self._events:
            if event.revoked:
                continue
            if self._is_playback_end(event) and event.source_stream_key:
                ended_stream_keys.add(event.source_stream_key)
        
        seen_stream_keys = set()
        for event in reversed(self._events):
            if event.revoked:
                continue
            if self._is_playback_begin(event):
                sk = event.source_stream_key
                if sk and sk not in ended_stream_keys and sk not in seen_stream_keys:
                    active_streams.append(event)
                    seen_stream_keys.add(sk)
        
        return active_streams
    
    def get_related_events(self, event_id: str, include_revoked: bool = False) -> List[HistoryEvent]:
        """Get all events related to a specific event."""
        event = self.get_event(event_id, include_revoked=True)
        if event is None:
            return []
        
        related = []
        for related_id in event.related_event_ids:
            related_event = self.get_event(related_id, include_revoked)
            if related_event:
                related.append(related_event)
        return related
    
    def link_events(self, event_id: str, related_event_id: str):
        """Establish a relationship between two events."""
        event = self._event_index.get(event_id)
        if event and related_event_id not in event.related_event_ids:
            event.related_event_ids.append(related_event_id)
    
    def _maybe_cleanup(self):
        """Periodic cleanup of expired events based on retention policy."""
        now = time.monotonic()
        if now - self._last_cleanup_time < self.config.cleanup_interval_seconds:
            return
        
        self._last_cleanup_time = now
        cutoff_time = now - self.config.max_age_seconds
        
        # Clean by time
        if self.config.retention_mode in (HistoryRetentionMode.BY_TIME, HistoryRetentionMode.BY_BOTH):
            self._events = [e for e in self._events if e.timestamp >= cutoff_time]
        
        # Clean by count
        if self.config.retention_mode in (HistoryRetentionMode.BY_COUNT, HistoryRetentionMode.BY_BOTH):
            if len(self._events) > self.config.max_events:
                removed = self._events[:-self.config.max_events]
                self._events = self._events[-self.config.max_events:]
                for e in removed:
                    self._event_index.pop(e.event_id, None)
        
        # Rebuild index
        self._event_index = {e.event_id: e for e in self._events}
    
    # === Extension interfaces (future) ===
    
    def export_for_summary(self, max_events: int = 100) -> List[Dict]:
        """Export events for LLM summary (future extension)."""
        events = self.get_recent_events(max_count=max_events)
        return [
            {
                "timestamp": e.timestamp,
                "data_type": e.data_type.value if e.data_type else None,
                "signal_type": e.signal_type.value if e.signal_type else None,
                "data": e.data,
            }
            for e in events
        ]
    
    def persist(self, storage_path: str):
        """Persist history to storage (future extension)."""
        raise NotImplementedError("Persistence not yet implemented")
    
    def load(self, storage_path: str):
        """Load history from storage (future extension)."""
        raise NotImplementedError("Persistence not yet implemented")
