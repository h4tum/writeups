def solve():
    # The flag has 39 characters based on $c = /byuctf.{33}/
    flag = bytearray(39)

    # Standard flag format
    flag[0:6] = b"byuctf"
    flag[6] = ord("{")

    # $i = { 7B 77 } -> "{w" at offset 6
    flag[6:8] = b"{w"

    # $m = { 62 ?? ?? ?? ?? ?? ?? ?? 68 } -> starts with 'b' (0) and ends with 'h' (8)
    flag[8] = ord("h")

    # $d = { 77 ?8 79 } -> "why" matching 'w' at offset 7
    flag[7:10] = b"why"

    # $k = { 6? 79 5F 64 } -> "?y_d". We have 'y' at 9, so this is 8..11 ("hy_d")
    flag[8:12] = b"hy_d"

    # $a = "\x76\x8d\xec" base64 -> base64 string matches "do3s"
    # Base64 of 'do3s' is v\x8d\xec, so the target string is 'do3s'
    flag[11:15] = b"do3s"

    # $f = { 73 5? 79 } -> "s_y". We have 's' at 14, so this is 14..16
    flag[14:17] = b"s_y"

    # $q = "yara". We have 'y' at 16, so this is 16..20
    flag[16:20] = b"yara"

    # uint32(21) == 0x6E347473 (little endian "st4n") -> offset 21..24
    flag[21:25] = b"st4n"

    # $l = { 5F ?? 7? ?? 6E } -> "_st4n". We have "st4n" at 21..24, so this is 20..24
    flag[20:25] = b"_st4n"

    # $b = { 5F 7? ?4 ?4 ?E 6? 5F } -> "_st4nd_". We have "_st4n" at 20..24, so this is 20..27
    flag[20:27] = b"_st4nd_"

    # $p = { 64 5f 66 } -> "d_f". We have "d_" at 25..26, so this is 25..28
    flag[25:28] = b"d_f"

    # uint16(28) == 0x7230 (little endian "0r") -> offset 28..29
    flag[28:30] = b"0r"

    # uint16be(29) == 0x725F (big endian "r_") -> offset 29..30
    flag[29:31] = b"r_"

    # $e = { 72 ?F 74 } -> "r_t". We have "r_" at 29..30, so this is 29..32
    flag[29:32] = b"r_t"

    # $g = "EY\x05E\x0e" xor (key 0x31) -> "th4t?". We have 't' at 31, so this is 31..36
    flag[31:36] = b"th4t?"

    # $j = /\?{3}\}/ -> "???}". We have '?' at 35, so this is 35..39
    flag[35:39] = b"???}"

    return flag.decode()


if __name__ == "__main__":
    print("Found Flag:", solve())
