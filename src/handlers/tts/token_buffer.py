"""
Token Buffer for TTS - 智能处理 LLM token-by-token 输出的文本拼接

设计原则：
1. 空格分隔语言（英语、法语、德语等）：等待遇到空格/标点/CJK字符后再发送，避免单词被截断
2. 非空格分隔语言（中文、日语、韩语、泰语等）：每个字符可独立发音，立即发送
3. 混合语言：智能切换处理策略，如 "今天是sunny day" 中的中英文混合

使用示例：
    buffer = TokenBuffer()
    for token in llm_tokens:
        text_to_send = buffer.process(token)
        if text_to_send:
            tts.send(text_to_send)
    # 结束时刷新剩余内容
    remaining = buffer.flush()
    if remaining:
        tts.send(remaining)
"""

import unicodedata
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional, Tuple


class CharType(Enum):
    """字符类型分类"""
    CJK = auto()           # 中日韩统一表意文字（可独立发送）
    HANGUL = auto()        # 韩文音节（可独立发送）
    THAI = auto()          # 泰语（可独立发送，但有些复杂情况）
    KANA = auto()          # 日文假名（可独立发送）
    LATIN = auto()         # 拉丁字母（需等待空格分隔）
    CYRILLIC = auto()      # 西里尔字母（需等待空格分隔）
    ARABIC = auto()        # 阿拉伯文（需等待空格分隔）
    HEBREW = auto()        # 希伯来文（需等待空格分隔）
    GREEK = auto()         # 希腊文（需等待空格分隔）
    SPACE = auto()         # 空白字符
    PUNCTUATION = auto()   # 标点符号
    NUMBER = auto()        # 数字
    OTHER = auto()         # 其他


def get_char_type(char: str) -> CharType:
    """
    根据 Unicode 范围判断字符类型
    
    Args:
        char: 单个字符
        
    Returns:
        CharType 枚举值
    """
    if not char:
        return CharType.OTHER
    
    code = ord(char)
    
    # 空白字符
    if char.isspace():
        return CharType.SPACE
    
    # CJK 统一表意文字（中文、日文汉字、韩文汉字）
    if (0x4E00 <= code <= 0x9FFF or      # CJK Unified Ideographs
        0x3400 <= code <= 0x4DBF or      # CJK Unified Ideographs Extension A
        0x20000 <= code <= 0x2A6DF or    # CJK Unified Ideographs Extension B
        0x2A700 <= code <= 0x2B73F or    # CJK Unified Ideographs Extension C
        0x2B740 <= code <= 0x2B81F or    # CJK Unified Ideographs Extension D
        0x2B820 <= code <= 0x2CEAF or    # CJK Unified Ideographs Extension E
        0x2CEB0 <= code <= 0x2EBEF or    # CJK Unified Ideographs Extension F
        0x30000 <= code <= 0x3134F or    # CJK Unified Ideographs Extension G
        0xF900 <= code <= 0xFAFF or      # CJK Compatibility Ideographs
        0x2F800 <= code <= 0x2FA1F):     # CJK Compatibility Ideographs Supplement
        return CharType.CJK
    
    # 日文假名
    if (0x3040 <= code <= 0x309F or      # Hiragana
        0x30A0 <= code <= 0x30FF or      # Katakana
        0x31F0 <= code <= 0x31FF or      # Katakana Phonetic Extensions
        0xFF65 <= code <= 0xFF9F):       # Halfwidth Katakana
        return CharType.KANA
    
    # 韩文音节
    if (0xAC00 <= code <= 0xD7AF or      # Hangul Syllables
        0x1100 <= code <= 0x11FF or      # Hangul Jamo
        0x3130 <= code <= 0x318F or      # Hangul Compatibility Jamo
        0xA960 <= code <= 0xA97F or      # Hangul Jamo Extended-A
        0xD7B0 <= code <= 0xD7FF):       # Hangul Jamo Extended-B
        return CharType.HANGUL
    
    # 泰语
    if 0x0E00 <= code <= 0x0E7F:         # Thai
        return CharType.THAI
    
    # 拉丁字母
    if (0x0041 <= code <= 0x007A or      # Basic Latin letters
        0x00C0 <= code <= 0x00FF or      # Latin-1 Supplement
        0x0100 <= code <= 0x017F or      # Latin Extended-A
        0x0180 <= code <= 0x024F or      # Latin Extended-B
        0x1E00 <= code <= 0x1EFF):       # Latin Extended Additional
        return CharType.LATIN
    
    # 西里尔字母（俄语等）
    if (0x0400 <= code <= 0x04FF or      # Cyrillic
        0x0500 <= code <= 0x052F):       # Cyrillic Supplement
        return CharType.CYRILLIC
    
    # 阿拉伯文
    if (0x0600 <= code <= 0x06FF or      # Arabic
        0x0750 <= code <= 0x077F or      # Arabic Supplement
        0x08A0 <= code <= 0x08FF):       # Arabic Extended-A
        return CharType.ARABIC
    
    # 希伯来文
    if 0x0590 <= code <= 0x05FF:         # Hebrew
        return CharType.HEBREW
    
    # 希腊文
    if (0x0370 <= code <= 0x03FF or      # Greek and Coptic
        0x1F00 <= code <= 0x1FFF):       # Greek Extended
        return CharType.GREEK
    
    # 数字
    if char.isdigit():
        return CharType.NUMBER
    
    # 标点符号（使用 Unicode category）
    category = unicodedata.category(char)
    if category.startswith('P') or category.startswith('S'):
        return CharType.PUNCTUATION
    
    return CharType.OTHER


