"""
HTML 报告生成器

生成可视化的 VAD/EOU 分析报告

分析目标：
- EOU 的核心作用是"守门员"——防止用户边思考边说时被 VAD 误截断
- Early VAD 的目的是快速检测用户真正说完时，尽早开始问答
"""
import html
from typing import List

from .analyzer_models import SessionAnalysis, UtteranceAnalysis


def generate_html_report(session: SessionAnalysis, output_path: str):
    """生成 HTML 报告"""
    html_content = f"""<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VAD/EOU 分析报告 - {html.escape(session.session_id)}</title>
    <style>
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        .card {{
            background: white;
            border-radius: 16px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            margin-bottom: 24px;
            overflow: hidden;
        }}
        .card-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px 24px;
        }}
        .card-header h1 {{
            font-size: 24px;
            font-weight: 600;
        }}
        .card-header h2 {{
            font-size: 18px;
            font-weight: 500;
            opacity: 0.9;
        }}
        .card-body {{
            padding: 24px;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 16px;
            margin-bottom: 24px;
        }}
        .stat-item {{
            background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%);
            border-radius: 12px;
            padding: 20px;
            text-align: center;
        }}
        .stat-value {{
            font-size: 28px;
            font-weight: 700;
            color: #667eea;
        }}
        .stat-value.good {{
            color: #10b981;
        }}
        .stat-value.warning {{
            color: #f59e0b;
        }}
        .stat-value.bad {{
            color: #ef4444;
        }}
        .stat-label {{
            font-size: 13px;
            color: #666;
            margin-top: 8px;
        }}
        .timeline {{
            position: relative;
            padding: 20px 0;
        }}
        .timeline-bar {{
            height: 40px;
            background: #e4e8ec;
            border-radius: 8px;
            position: relative;
            margin-bottom: 8px;
            overflow: hidden;
        }}
        .timeline-fill {{
            position: absolute;
            height: 100%;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            border-radius: 8px;
        }}
        .timeline-marker {{
            position: absolute;
            top: 0;
            height: 100%;
            width: 3px;
            transform: translateX(-50%);
        }}
        .timeline-marker.speech-start {{
            background: #10b981;
        }}
        .timeline-marker.early-vad-end {{
            background: #f59e0b;
        }}
        .timeline-marker.speech-end {{
            background: #ef4444;
        }}
        .timeline-marker.eou-signal {{
            background: #8b5cf6;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            top: 50%;
            transform: translate(-50%, -50%);
        }}
        .timeline-marker.asr-complete {{
            background: #3b82f6;
        }}
        .timeline-legend {{
            display: flex;
            gap: 16px;
            flex-wrap: wrap;
            margin-top: 12px;
        }}
        .legend-item {{
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 12px;
            color: #666;
        }}
        .legend-color {{
            width: 16px;
            height: 16px;
            border-radius: 4px;
        }}
        .utterance-card {{
            border: 1px solid #e4e8ec;
            border-radius: 12px;
            margin-bottom: 16px;
            overflow: hidden;
        }}
        .utterance-card.accelerated {{
            border-color: #10b981;
            border-width: 2px;
        }}
        .utterance-card.protected {{
            border-color: #3b82f6;
            border-width: 2px;
        }}
        .utterance-card.reconnected {{
            border-color: #4f46e5;
            border-width: 2px;
        }}
        .utterance-card.false-trigger {{
            border-color: #ef4444;
            border-width: 2px;
        }}
        .utterance-header {{
            background: #f8f9fa;
            padding: 16px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid #e4e8ec;
        }}
        .utterance-title {{
            font-weight: 600;
            color: #333;
        }}
        .utterance-badges {{
            display: flex;
            gap: 8px;
        }}
        .badge {{
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 500;
        }}
        .badge-success {{
            background: #d1fae5;
            color: #059669;
        }}
        .badge-warning {{
            background: #fef3c7;
            color: #d97706;
        }}
        .badge-info {{
            background: #dbeafe;
            color: #2563eb;
        }}
        .badge-danger {{
            background: #fee2e2;
            color: #dc2626;
        }}
        .badge-secondary {{
            background: #f3f4f6;
            color: #6b7280;
        }}
        .utterance-body {{
            padding: 16px;
        }}
        .asr-text {{
            background: #f8f9fa;
            padding: 12px 16px;
            border-radius: 8px;
            font-size: 16px;
            color: #333;
            margin-bottom: 16px;
            border-left: 4px solid #667eea;
        }}
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
            gap: 12px;
        }}
        .metric-item {{
            background: #f8f9fa;
            padding: 12px;
            border-radius: 8px;
            text-align: center;
        }}
        .metric-value {{
            font-size: 18px;
            font-weight: 600;
            color: #667eea;
        }}
        .metric-label {{
            font-size: 11px;
            color: #666;
            margin-top: 4px;
        }}
        .issues-list {{
            border-radius: 8px;
            padding: 16px;
        }}
        .issue-item {{
            padding: 12px;
            border-radius: 8px;
            margin-bottom: 8px;
            font-size: 14px;
        }}
        .issue-item.warning {{
            background: #fef3c7;
            border: 1px solid #fcd34d;
            color: #92400e;
        }}
        .issue-item.info {{
            background: #dbeafe;
            border: 1px solid #93c5fd;
            color: #1e40af;
        }}
        .issue-item:last-child {{
            margin-bottom: 0;
        }}
        .config-section {{
            background: #f8f9fa;
            border-radius: 8px;
            padding: 16px;
        }}
        .config-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 12px;
        }}
        .config-item {{
            font-size: 14px;
        }}
        .config-key {{
            color: #666;
        }}
        .config-value {{
            font-weight: 500;
            color: #333;
        }}
        .effect-summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
            margin-bottom: 20px;
        }}
        .effect-card {{
            padding: 16px;
            border-radius: 12px;
            text-align: center;
        }}
        .effect-card.accelerated {{
            background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        }}
        .effect-card.protected {{
            background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
        }}
        .effect-card.missed {{
            background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        }}
        .effect-card.false-trigger {{
            background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        }}
        .effect-card.reconnected {{
            background: linear-gradient(135deg, #e0e7ff 0%, #c7d2fe 100%);
        }}
        .effect-count {{
            font-size: 36px;
            font-weight: 700;
        }}
        .effect-label {{
            font-size: 14px;
            margin-top: 4px;
        }}
        .effect-card.accelerated .effect-count {{ color: #059669; }}
        .effect-card.protected .effect-count {{ color: #2563eb; }}
        .effect-card.missed .effect-count {{ color: #d97706; }}
        .effect-card.false-trigger .effect-count {{ color: #dc2626; }}
        .effect-card.reconnected .effect-count {{ color: #4f46e5; }}
    </style>
</head>
<body>
    <div class="container">
        <!-- 标题卡片 -->
        <div class="card">
            <div class="card-header">
                <h1>VAD/EOU 分析报告</h1>
                <h2>Session: {html.escape(session.session_id)}</h2>
            </div>
            <div class="card-body">
                <div class="stats-grid">
                    <div class="stat-item">
                        <div class="stat-value">{session.total_utterances}</div>
                        <div class="stat-label">总语句数</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">{_format_ms(session.avg_speech_duration_ms)}</div>
                        <div class="stat-label">平均语音时长</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">{_format_ms(session.avg_eou_decision_time_ms)}</div>
                        <div class="stat-label">EOU 决策时间</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value good">{_format_ms(session.total_time_saved_ms)}</div>
                        <div class="stat-label">EOU 节省时间</div>
                    </div>
                </div>
                
                <p style="color: #666; font-size: 14px;">
                    开始时间: {session.start_time.strftime('%Y-%m-%d %H:%M:%S') if session.start_time else 'N/A'}<br>
                    结束时间: {session.end_time.strftime('%Y-%m-%d %H:%M:%S') if session.end_time else 'N/A'}
                </p>
            </div>
        </div>
        
        <!-- EOU 效果汇总 -->
        {_generate_effect_summary(session)}
        
        <!-- 问题列表 -->
        {_generate_issues_section(session)}
        
        <!-- 配置信息 -->
        {_generate_config_section(session)}
        
        <!-- 语句详情 -->
        <div class="card">
            <div class="card-header">
                <h2>语句详情</h2>
            </div>
            <div class="card-body">
                {_generate_utterances_section(session.utterances)}
            </div>
        </div>
        
        <!-- 时间线图例 -->
        <div class="card">
            <div class="card-body">
                <div class="timeline-legend">
                    <div class="legend-item">
                        <div class="legend-color" style="background: #10b981;"></div>
                        语音开始
                    </div>
                    <div class="legend-item">
                        <div class="legend-color" style="background: #f59e0b;"></div>
                        Early VAD End
                    </div>
                    <div class="legend-item">
                        <div class="legend-color" style="background: #ef4444;"></div>
                        语音结束
                    </div>
                    <div class="legend-item">
                        <div class="legend-color" style="background: #8b5cf6; border-radius: 50%;"></div>
                        EOU Signal
                    </div>
                    <div class="legend-item">
                        <div class="legend-color" style="background: #3b82f6;"></div>
                        ASR 完成
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        document.querySelectorAll('.utterance-card').forEach(card => {{
            card.querySelector('.utterance-header').addEventListener('click', () => {{
                card.classList.toggle('collapsed');
            }});
        }});
    </script>
</body>
</html>"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)


def _format_ms(value) -> str:
    """格式化毫秒值"""
    if value is None:
        return "N/A"
    return f"{value:.0f}ms"


def _format_percent(value) -> str:
    """格式化百分比"""
    if value is None:
        return "N/A"
    return f"{value * 100:.1f}%"


def _generate_effect_summary(session: SessionAnalysis) -> str:
    """生成 EOU 效果汇总"""
    return f"""
        <div class="card">
            <div class="card-header" style="background: linear-gradient(135deg, #10b981 0%, #059669 100%);">
                <h2>🎯 EOU 效果分析</h2>
            </div>
            <div class="card-body">
                <div class="effect-summary">
                    <div class="effect-card accelerated">
                        <div class="effect-count">{session.accelerated_count}</div>
                        <div class="effect-label">✓ 加速响应<br><small>EOU 正确触发，加快了短句响应</small></div>
                    </div>
                    <div class="effect-card protected">
                        <div class="effect-count">{session.protected_count}</div>
                        <div class="effect-label">✓ 保护长句<br><small>EOU 正确未触发，避免截断</small></div>
                    </div>
                    <div class="effect-card reconnected">
                        <div class="effect-count">{session.reconnected_count}</div>
                        <div class="effect-label">↻ 重连修正<br><small>误判被重连机制自动修正</small></div>
                    </div>
                    <div class="effect-card missed">
                        <div class="effect-count">{session.missed_count}</div>
                        <div class="effect-label">⚠ 漏触发<br><small>短句未被 EOU 加速</small></div>
                    </div>
                    <div class="effect-card false-trigger">
                        <div class="effect-count">{session.false_trigger_count}</div>
                        <div class="effect-label">✗ 误触发<br><small>可能误截断未完成语句</small></div>
                    </div>
                </div>
                
                <div class="stats-grid" style="margin-bottom: 0;">
                    <div class="stat-item">
                        <div class="stat-value">{_format_ms(session.avg_latency_with_eou_ms)}</div>
                        <div class="stat-label">EOU 加速时延迟</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">{_format_ms(session.avg_latency_without_eou_ms)}</div>
                        <div class="stat-label">无 EOU 时延迟</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">{_format_percent(session.eou_trigger_rate)}</div>
                        <div class="stat-label">EOU 触发率</div>
                    </div>
                </div>
            </div>
        </div>
    """


def _generate_issues_section(session: SessionAnalysis) -> str:
    """生成问题列表部分"""
    if not session.issues:
        return """
        <div class="card">
            <div class="card-header" style="background: linear-gradient(135deg, #10b981 0%, #059669 100%);">
                <h2>✓ 无问题检测到</h2>
            </div>
            <div class="card-body">
                <p style="color: #666;">VAD/EOU 系统运行正常，未检测到需要关注的问题。</p>
            </div>
        </div>
        """
    
    issues_html = []
    for issue in session.issues:
        severity = issue.get("severity", "info")
        issues_html.append(
            f'<div class="issue-item {severity}">#{issue.get("utterance_id", "?")} - {html.escape(issue.get("detail", ""))}</div>'
        )
    
    return f"""
        <div class="card">
            <div class="card-header" style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);">
                <h2>⚠️ 需要关注 ({len(session.issues)})</h2>
            </div>
            <div class="card-body">
                <div class="issues-list">
                    {''.join(issues_html)}
                </div>
            </div>
        </div>
    """


def _generate_config_section(session: SessionAnalysis) -> str:
    """生成配置信息部分"""
    vad_config = session.config.get("vad", {})
    eou_config = session.config.get("eou", {})
    
    config_items = []
    
    # VAD 配置
    if vad_config:
        config_items.append(f'<div class="config-item"><span class="config-key">VAD end_delay:</span> <span class="config-value">{vad_config.get("end_delay", "N/A")}</span></div>')
        config_items.append(f'<div class="config-item"><span class="config-key">VAD early_end_delay:</span> <span class="config-value">{vad_config.get("early_end_delay", "N/A")}</span></div>')
    
    # EOU 配置
    if eou_config:
        config_items.append(f'<div class="config-item"><span class="config-key">EOU threshold:</span> <span class="config-value">{eou_config.get("threshold", "N/A")}</span></div>')
        config_items.append(f'<div class="config-item"><span class="config-key">EOU max_buffer:</span> <span class="config-value">{eou_config.get("max_buffer_seconds", "N/A")}s</span></div>')
    
    if not config_items:
        return ""
    
    return f"""
        <div class="card">
            <div class="card-header" style="background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);">
                <h2>⚙️ 配置信息</h2>
            </div>
            <div class="card-body">
                <div class="config-section">
                    <div class="config-grid">
                        {''.join(config_items)}
                    </div>
                </div>
            </div>
        </div>
    """


def _get_result_badge(utterance: UtteranceAnalysis) -> str:
    """获取语句结果徽章"""
    result_type = utterance.eou_result_type
    
    if result_type == "accelerated":
        return '<span class="badge badge-success">✓ 加速</span>'
    elif result_type == "protected":
        return '<span class="badge badge-info">✓ 保护</span>'
    elif result_type == "reconnected":
        return '<span class="badge badge-info">↻ 重连修正</span>'
    elif result_type == "missed":
        return '<span class="badge badge-warning">⚠ 漏触发</span>'
    elif result_type == "false_trigger":
        return '<span class="badge badge-danger">✗ 误触发</span>'
    else:
        return '<span class="badge badge-secondary">正常</span>'


def _get_type_badge(utterance: UtteranceAnalysis) -> str:
    """获取语句类型徽章"""
    utype = utterance.utterance_type
    
    if utype == "short_complete":
        return '<span class="badge badge-info">短句</span>'
    elif utype == "long_thinking":
        return '<span class="badge badge-secondary">思考中</span>'
    elif utype == "long_complete":
        return '<span class="badge badge-secondary">长句</span>'
    else:
        return ''


def _generate_utterances_section(utterances: List[UtteranceAnalysis]) -> str:
    """生成语句详情部分"""
    if not utterances:
        return "<p style='color: #666;'>没有语句数据</p>"
    
    utterances_html = []
    
    for utterance in utterances:
        # 计算时间线范围
        all_times = []
        if utterance.speech_start_ms is not None:
            all_times.append(utterance.speech_start_ms)
        if utterance.speech_end_ms is not None:
            all_times.append(utterance.speech_end_ms)
        if utterance.asr_completed_ms is not None:
            all_times.append(utterance.asr_completed_ms)
        for event in utterance.vad_events:
            all_times.append(event.timestamp_ms)
        for event in utterance.eou_events:
            all_times.append(event.timestamp_ms)
        
        if not all_times:
            continue
        
        min_time = min(all_times)
        max_time = max(all_times)
        time_range = max_time - min_time if max_time > min_time else 1000
        
        # 生成时间线标记
        markers = []
        
        # VAD 事件标记
        for event in utterance.vad_events:
            pos = ((event.timestamp_ms - min_time) / time_range) * 100
            marker_class = {
                "speech_start": "speech-start",
                "early_vad_end": "early-vad-end",
                "speech_end": "speech-end"
            }.get(event.event_type, "")
            if marker_class:
                markers.append(f'<div class="timeline-marker {marker_class}" style="left: {pos:.1f}%;"></div>')
        
        # EOU 事件标记
        for event in utterance.eou_events:
            if event.event_type == "signal_sent":
                pos = ((event.timestamp_ms - min_time) / time_range) * 100
                markers.append(f'<div class="timeline-marker eou-signal" style="left: {pos:.1f}%;"></div>')
        
        # ASR 完成标记
        if utterance.asr_completed_ms is not None:
            pos = ((utterance.asr_completed_ms - min_time) / time_range) * 100
            markers.append(f'<div class="timeline-marker asr-complete" style="left: {pos:.1f}%;"></div>')
        
        # 语音填充区域
        fill_start = 0
        fill_end = 100
        if utterance.speech_start_ms is not None:
            fill_start = ((utterance.speech_start_ms - min_time) / time_range) * 100
        if utterance.speech_end_ms is not None:
            fill_end = ((utterance.speech_end_ms - min_time) / time_range) * 100
        
        # 获取徽章
        result_badge = _get_result_badge(utterance)
        type_badge = _get_type_badge(utterance)
        
        # ASR 文本
        asr_text_html = ""
        if utterance.asr_text:
            asr_text_html = f'<div class="asr-text">"{html.escape(utterance.asr_text)}"</div>'
        
        # 卡片额外样式
        card_class = ""
        if utterance.eou_result_type == "accelerated":
            card_class = "accelerated"
        elif utterance.eou_result_type == "protected":
            card_class = "protected"
        elif utterance.eou_result_type == "reconnected":
            card_class = "reconnected"
        elif utterance.eou_result_type == "false_trigger":
            card_class = "false-trigger"
        
        utterances_html.append(f"""
            <div class="utterance-card {card_class}">
                <div class="utterance-header">
                    <span class="utterance-title">语句 #{utterance.utterance_id}</span>
                    <div class="utterance-badges">
                        {type_badge}
                        {result_badge}
                    </div>
                </div>
                <div class="utterance-body">
                    {asr_text_html}
                    
                    <div class="timeline">
                        <div class="timeline-bar">
                            <div class="timeline-fill" style="left: {fill_start:.1f}%; width: {fill_end - fill_start:.1f}%;"></div>
                            {''.join(markers)}
                        </div>
                        <div style="display: flex; justify-content: space-between; font-size: 11px; color: #666;">
                            <span>{min_time:.0f}ms</span>
                            <span>{max_time:.0f}ms</span>
                        </div>
                    </div>
                    
                    <div class="metrics-grid">
                        <div class="metric-item">
                            <div class="metric-value">{_format_ms(utterance.speech_duration_ms)}</div>
                            <div class="metric-label">语音时长</div>
                        </div>
                        <div class="metric-item">
                            <div class="metric-value">{_format_ms(utterance.early_to_end_delay_ms)}</div>
                            <div class="metric-label">Early→End</div>
                        </div>
                        <div class="metric-item">
                            <div class="metric-value">{_format_ms(utterance.eou_decision_time_ms)}</div>
                            <div class="metric-label">EOU 决策</div>
                        </div>
                        <div class="metric-item">
                            <div class="metric-value">{_format_ms(utterance.total_latency_ms)}</div>
                            <div class="metric-label">总延迟</div>
                        </div>
                        <div class="metric-item">
                            <div class="metric-value">{f'{utterance.eou_final_probability:.2f}' if utterance.eou_final_probability else 'N/A'}</div>
                            <div class="metric-label">EOU 置信度</div>
                        </div>
                        <div class="metric-item">
                            <div class="metric-value">{_format_ms(utterance.time_saved_ms) if utterance.time_saved_ms else 'N/A'}</div>
                            <div class="metric-label">节省时间</div>
                        </div>
                    </div>
                </div>
            </div>
        """)
    
    return '\n'.join(utterances_html)
