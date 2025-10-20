import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

def plot_sleep_report(hypno, events=None, spo2=None, hr=None, position=None, leg_movements=None, epoch_sec=30):
    n_epochs = len(hypno)
    time_min = np.arange(n_epochs) * epoch_sec / 60

    fig = make_subplots(
        rows=5, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.04,
        row_heights=[0.4, 0.15, 0.15, 0.15, 0.15],
        subplot_titles=("Sleep Stages", "SpO2 (%)", "Heart Rate (BPM)", "Respiratory Events", "Body Position")
    )

    stage_map = {'W': 0, 'N1': 1, 'N2': 2, 'N3': 3, 'R': 4}
    y_hypno = [stage_map.get(s, 0) for s in hypno]
    fig.add_trace(go.Scatter(x=time_min, y=y_hypno, mode='lines', line=dict(width=2), name='Stage'), row=1, col=1)
    fig.update_yaxes(tickvals=list(stage_map.values()), ticktext=list(stage_map.keys()), row=1, col=1)

    if spo2 is not None:
        spo2_time = np.linspace(0, time_min[-1], len(spo2))
        fig.add_trace(go.Scatter(x=spo2_time, y=spo2, line=dict(color='blue'), name='SpO2'), row=2, col=1)

    if hr is not None:
        hr_time = np.linspace(0, time_min[-1], len(hr))
        fig.add_trace(go.Scatter(x=hr_time, y=hr, line=dict(color='red'), name='HR'), row=3, col=1)

    if events:
        for ev in events:
            fig.add_vrect(x0=ev['start']/60, x1=ev['end']/60, fillcolor='red', opacity=0.3, row=4, col=1)

    if position is not None:
        pos_time = np.linspace(0, time_min[-1], len(position))
        fig.add_trace(go.Scatter(x=pos_time, y=position, mode='lines', name='Position'), row=5, col=1)

    fig.update_layout(height=1000, showlegend=False, xaxis_title="Time (min)")
    fig.update_xaxes(title_text="Time (min)", row=5, col=1)
    return fig