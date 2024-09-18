import numpy as np
import wave

from test_encrypt import decrypt_file


# Read WAV file
def read_wav(file_path):
    with wave.open(file_path, 'rb') as wav_file:
        # Get audio parameters
        # Including: channels, sample width, framerate,frames, compress type, compress name
        params = wav_file.getparams()
        # frames = wav_file.readframes(wav_file.getnframes())
    return params

# Validate decryption result
def validate_decryption(original_file, decrypted_file):
    # Read original audio data
    params_orig = read_wav(original_file)
    # Read decrypted audio data
    params_decr = read_wav(decrypted_file)

    print(f"\nOriginal file parameters: {params_orig}")
    print(f"Decrypted file parameters: {params_decr}\n")

    # Compare original and decrypted audio data
    # if params_orig == params_decr:
    if params_orig == params_decr:
        print("Verification successful: the decrypted audio is same with the original audio.")
    else:
        print("Authentication failed: The decrypted audio is different with the original audio.")

def main():
    decrypted_file = 'decrypted_output.wav'
    original_file = 'input.wav'
    validate_decryption(original_file, decrypted_file)

if __name__ == "__main__":
    main()
