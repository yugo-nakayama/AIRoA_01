# AI Shape-Sorting Robot Arm (PAI Final Assignment)

Camera image -> AI (MLP) shape recognition -> inverse kinematics + PD control -> pick & place into bins.

## Demo (YouTube)
- https://youtu.be/hAfBYNnbS-E
- Local copies: `outputs/PAI_final_demo.mp4`, `outputs/PAI_final_demo_repro_01.mp4`

## Run
```bash
pip install -r requirements.txt
python vision.py   # generate synthetic data & train MLP (~15 s, CPU)
python main.py     # run 3 episodes, writes outputs/demo_raw.mp4 and outputs/results.json
ffmpeg -i outputs/demo_raw.mp4 -c:v libx264 -pix_fmt yuv420p outputs/demo.mp4
```
## Files
- `sim.py`    2-link planar arm (FK/IK, PD joint control), top-down camera renderer
- `vision.py` contour detection + MLP shape classifier (color/brightness-invariant silhouette feature)
- `main.py`   perception -> decision -> planning -> control loop, video recording
