def compute_arousal_metrics(hypno, total_sleep_min):
    # 实际需 EEG 频谱，此处用模拟值
    spontaneous = 46
    res = limb = plm = 0
    total = spontaneous + res + limb + plm
    hours = total_sleep_min / 60
    return {
        "TotalArousalIndex": total / hours,
        "SpontaneousArousalIndex": spontaneous / hours,
        "RespiratoryArousalIndex": res / hours,
        "LimbArousalIndex": limb / hours,
        "PLMArousalIndex": plm / hours
    }