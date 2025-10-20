def compute_position_ahi(events, position_signal, fs):
    # position_signal: 0=supine, 1=left, 2=right, 3=prone
    # Simplified: assume position is constant per epoch
    pos_ahi = {
        "Supine": {"AHI": 0.0, "duration_min": 0},
        "Left": {"AHI": 0.0, "duration_min": 0},
        "Right": {"AHI": 0.0, "duration_min": 0},
        "Prone": {"AHI": 0.0, "duration_min": 0}
    }
    return pos_ahi