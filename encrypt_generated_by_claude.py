import wave
import random
from math import gcd

def is_prime(n, k=5):
    """Miller-Rabin primality test"""
    if n < 2: return False
    for p in [2,3,5,7,11,13,17,19,23,29]:
        if n % p == 0: return n == p
    s, d = 0, n-1
    while d % 2 == 0:
        s, d = s+1, d//2
    for i in range(k):
        x = pow(random.randint(2, n-1), d, n)
        if x == 1 or x == n-1: continue
        for r in range(s-1):
            x = pow(x, 2, n)
            if x == n-1: break
        else: return False
    return True

def generate_large_prime(bits):
    """Generate a large prime number"""
    while True:
        p = random.getrandbits(bits)
        if is_prime(p):
            return p

def find_primitive_root(p):
    """Find a primitive root modulo p"""
    if p == 2: return 1
    p1 = 2
    p2 = (p - 1) // p1
    while True:
        g = random.randint(2, p - 1)
        if not (pow(g, (p-1)//p1, p) == 1) and not (pow(g, (p-1)//p2, p) == 1):
            return g

def generate_keypair(bits=1024):
    """Generate p, g, and keypair"""
    p = generate_large_prime(bits)
    g = find_primitive_root(p)
    private_key = random.randint(1, p-2)
    public_key = pow(g, private_key, p)
    return p, g, public_key, private_key

def encrypt_audio(input_file, output_file, public_key, p, g):
    with wave.open(input_file, 'rb') as wav_file:
        params = wav_file.getparams()
        frames = wav_file.readframes(wav_file.getnframes())
    
    audio_data = list(frames)
    
    encrypted_data = []
    for sample in audio_data:
        k = random.randint(1, p-2)
        c1 = pow(g, k, p)
        c2 = (sample * pow(public_key, k, p)) % p
        encrypted_data.extend([c1, c2])
    
    with wave.open(output_file, 'wb') as encrypted_wav:
        encrypted_wav.setparams(params)
        encrypted_wav.writeframes(bytes(encrypted_data))

def decrypt_audio(input_file, output_file, private_key, p):
    with wave.open(input_file, 'rb') as encrypted_wav:
        params = encrypted_wav.getparams()
        encrypted_frames = encrypted_wav.readframes(encrypted_wav.getnframes())
    
    encrypted_data = list(encrypted_frames)
    
    decrypted_data = []
    for i in range(0, len(encrypted_data), 2):
        c1 = encrypted_data[i]
        c2 = encrypted_data[i+1]
        s = pow(c1, private_key, p)
        plain = (c2 * pow(s, p-2, p)) % p
        decrypted_data.append(plain)
    
    with wave.open(output_file, 'wb') as decrypted_wav:
        decrypted_wav.setparams(params)
        decrypted_wav.writeframes(bytes(decrypted_data))

def validate_audio(original_file, decrypted_file):
    with wave.open(original_file, 'rb') as original, wave.open(decrypted_file, 'rb') as decrypted:
        return original.readframes(original.getnframes()) == decrypted.readframes(decrypted.getnframes())

def main():
    # 生成p, g, 和密钥对
    p, g, public_key, private_key = generate_keypair()
    print(f"Generated prime p: {p}")
    print(f"Generated primitive root g: {g}")
    print(f"Public key: {public_key}")
    print(f"Private key: {private_key}")
    
    # 加密音频
    encrypt_audio('input.wav', 'encrypted.wav', public_key, p, g)
    
    # 解密音频
    decrypt_audio('encrypted.wav', 'decrypted.wav', private_key, p)
    
    # 验证
    if validate_audio('input.wav', 'decrypted.wav'):
        print("验证成功：解密后的音频与原始音频匹配")
    else:
        print("验证失败：解密后的音频与原始音频不匹配")

if __name__ == "__main__":
    main()
