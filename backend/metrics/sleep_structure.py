import numpy as np

def compute_sleep_structure(hypno, lights_off_sec, lights_on_sec, epoch_sec=30):
    tib_sec = lights_on_sec - lights_off_sec
    sleep_mask = np.array(hypno) != 'W'
    if not np.any(sleep_mask):
        return {}
    first_sleep = np.where(sleep_mask)[0][0]
    last_sleep = np.where(sleep_mask)[0][-1]
    tst_epochs = np.sum(sleep_mask[first_sleep:last_sleep+1])
    tst_sec = tst_epochs * epoch_sec
    se = tst_sec / tib_sec * 100
    sl_sec = first_sleep * epoch_sec
    rem_after = hypno[first_sleep:]
    rem_idx = np.where(np.array(rem_after) == 'R')[0]
    rem_latency_sec = rem_idx[0] * epoch_sec if len(rem_idx) > 0 else None

    stage_dur = {}
    for stage in ['W', 'N1', 'N2', 'N3', 'R']:
        stage_dur[stage] = np.sum(np.array(hypno) == stage) * epoch_sec / 60

    return {
        "TIB_min": tib_sec / 60,
        "TST_min": tst_sec / 60,
        "SleepEfficiency_%": se,
        "SleepLatency_min": sl_sec / 60,
        "REMLatency_min": rem_latency_sec / 60 if rem_latency_sec else None,
        "StageDuration_min": stage_dur
    }