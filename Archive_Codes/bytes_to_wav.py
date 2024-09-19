from pydub import AudioSegment
import numpy as np


def bytes_to_wav(input_bin_path, output_wav_path, frame_rate, sample_width=2, channels=1):
    # Read byte data from binary file
    with open(input_bin_path, 'rb') as bin_file:
        audio_bytes = bin_file.read()

    # Convert byte data to a NumPy array
    audio_data = np.frombuffer(audio_bytes, dtype=np.int16)

    # Create an AudioSegment instance
    audio = AudioSegment(
        data=audio_data.tobytes(),
        sample_width=sample_width,
        frame_rate=frame_rate,
        channels=channels
    )

    # Export the AudioSegment instance as a WAV file
    audio.export(output_wav_path, format="wav")

    print(f"Binary file has been successfully converted and saved as a WAV file: {output_wav_path}")


# 主函数
def main():
    # Input binary file path
    input_path = input("Please enter the input path of binary file:(end with .bin) \n")
    input_bin_path = input_path  # Replace 'output_audio.bin' with your input file path

    # Output WAV file path
    output_path = input("Please enter the output path of wav file:(end with \) \n")
    output_wav_path = output_path + 'reconstructed.wav'  # Replace 'reconstructed.wav' with your output WAV file path

    # Set audio parameters
    frame_rate = 44100  # Frame rate of your original audio (Normally it's 44100)
    sample_width = 2  # Sample width (bytes) of your original audio (Normally it's 2 for 16bits audio)
    channels = 2  # Number of channels in your original audio (2 means stereo)

    # Convert binary file to WAV file
    bytes_to_wav(input_bin_path, output_wav_path, frame_rate, sample_width, channels)


if __name__ == '__main__':
    main()