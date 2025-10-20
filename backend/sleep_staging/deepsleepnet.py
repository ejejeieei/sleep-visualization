import torch
import torch.nn as nn
import numpy as np
from scipy.signal import resample

class DeepSleepNet(nn.Module):
    def __init__(self, n_classes=5):
        super().__init__()
        self.fine_conv = nn.Sequential(
            nn.Conv1d(1, 64, kernel_size=50, stride=6, padding=25),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.MaxPool1d(8, stride=8),
            nn.Dropout(0.5),
            nn.Conv1d(64, 128, kernel_size=8, padding=4),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Conv1d(128, 128, kernel_size=8, padding=4),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Conv1d(128, 128, kernel_size=8, padding=4),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.MaxPool1d(4, stride=4),
            nn.Flatten()
        )
        self.coarse_conv = nn.Sequential(
            nn.Conv1d(1, 64, kernel_size=400, stride=50, padding=200),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.MaxPool1d(4, stride=4),
            nn.Dropout(0.5),
            nn.Conv1d(64, 128, kernel_size=6, padding=3),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Conv1d(128, 128, kernel_size=6, padding=3),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Conv1d(128, 128, kernel_size=6, padding=3),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.MaxPool1d(2, stride=2),
            nn.Flatten()
        )
        self.classifier = nn.Sequential(
            nn.Linear(128 * 9 + 128 * 32, 1024),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(1024, n_classes)
        )

    def forward(self, x):
        x_fine = self.fine_conv(x)
        x_coarse = self.coarse_conv(x)
        x = torch.cat([x_fine, x_coarse], dim=1)
        return self.classifier(x)

def load_deepsleepnet_model(model_path=None):
    model = DeepSleepNet(n_classes=5)
    if model_path:
        model.load_state_dict(torch.load(model_path, map_location='cpu'))
    model.eval()
    return model

def preprocess_epoch(eeg_epoch, target_fs=100, epoch_sec=30):
    current_len = len(eeg_epoch)
    current_fs = current_len / epoch_sec
    target_len = int(target_fs * epoch_sec)
    if abs(current_fs - target_fs) > 1:
        eeg_epoch = resample(eeg_epoch, target_len)
    return eeg_epoch.astype(np.float32)

def stage_sleep_deepsleepnet(eeg_signal, fs, model_path=None):
    model = load_deepsleepnet_model(model_path)
    epoch_sec = 30
    epoch_samples = int(fs * epoch_sec)
    n_epochs = len(eeg_signal) // epoch_samples
    hypno = []
    stage_map = {0: 'W', 1: 'N1', 2: 'N2', 3: 'N3', 4: 'R'}

    for i in range(n_epochs):
        start = i * epoch_samples
        end = start + epoch_samples
        epoch = eeg_signal[start:end]
        if len(epoch) < epoch_samples:
            break
        epoch = preprocess_epoch(epoch, target_fs=100, epoch_sec=30)
        x = torch.tensor(epoch).unsqueeze(0).unsqueeze(0)
        with torch.no_grad():
            logits = model(x)
            pred = torch.argmax(logits, dim=1).item()
        hypno.append(stage_map[pred])
    return hypno