def is_immediate_sendable(char_type: CharType) -> bool:
    """
    判断该类型的字符是否可以立即发送（无需等待后续字符）
    
    CJK、假名、韩文、泰语等可以独立发音，无需等待空格分隔
    """
    return char_type in {
        CharType.CJK,
        CharType.KANA,
        CharType.HANGUL,
        CharType.THAI,
        CharType.SPACE,
        CharType.PUNCTUATION,
    }


def is_word_char(char_type: CharType) -> bool:
    """
    判断该类型字符是否是需要等待空格分隔的"单词字符"
    
    拉丁字母、西里尔字母、阿拉伯文、希腊文、数字等需要等待空格
    """
    return char_type in {
        CharType.LATIN,
        CharType.CYRILLIC,
        CharType.ARABIC,
        CharType.HEBREW,
        CharType.GREEK,
        CharType.NUMBER,
    }


@dataclass
class TokenBuffer:
    """
    Token 缓冲器 - 智能处理 LLM token 流
    
    处理策略：
    1. 收到 CJK/假名/韩文等字符时，立即输出（连同之前缓冲的完整内容）
    2. 收到拉丁字母等需要空格分隔的字符时，暂存到缓冲区
    3. 收到空格/标点时，输出缓冲区内容 + 当前字符
    4. 流结束时，flush 输出所有剩余内容
    
    Attributes:
        buffer: 当前缓冲的文本
        min_buffer_chars: 最小缓冲字符数，用于某些场景的批量发送优化
        max_buffer_chars: 最大缓冲字符数，超过后强制发送（防止过长等待）
    """
    buffer: str = ""
    min_buffer_chars: int = 0
    max_buffer_chars: int = 200
    
    def process(self, token: Optional[str]) -> str:
        """
        处理输入的 token，返回可以发送给 TTS 的文本
        
        Args:
            token: 输入的 token 文本（可能是 None 或空字符串）
            
        Returns:
            可以发送给 TTS 的文本（可能为空字符串，表示暂时不发送）
        """
        if not token:
            return ""
        
        result = []
        
        for char in token:
            char_type = get_char_type(char)
            
            if is_immediate_sendable(char_type):
                # CJK、假名、韩文、标点、空格等可以立即发送
                # 先输出缓冲区内容，再输出当前字符
                if self.buffer:
                    result.append(self.buffer)
                    self.buffer = ""
                result.append(char)
            elif is_word_char(char_type):
                # 拉丁字母等需要缓冲，等待完整单词
                self.buffer += char
                # 检查是否超过最大缓冲限制
                if len(self.buffer) >= self.max_buffer_chars:
                    result.append(self.buffer)
                    self.buffer = ""
            else:
                # 其他字符（如特殊符号），直接追加到缓冲区
                self.buffer += char
        
        output = "".join(result)
        
        # 检查最小输出长度
        if output and len(output) < self.min_buffer_chars:
            self.buffer = output + self.buffer
            return ""
        
        return output
    
    def flush(self) -> str:
        """
        刷新缓冲区，返回所有剩余内容
        
        在输入流结束时调用此方法
        
        Returns:
            缓冲区中剩余的所有文本
        """
        result = self.buffer
        self.buffer = ""
        return result
    
    def clear(self) -> None:
        """清空缓冲区"""
        self.buffer = ""
    
    def peek(self) -> str:
        """查看当前缓冲区内容（不清空）"""
        return self.buffer
    
    def __len__(self) -> int:
        """返回当前缓冲区长度"""
        return len(self.buffer)


