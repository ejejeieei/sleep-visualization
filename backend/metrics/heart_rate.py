import numpy as np

def compute_heart_rate_metrics(hr_signal):
    if hr_signal is None or len(hr_signal) == 0:
        return {}
    return {
        "MeanHR": float(np.mean(hr_signal)),
        "MinHR": float(np.min(hr_signal)),
        "MaxHR": float(np.max(hr_signal))
    }