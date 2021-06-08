import matlab.engine
import numpy as np

engine = matlab.engine.start_matlab()
eng = matlab.engine.start_matlab()
a = matlab.double(np.array([1,4,9,16,25]).tolist())
b = eng.sqrt(a)
print(b)