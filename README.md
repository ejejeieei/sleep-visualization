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
```


```bash
sleep-analysis-system/                # 项目根目录
│
├── backend/                          # FastAPI 后端服务（提供 REST API）
│   ├── main.py                       # API 入口（/api/analyze）
│   ├── edf_loader.py                 # EDF 读取与通道映射
│   ├── sleep_staging/
│   │   ├── __init__.py
│   │   ├── yasa_stager.py            # YASA 睡眠分期（baseline）
│   │   └── deepsleepnet.py           # DeepSleepNet 推理（可选）
│   ├── metrics/
│   │   ├── __init__.py
│   │   ├── sleep_structure.py        # TIB, TST, SE, SL, REM latency 等
│   │   ├── respiratory.py            # AHI, 阻塞性/中枢性/混合性事件、打鼾
│   │   ├── spo2_metrics.py           # SpO₂ 平均/最低/ODI/各阈值时长
│   │   ├── heart_rate.py             # 平均/最低/最高心率
│   │   ├── arousals.py               # 微觉醒（自发性/呼吸/腿动/PLM）
│   │   ├── limb_movement.py          # PLM / LM 次数与指数
│   │   └── position_ahi.py           # 体位相关 AHI（仰卧/侧卧等）
│   └── viz/
│       └── plot_generator.py         # 生成 Plotly 图表（hypnogram + 趋势图）
│
├── frontend/                         # Streamlit 前端（用户界面）
│   └── app.py                        # 文件上传 + 调用 backend API + 展示结果
│
├── utils/                            # 全局工具与常量（跨前后端共享）
│   ├── __init__.py
│   └── aasm_rules.py                 # AASM 标准常量（如 EPOCH_SEC=30）
│
├── models/                           # 预训练模型文件（非代码）
│   └── README.md                     # 说明：存放 deepsleepnet.pth 等
│
├── data/                             # （可选）示例数据
│   └── sample.edf
│
├── requirements.txt                  # 所有依赖（backend + frontend）
├── README.md                         # 项目说明
└── .gitignore