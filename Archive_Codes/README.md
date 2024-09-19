# Audio Conversion Scripts
This repository contains two Python scripts to convert between .wav audio files and binary files.

## Files
wav_to_bytes.py: Converts a WAV file into a binary file.  
bytes_to_wav.py: Converts a binary file back into a WAV file.  

## Before running
Ensure you have the following Python packages installed:  
**(1)pydub**  
**(2)numpy**

## Usage
### Please enter the input path of wav file: 
/path/to/testaudio.wav
### Please enter the input path of binary file: 
/path/to/output_audio.bin  
### Please enter the output path of wav file: 
/path/to/output/

**You can ignore the RuntimeWarning as it can run normally.**

## Attention
Do not change the audio configurations (parameters) part, it has already been tested by Yujie and it works well.

## About audio parameters
For example, a 44.1kHz frequency, 16bits depth audio:  
- 44100 times of sampling rate per second
- Each sample is represented using 16 bits of binary
- 2^16 = 65,536 possible values. The actual range is -32,768 to +32,767 (because 0 is included).
- Each sample takes up 2 bytes. One second of audio data takes up: 44,100 * 2 = 88,200 bytes ≈ 86.13 KB.
- For stereo, it's 172.27 KB/second