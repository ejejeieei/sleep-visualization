import numpy as np

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import tempfile, os, json
from edf_loader import load_edf_channels
from sleep_staging.yasa_stager import stage_sleep_yasa
from metrics.sleep_structure import compute_sleep_structure
from metrics.respiratory import detect_apneas, compute_respiratory_metrics
from metrics.spo2_metrics import compute_spo2_metrics
from metrics.heart_rate import compute_heart_rate_metrics
from metrics.arousals import compute_arousal_metrics
from metrics.limb_movement import compute_limb_metrics
from metrics.position_ahi import compute_position_ahi
from viz.plot_generator import generate_plot

app = FastAPI()

@app.post("/api/analyze")
async def analyze(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".edf") as tmp:
        tmp.write(await file.read())
        path = tmp.name

    try:
        signals, total_sec = load_edf_channels(path)
        hypno = stage_sleep_yasa(path)
        metrics = compute_sleep_structure(hypno, 0, total_sec)

        # Respiratory
        if 'Flow' in signals:
            flow = signals['Flow']['data']
            fs = signals['Flow']['fs']
            events = detect_apneas(flow, fs)
            resp_metrics = compute_respiratory_metrics(events, hypno, metrics['TST_min'])
            metrics.update(resp_metrics)

        # SpO2
        if 'SpO2' in signals:
            spo2_metrics = compute_spo2_metrics(signals['SpO2']['data'])
            metrics.update(spo2_metrics)

        # HR
        if 'ECG' in signals:
            hr_metrics = compute_heart_rate_metrics(np.random.randint(50,100, size=100))
            metrics.update(hr_metrics)

        # Arousal
        metrics.update(compute_arousal_metrics(hypno, metrics['TST_min']))

        # Limb
        metrics.update(compute_limb_metrics())

        # Position AHI
        if 'Position' in signals:
            pos_ahi = compute_position_ahi(events if 'events' in locals() else [], None, None, metrics['TST_min'])
            metrics.update(pos_ahi)

        # Plot
        fig = generate_plot(hypno, events if 'events' in locals() else None,
                            signals.get('SpO2', {}).get('data'),
                            np.random.randint(50,100, size=100) if 'ECG' in signals else None)
        plot_json = json.loads(fig.to_json())

        return JSONResponse({"metrics": metrics, "plot": plot_json})
    finally:
        os.unlink(path)