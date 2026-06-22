import random
import os

PRIME = 257

def deter(m):
    return (
    m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
    - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
    + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0])
    )

def inverse_matrix_mod(m, mod=PRIME):
    det = deter(m) % mod
    det_inv = pow(det, -1, mod)
    c = [[
            (m[1][1] * m[2][2] - m[1][2] * m[2][1]),
            -(m[1][0] * m[2][2] - m[1][2] * m[2][0]),
            (m[1][0] * m[2][1] - m[1][1] * m[2][0])
        ],[
            -(m[0][1] * m[2][2] - m[0][2] * m[2][1]),
            (m[0][0] * m[2][2] - m[0][2] * m[2][0]),
            -(m[0][0] * m[2][1] - m[0][1] * m[2][0])
        ],[
            (m[0][1] * m[1][2] - m[0][2] * m[1][1]),
            -(m[0][0] * m[1][2] - m[0][2] * m[1][0]),
            (m[0][0] * m[1][1] - m[0][1] * m[1][0])
        ]]
    adj = [[c[j][i] for j in range(3)]for i in range(3)]
    inverse = []
    for row in adj:
        new_row = []
        for value in row:
            new_row.append((value * det_inv) % mod)
        inverse.append(new_row)
    return inverse

def sequence(seed):

    x = seed

    while True:
        x = (
            x * x
            + 17 * x
            + 31
        ) % 2147483647
        yield x


def gen_matrix(seed):

    seq = sequence(seed)

    while True:
        matrix = [
            [
                (next(seq) % 50) + 1
                for _ in range(3)
            ]
            for _ in range(3)
        ]
        determinant = deter(matrix) % PRIME
        if determinant:
            return tuple(tuple(row)for row in matrix)


def matrix_vec_multi(matrix, vector):

    result = []

    for row in matrix:
        total = 0
        for i in range(3):
            total += row[i] * vector[i]
        result.append(total % PRIME)

    return result

def encrypt_file(in_path, out_path, seed):
    block_counter = 0

    with open(in_path, "r", encoding="utf-8") as inp,\
        open(out_path, "wb") as out:
        out.write(seed.to_bytes(8, "big"))
        block = []
        while True:
            char = inp.read(1)
            if not char:
                break
            block.append(ord(char))
            if len(block) == 3:
                key = gen_matrix(seed + block_counter)
                cipher = matrix_vec_multi(key, block)
                block_counter += 1
                for value in cipher:
                    out.write(value.to_bytes(2, "big"))
                block.clear()

        if block:
            while len(block) < 3:
                block.append(0)
            key = gen_matrix(seed + block_counter)
            cipher = matrix_vec_multi(key, block)
            block_counter += 1
            for value in cipher:
                out.write(value.to_bytes(2, "big"))

def decrypt_file(in_path, out_path):
    block_counter = 0

    with open(in_path, "rb") as inp:
        seed = int.from_bytes(inp.read(8), "big")
        with open(out_path, "w", encoding="utf-8") as out:
            while True:
                block = []
                for _ in range(3):
                    raw = inp.read(2)
                    if not raw:
                        break
                    block.append(int.from_bytes(raw, "big"))
                if len(block) != 3:
                    break
                key = gen_matrix(seed + block_counter)
                inv_key = inverse_matrix_mod(key)
                plain = matrix_vec_multi(
                    inv_key,
                    block
                )
                block_counter += 1
                for value in plain:
                    if value != 0:
                        out.write(chr(value))

    
if __name__ == "__main__":
    seed = 987654321

encrypt_file(
    "message.txt",
    "cipher.bin",
    seed
)

decrypt_file(
    "cipher.bin",
    "restored.txt"
)

os.system('cls')
'''with open("big.txt", "w") as f:
    f.write("Hello World\n" * 1_000_000)'''

with open("message.txt") as a:
    original = a.read()

with open("restored.txt") as b:
    restored = b.read()

print(original == restored)

