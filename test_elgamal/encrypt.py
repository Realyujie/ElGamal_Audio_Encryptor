import wave
import numpy as np
import secrets
import pickle
from sympy import randprime

# 1. 读取 WAV 文件
def read_wav(file_path):
    with wave.open(file_path, 'rb') as wav_file:
        params = wav_file.getparams()  # 获取音频参数
        frames = wav_file.readframes(params.nframes)
        audio_data = np.frombuffer(frames, dtype=np.int16)  # 假设 16 位深度
    return params, audio_data

# 2. 分块处理音频数据
def divide_into_blocks(audio_data, block_size):
    num_blocks = (len(audio_data) + block_size - 1) // block_size  # 计算块数
    blocks = []
    for i in range(num_blocks):
        block = audio_data[i * block_size : (i + 1) * block_size]
        blocks.append(block)
    return blocks

# 3. 密钥生成
def generate_large_prime(bit_length):
    lower_bound = 1 << (bit_length - 1)
    upper_bound = (1 << bit_length) - 1
    p = randprime(lower_bound, upper_bound)
    return p

def key_generation(block_bit_length):
    p_bit_length = block_bit_length + 10  # p 的位长度比块的位长度大一些
    p = generate_large_prime(p_bit_length)
    g = 2  # 选择生成元 g，可以是 2 或 3
    x = secrets.randbelow(p - 2) + 1  # 私钥 x，1 < x < p - 1
    y = pow(g, x, p)  # 公钥 y
    public_key = (p, g, y)
    private_key = x
    return public_key, private_key

# 4. 加密
def encrypt_blocks(public_key, blocks):
    p, g, y = public_key
    encrypted_blocks = []
    for block in blocks:
        # 将块转换为字节串，再转换为整数
        block_bytes = block.tobytes()
        m = int.from_bytes(block_bytes, byteorder='big', signed=False)  # 改为 signed=False
        if m >= p:
            raise ValueError("明文 m 必须小于素数 p")
        # 加密
        k = secrets.randbelow(p - 2) + 1  # 随机数 k，1 < k < p - 1
        a = pow(g, k, p)
        b = (pow(y, k, p) * m) % p
        encrypted_blocks.append((a, b))
    return encrypted_blocks

# 5. 保存加密后的数据
def save_encrypted_data(file_path, encrypted_blocks, params, block_size, public_key):
    data = {
        'encrypted_blocks': encrypted_blocks,
        'params': params,
        'block_size': block_size,
        'public_key': public_key
    }
    with open(file_path, 'wb') as f:
        pickle.dump(data, f)

# **新增**：保存私钥
def save_private_key(file_path, private_key):
    with open(file_path, 'wb') as f:
        pickle.dump(private_key, f)

# 6. 主流程
def main():
    # 设置块大小（采样点数量）
    block_size = 16  # 可以根据需求调整

    # 读取原始音频文件
    input_file = 'input.wav'  # 输入的 WAV 文件路径
    params, audio_data = read_wav(input_file)

    # 分块处理音频数据
    blocks = divide_into_blocks(audio_data, block_size)

    # 计算每个块的位长度
    block_bit_length = 16 * block_size  # 每个采样点 16 位

    # 密钥生成
    public_key, private_key = key_generation(block_bit_length)

    # 加密音频数据块
    encrypted_blocks = encrypt_blocks(public_key, blocks)

    # 保存加密后的数据
    output_file = 'encrypted_data.pkl'  # 输出的加密文件路径
    save_encrypted_data(output_file, encrypted_blocks, params, block_size, public_key)

    # 保存私钥到单独的文件
    private_key_file = 'private_key.pkl'
    save_private_key(private_key_file, private_key)

    print(f"加密完成！加密数据已保存到 {output_file}")
    print(f"私钥已保存到 {private_key_file}，请妥善保管！")

if __name__ == '__main__':
    main()
