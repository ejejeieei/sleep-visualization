import numpy as np

def detect_apneas(flow, fs, min_duration=10, threshold_ratio=0.1):
    baseline = np.mean(np.abs(flow[:int(10*fs)]))
    window = int(min_duration * fs)
    events = []
    i = 0
    while i <= len(flow) - window:
        if np.mean(np.abs(flow[i:i+window])) < threshold_ratio * baseline:
            start = i / fs
            end = (i + window) / fs
            events.append({'start': start, 'end': end, 'type': 'Obstructive'})
            i += window
        else:
            i += 1
    return events

def compute_respiratory_metrics(events, hypno, tst_min, epoch_sec=30):
    ahi = len(events) / (tst_min / 60) if tst_min > 0 else 0
    return {
        "AHI": ahi,
        "ApneaCount": len(events),
        "ApneaIndex": ahi,
        "SnoreTime_min": 0,  # 需音频，暂为0
        "SnoreCount": 0,
        "SnoreIndex": 0
    }