@dataclass
class SentenceAwareTokenBuffer(TokenBuffer):
    """
    句子感知的 Token 缓冲器
    
    在 TokenBuffer 基础上，增加按句子/从句分隔的功能。
    当遇到句末标点时，立即发送完整句子，提升 TTS 的流畅性。
    
    Attributes:
        sentence_delimiters: 句子分隔符集合
        clause_delimiters: 从句分隔符集合（可选用于更细粒度的分隔）
        split_on_clause: 是否在从句处也进行分隔
    """
    sentence_delimiters: set = field(default_factory=lambda: {
        '。', '！', '？', '；',  # 中文标点
        '.', '!', '?', ';',    # 英文标点
        '।', '؟', '।',         # 其他语言句末标点
    })
    clause_delimiters: set = field(default_factory=lambda: {
        '，', '：', '、',       # 中文标点
        ',', ':',              # 英文标点
    })
    split_on_clause: bool = False
    _pending_output: str = field(default="", init=False)
    
    def process(self, token: Optional[str]) -> str:
        """
        处理输入 token，在句子边界处返回完整内容
        """
        if not token:
            return ""
        
        # 先用父类方法处理 token
        immediate_output = super().process(token)
        self._pending_output += immediate_output
        
        # 检查是否有完整句子可以发送
        result = []
        remaining = ""
        
        i = 0
        last_split = 0
        
        while i < len(self._pending_output):
            char = self._pending_output[i]
            
            is_sentence_end = char in self.sentence_delimiters
            is_clause_end = self.split_on_clause and char in self.clause_delimiters
            
            if is_sentence_end or is_clause_end:
                # 包含当前标点，作为一个完整段落
                result.append(self._pending_output[last_split:i + 1])
                last_split = i + 1
            
            i += 1
        
        # 剩余部分保留在 pending
        remaining = self._pending_output[last_split:]
        self._pending_output = remaining
        
        return "".join(result)
    
    def flush(self) -> str:
        """刷新所有缓冲内容"""
        parent_flush = super().flush()
        result = self._pending_output + parent_flush
        self._pending_output = ""
        return result
    
    def clear(self) -> None:
        """清空所有缓冲区"""
        super().clear()
        self._pending_output = ""


# 便捷函数
def create_token_buffer(
    sentence_aware: bool = False,
    split_on_clause: bool = False,
    min_buffer_chars: int = 0,
    max_buffer_chars: int = 200,
) -> TokenBuffer:
    """
    创建 Token 缓冲器的工厂函数
    
    Args:
        sentence_aware: 是否启用句子感知模式
        split_on_clause: 是否在从句处也分隔（仅 sentence_aware=True 时有效）
        min_buffer_chars: 最小缓冲字符数
        max_buffer_chars: 最大缓冲字符数
        
    Returns:
        TokenBuffer 或 SentenceAwareTokenBuffer 实例
    """
    if sentence_aware:
        return SentenceAwareTokenBuffer(
            min_buffer_chars=min_buffer_chars,
            max_buffer_chars=max_buffer_chars,
            split_on_clause=split_on_clause,
        )
    else:
        return TokenBuffer(
            min_buffer_chars=min_buffer_chars,
            max_buffer_chars=max_buffer_chars,
        )
