import numpy as np

def compute_spo2_metrics(spo2, tst_mask=None):
    if tst_mask is not None:
        spo2 = spo2[tst_mask]
    if len(spo2) == 0:
        return {}
    mean_spo2 = np.mean(spo2)
    min_spo2 = np.min(spo2)
    odi = 0  # 简化
    thresholds = [95, 90, 85, 80, 70, 60, 50]
    time_below = {}
    for th in thresholds:
        dur_sec = np.sum(spo2 < th) * (len(spo2) / len(spo2))  # 假设 1Hz
        time_below[f"SpO2<{th}%_min"] = dur_sec / 60
    return {
        "MeanSpO2_%": float(mean_spo2),
        "MinSpO2_%": float(min_spo2),
        "ODI": odi,
        **time_below
    }