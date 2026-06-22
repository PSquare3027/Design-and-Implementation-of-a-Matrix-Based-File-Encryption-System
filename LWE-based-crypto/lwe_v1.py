PRIME = 257

KEY = ((2, 3, 5),(4, 8, 1),(11, 6, 19))

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
    adj = [[c[j][i] for j in range(3)] for i in range(3)]
    inverse = []
    for row in adj:
        inverse_row = []
        for value in row:
            inverse_row.append(
                (value * det_inv) % mod
            )
        inverse.append(inverse_row)
    return inverse

INV_KEY = inverse_matrix_mod(KEY)

def mat_vec_mul(matrix, vector, mod=PRIME):

    result = []

    for row in matrix:
        total = 0
        for i in range(3):
            total += row[i] * vector[i]
        result.append(total % mod)
    return result

def encrypt_file(in_path, out_path):

    with open(in_path, "r", encoding="utf-8") as inp, \
        open(out_path, "wb") as out:
        block = []
        while True:
            char = inp.read(1)
            if not char:
                break
            block.append(ord(char))
            if len(block) == 3:
                cipher = mat_vec_mul(KEY, block)
                for value in cipher:
                    out.write(value.to_bytes(2, "big"))
                block.clear()
        if block:
            while len(block) < 3:
                block.append(0)
            cipher = mat_vec_mul(KEY, block)
            for value in cipher:
                out.write(value.to_bytes(2, "big"))


def decrypt_file(in_path, out_path):
    with open(in_path, "rb") as inp, \
        open(out_path, "w", encoding="utf-8") as out:
        while True:
            block = []
            for _ in range(3):
                raw = inp.read(2)
                if not raw:
                    break
                block.append(int.from_bytes(raw, "big"))
            if len(block) != 3:
                break
            plain = mat_vec_mul(INV_KEY,block)
            for value in plain:
                if value != 0:
                    out.write(chr(value))


if __name__ == "__main__":
    encrypt_file(
        "message.txt",
        "cipher.bin"
    )

    decrypt_file(
        "cipher.bin",
        "restored.txt"
    )
