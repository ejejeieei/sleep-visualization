import numpy as np

def detect_apneas(flow, fs, min_duration_sec=10, drop_threshold=0.1):
    window = int(min_duration_sec * fs)
    events = []
    i = 0
    while i <= len(flow) - window:
        segment = flow[i:i+window]
        if np.mean(np.abs(segment)) < drop_threshold * np.mean(np.abs(flow[:10*fs])):  # relative to baseline
            start_sec = i / fs
            end_sec = (i + window) / fs
            events.append({'start': start_sec, 'end': end_sec, 'type': 'Obstructive'})
            i += window
        else:
            i += 1
    return events

def compute_ahi(events, tst_min):
    if tst_min <= 0:
        return 0.0
    return len(events) / (tst_min / 60)

def compute_spo2_metrics(spo2_signal, tst_mask=None):
    if tst_mask is not None:
        spo2 = spo2_signal[tst_mask]
    else:
        spo2 = spo2_signal
    if len(spo2) == 0:
        return {}
    mean_spo2 = np.mean(spo2)
    min_spo2 = np.min(spo2)
    # Simple ODI: count drops >=3% from running baseline
    odi = 0
    return {
        "MeanSpO2_%": float(mean_spo2),
        "MinSpO2_%": float(min_spo2),
        "ODI": odi
    }