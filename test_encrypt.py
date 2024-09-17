import random
from math import gcd

def generate_large_prime(bit_length):
    # 使用 Miller-Rabin 素性测试来生成大素数
    def is_prime(n, k=5):
        if n == 2 or n == 3:
            return True
        if n < 2 or n % 2 == 0:
            return False
        r, s = 0, n - 1
        while s % 2 == 0:
            r += 1
            s //= 2
        for _ in range(k):
            a = random.randrange(2, n - 1)
            x = pow(a, s, n)
            if x == 1 or x == n - 1:
                continue
            for _ in range(r - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False
        return True

    while True:
        p = random.getrandbits(bit_length)
        if is_prime(p):
            return p

def generate_keys(bit_length):
    p = generate_large_prime(bit_length)
    g = 2  # 使用2作为生成元，对于大多数素数来说都是可行的
    x = random.randint(1, p-2)  # 私钥
    h = pow(g, x, p)  # 公钥
    return ((p, g, h), x)

def encrypt_block(m, public_key):
    p, g, h = public_key
    k = random.randint(1, p-2)
    c1 = pow(g, k, p)
    s = pow(h, k, p)
    c2 = (m * s) % p
    return (c1, c2)

def decrypt_block(c, private_key, p):
    c1, c2 = c
    s = pow(c1, private_key, p)
    m = (c2 * pow(s, p-2, p)) % p  # 使用费马小定理计算模逆
    return m

def encrypt_file(input_file, output_file, public_key):
    block_size = (public_key[0].bit_length() - 1) // 8  # 确保每个块小于 p
    with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        while True:
            block = f_in.read(block_size)
            if not block:
                break
            m = int.from_bytes(block, 'big')
            c1, c2 = encrypt_block(m, public_key)
            f_out.write(c1.to_bytes((public_key[0].bit_length() + 7) // 8, 'big'))
            f_out.write(c2.to_bytes((public_key[0].bit_length() + 7) // 8, 'big'))

def decrypt_file(input_file, output_file, private_key, p):
    block_size = (p.bit_length() + 7) // 8
    with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        while True:
            c1 = f_in.read(block_size)
            if not c1:
                break
            c2 = f_in.read(block_size)
            if not c2:
                break
            c1 = int.from_bytes(c1, 'big')
            c2 = int.from_bytes(c2, 'big')
            m = decrypt_block((c1, c2), private_key, p)
            f_out.write(m.to_bytes((p.bit_length() - 1) // 8, 'big'))

# 主程序
if __name__ == "__main__":
    # 生成密钥
    # public_key, private_key = generate_keys(2048)  # 使用2048位的密钥长度
    # p, g, h = public_key
    print(generate_large_prime(1024))

    # 加密文件
    # encrypt_file("audio.bin", "encrypted_audio.bin", public_key)
    # print("File encrypted successfully.")

    # 解密文件
    # decrypt_file("encrypted_audio.bin", "decrypted_audio.bin", private_key, p)
    # print("File decrypted successfully.")