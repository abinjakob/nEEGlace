# -*- coding: utf-8 -*-
"""
Created on Thu May 23 17:31:28 2024

@author: messung
"""
# from pylsl import StreamInlet, resolve_stream, StreamInfo
# streams = resolve_stream('type', 'EEG')
# inlet = StreamInlet(streams[0])
# # retrieving sampling rate 
# srate = inlet.info().nominal_srate()
# try:
#     sample, timestamp = inlet.pull_sample(timeout= 5.0)
#     if sample:
#         print(sample)
#     else:
#         print('no sample')
# except Exception as e:
#     print(f'An error {e}')

from pylsl import StreamInlet, resolve_streams

# Resolve EEG streams on the network
print("Resolving EEG streams...")
streams = resolve_streams()

if len(streams) == 0:
    raise RuntimeError("No EEG streams found.")

# Print information about the resolved streams
for i, stream in enumerate(streams):
    print(f"\nStream {i}:")
    print(f"Name: {stream.name()}")
    print(f"Type: {stream.type()}")
    print(f"Channel Count: {stream.channel_count()}")
    print(f"Nominal Sampling Rate: {stream.nominal_srate()} Hz")
    print(f"Source ID: {stream.source_id()}")

# Create an inlet to read from the first found stream
print("Creating inlet to the first found stream...")
inlet = StreamInlet(streams[0])

# Retrieve the sampling rate of the stream
srate = inlet.info().nominal_srate()
print(f"Sampling rate: {srate}")

# Attempt to pull a sample from the stream with a timeout of 5 seconds
print("Attempting to pull a sample...")
try:
    sample, timestamp = inlet.pull_sample(timeout=5.0)
    if sample:
        print(f"Sample: {sample}, Timestamp: {timestamp}")
    else:
        print("No sample received within the timeout period. Retrying...")
        # Retry pulling the sample
        sample, timestamp = inlet.pull_sample(timeout=10.0)
        if sample:
            print(f"Sample: {sample}, Timestamp: {timestamp}")
        else:
            print("No sample received after retrying.")
except Exception as e:
    print(f"An error occurred: {e}")