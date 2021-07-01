### How to run?

The software is in two pieces.
1. The simulator (Matlab + OpenDSS)
2. The Learning Agent (Python RLLib)

For running the simulator on __Windows__:
1. Install Matlab
2. Install OpenDSS
3. Install Matlab engine on Python + Requirements
4. Run `remote_server.py`


For running the Learning Agent:
1. Run the simulator first.
2. Install Tensorflow + Torch + Ray + Requirements
3. Run `ray_test.py`.