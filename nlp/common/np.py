
from config import GPU

if GPU:
    raise NotImplementedError("GPU support is not implemented yet.")
else:
    import numpy as np