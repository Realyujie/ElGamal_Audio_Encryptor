import wave
import numpy as np
import secrets
import pickle
from sympy import randprime

# 1. Read the wav file
def read_wav(file_path):
    with wave.open(file_path, 'rb') as wav_file:
        params = wav_file.getparams()  # Get audio parameters
        frames = wav_file.readframes(params.nframes)
        audio_data = np.frombuffer(frames, dtype=np.int16)  # Assuming 16-bit depth
    return params, audio_data

# 2. Divide the audio_data to blocks
def divide_into_blocks(audio_data, block_size):
    num_blocks = (len(audio_data) + block_size - 1) // block_size  # Calculate block number
    blocks = []
    for i in range(num_blocks):
        block = audio_data[i * block_size : (i + 1) * block_size]
        blocks.append(block)
    return blocks

# 3. Generate secrets
def generate_large_prime(bit_length):
    lower_bound = 1 << (bit_length - 1)
    upper_bound = (1 << bit_length) - 1
    p = randprime(lower_bound, upper_bound)
    return p

def key_generation(block_bit_length):
    p_bit_length = block_bit_length + 10  # p's bit length is slightly larger than block's bit length
    p = generate_large_prime(p_bit_length)
    g = 2  # Choose a generator g, could be 2 or 3
    x = secrets.randbelow(p - 2) + 1  # Private key x, 1 < x < p - 1
    y = pow(g, x, p)  # public key y
    public_key = (p, g, y)
    private_key = x
    return public_key, private_key

# 4. Encryption
def encrypt_blocks(public_key, blocks):
    p, g, y = public_key
    encrypted_blocks = []
    for block in blocks:
        # Convert block to bytes, then to integer
        block_bytes = block.tobytes()
        m = int.from_bytes(block_bytes, byteorder='big', signed=False)  # signed=False
        if m >= p:
            raise ValueError("Plaintext m must be less than prime p")
        # Encrypt
        k = secrets.randbelow(p - 2) + 1  # Random number k，1 < k < p - 1
        a = pow(g, k, p)
        b = (pow(y, k, p) * m) % p
        encrypted_blocks.append((a, b))
    return encrypted_blocks

# 5. Save encrypted data
def save_encrypted_data(file_path, encrypted_blocks, params, block_size, public_key):
    data = {
        'encrypted_blocks': encrypted_blocks,
        'params': params,
        'block_size': block_size,
        'public_key': public_key
    }
    with open(file_path, 'wb') as f:
        pickle.dump(data, f)

# Save private key as file
def save_private_key(file_path, private_key):
    with open(file_path, 'wb') as f:
        pickle.dump(private_key, f)

# 6. Main process
def main():
    # Set block size (number of samples)
    block_size = 16  # Change as needed

    # Read the original audio file
    input_file = 'input.wav'  # Input audio file path
    params, audio_data = read_wav(input_file)

    # Divide audio into blocks
    blocks = divide_into_blocks(audio_data, block_size)

    # Calculate bit length of each block
    block_bit_length = 16 * block_size  # 16 bits per sample

    # Key generation
    public_key, private_key = key_generation(block_bit_length)

    # Encrypt audio data blocks
    encrypted_blocks = encrypt_blocks(public_key, blocks)

    # Save encrypted data
    output_file = 'encrypted_data.pkl'  # Encrypted file output path
    save_encrypted_data(output_file, encrypted_blocks, params, block_size, public_key)

    # Save private key to a separate file
    private_key_file = 'private_key.pkl'
    save_private_key(private_key_file, private_key)

    print(f"Encryption completed! The encrypted file has been save to {output_file}")
    print(f"Private key has been save to {private_key_file}")

if __name__ == '__main__':
    main()
