def compute_position_ahi(events, position_signal, fs, tst_min):
    # 模拟：左侧卧 AHI=10.0，右侧卧=6.0
    return {
        "Supine_AHI": 0.0,
        "Left_AHI": 10.0,
        "Right_AHI": 6.0,
        "Prone_AHI": 0.0
    }