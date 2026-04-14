"""
Token Buffer 单元测试

测试各种语言场景下的 token 缓冲和拼合逻辑
"""

import pytest
from token_buffer import (
    TokenBuffer,
    SentenceAwareTokenBuffer,
    create_token_buffer,
    get_char_type,
    CharType,
    is_immediate_sendable,
    is_word_char,
)


class TestCharTypeDetection:
    """测试字符类型检测"""
    
    def test_cjk_characters(self):
        """测试 CJK 字符识别"""
        assert get_char_type('中') == CharType.CJK
        assert get_char_type('国') == CharType.CJK
        assert get_char_type('日') == CharType.CJK
        assert get_char_type('本') == CharType.CJK
        assert get_char_type('語') == CharType.CJK  # 日文汉字
    
    def test_kana_characters(self):
        """测试日文假名识别"""
        assert get_char_type('あ') == CharType.KANA  # 平假名
        assert get_char_type('ア') == CharType.KANA  # 片假名
        assert get_char_type('の') == CharType.KANA
    
    def test_hangul_characters(self):
        """测试韩文识别"""
        assert get_char_type('한') == CharType.HANGUL
        assert get_char_type('국') == CharType.HANGUL
        assert get_char_type('어') == CharType.HANGUL
    
    def test_latin_characters(self):
        """测试拉丁字母识别"""
        assert get_char_type('a') == CharType.LATIN
        assert get_char_type('Z') == CharType.LATIN
        assert get_char_type('é') == CharType.LATIN
        assert get_char_type('ñ') == CharType.LATIN
    
    def test_cyrillic_characters(self):
        """测试西里尔字母识别"""
        assert get_char_type('а') == CharType.CYRILLIC
        assert get_char_type('Б') == CharType.CYRILLIC
        assert get_char_type('ж') == CharType.CYRILLIC
    
    def test_space_and_punctuation(self):
        """测试空格和标点识别"""
        assert get_char_type(' ') == CharType.SPACE
        assert get_char_type('\t') == CharType.SPACE
        assert get_char_type('\n') == CharType.SPACE
        assert get_char_type('.') == CharType.PUNCTUATION
        assert get_char_type('，') == CharType.PUNCTUATION
        assert get_char_type('。') == CharType.PUNCTUATION
    
    def test_numbers(self):
        """测试数字识别"""
        assert get_char_type('0') == CharType.NUMBER
        assert get_char_type('9') == CharType.NUMBER


class TestTokenBuffer:
    """测试 TokenBuffer 核心功能"""
    
    def test_english_word_buffering(self):
        """测试英文单词缓冲 - 模拟 LLM 拆分单词的情况"""
        buffer = TokenBuffer()
        
        # 模拟 "Hello world" 被拆成 "Hel", "lo ", "wor", "ld"
        result1 = buffer.process("Hel")
        assert result1 == ""  # 缓冲中，等待完整单词
        
        result2 = buffer.process("lo ")
        assert result2 == "Hello "  # 遇到空格，输出完整单词
        
        result3 = buffer.process("wor")
        assert result3 == ""  # 继续缓冲
        
        result4 = buffer.process("ld")
        assert result4 == ""  # 继续缓冲
        
        # 最后 flush
        final = buffer.flush()
        assert final == "world"
    
    def test_chinese_immediate_output(self):
        """测试中文立即输出 - 中文字符无需缓冲"""
        buffer = TokenBuffer()
        
        # 中文一个个字符输入
        result1 = buffer.process("你")
        assert result1 == "你"
        
        result2 = buffer.process("好")
        assert result2 == "好"
        
        result3 = buffer.process("世界")
        assert result3 == "世界"
        
        # flush 应该为空
        assert buffer.flush() == ""
    
    def test_japanese_mixed(self):
        """测试日语混合文本 - 汉字和假名"""
        buffer = TokenBuffer()
        
        result = buffer.process("私は学生です")
        assert result == "私は学生です"  # 日文应该立即输出
    
    def test_mixed_chinese_english(self):
        """测试中英混合 - 如 "今天是sunny day" """
        buffer = TokenBuffer()
        
        # "今天是sun" -> 中文立即输出，"sun"缓冲
        result1 = buffer.process("今天是sun")
        assert result1 == "今天是"  # 中文输出，英文缓冲
        
        # "ny " -> 和之前的 "sun" 拼接，输出 "sunny "
        result2 = buffer.process("ny ")
        assert result2 == "sunny "
        
        # "day" -> 缓冲
        result3 = buffer.process("day")
        assert result3 == ""
        
        # flush
        final = buffer.flush()
        assert final == "day"
    
    def test_punctuation_triggers_output(self):
        """测试标点符号触发输出"""
        buffer = TokenBuffer()
        
        result1 = buffer.process("Hello")
        assert result1 == ""  # 缓冲
        
        result2 = buffer.process(",")
        assert result2 == "Hello,"  # 标点触发输出
        
        result3 = buffer.process(" world")
        assert result3 == " "  # 空格输出，world 缓冲
        
        result4 = buffer.process("!")
        assert result4 == "world!"
    
    def test_empty_and_none_input(self):
        """测试空输入和 None 输入"""
        buffer = TokenBuffer()
        
        assert buffer.process(None) == ""
        assert buffer.process("") == ""
        assert buffer.process("Hello") == ""
        assert buffer.flush() == "Hello"
    
    def test_max_buffer_limit(self):
        """测试最大缓冲限制"""
        buffer = TokenBuffer(max_buffer_chars=10)
        
        # 输入超过限制的连续拉丁字符
        result = buffer.process("abcdefghijklmno")  # 15 个字符
        assert result == "abcdefghij"  # 前 10 个被强制输出
        assert buffer.flush() == "klmno"  # 剩余的
    
    def test_korean_immediate_output(self):
        """测试韩文立即输出"""
        buffer = TokenBuffer()
        
        result = buffer.process("안녕하세요")
        assert result == "안녕하세요"


