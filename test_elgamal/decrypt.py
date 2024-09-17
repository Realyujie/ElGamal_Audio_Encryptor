import wave
import numpy as np
import pickle

# 1. 读取加密数据
def load_encrypted_data(file_path):
    with open(file_path, 'rb') as f:
        data = pickle.load(f)
    return data

# 2. 读取私钥
def load_private_key(file_path):
    with open(file_path, 'rb') as f:
        private_key = pickle.load(f)
    return private_key

# 3. 解密
def decrypt_blocks(private_key, public_key, encrypted_blocks, block_size):
    p, g, y = public_key
    x = private_key
    decrypted_blocks = []
    for a, b in encrypted_blocks:
        s = pow(a, x, p)
        # 计算 s 在模 p 下的乘法逆元
        try:
            s_inv = pow(s, -1, p)
        except ValueError:
            # 如果 s 与 p 不是互质，无法计算逆元
            raise ValueError("无法计算乘法逆元，解密失败。")
        m = (b * s_inv) % p
        # 将整数 m 转换回字节串，使用固定的字节长度
        block_bytes = m.to_bytes(block_size * 2, byteorder='big', signed=False)  # 改为固定字节长度，signed=False
        decrypted_blocks.append(block_bytes)
    return decrypted_blocks

# 4. 拼接并转换音频数据
def reconstruct_audio_data(decrypted_blocks, block_size, total_samples):
    audio_data = b''.join(decrypted_blocks)
    # 将字节串转换为 numpy 数组
    audio_data = np.frombuffer(audio_data, dtype=np.int16)
    # 截断到原始长度
    audio_data = audio_data[:total_samples]
    return audio_data

# 5. 保存解密后的 WAV 文件
def write_wav(file_path, params, audio_data):
    audio_data_bytes = audio_data.astype(np.int16).tobytes()
    with wave.open(file_path, 'wb') as wav_file:
        wav_file.setparams(params)
        wav_file.writeframes(audio_data_bytes)

# 验证解密结果
# def validate_decryption(original_audio_file, decrypted_audio_file):
#     # 读取原始音频数据
#     params_orig, audio_data_orig = read_wav(original_audio_file)
#     # 读取解密后的音频数据
#     params_decrypted, audio_data_decrypted = read_wav(decrypted_audio_file)
#     # 比较音频数据
#     if np.array_equal(audio_data_orig, audio_data_decrypted):
#         print("验证成功：解密后的音频与原始音频一致。")
#     else:
#         print("验证失败：解密后的音频与原始音频不一致。")

# 读取 WAV 文件（用于验证）
def read_wav(file_path):
    with wave.open(file_path, 'rb') as wav_file:
        params = wav_file.getparams()  # 获取音频参数
        frames = wav_file.readframes(params.nframes)
        audio_data = np.frombuffer(frames, dtype=np.int16)
    return params, audio_data

# 6. 主流程
def main():
    # 加密数据文件路径
    encrypted_file = 'encrypted_data.pkl'
    # 私钥文件路径
    private_key_file = 'private_key.pkl'

    # 读取加密数据
    data = load_encrypted_data(encrypted_file)
    encrypted_blocks = data['encrypted_blocks']
    params = data['params']
    block_size = data['block_size']
    public_key = data['public_key']

    # 读取私钥
    private_key = load_private_key(private_key_file)

    # 解密音频数据块
    decrypted_blocks = decrypt_blocks(private_key, public_key, encrypted_blocks, block_size)

    # 计算总采样点数
    total_samples = params.nframes * params.nchannels

    # 重构音频数据
    audio_data = reconstruct_audio_data(decrypted_blocks, block_size, total_samples)

    # 保存解密后的音频文件
    output_file = 'decrypted_output.wav'
    write_wav(output_file, params, audio_data)

    print(f"解密完成！解密后的音频文件已保存到 {output_file}")

    # 验证解密结果
    # original_audio_file = 'input.wav'
    # validate_decryption(original_audio_file, output_file)

if __name__ == '__main__':
    main()
