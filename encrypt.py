import wave
import numpy as np
import secrets
import pickle
import math
import random
from sympy import *

# 1. Read the wav file
def read_wav(file_path):
    with wave.open(file_path, 'rb') as wav_file:
        params = wav_file.getparams()  # Get audio parameters
        frames = wav_file.readframes(params.nframes) # Read audio frames, return a bytes string
        audio_data = np.frombuffer(frames, dtype=np.int16)  # Assuming 16-bit depth
    return params, audio_data

# 2. Divide the audio_data to blocks
def divide_into_blocks(audio_data, block_size):
    # Calculate block number
    # blok_size - 1 to ensure if there's any remaining, will distribute an extra block
    num_blocks = (len(audio_data) + block_size - 1) // block_size
    # block size is 16, so 16*16bits = 256 bits for each block
    blocks = []
    for i in range(num_blocks):
        block = audio_data[i * block_size : (i + 1) * block_size] # [starting index : ending index]
        blocks.append(block)
    return blocks

# 3. Generate secrets
def generate_prime_candidate(bits):
    p = random.getrandbits(bits)
    p |= (1 << bits - 1) | 1  # Make sure it's odd and has the right number of bits
    return p

def generate_large_prime(bits):
    p = generate_prime_candidate(bits)
    while not isprime(p):
        p += 2
    return p

def generate_safe_prime(bits):
    while True:
        q = generate_large_prime(bits - 1)
        p = 2 * q + 1
        if isprime(p):
            return p, q

def find_generator(p, q):
    while True:
        g = random.randint(2, p-1)
        if pow(g, 2, p) != 1 and pow(g, q, p) != 1:
            return g

def key_generation(bits):
    p, q = generate_safe_prime(bits)
    g = find_generator(p, q)
    x = random.randint(2, p-2)  # private key
    y = pow(g, x, p)  # public key
    print(p)
    print(q)
    print(x)
    print(y)
    return (p, g, y), x

# 4. Encryption
def encrypt_blocks(public_key, blocks):
    p, g, y = public_key
    encrypted_blocks = []
    for block in blocks:
        # Convert block to bytes, then to integer
        block_bytes = block.tobytes()
        m = int.from_bytes(block_bytes, byteorder='big', signed=False)  # signed=False
        if m >= p:
            raise ValueError("The integer m must be less than prime p")
        # Encrypt
        k = secrets.randbelow(p - 2) + 1  # Random number k，1 < k < p - 1
        a = pow(g, k, p) # First part γ = g^k mod p
        b = (pow(y, k, p) * m) % p # Second part δ = (y^k * m) mod p
        encrypted_blocks.append((a, b))
    return encrypted_blocks

# 5. Save encrypted data
def save_encrypted_data(file_path, encrypted_blocks, params, block_size, public_key):
    # Create a dictionary data
    data = {
        'encrypted_blocks': encrypted_blocks,
        'params': params,
        'block_size': block_size,
        'public_key': public_key
    }
    # 'bin' for save as .bin file, 'wb' for ensure write in binary
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
    public_key, private_key = key_generation(512)

    # Encrypt audio data blocks
    encrypted_blocks = encrypt_blocks(public_key, blocks)

    # Save encrypted data
    output_file = 'encrypted_data.bin'  # Encrypted file output path
    save_encrypted_data(output_file, encrypted_blocks, params, block_size, public_key)

    # Save private key to a separate file
    private_key_file = 'private_key.bin'
    save_private_key(private_key_file, private_key)

    print(f"Encryption completed! The encrypted file has been save to {output_file}")
    print(f"Private key has been save to {private_key_file}")

if __name__ == '__main__':
    main()
