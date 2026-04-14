"""
Text Filter for TTS - 文本过滤工具，用于清理 LLM 输出的 markdown 文本

设计原则：
1. 移除各种括号及其中的内容（圆括号、方括号、花括号等）
2. 将强调标记转换为对应语言的引号
3. 移除 markdown 标记（标题、列表、链接、代码块等）
4. 保留正常对话的标点符号（逗号、句号、问号、感叹号等）
5. 支持增量文本流处理（能处理不完整的 markdown 标记）

使用示例：
    filter = TextFilter(
        remove_brackets=True,
        convert_emphasis_to_quotes=True,
        remove_markdown=True
    )
    filtered_text = filter.filter("这是**重要**的内容")
    # 输出: 这是「重要」的内容
"""

import re
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class TextFilterConfig:
    """
    文本过滤器配置
    
    Attributes:
        remove_brackets: 是否移除各种括号及其中的内容
        remove_code_blocks: 是否移除代码块
        remove_markdown_links: 是否移除 markdown 链接和图片
        remove_markdown_formatting: 是否移除 markdown 格式化标记（标题、列表等）
        convert_emphasis_to_quotes: 是否将强调标记转换为引号
        remove_special_tokens: 是否移除特殊标记（如 <|...|>）
        chinese_quote_style: 中文引号样式，可选 '「」' 或 '""'
        english_quote_style: 英文引号样式，可选 '"' 或 '''
        chinese_threshold: 判断文本为中文的阈值（中文字符占比）
    """
    remove_brackets: bool = True
    remove_code_blocks: bool = True
    remove_markdown_links: bool = True
    remove_markdown_formatting: bool = True
    convert_emphasis_to_quotes: bool = True
    remove_special_tokens: bool = True
    chinese_quote_style: str = '「」'
    english_quote_style: str = '"'
    chinese_threshold: float = 0.3


