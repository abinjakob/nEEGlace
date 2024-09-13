import pylsl
import numpy as np
import math
import time
from typing import List, Tuple
from pylsl import resolve_stream

# parameters for the plotting window
plotPeriod = 5  # time period to show (in seconds)

class Inlet:
    def __init__(self, info: pylsl.StreamInfo):
        self.inlet = pylsl.StreamInlet(info, max_buflen=plotPeriod, processing_flags=pylsl.proc_clocksync | pylsl.proc_dejitter)
        self.name = info.name()
        self.nchan = info.channel_count()
        # Initialize the buffer in the Inlet class
        bufsize = (2 * math.ceil(info.nominal_srate() * plotPeriod), info.channel_count())
        self.buffer = np.empty(bufsize, dtype=DataInlet.dtypes[info.channel_format()])
    
    def pull_data(self) -> Tuple[np.ndarray, np.ndarray]:
        # Pull data and return it
        _, ts = self.inlet.pull_chunk(timeout=0.0, max_samples=self.buffer.shape[0], dest_obj=self.buffer)
        return np.asarray(ts), self.buffer[:len(ts), :]

class DataInlet(Inlet):
    dtypes = [[], np.float32, np.float64, None, np.int32, np.int16, np.int8, np.int64]    

def connectstreams() -> List[DataInlet]:
    print("Looking for nEEGlace...")
    startTime = time.time()
    inlets: List[DataInlet] = []   
    while True:
        # 10s search period
        if time.time() - startTime > 10:
            print('No streams found..')
            break
        
        streams = resolve_stream('type', 'EEG')
        
        if streams:
            for info in streams:
                if info.nominal_srate() != pylsl.IRREGULAR_RATE and info.channel_format() != pylsl.cf_string:
                    print('Connected to nEEGlace')
                    inlets.append(DataInlet(info))
                    return inlets, info
                else:
                    print('nEEGlace not detected')
        else:
            print('No EEG streams found, retrying...')
        time.sleep(0.5)
    
    if not inlets:
        print('nEEGlace stream not detected')

    return inlets, info
