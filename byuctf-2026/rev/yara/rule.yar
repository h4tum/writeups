rule fleg {    
    meta:
        description = "What is fleg?"
        author = "overllama"

    strings:
        $a = "\x76\x8d\xec" base64 // do3s - 64 6F 33 73
        $b = { 5F 7? ?4 ?4 ?E 6? 5F }
        $c = /byuctf.{33}/
        $d = { 77 ?8 79 }
        $e = { 72 ?F 74 }
        $f = { 73 5? 79 }
        $g = "EY\x05E\x0e" xor // th4t? - 74 68 34 74 3F
        $h = { 6? 30 72 }
        $i = { 7B 77 }
        $j = /\?{3}\}/ // 3F 3F 3F 7D
        $k = { 6? 79 5F 64 }
        $l = { 5F ?? 7? ?? 6E }
        $m = { 62 ?? ?? ?? ?? ?? ?? ?? 68 }
        $n = { 74 68 }
        $o = { 7? 6? 3? 7? 3F }
        $p = { 64 5f 66 }
        $q = "yara"

    condition:
        all of them and 
        uint32(21) == 0x6E347473 and
        uint16(28) == 0x7230 and
        uint16be(29) == 0x725F
}

