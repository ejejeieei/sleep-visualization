# app.py
import streamlit as st
import requests
import plotly.express as px
import plotly.graph_objects as go

BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="睡眠报告可视化系统", layout="wide")
st.title("🧠 睡眠报告可视化与算法交互平台")

# 初始化 session state
if "selected_report" not in st.sidebar.session_state:
    st.sidebar.session_state.selected_report = None

# 1. 数据选择面板
st.sidebar.header("📁 数据源管理")

# 获取已有报告
try:
    resp = requests.get(f"{BASE_URL}/api/reports")
    reports = resp.json()
except:
    reports = []
    st.sidebar.error("无法连接后端，请启动 FastAPI 服务")

report_labels = {r["report_id"]: r["label"] for r in reports}
selected_id = st.sidebar.selectbox(
    "选择报告",
    options=[""] + list(report_labels.keys()),
    format_func=lambda x: report_labels.get(x, "请选择...") if x else "请选择..."
)

if selected_id:
    st.sidebar.session_state.selected_report = selected_id

# 手动添加报告
with st.sidebar.expander("➕ 添加新报告"):
    data_path = st.text_input("数据路径（PDF）", value="/path/to/report.pdf")
    label = st.text_input("自定义标签", value="新报告")
    if st.button("添加"):
        res = requests.post(f"{BASE_URL}/api/reports", json={"data_path": data_path, "label": label})
        if res.status_code == 200:
            st.success("添加成功！请刷新页面")
        else:
            st.error("添加失败")

# 2. 主面板：指标可视化
if st.sidebar.session_state.selected_report:
    report_id = st.sidebar.session_state.selected_report
    try:
        metrics = requests.get(f"{BASE_URL}/api/reports/{report_id}/metrics").json()
    except:
        st.error("无法加载指标数据")
        metrics = {}

    if metrics:
        # 睡眠结构饼图
        st.subheader("🛌 睡眠结构")
        sleep_stages = {
            "REM": metrics.get("REM占比_%", 0),
            "N3": metrics.get("N3占比_%", 0),
            "N1+N2": 100 - metrics.get("REM占比_%", 0) - metrics.get("N3占比_%", 0)
        }
        fig_pie = px.pie(
            names=list(sleep_stages.keys()),
            values=list(sleep_stages.values()),
            title="睡眠分期占比"
        )
        st.plotly_chart(fig_pie, use_container_width=True)

        # 关键指标卡片
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("AHI", f"{metrics.get('AHI', 'N/A')}")
        col2.metric("睡眠效率 (%)", f"{metrics.get('睡眠效率_%', 'N/A')}")
        col3.metric("最低 SpO₂ (%)", f"{metrics.get('最低SpO2_%', 'N/A')}")
        col4.metric("微觉醒指数", f"{metrics.get('微觉醒指数_次_per_hr', 'N/A')}")

        # 算法交互
        st.subheader("⚙️ 算法分析")
        algo = st.selectbox("选择算法", ["ahi_prediction", "sleep_quality_score"])
        if st.button("运行算法"):
            res = requests.post(f"{BASE_URL}/api/algorithms/run", json={
                "algorithm": algo,
                "report_id": report_id,
                "params": {}
            })
            if res.ok:
                result = res.json()
                st.success(result["result"])
                if "visualization_data" in result:
                    data = result["visualization_data"]
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=data["ahi"],
                        title={'text': "AHI 风险等级"},
                        gauge={
                            'axis': {'range': [0, 40]},
                            'steps': [
                                {'range': [0, 5], 'color': "lightgreen"},
                                {'range': [5, 15], 'color': "yellow"},
                                {'range': [15, 30], 'color': "orange"},
                                {'range': [30, 40], 'color': "red"}
                            ]
                        }
                    ))
                    st.plotly_chart(fig)
            else:
                st.error("算法执行失败")

else:
    st.info("👈 请在左侧选择或添加一份睡眠报告")