class TestSentenceAwareTokenBuffer:
    """测试句子感知 TokenBuffer"""
    
    def test_sentence_split_chinese(self):
        """测试中文句子分割"""
        buffer = SentenceAwareTokenBuffer()
        
        result1 = buffer.process("你好。")
        assert result1 == "你好。"
        
        result2 = buffer.process("世界！")
        assert result2 == "世界！"
    
    def test_sentence_split_english(self):
        """测试英文句子分割"""
        buffer = SentenceAwareTokenBuffer()
        
        # "Hello world. " 被拆分输入
        result1 = buffer.process("Hel")
        assert result1 == ""
        
        result2 = buffer.process("lo ")
        assert result2 == ""  # 空格不是句末，继续等待
        
        result3 = buffer.process("world")
        assert result3 == ""
        
        result4 = buffer.process(". ")
        assert result4 == "Hello world. "  # 句号触发句子输出
    
    def test_clause_split_disabled(self):
        """测试禁用从句分割"""
        buffer = SentenceAwareTokenBuffer(split_on_clause=False)
        
        result1 = buffer.process("Hello, world")
        assert result1 == ""  # 逗号不触发分割（因为 split_on_clause=False）
        
        result2 = buffer.process(".")
        assert "Hello, world." in result2
    
    def test_clause_split_enabled(self):
        """测试启用从句分割"""
        buffer = SentenceAwareTokenBuffer(split_on_clause=True)
        
        result1 = buffer.process("你好，")
        assert result1 == "你好，"  # 中文逗号触发分割
        
        result2 = buffer.process("世界")
        assert result2 == ""
        
        result3 = buffer.process("。")
        assert result3 == "世界。"


class TestCreateTokenBuffer:
    """测试工厂函数"""
    
    def test_create_basic_buffer(self):
        """测试创建基础 buffer"""
        buffer = create_token_buffer()
        assert isinstance(buffer, TokenBuffer)
        assert not isinstance(buffer, SentenceAwareTokenBuffer)
    
    def test_create_sentence_aware_buffer(self):
        """测试创建句子感知 buffer"""
        buffer = create_token_buffer(sentence_aware=True)
        assert isinstance(buffer, SentenceAwareTokenBuffer)
    
    def test_create_with_custom_config(self):
        """测试自定义配置"""
        buffer = create_token_buffer(
            sentence_aware=True,
            split_on_clause=True,
            max_buffer_chars=50,
        )
        assert isinstance(buffer, SentenceAwareTokenBuffer)
        assert buffer.max_buffer_chars == 50
        assert buffer.split_on_clause is True


class TestRealWorldScenarios:
    """真实场景测试"""
    
    def test_llm_typical_output(self):
        """模拟 LLM 典型的 token 输出"""
        buffer = TokenBuffer()
        
        # 模拟 GPT 风格的 token 输出
        tokens = ["I", " am", " a", " large", " language", " model", "."]
        
        outputs = []
        for token in tokens:
            result = buffer.process(token)
            if result:
                outputs.append(result)
        
        final = buffer.flush()
        if final:
            outputs.append(final)
        
        full_text = "".join(outputs)
        assert full_text == "I am a large language model."
    
    def test_llm_chinese_output(self):
        """模拟 LLM 中文输出"""
        buffer = TokenBuffer()
        
        # 中文通常按字或词输出
        tokens = ["我", "是", "一个", "大", "语言", "模型", "。"]
        
        outputs = []
        for token in tokens:
            result = buffer.process(token)
            if result:
                outputs.append(result)
        
        final = buffer.flush()
        if final:
            outputs.append(final)
        
        full_text = "".join(outputs)
        assert full_text == "我是一个大语言模型。"
    
    def test_llm_mixed_output(self):
        """模拟 LLM 中英混合输出"""
        buffer = TokenBuffer()
        
        # 中英混合: "我是ChatGPT，很高兴认识你。"
        tokens = ["我是", "Chat", "GPT", "，", "很高兴", "认识", "你", "。"]
        
        outputs = []
        for token in tokens:
            result = buffer.process(token)
            if result:
                outputs.append(result)
        
        final = buffer.flush()
        if final:
            outputs.append(final)
        
        full_text = "".join(outputs)
        assert full_text == "我是ChatGPT，很高兴认识你。"
    
    def test_streaming_tts_simulation(self):
        """模拟流式 TTS 发送场景"""
        buffer = SentenceAwareTokenBuffer()
        
        # 模拟用户问 "What is AI?" 的回答
        tokens = [
            "Art", "ificial", " Int", "elli", "gence", 
            " is", " a", " branch", " of", " computer", " science", ".",
            " It", " aims", " to", " create", " intelligent", " machines", "."
        ]
        
        sentences_sent = []
        for token in tokens:
            result = buffer.process(token)
            if result:
                sentences_sent.append(result)
        
        final = buffer.flush()
        if final:
            sentences_sent.append(final)
        
        # 验证按句子分隔
        full_text = "".join(sentences_sent)
        assert "Artificial Intelligence is a branch of computer science." in full_text
        assert "It aims to create intelligent machines." in full_text


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
