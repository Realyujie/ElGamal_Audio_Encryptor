import wave
import numpy as np
import pickle
import validate

# 1. Load encrypted data
def load_encrypted_data(file_path):
    with open(file_path, 'rb') as f:
        data = pickle.load(f)
    return data

# 2. Load private key
def load_private_key(file_path):
    with open(file_path, 'rb') as f:
        private_key = pickle.load(f)
    return private_key

# 3. Decryption
def decrypt_blocks(private_key, public_key, encrypted_blocks, block_size):
    p, g, y = public_key
    x = private_key
    decrypted_blocks = []
    for a, b in encrypted_blocks:
        s = pow(a, x, p)
        # Calculate the modular inverse of s modulo p
        try:
            s_inv = pow(s, -1, p)
        except ValueError:
            # If s and p are not coprime, cannot compute inverse
            raise ValueError("Cannot compute multiplicative inverse, decryption failed.")
        m = (b * s_inv) % p
        # Convert integer m back to bytes using fixed byte length
        block_bytes = m.to_bytes(block_size * 2, byteorder='big', signed=False)  # # Use fixed byte length, signed=False
        decrypted_blocks.append(block_bytes)
    return decrypted_blocks

# 4. Reconstruct and convert audio data
def reconstruct_audio_data(decrypted_blocks, block_size, total_samples):
    audio_data = b''.join(decrypted_blocks)
    # Convert byte string to numpy array
    audio_data = np.frombuffer(audio_data, dtype=np.int16)
    # Truncate to original length
    audio_data = audio_data[:total_samples]
    return audio_data

# 5. Save decrypted WAV file
def write_wav(file_path, params, audio_data):
    audio_data_bytes = audio_data.astype(np.int16).tobytes()
    with wave.open(file_path, 'wb') as wav_file:
        wav_file.setparams(params)
        wav_file.writeframes(audio_data_bytes)

# 6. Main process
def main():
    # Encrypted data file path
    encrypted_file = 'encrypted_data.bin'
    # Private key file path
    private_key_file = 'private_key.bin'

    # Load encrypted data
    data = load_encrypted_data(encrypted_file)
    encrypted_blocks = data['encrypted_blocks']
    params = data['params']
    block_size = data['block_size']
    public_key = data['public_key']

    # Load private key
    private_key = load_private_key(private_key_file)

    # Decrypt audio data blocks
    decrypted_blocks = decrypt_blocks(private_key, public_key, encrypted_blocks, block_size)

    # Calculate total number of samples
    total_samples = params.nframes * params.nchannels

    # Reconstruct audio data
    audio_data = reconstruct_audio_data(decrypted_blocks, block_size, total_samples)

    # Save decrypted audio file
    output_file = 'decrypted_output.wav'
    write_wav(output_file, params, audio_data)

    print(f"\nDecryption complete! Decrypted audio file saved to {output_file}")

    original_file = 'input.wav'  # Path to the original audio file
    validate.validate_decryption(original_file, output_file)

if __name__ == '__main__':
    main()
