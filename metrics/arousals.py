def compute_arousal_metrics(hypno, total_sleep_min, spontaneous_count=0, res_count=0, limb_count=0, plm_count=0):
    total_hours = total_sleep_min / 60
    return {
        "TotalArousalIndex": (spontaneous_count + res_count + limb_count + plm_count) / total_hours,
        "SpontaneousArousalIndex": spontaneous_count / total_hours,
        "RespiratoryArousalIndex": res_count / total_hours,
        "LimbArousalIndex": limb_count / total_hours,
        "PLMArousalIndex": plm_count / total_hours
    }