import z3


def solve():
    s = z3.Solver()

    file = [z3.BitVec(f"file_{i}", 8) for i in range(46)]

    # Restrict to alphanumeric, underscore and braces to get the sensible flag
    for i in range(46):
        c = file[i]
        is_lower = z3.And(c >= ord("a"), c <= ord("z"))
        is_digit = z3.And(c >= ord("0"), c <= ord("9"))
        is_underscore = c == ord("_")
        is_brace = z3.Or(c == ord("{"), c == ord("}"))
        s.add(z3.Or(is_lower, is_digit, is_underscore, is_brace))

    # Force the 'b' character because modulo 256 arithmetic allows '2' as well
    # for the 'b3' part of 'c4n_b3_r3v3rs3_3ng1n33r3d'
    s.add(file[20] == ord("b"))

    # Prefix and Suffix
    prefix = b"byuctf{"
    for i, char in enumerate(prefix):
        s.add(file[i] == char)
    s.add(file[45] == ord("}"))

    # Indices checking for '3'
    indices_3 = [13, 21, 24, 26, 29, 31, 36, 37, 39]
    for idx in indices_3:
        s.add(file[idx] == ord("3"))

    # Extracted constraints from assembly
    s.add((file[34] * file[1]) == 41)
    s.add((file[40] * file[4]) == 80)
    s.add((file[12] * file[6]) == 145)
    s.add((file[36] * file[7]) == 233)
    s.add((file[26] * file[8]) == 41)
    s.add((file[45] * file[9]) == 170)
    s.add((file[24] * file[10]) == 130)
    s.add((file[38] * file[11]) == 210)
    s.add((file[27] * file[12]) == 22)
    s.add((file[42] * file[13]) == 28)
    s.add((file[0] * file[14]) == 6)
    s.add((file[25] * file[15]) == 202)
    s.add((file[32] * file[16]) == 138)
    s.add((file[41] * file[17]) == 76)
    s.add((file[18] * file[22]) == 210)
    s.add((file[19] * file[6]) == 165)
    s.add((file[20] * file[43]) == 96)
    s.add((file[1] * file[22]) == 231)
    s.add((file[23] * file[39]) == 182)
    s.add((file[15] * file[26]) == 237)
    s.add((file[28] * file[39]) == 233)
    s.add((file[30] * file[37]) == 237)
    s.add((file[4] * file[33]) == 172)
    s.add((file[17] * file[35]) == 88)
    s.add((file[37] * file[11]) == 195)
    s.add((file[16] * file[38]) == 22)
    s.add((file[8] * file[40]) == 236)
    s.add((file[22] * file[41]) == 65)
    s.add((file[43] * file[11]) == 48)
    s.add((file[2] * file[44]) == 240)

    if s.check() == z3.sat:
        m = s.model()
        flag = "".join(chr(m[file[i]].as_long()) for i in range(46))
        print("Flag:", flag)
    else:
        print("UNSAT")


if __name__ == "__main__":
    solve()
