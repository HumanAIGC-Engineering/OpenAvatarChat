"""
JSON 导出器

导出结构化的 VAD/EOU 分析数据，用于 AI 分析

分析目标：
- EOU 的核心作用是"守门员"——防止用户边思考边说时被 VAD 误截断
- Early VAD 的目的是快速检测用户真正说完时，尽早开始问答
"""
import json
from datetime import datetime
from typing import Any, Dict, List

from .analyzer_models import SessionAnalysis, UtteranceAnalysis


def export_json(session: SessionAnalysis, output_path: str):
    """导出 JSON 分析数据"""
    
    data = {
        "session_id": session.session_id,
        "analysis_timestamp": datetime.now().isoformat(),
        "session_time": {
            "start": session.start_time.isoformat() if session.start_time else None,
            "end": session.end_time.isoformat() if session.end_time else None,
        },
        "config": session.config,
        "summary": _build_summary(session),
        "eou_effect_analysis": _build_eou_effect_analysis(session),
        "utterances": [_build_utterance_data(u) for u in session.utterances],
        "ai_analysis_prompt": _build_ai_prompt(session)
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _build_summary(session: SessionAnalysis) -> Dict[str, Any]:
    """构建汇总数据"""
    return {
        "total_utterances": session.total_utterances,
        "avg_speech_duration_ms": session.avg_speech_duration_ms,
        "avg_early_to_end_delay_ms": session.avg_early_to_end_delay_ms,
        "avg_eou_decision_time_ms": session.avg_eou_decision_time_ms,
        "avg_total_latency_ms": session.avg_total_latency_ms,
        "eou_trigger_rate": session.eou_trigger_rate,
    }


def _build_eou_effect_analysis(session: SessionAnalysis) -> Dict[str, Any]:
    """构建 EOU 效果分析"""
    return {
        "effect_classification": {
            "accelerated": {
                "count": session.accelerated_count,
                "description": "EOU 正确触发，加速了短句/完整句的响应",
                "is_good": True
            },
            "protected": {
                "count": session.protected_count,
                "description": "EOU 正确未触发，保护了长句/思考中的语句不被截断",
                "is_good": True
            },
            "reconnected": {
                "count": session.reconnected_count,
                "description": "EOU 误判被重连机制自动修正，取消了错误的 stream 并重新开始",
                "is_good": True
            },
            "missed": {
                "count": session.missed_count,
                "description": "短句/完整句未被 EOU 加速，可能需要调低 threshold",
                "is_good": False
            },
            "false_trigger": {
                "count": session.false_trigger_count,
                "description": "EOU 可能误触发，截断了未完成的语句，可能需要调高 threshold",
                "is_good": False
            },
            "normal": {
                "count": session.normal_count,
                "description": "正常 VAD 结束，无 EOU 参与"
            }
        },
        "latency_comparison": {
            "avg_latency_with_eou_ms": session.avg_latency_with_eou_ms,
            "avg_latency_without_eou_ms": session.avg_latency_without_eou_ms,
            "total_time_saved_ms": session.total_time_saved_ms
        },
        "issues": session.issues,
        "issues_by_type": _group_issues_by_type(session.issues)
    }


def _group_issues_by_type(issues: List[Dict[str, Any]]) -> Dict[str, int]:
    """按类型分组统计问题"""
    counts = {}
    for issue in issues:
        issue_type = issue.get("type", "unknown")
        counts[issue_type] = counts.get(issue_type, 0) + 1
    return counts


def _build_utterance_data(utterance: UtteranceAnalysis) -> Dict[str, Any]:
    """构建单个语句的数据"""
    return {
        "id": utterance.utterance_id,
        "stream_key": utterance.stream_key,
        "asr_text": utterance.asr_text,
        
        # 语句分类
        "classification": {
            "utterance_type": utterance.utterance_type,
            "is_sentence_complete": utterance.is_sentence_complete,
            "eou_result_type": utterance.eou_result_type,
        },
        
        # 重连信息
        "reconnection": {
            "was_reconnected": utterance.was_reconnected,
            "cancelled_stream_key": utterance.cancelled_stream_key,
            "reconnect_time_gap_ms": utterance.reconnect_time_gap_ms,
        },
        
        # 时间线数据
        "timeline": {
            "speech_start_ms": utterance.speech_start_ms,
            "early_vad_end_ms": utterance.early_vad_end_ms,
            "speech_end_ms": utterance.speech_end_ms,
            "asr_completed_ms": utterance.asr_completed_ms,
        },
        
        # 计算指标
        "metrics": {
            "speech_duration_ms": utterance.speech_duration_ms,
            "early_to_end_delay_ms": utterance.early_to_end_delay_ms,
            "eou_decision_time_ms": utterance.eou_decision_time_ms,
            "total_latency_ms": utterance.total_latency_ms,
            "time_saved_ms": utterance.time_saved_ms,
        },
        
        # EOU 效果
        "eou_analysis": {
            "triggered": utterance.eou_triggered,
            "effective": utterance.eou_effective,
            "prediction_count": utterance.eou_prediction_count,
            "final_probability": utterance.eou_final_probability,
        },
        
        # 详细事件
        "events": {
            "vad": [
                {
                    "timestamp_ms": e.timestamp_ms,
                    "type": e.event_type,
                    "sample_id": e.sample_id,
                    "extra_data": e.extra_data
                }
                for e in utterance.vad_events
            ],
            "eou": [
                {
                    "timestamp_ms": e.timestamp_ms,
                    "type": e.event_type,
                    "prediction": e.prediction,
                    "probability": e.probability,
                    "buffer_duration_ms": e.buffer_duration_ms
                }
                for e in utterance.eou_events
            ],
            "asr": [
                {
                    "timestamp_ms": e.timestamp_ms,
                    "type": e.event_type,
                    "text": e.text,
                    "source": e.source
                }
                for e in utterance.asr_events
            ]
        }
    }


def _build_ai_prompt(session: SessionAnalysis) -> str:
    """构建 AI 分析提示"""
    
    # 提取配置信息
    vad_config = session.config.get("vad", {})
    eou_config = session.config.get("eou", {})
    
    prompt = f"""以下是 VAD/EOU 语音端点检测系统的分析数据，请评估其工作效果并提供优化建议。

## 系统目标说明
- **Early VAD** 的目的是快速检测用户真正说完时，尽早开始问答
- **EOU（End of Utterance）** 的作用是"守门员"——当用户在"边思考边说"时，防止 VAD 因为短暂停顿而误判为结束，导致用户的提问被截断

## 系统配置
- VAD end_delay: {vad_config.get('end_delay', 'N/A')} 样本
- VAD early_end_delay: {vad_config.get('early_end_delay', 'N/A')} 样本
- EOU threshold: {eou_config.get('threshold', 'N/A')}
- EOU max_buffer: {eou_config.get('max_buffer_seconds', 'N/A')} 秒

## EOU 效果统计
- 总语句数: {session.total_utterances}
- ✓ 加速响应: {session.accelerated_count} 次（EOU 正确触发，加快了短句响应）
- ✓ 保护长句: {session.protected_count} 次（EOU 正确未触发，避免截断思考中的用户）
- ↻ 重连修正: {session.reconnected_count} 次（EOU 误判被重连机制自动修正）
- ⚠ 漏触发: {session.missed_count} 次（短句未被 EOU 加速）
- ✗ 误触发: {session.false_trigger_count} 次（可能误截断未完成语句）

## 延迟对比
- EOU 加速时平均延迟: {f'{session.avg_latency_with_eou_ms:.0f}ms' if session.avg_latency_with_eou_ms else 'N/A'}
- 无 EOU 时平均延迟: {f'{session.avg_latency_without_eou_ms:.0f}ms' if session.avg_latency_without_eou_ms else 'N/A'}
- 总共节省时间: {session.total_time_saved_ms:.0f}ms

## 检测到的问题
"""
    
    if session.issues:
        issues_by_type = _group_issues_by_type(session.issues)
        for issue_type, count in issues_by_type.items():
            prompt += f"- {issue_type}: {count} 次\n"
    else:
        prompt += "- 无问题检测到\n"
    
    prompt += """
## 请分析以下内容:
1. **EOU 效果评估**：加速响应和保护长句的效果如何？漏触发和误触发的比例是否可接受？
2. **Threshold 调整建议**：
   - 如果漏触发较多（短句没被加速），建议降低 threshold
   - 如果误触发较多（可能截断了未完成的句子），建议提高 threshold
3. **Early VAD 配置**：early_end_delay 设置是否合适？是否能及时触发 EOU 检测？
4. **整体延迟**：EOU 加速效果是否明显？是否达到了减少响应延迟的目标？
5. **具体案例分析**：查看 utterances 中被标记为 "missed" 或 "false_trigger" 的案例，分析原因

详细事件数据请参考 utterances 字段。
"""
    
    return prompt
