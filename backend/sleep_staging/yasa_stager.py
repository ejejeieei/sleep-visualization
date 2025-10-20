import mne
import yasa

def stage_sleep_yasa(edf_path):
    raw = mne.io.read_raw_edf(edf_path, preload=True, verbose=False)
    eeg_ch = eog_ch = emg_ch = None
    for ch in raw.ch_names:
        ch_u = ch.upper()
        if 'FP' in ch_u or 'EEG' in ch_u:
            eeg_ch = ch
        elif 'EOG' in ch_u:
            eog_ch = ch
        elif 'EMG' in ch_u or 'CHIN' in ch_u:
            emg_ch = ch
    if eeg_ch is None:
        raise ValueError("No EEG channel found for staging")
    sls = yasa.SleepStaging(raw, eeg_name=eeg_ch, eog_name=eog_ch, emg_name=emg_ch)
    hypno = sls.predict()
    return hypno.tolist()