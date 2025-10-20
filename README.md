# 多模态睡眠分析 Web 系统

支持 `.edf` 格式多导联/单导联睡眠数据上传，自动分析并可视化：

- 睡眠分期（YASA / DeepSleepNet）
- 睡眠结构指标（TST, SE, SL, REM latency）
- 呼吸事件（AHI, 阻塞性/中枢性/混合性）
- 血氧（SpO₂, ODI）
- 心率
- 微觉醒指数
- 体位相关 AHI
- 腿动（PLM/LM）

## 运行

```bash
pip install -r requirements.txt
streamlit run app.py #streamlit命令需要在conda环境下执行