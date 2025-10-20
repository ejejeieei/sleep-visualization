# frontend/app.py
import streamlit as st
import requests
import json
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(layout="wide", page_title="睡眠分析报告")
st.title("🧠 多模态睡眠分析系统")

# 上传文件
uploaded_file = st.file_uploader("上传 .edf 文件", type=["edf"])

if uploaded_file:
    with st.spinner("正在分析..."):
        try:
            files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
            res = requests.post("http://127.0.0.1:8000/api/analyze", files=files, timeout=60)
            if res.status_code == 200:
                data = res.json()
                metrics = data["metrics"]
                plot_json = data["plot"]

                # ========== 个人资料与记录信息 ==========
                st.header("📋 个人资料与记录信息")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("姓名", "黄浩")
                    st.metric("性别", "男")
                    st.metric("年龄", "29")
                with col2:
                    st.metric("关灯时间", "23:11:34")
                    st.metric("开灯时间", "03:50:14")
                    st.metric("总记录时间", f"{metrics.get('TIB_min', 'N/A')} 分钟")
                with col3:
                    st.metric("总睡眠时间", f"{metrics.get('TST_min', 'N/A')} 分钟")
                    st.metric("睡眠效率", f"{metrics.get('SleepEfficiency_%', 'N/A'):.1f}%")
                    st.metric("睡眠潜伏期", f"{metrics.get('SleepLatency_min', 'N/A')} 分钟")

                # ========== 睡眠分期表 ==========
                st.header("📊 睡眠分期")
                stage_data = metrics.get("StageDuration_min", {})
                df_stage = pd.DataFrame({
                    "睡眠阶段": ["清醒期 (W)", "REM期 (R)", "N1期", "N2期", "N3期"],
                    "持续时间 (分钟)": [
                        stage_data.get("W", 0),
                        stage_data.get("R", 0),
                        stage_data.get("N1", 0),
                        stage_data.get("N2", 0),
                        stage_data.get("N3", 0)
                    ],
                    "%睡眠时间": [
                        round(stage_data.get("W", 0) / metrics.get('TST_min', 1) * 100, 1) if metrics.get('TST_min', 0) > 0 else 0,
                        round(stage_data.get("R", 0) / metrics.get('TST_min', 1) * 100, 1) if metrics.get('TST_min', 0) > 0 else 0,
                        round(stage_data.get("N1", 0) / metrics.get('TST_min', 1) * 100, 1) if metrics.get('TST_min', 0) > 0 else 0,
                        round(stage_data.get("N2", 0) / metrics.get('TST_min', 1) * 100, 1) if metrics.get('TST_min', 0) > 0 else 0,
                        round(stage_data.get("N3", 0) / metrics.get('TST_min', 1) * 100, 1) if metrics.get('TST_min', 0) > 0 else 0
                    ]
                })
                st.dataframe(df_stage, width=True)

                # ========== 呼吸事件 ==========
                st.header("💨 呼吸事件")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("AHI (/hr)", f"{metrics.get('AHI', 0):.1f}")
                    st.metric("阻塞性次数", metrics.get('ApneaCount', 0))
                    st.metric("低通气次数", metrics.get('HypopneaCount', 0))
                with col2:
                    st.metric("打鼾总时间", f"{metrics.get('SnoreTime_min', 0):.0f} 分钟")
                    st.metric("打鼾次数", metrics.get('SnoreCount', 0))
                    st.metric("鼾声指数", f"{metrics.get('SnoreIndex', 0):.1f}")

                # ========== 血氧饱和度 ==========
                st.header("🩸 血氧饱和度")
                col1, col2 = st.columns(2)

                # 安全获取并格式化数值
                def safe_float(value, default="N/A"):
                    if value is None or value == "N/A":
                        return default
                    try:
                        return f"{float(value):.1f}"
                    except (ValueError, TypeError):
                        return default

                with col1:
                    st.metric("平均 SpO₂ (TST)", f"{safe_float(metrics.get('MeanSpO2_%'))}%")
                    st.metric("最低 SpO₂", f"{safe_float(metrics.get('MinSpO2_%'))}%")

                with col2:
                    st.metric("ODI (3%)", safe_float(metrics.get('ODI'), "0.0"))
                    st.metric("SpO₂ < 90% 时间", f"{safe_float(metrics.get('SpO2<90%_min'), '0.0')} 分钟")

                # ========== 心率 ==========
                st.header("❤️ 心率")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("平均心率", f"{metrics.get('MeanHR', 'N/A'):.0f} 次/分")
                with col2:
                    st.metric("最低心率", f"{metrics.get('MinHR', 'N/A'):.0f} 次/分")
                    st.metric("最高心率", f"{metrics.get('MaxHR', 'N/A'):.0f} 次/分")

                # ========== 微觉醒与肢体运动 ==========
                st.header("😴 微觉醒与肢体运动")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("微觉醒指数", f"{metrics.get('TotalArousalIndex', 0):.1f}")
                    st.metric("自发性微觉醒", f"{metrics.get('SpontaneousArousalIndex', 0):.1f}")
                with col2:
                    st.metric("PLM 指数", f"{metrics.get('PLMIndex', 0):.1f}")
                    st.metric("LM 指数", f"{metrics.get('LMIndex', 0):.1f}")

                # ========== 体位相关 AHI ==========
                st.header("🛏️ 体位相关 AHI")
                pos_ahi = {
                    "仰卧位": metrics.get("Supine_AHI", 0),
                    "左侧卧位": metrics.get("Left_AHI", 0),
                    "右侧卧位": metrics.get("Right_AHI", 0),
                    "俯卧位": metrics.get("Prone_AHI", 0)
                }
                df_pos = pd.DataFrame(list(pos_ahi.items()), columns=["体位", "AHI"])
                st.dataframe(df_pos,width=True)

                # ========== 图形概括 ==========
                st.header("📈 图形概括")

                # 从后端获取的 Plotly 图
                fig = go.Figure(plot_json)
                st.plotly_chart(fig, width=True)

                # ========== 概述与结论 ==========
                st.header("📝 概述与结论")
                overview = """
                患者在整夜睡眠中采用柔灵多模态睡眠呼吸监测系统进行监测，整夜监测信号良好，按照AASM manual的规则分析睡眠及相关事件。

                **睡眠结构**：睡眠效率正常，89.9%；睡眠潜伏期正常；REM期潜伏期缩短；睡眠中自发性微觉醒次数增加，清醒时间正常，睡眠结构紊乱，N3期睡眠比例增多，REM期睡眠比例减少。

                **呼吸事件**：AHI：9.6 轻度睡眠呼吸暂停，阻塞性睡眠呼吸暂停25次，低通气15次

                **血氧情况**：睡眠中平均血氧饱和度98%，最低血氧饱和度86%。

                **心电事件**：睡眠中平均心率63次/分，最慢心率50次/分，最快心率103次/分

                **特殊事件**：夜间周期性腿动指数：1.4
                """
                st.markdown(overview)

                conclusion = "**结论：**\n- 轻度阻塞性睡眠呼吸暂停\n- 低通气\n- 睡眠结构紊乱"
                st.success(conclusion)

                # ========== 医生签名 ==========
                st.header("👨‍⚕️ 医生签名")
                st.text_input("医生签名", value="张医生")
                st.date_input("报告日期", value=pd.to_datetime("2023-08-01"))

            else:
                st.error(f"分析失败: {res.text}")
        except Exception as e:
            st.error(f"请求失败: {e}")