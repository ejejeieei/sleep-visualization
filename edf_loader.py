import pyedflib
import numpy as np

def load_edf_channels(edf_path):
    with pyedflib.EdfReader(edf_path) as f:
        n = f.signals_in_file
        signal_labels = [label.strip().upper() for label in f.getSignalLabels()]
        fs_list = f.getSampleFrequencies()
        signals = {}
        for i in range(n):
            sig = f.readSignal(i)
            label = signal_labels[i]
            key = None
            if 'EEG' in label or 'FP1' in label or 'FP2' in label or 'FZ' in label:
                key = 'EEG'
            elif 'EOG' in label:
                key = 'EOG'
            elif 'EMG' in label or 'CHIN' in label:
                key = 'EMG'
            elif 'ECG' in label or 'EKG' in label:
                key = 'ECG'
            elif 'SPO2' in label or 'O2' in label:
                key = 'SpO2'
            elif 'FLOW' in label or 'NASAL' in label:
                key = 'Flow'
            elif 'THOR' in label or 'ABDO' in label:
                key = 'Thoracic'
            elif 'POSITION' in label or 'POS' in label:
                key = 'Position'
            elif 'LEG' in label:
                key = 'Leg_EMG'
            else:
                key = label
            if key in signals:
                key = f"{key}_{i}"
            signals[key] = {
                'data': sig.astype(np.float32),
                'fs': float(fs_list[i])
            }
    total_seconds = len(signals[list(signals.keys())[0]]['data']) / signals[list(signals.keys())[0]]['fs']
    return signals, total_seconds