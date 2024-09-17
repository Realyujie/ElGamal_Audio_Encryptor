import wave
import numpy as np
from Crypto.Util import number
from Crypto.Random import random

def generate_keys(bits=256):
    p = number.getPrime(bits)
    g = random.randint(2, p-1)
    x = random.randint(1, p-2)
    h = pow(g, x, p)
    return (p, g, h), x

def encrypt_audio(public_key, audio_data):
    p, g, h = public_key
    y = random.randint(1, p-2)
    c1 = pow(g, y, p)
    s = pow(h, y, p)
    encrypted_data = [(sample * s) % p for sample in audio_data]
    return c1, encrypted_data

def decrypt_audio(private_key, public_key, c1, encrypted_data):
    p, _, _ = public_key
    x = private_key
    s = pow(c1, x, p)
    s_inv = pow(s, -1, p)
    decrypted_data = [(sample * s_inv) % p for sample in encrypted_data]
    return decrypted_data

def audio_to_int_array(audio_file):
    with wave.open(audio_file, 'rb') as wav:
        params = wav.getparams()
        frames = wav.readframes(params.nframes)
        audio_data = np.frombuffer(frames, dtype=np.int16)
    return audio_data, params

def int_array_to_audio(audio_data, params, output_file):
    with wave.open(output_file, 'wb') as wav:
        wav.setparams(params)
        wav.writeframes(audio_data.astype(np.int16).tobytes())

# Key generation
public_key, private_key = generate_keys()

# Encryption
input_file = "input.wav"
audio_data, params = audio_to_int_array(input_file)
c1, encrypted_data = encrypt_audio(public_key, audio_data)

# Decryption
decrypted_data = decrypt_audio(private_key, public_key, c1, encrypted_data)

# Save decrypted audio
output_file = "decrypted.wav"
int_array_to_audio(np.array(decrypted_data), params, output_file)

# Validation
original_data, _ = audio_to_int_array(input_file)
decrypted_data = np.array(decrypted_data)

integrity_check = np.array_equal(original_data, decrypted_data)
print(f"Integrity check: {'Passed' if integrity_check else 'Failed'}")

if not integrity_check:
    mse = np.mean((original_data - decrypted_data) ** 2)
    print(f"Mean Squared Error: {mse}")
