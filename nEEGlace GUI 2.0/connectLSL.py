# connect_stream.py
import pylsl
import time
import numpy as np
from typing import List, Tuple
from pylsl import resolve_stream
import sys


class Inlet:
    def __init__(self, info: pylsl.StreamInfo, plotPeriod: int):
        self.inlet = pylsl.StreamInlet(info, max_buflen=plotPeriod, processing_flags=pylsl.proc_clocksync | pylsl.proc_dejitter)
        self.name = info.name()
        self.nchan = info.channel_count()

class DataInlet(Inlet):
    dtypes = [[], np.float32, np.float64, None, np.int32, np.int16, np.int8, np.int64]    

    def __init__(self, info: pylsl.StreamInfo, plotPeriod: int):
        super().__init__(info, plotPeriod)
        bufsize = (2 * int(info.nominal_srate() * plotPeriod), info.channel_count())
        self.buffer = np.empty(bufsize, dtype=self.dtypes[info.channel_format()])

    def pull_data(self):
        # Pull data from the inlet
        _, ts = self.inlet.pull_chunk(timeout=0.0, max_samples=self.buffer.shape[0], dest_obj=self.buffer)
        return np.asarray(ts), self.buffer[:len(ts), :]
    
    def pullsample(self):
        # Pull a single sample and its timestamp
        sample, timestamp = self.inlet.pull_sample(timeout=0.0)
        return timestamp, sample
    
    def pullchunk(self):
        # Pull a single sample and its timestamp
        sample, timestamp = self.inlet.pull_chunk(timeout=0.0)
        return timestamp, sample

def connectstreams(plotPeriod: int = 5) -> Tuple[List[DataInlet], pylsl.StreamInfo]:
    print("Looking for nEEGlace...")
    startTime = time.time()
    inlets: List[DataInlet] = []
    
    while True:
        if time.time() - startTime > 10:
            print('No streams found..')
            break

        streams = resolve_stream('type', 'ExG')
        
        if streams:
            for info in streams:
                if info.nominal_srate() != pylsl.IRREGULAR_RATE and info.channel_format() != pylsl.cf_string:
                    print('Connected to nEEGlace')
                    inlets.append(DataInlet(info, plotPeriod))
                    return inlets, info
                else:
                    print('nEEGlace not detected')
        else:
            print('No EEG streams found, retrying...')
        
        time.sleep(0.5)
    
    if not inlets:
        print('nEEGlace stream not detected')
    
    return inlets, None
