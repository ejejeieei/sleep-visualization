import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

def generate_plot(hypno, events=None, spo2=None, hr=None, position=None, epoch_sec=30):
    n = len(hypno)
    time_min = np.arange(n) * epoch_sec / 60
    fig = make_subplots(rows=5, cols=1, shared_xaxes=True, vertical_spacing=0.03,
                        row_heights=[0.4,0.15,0.15,0.15,0.15])
    stage_map = {'W':0,'N1':1,'N2':2,'N3':3,'R':4}
    y = [stage_map.get(s,0) for s in hypno]
    fig.add_trace(go.Scatter(x=time_min, y=y, mode='lines'), row=1, col=1)
    fig.update_yaxes(tickvals=list(stage_map.values()), ticktext=list(stage_map.keys()), row=1, col=1)
    if spo2 is not None:
        t_spo2 = np.linspace(0, time_min[-1], len(spo2))
        fig.add_trace(go.Scatter(x=t_spo2, y=spo2), row=2, col=1)
    if hr is not None:
        t_hr = np.linspace(0, time_min[-1], len(hr))
        fig.add_trace(go.Scatter(x=t_hr, y=hr), row=3, col=1)
    if events:
        for ev in events:
            fig.add_vrect(x0=ev['start']/60, x1=ev['end']/60, fillcolor='red', opacity=0.3, row=4, col=1)
    if position is not None:
        t_pos = np.linspace(0, time_min[-1], len(position))
        fig.add_trace(go.Scatter(x=t_pos, y=position, mode='lines'), row=5, col=1)
    fig.update_layout(height=1000, showlegend=False, xaxis_title="Time (min)")
    return fig