from pydub import AudioSegment


def wav_to_bytes(input_wav_path, output_bin_path):
    # Read from wav file
    audio = AudioSegment.from_wav(input_wav_path)

    # Get the audio data in byte form
    audio_bytes = audio.raw_data

    # Write the byte data to a binary file
    with open(output_bin_path, 'wb') as bin_file:
        bin_file.write(audio_bytes)

    print(f"Audio data has been successfully converted and saved as a binary file: {output_bin_path}")


# Main function
def main():
    # Input WAV file path
    input_path = input('Please enter the path of wav file:(end with .wav) \n')
    input_wav_path = input_path  # Replace 'input.wav' with your WAV file path

    # Output binary file path
    output_path = input("Please enter the path of the output:(end with \) \n")
    output_bin_path = output_path + 'output_audio.bin'  # Replace 'output_audio.bin' with your desired binary file path

    # Convert WAV file to byte file
    wav_to_bytes(input_wav_path, output_bin_path)


if __name__ == '__main__':
    main()