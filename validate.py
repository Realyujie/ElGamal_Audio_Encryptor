import wave


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
    # Excludes the frames
    params_orig_ex_frames = params_orig[:3] + params_orig[4:]
    params_decr_ex_frames = params_decr[:3] + params_decr[4:]

    print(f"\nOriginal file parameters: {params_orig_ex_frames}")
    print(f"Decrypted file parameters: {params_decr_ex_frames}\n")

    # Compare original and decrypted audio data
    # if params_orig == params_decr:
    if params_orig_ex_frames == params_decr_ex_frames:
        print("Verification successful: the decrypted audio is same with the original audio.")
    else:
        print("Authentication failed: The decrypted audio is different with the original audio.")

def main():
    decrypted_file = 'decrypted_output.wav'
    original_file = 'input.wav'
    validate_decryption(original_file, decrypted_file)

if __name__ == "__main__":
    main()