class TextFilter:
    """
    文本过滤器 - 清理文本，只保留 TTS 可以直接念出的内容
    
    支持增量文本流处理，能处理不完整的 markdown 标记。
    """
    
    def __init__(self, config: Optional[TextFilterConfig] = None):
        """
        初始化文本过滤器
        
        Args:
            config: 过滤器配置，如果为 None 则使用默认配置
        """
        self.config = config or TextFilterConfig()
    
    def filter(self, text: str) -> str:
        """
        过滤文本，只保留 TTS 可以直接念出的内容
        
        Args:
            text: 输入的文本（可能包含 markdown 标记）
            
        Returns:
            过滤后的文本，适合 TTS 朗读
        """
        if not text:
            return text
        
        # 1. 移除代码块
        if self.config.remove_code_blocks:
            text = self._remove_code_blocks(text)
        
        # 2. 移除各种括号及其中的内容
        if self.config.remove_brackets:
            text = self._remove_brackets(text)
        
        # 3. 移除 markdown 链接和图片
        if self.config.remove_markdown_links:
            text = self._remove_markdown_links(text)
        
        # 4. 移除 markdown 格式化标记
        if self.config.remove_markdown_formatting:
            text = self._remove_markdown_formatting(text)
        
        # 5. 移除特殊标记
        if self.config.remove_special_tokens:
            text = self._remove_special_tokens(text)
        
        # 6. 处理强调标记，转换为引号
        if self.config.convert_emphasis_to_quotes:
            text = self._convert_emphasis_to_quotes(text)
        
        # 7. 清理空白字符
        text = self._clean_whitespace(text)
        
        return text
    
    def _remove_code_blocks(self, text: str) -> str:
        """移除代码块"""
        text = re.sub(r'```[\s\S]*?```', '', text)  # 多行代码块
        text = re.sub(r'`[^`\n]*`', '', text)  # 行内代码（避免跨行匹配）
        return text
    
    def _remove_brackets(self, text: str) -> str:
        """移除各种括号及其中的内容"""
        # 圆括号：()、（）
        text = re.sub(r'\([^)]*\)', '', text)
        text = re.sub(r'（[^）]*）', '', text)
        # 方括号：[]、【】
        text = re.sub(r'\[[^\]]*\]', '', text)
        text = re.sub(r'【[^】]*】', '', text)
        # 花括号：{}、｛｝
        text = re.sub(r'\{[^}]*\}', '', text)
        text = re.sub(r'｛[^｝]*｝', '', text)
        # 尖括号：<>、〈〉、«»
        text = re.sub(r'<[^>]*>', '', text)
        text = re.sub(r'〈[^〉]*〉', '', text)
        text = re.sub(r'«[^»]*»', '', text)
        # 其他中文括号：『』、「」
        text = re.sub(r'『[^』]*』', '', text)
        text = re.sub(r'「[^」]*」', '', text)
        return text
    
    def _remove_markdown_links(self, text: str) -> str:
        """移除 markdown 链接和图片"""
        text = re.sub(r'!\[([^\]]*)\]\([^\)]+\)', '', text)  # 图片 ![alt](url)
        text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)  # 链接 [text](url)，保留文本
        return text
    
    def _remove_markdown_formatting(self, text: str) -> str:
        """移除 markdown 格式化标记"""
        # 移除标题标记（# 开头）
        text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
        
        # 移除列表标记（-、*、+ 开头）
        text = re.sub(r'^[\s]*[-*+]\s+', '', text, flags=re.MULTILINE)
        text = re.sub(r'^[\s]*\d+\.\s+', '', text, flags=re.MULTILINE)  # 有序列表
        
        # 移除引用标记（> 开头）
        text = re.sub(r'^>\s+', '', text, flags=re.MULTILINE)
        
        # 移除表格标记
        text = re.sub(r'\|', '', text)  # 表格分隔符
        text = re.sub(r'^[\s]*:?-+:?[\s]*$', '', text, flags=re.MULTILINE)  # 表格分隔行
        
        # 移除水平线和标题下划线
        text = re.sub(r'---+', '', text)
        text = re.sub(r'===+', '', text)
        
        return text
    
    def _remove_special_tokens(self, text: str) -> str:
        """移除特殊标记"""
        text = re.sub(r'<\|.*?\|>', '', text)
        return text
    
    def _convert_emphasis_to_quotes(self, text: str) -> str:
        """将强调标记转换为引号"""
        # 检测文本主要语言（简单启发式：中文字符占比）
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
        total_chars = len(re.sub(r'\s', '', text))
        is_chinese_dominant = total_chars > 0 and chinese_chars / total_chars > self.config.chinese_threshold
        
        # 根据语言选择合适的引号
        if is_chinese_dominant:
            if self.config.chinese_quote_style == '「」':
                quote_open = '「'
                quote_close = '」'
            else:
                quote_open = '"'
                quote_close = '"'
        else:
            if self.config.english_quote_style == '"':
                quote_open = '"'
                quote_close = '"'
            else:
                quote_open = "'"
                quote_close = "'"
        
        # 将强调标记转换为引号
        # 先处理粗体 **text** 和 __text__（需要完整配对）
        text = re.sub(r'\*\*([^*]+?)\*\*', rf'{quote_open}\1{quote_close}', text)
        text = re.sub(r'__([^_]+?)__', rf'{quote_open}\1{quote_close}', text)
        
        # 再处理斜体 *text* 和 _text_（但要避免匹配已处理的粗体）
        text = re.sub(r'(?<!\*)\*(?!\*)([^*\n]+?)(?<!\*)\*(?!\*)', rf'{quote_open}\1{quote_close}', text)
        text = re.sub(r'(?<!_)_(?!_)([^_\n]+?)(?<!_)_(?!_)', rf'{quote_open}\1{quote_close}', text)
        
        # 处理未配对的强调标记（增量文本中可能出现）
        # 移除未配对的标记符号，但保留其中的文本内容
        text = re.sub(r'\*\*([^*\n]+?)(?=\*\*|$)', r'\1', text)
        text = re.sub(r'__([^_\n]+?)(?=__|$)', r'\1', text)
        # 移除剩余的未配对标记符号
        text = re.sub(r'\*\*+', '', text)
        text = re.sub(r'__+', '', text)
        text = re.sub(r'(?<!\*)\*(?!\*)', '', text)  # 移除单个未配对的 *
        text = re.sub(r'(?<!_)_(?!_)', '', text)  # 移除单个未配对的 _
        
        return text
    
    def _clean_whitespace(self, text: str) -> str:
        """
        清理多余的空白字符
        
        策略：
        - 将多个连续空格合并为一个空格
        - 将换行符、制表符等替换为空格（TTS 不需要换行）
        - 清理多个连续空格
        - 不 strip 开头和结尾，保留必要的空格（特别是对于增量文本流）
        """
        # 将换行符、制表符等替换为空格
        text = re.sub(r'[\n\r\t]+', ' ', text)
        # 将多个连续空格合并为一个空格
        text = re.sub(r' +', ' ', text)
        return text


def create_text_filter(
    remove_brackets: bool = True,
    remove_code_blocks: bool = True,
    remove_markdown_links: bool = True,
    remove_markdown_formatting: bool = True,
    convert_emphasis_to_quotes: bool = True,
    remove_special_tokens: bool = True,
    chinese_quote_style: str = '「」',
    english_quote_style: str = '"',
    chinese_threshold: float = 0.3,
) -> TextFilter:
    """
    创建文本过滤器的工厂函数
    
    Args:
        remove_brackets: 是否移除各种括号及其中的内容
        remove_code_blocks: 是否移除代码块
        remove_markdown_links: 是否移除 markdown 链接和图片
        remove_markdown_formatting: 是否移除 markdown 格式化标记
        convert_emphasis_to_quotes: 是否将强调标记转换为引号
        remove_special_tokens: 是否移除特殊标记
        chinese_quote_style: 中文引号样式
        english_quote_style: 英文引号样式
        chinese_threshold: 判断文本为中文的阈值
        
    Returns:
        TextFilter 实例
    """
    config = TextFilterConfig(
        remove_brackets=remove_brackets,
        remove_code_blocks=remove_code_blocks,
        remove_markdown_links=remove_markdown_links,
        remove_markdown_formatting=remove_markdown_formatting,
        convert_emphasis_to_quotes=convert_emphasis_to_quotes,
        remove_special_tokens=remove_special_tokens,
        chinese_quote_style=chinese_quote_style,
        english_quote_style=english_quote_style,
        chinese_threshold=chinese_threshold,
    )
    return TextFilter(config)
