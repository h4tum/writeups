TEXT main.(*program).run(SB) /home/macen/ctf/overllama/homebrew/rev/service/main.go
  main.go:88		0x6376c0		4c8d6424a0			LEAQ -0x60(SP), R12				
  main.go:88		0x6376c5		4d3b6610			CMPQ R12, 0x10(R14)				
  main.go:88		0x6376c9		0f86e9090000			JBE 0x6380b8					
  main.go:88		0x6376cf		55				PUSHQ BP					
  main.go:88		0x6376d0		4889e5				MOVQ SP, BP					
  main.go:88		0x6376d3		4881ecd8000000			SUBQ $0xd8, SP					
  main.go:90		0x6376da		440f11bc24a8000000		MOVUPS X15, 0xa8(SP)				
  main.go:90		0x6376e3		440f11bc24b8000000		MOVUPS X15, 0xb8(SP)				
  main.go:90		0x6376ec		48c78424b000000012000000	MOVQ $0x12, 0xb0(SP)				
  main.go:90		0x6376f8		488d150dc60700			LEAQ 0x7c60d(IP), DX				
  main.go:90		0x6376ff		48899424a8000000		MOVQ DX, 0xa8(SP)				
  main.go:90		0x637707		48c78424c000000008000000	MOVQ $0x8, 0xc0(SP)				
  main.go:90		0x637713		488d1523940700			LEAQ 0x79423(IP), DX				
  main.go:90		0x63771a		48899424b8000000		MOVQ DX, 0xb8(SP)				
  path.go:131		0x637722		488d8424a8000000		LEAQ 0xa8(SP), AX				
  path.go:131		0x63772a		bb02000000			MOVL $0x2, BX					
  path.go:131		0x63772f		4889d9				MOVQ BX, CX					
  path.go:131		0x637732		e8097cedff			CALL path/filepath.join(SB)			
  main.go:91		0x637737		e8e4baebff			CALL os.ReadFile(SB)				
  main.go:91		0x63773c		0f1f4000			NOPL 0(AX)					
  main.go:92		0x637740		4885ff				TESTQ DI, DI					
  main.go:92		0x637743		0f8570010000			JNE 0x6378b9					
  main.go:91		0x637749		48899c2498000000		MOVQ BX, 0x98(SP)				
  main.go:91		0x637751		48898424a0000000		MOVQ AX, 0xa0(SP)				
  main.go:96		0x637759		48c74424500d000000		MOVQ $0xd, 0x50(SP)				
  main.go:96		0x637762		48c744245815000000		MOVQ $0x15, 0x58(SP)				
  main.go:96		0x63776b		48c744246018000000		MOVQ $0x18, 0x60(SP)				
  main.go:96		0x637774		48c74424681a000000		MOVQ $0x1a, 0x68(SP)				
  main.go:96		0x63777d		48c74424701d000000		MOVQ $0x1d, 0x70(SP)				
  main.go:96		0x637786		48c74424781f000000		MOVQ $0x1f, 0x78(SP)				
  main.go:96		0x63778f		48c784248000000024000000	MOVQ $0x24, 0x80(SP)				
  main.go:96		0x63779b		48c784248800000025000000	MOVQ $0x25, 0x88(SP)				
  main.go:96		0x6377a7		48c784249000000027000000	MOVQ $0x27, 0x90(SP)				
  main.go:97		0x6377b3		440f11bc24c8000000		MOVUPS X15, 0xc8(SP)				
  main.go:97		0x6377bc		0f1f4000			NOPL 0(AX)					
  main.go:97		0x6377c0		e81baee3ff			CALL runtime.convTslice(SB)			
  main.go:97		0x6377c5		488d1574a70100			LEAQ 0x1a774(IP), DX				
  main.go:97		0x6377cc		48899424c8000000		MOVQ DX, 0xc8(SP)				
  main.go:97		0x6377d4		48898424d0000000		MOVQ AX, 0xd0(SP)				
  main.go:97		0x6377dc		488d056fca0700			LEAQ 0x7ca6f(IP), AX				
  main.go:97		0x6377e3		bb13000000			MOVL $0x13, BX					
  main.go:97		0x6377e8		488d8c24c8000000		LEAQ 0xc8(SP), CX				
  main.go:97		0x6377f0		bf01000000			MOVL $0x1, DI					
  main.go:97		0x6377f5		4889fe				MOVQ DI, SI					
  main.go:97		0x6377f8		e8238dfbff			CALL github.com/charmbracelet/log.Infof(SB)	
  main.go:98		0x6377fd		488d442430			LEAQ 0x30(SP), AX				
  main.go:98		0x637802		488b9c24a0000000		MOVQ 0xa0(SP), BX				
  main.go:98		0x63780a		488b8c2498000000		MOVQ 0x98(SP), CX				
  main.go:98		0x637812		e84955e2ff			CALL runtime.slicebytetostring(SB)		
  strings.go:517	0x637817		90				NOPL						
  strings.go:17		0x637818		4883fb07			CMPQ BX, $0x7					
  strings.go:17		0x63781c		7c78				JL 0x637896					
  strings.go:17		0x63781e		488d1d04880700			LEAQ 0x78804(IP), BX				
  strings.go:17		0x637825		b907000000			MOVL $0x7, CX					
  strings.go:17		0x63782a		e8f1f9dcff			CALL runtime.memequal(SB)			
  strings.go:17		0x63782f		84c0				TESTL AL, AL					
  main.go:98		0x637831		7463				JE 0x637896					
  main.go:102		0x637833		31c0				XORL AX, AX					
  main.go:102		0x637835		488b9c24a0000000		MOVQ 0xa0(SP), BX				
  main.go:102		0x63783d		488b8c2498000000		MOVQ 0x98(SP), CX				
  main.go:102		0x637845		e81655e2ff			CALL runtime.slicebytetostring(SB)		
  main.go:102		0x63784a		e83150edff			CALL strings.Fields(SB)				
  main.go:102		0x63784f		4885db				TESTQ BX, BX					
  main.go:102		0x637852		0f8655080000			JBE 0x6380ad					
  main.go:102		0x637858		488378082e			CMPQ 0x8(AX), $0x2e				
  main.go:103		0x63785d		7514				JNE 0x637873					
  main.go:103		0x63785f		488b9424a0000000		MOVQ 0xa0(SP), DX				
  main.go:103		0x637867		488b8c2498000000		MOVQ 0x98(SP), CX				
  main.go:103		0x63786f		31c0				XORL AX, AX					
  main.go:103		0x637871		eb52				JMP 0x6378c5					
  main.go:104		0x637873		488d0586db0100			LEAQ 0x1db86(IP), AX				
  main.go:104		0x63787a		488d1d2fab0d00			LEAQ 0xdab2f(IP), BX				
  main.go:104		0x637881		31c9				XORL CX, CX					
  main.go:104		0x637883		31ff				XORL DI, DI					
  main.go:104		0x637885		4889fe				MOVQ DI, SI					
  main.go:104		0x637888		e8538bfbff			CALL github.com/charmbracelet/log.Error(SB)	
  main.go:105		0x63788d		4881c4d8000000			ADDQ $0xd8, SP					
  main.go:105		0x637894		5d				POPQ BP						
  main.go:105		0x637895		c3				RET						
  main.go:99		0x637896		488d0563db0100			LEAQ 0x1db63(IP), AX				
  main.go:99		0x63789d		488d1d0cab0d00			LEAQ 0xdab0c(IP), BX				
  main.go:99		0x6378a4		31c9				XORL CX, CX					
  main.go:99		0x6378a6		31ff				XORL DI, DI					
  main.go:99		0x6378a8		4889fe				MOVQ DI, SI					
  main.go:99		0x6378ab		e8308bfbff			CALL github.com/charmbracelet/log.Error(SB)	
  main.go:100		0x6378b0		4881c4d8000000			ADDQ $0xd8, SP					
  main.go:100		0x6378b7		5d				POPQ BP						
  main.go:100		0x6378b8		c3				RET						
  main.go:94		0x6378b9		4881c4d8000000			ADDQ $0xd8, SP					
  main.go:94		0x6378c0		5d				POPQ BP						
  main.go:94		0x6378c1		c3				RET						
  main.go:107		0x6378c2		48ffc0				INCQ AX						
  main.go:107		0x6378c5		4883f809			CMPQ AX, $0x9					
  main.go:107		0x6378c9		7d43				JGE 0x63790e					
  main.go:108		0x6378cb		4c8b44c450			MOVQ 0x50(SP)(AX*8), R8				
  main.go:108		0x6378d0		4c39c1				CMPQ CX, R8					
  main.go:108		0x6378d3		0f86cc070000			JBE 0x6380a5					
  main.go:108		0x6378d9		460fb60402			MOVZX 0(DX)(R8*1), R8				
  main.go:108		0x6378de		6690				NOPW						
  main.go:108		0x6378e0		4180f833			CMPL R8, $0x33					
  main.go:108		0x6378e4		74dc				JE 0x6378c2					
  main.go:108		0x6378e6		488d0513db0100			LEAQ 0x1db13(IP), AX				
  main.go:108		0x6378ed		488d1dbcaa0d00			LEAQ 0xdaabc(IP), BX				
  main.go:108		0x6378f4		31c9				XORL CX, CX					
  main.go:108		0x6378f6		31ff				XORL DI, DI					
  main.go:108		0x6378f8		4889fe				MOVQ DI, SI					
  main.go:108		0x6378fb		0f1f440000			NOPL 0(AX)(AX*1)				
  main.go:108		0x637900		e8db8afbff			CALL github.com/charmbracelet/log.Error(SB)	
  main.go:108		0x637905		4881c4d8000000			ADDQ $0xd8, SP					
  main.go:108		0x63790c		5d				POPQ BP						
  main.go:108		0x63790d		c3				RET						
  main.go:111		0x63790e		4883f901			CMPQ CX, $0x1					
  main.go:111		0x637912		0f8681070000			JBE 0x638099					
  main.go:111		0x637918		0f1f840000000000		NOPL 0(AX)(AX*1)				
  main.go:111		0x637920		4883f922			CMPQ CX, $0x22					
  main.go:111		0x637924		0f8665070000			JBE 0x63808f					
  main.go:111		0x63792a		440fb64201			MOVZX 0x1(DX), R8				
  main.go:111		0x63792f		440fb64a22			MOVZX 0x22(DX), R9				
  main.go:111		0x637934		450fafc8			IMULL R8, R9					
  main.go:111		0x637938		0f1f840000000000		NOPL 0(AX)(AX*1)				
  main.go:111		0x637940		4180f929			CMPL R9, $0x29					
  main.go:111		0x637944		0f850d070000			JNE 0x638057					
  main.go:114		0x63794a		4883f928			CMPQ CX, $0x28					
  main.go:114		0x63794e		0f8631070000			JBE 0x638085					
  main.go:114		0x637954		440fb64a04			MOVZX 0x4(DX), R9				
  main.go:114		0x637959		440fb65228			MOVZX 0x28(DX), R10				
  main.go:114		0x63795e		4589d3				MOVL R10, R11					
  main.go:114		0x637961		450fafd1			IMULL R9, R10					
  main.go:114		0x637965		4180fa50			CMPL R10, $0x50					
  main.go:114		0x637969		0f85c5060000			JNE 0x638034					
  main.go:116		0x63796f		440fb65206			MOVZX 0x6(DX), R10				
  main.go:116		0x637974		440fb6620c			MOVZX 0xc(DX), R12				
  main.go:116		0x637979		4589e5				MOVL R12, R13					
  main.go:116		0x63797c		450fafe2			IMULL R10, R12					
  main.go:116		0x637980		4180fc91			CMPL R12, $0x91					
  main.go:116		0x637984		0f8587060000			JNE 0x638011					
  main.go:117		0x63798a		440fb66207			MOVZX 0x7(DX), R12				
  main.go:117		0x63798f		440fb67a24			MOVZX 0x24(DX), R15				
  main.go:117		0x637994		450faffc			IMULL R12, R15					
  main.go:117		0x637998		0f1f840000000000		NOPL 0(AX)(AX*1)				
  main.go:117		0x6379a0		4180ffe9			CMPL R15, $0xe9					
  main.go:117		0x6379a4		0f8544060000			JNE 0x637fee					
  main.go:118		0x6379aa		440fb66208			MOVZX 0x8(DX), R12				
  main.go:118		0x6379af		440fb67a1a			MOVZX 0x1a(DX), R15				
  main.go:118		0x6379b4		4489f8				MOVL R15, AX					
  main.go:118		0x6379b7		450faffc			IMULL R12, R15					
  main.go:118		0x6379bb		0f1f440000			NOPL 0(AX)(AX*1)				
  main.go:118		0x6379c0		4180ff29			CMPL R15, $0x29					
  main.go:118		0x6379c4		0f85fd050000			JNE 0x637fc7					
  main.go:119		0x6379ca		4883f92d			CMPQ CX, $0x2d					
  main.go:119		0x6379ce		0f86a6060000			JBE 0x63807a					
  main.go:119		0x6379d4		440fb67a09			MOVZX 0x9(DX), R15				
  main.go:119		0x6379d9		0fb64a2d			MOVZX 0x2d(DX), CX				
  main.go:119		0x6379dd		410fafcf			IMULL R15, CX					
  main.go:119		0x6379e1		80f9aa				CMPL CL, $0xaa					
  main.go:119		0x6379e4		0f85ba050000			JNE 0x637fa4					
  main.go:120		0x6379ea		440fb67a0a			MOVZX 0xa(DX), R15				
  main.go:120		0x6379ef		0fb64a18			MOVZX 0x18(DX), CX				
  main.go:120		0x6379f3		410fafcf			IMULL R15, CX					
  main.go:120		0x6379f7		660f1f840000000000		NOPW 0(AX)(AX*1)				
  main.go:120		0x637a00		80f982				CMPL CL, $0x82					
  main.go:120		0x637a03		0f8578050000			JNE 0x637f81					
  main.go:121		0x637a09		440fb67a0b			MOVZX 0xb(DX), R15				
  main.go:121		0x637a0e		0fb64a26			MOVZX 0x26(DX), CX				
  main.go:121		0x637a12		89cb				MOVL CX, BX					
  main.go:121		0x637a14		410fafcf			IMULL R15, CX					
  main.go:121		0x637a18		0f1f840000000000		NOPL 0(AX)(AX*1)				
  main.go:121		0x637a20		80f9d2				CMPL CL, $0xd2					
  main.go:121		0x637a23		0f8534050000			JNE 0x637f5d					
  main.go:122		0x637a29		0fb64a1b			MOVZX 0x1b(DX), CX				
  main.go:122		0x637a2d		410fafcd			IMULL R13, CX					
  main.go:122		0x637a31		80f916				CMPL CL, $0x16					
  main.go:122		0x637a34		0f8500050000			JNE 0x637f3a					
  main.go:123		0x637a3a		440fb66a0d			MOVZX 0xd(DX), R13				
  main.go:123		0x637a3f		0fb64a2a			MOVZX 0x2a(DX), CX				
  main.go:123		0x637a43		410fafcd			IMULL R13, CX					
  main.go:123		0x637a47		80f91c				CMPL CL, $0x1c					
  main.go:123		0x637a4a		0f85c7040000			JNE 0x637f17					
  main.go:124		0x637a50		440fb66a0e			MOVZX 0xe(DX), R13				
  main.go:124		0x637a55		0fb60a				MOVZX 0(DX), CX					
  main.go:124		0x637a58		410fafcd			IMULL R13, CX					
  main.go:124		0x637a5c		0f1f4000			NOPL 0(AX)					
  main.go:124		0x637a60		80f906				CMPL CL, $0x6					
  main.go:124		0x637a63		0f858b040000			JNE 0x637ef4					
  main.go:125		0x637a69		440fb66a0f			MOVZX 0xf(DX), R13				
  main.go:125		0x637a6e		0fb64a19			MOVZX 0x19(DX), CX				
  main.go:125		0x637a72		410fafcd			IMULL R13, CX					
  main.go:125		0x637a76		80f9ca				CMPL CL, $0xca					
  main.go:125		0x637a79		0f8552040000			JNE 0x637ed1					
  main.go:126		0x637a7f		0fb64a10			MOVZX 0x10(DX), CX				
  main.go:126		0x637a83		0fb67220			MOVZX 0x20(DX), SI				
  main.go:126		0x637a87		0faff1				IMULL CX, SI					
  main.go:126		0x637a8a		4080fe8a			CMPL SI, $0x8a					
  main.go:126		0x637a8e		0f851a040000			JNE 0x637eae					
  main.go:127		0x637a94		0fb67211			MOVZX 0x11(DX), SI				
  main.go:127		0x637a98		0fb67a29			MOVZX 0x29(DX), DI				
  main.go:127		0x637a9c		40887c242f			MOVB DI, 0x2f(SP)				
  main.go:127		0x637aa1		0faffe				IMULL SI, DI					
  main.go:127		0x637aa4		4080ff4c			CMPL DI, $0x4c					
  main.go:127		0x637aa8		0f85d9030000			JNE 0x637e87					
  main.go:114		0x637aae		44885c242e			MOVB R11, 0x2e(SP)				
  main.go:128		0x637ab3		0fb67a12			MOVZX 0x12(DX), DI				
  main.go:128		0x637ab7		440fb65a16			MOVZX 0x16(DX), R11				
  main.go:128		0x637abc		410faffb			IMULL R11, DI					
  main.go:128		0x637ac0		4080ffd2			CMPL DI, $0xd2					
  main.go:128		0x637ac4		0f859a030000			JNE 0x637e64					
  main.go:129		0x637aca		0fb67a13			MOVZX 0x13(DX), DI				
  main.go:129		0x637ace		410faffa			IMULL R10, DI					
  main.go:129		0x637ad2		4080ffa5			CMPL DI, $0xa5					
  main.go:129		0x637ad6		0f8565030000			JNE 0x637e41					
  main.go:130		0x637adc		440fb65214			MOVZX 0x14(DX), R10				
  main.go:130		0x637ae1		0fb67a2b			MOVZX 0x2b(DX), DI				
  main.go:130		0x637ae5		440fafd7			IMULL DI, R10					
  main.go:130		0x637ae9		4180fa60			CMPL R10, $0x60					
  main.go:130		0x637aed		0f852a030000			JNE 0x637e1d					
  main.go:132		0x637af3		450fafc3			IMULL R11, R8					
  main.go:132		0x637af7		660f1f840000000000		NOPW 0(AX)(AX*1)				
  main.go:132		0x637b00		4180f8e7			CMPL R8, $0xe7					
  main.go:132		0x637b04		0f85f0020000			JNE 0x637dfa					
  main.go:133		0x637b0a		440fb64217			MOVZX 0x17(DX), R8				
  main.go:133		0x637b0f		440fb65227			MOVZX 0x27(DX), R10				
  main.go:133		0x637b14		450fafc2			IMULL R10, R8					
  main.go:133		0x637b18		0f1f840000000000		NOPL 0(AX)(AX*1)				
  main.go:133		0x637b20		4180f8b6			CMPL R8, $0xb6					
  main.go:133		0x637b24		0f85ad020000			JNE 0x637dd7					
  main.go:136		0x637b2a		440fafe8			IMULL AX, R13					
  main.go:136		0x637b2e		4180fded			CMPL R13, $0xed					
  main.go:136		0x637b32		0f857c020000			JNE 0x637db4					
  main.go:138		0x637b38		440fb6421c			MOVZX 0x1c(DX), R8				
  main.go:138		0x637b3d		450fafc2			IMULL R10, R8					
  main.go:138		0x637b41		4180f8e9			CMPL R8, $0xe9					
  main.go:138		0x637b45		0f8546020000			JNE 0x637d91					
  main.go:140		0x637b4b		440fb6421e			MOVZX 0x1e(DX), R8				
  main.go:140		0x637b50		440fb65225			MOVZX 0x25(DX), R10				
  main.go:140		0x637b55		450fafc2			IMULL R10, R8					
  main.go:140		0x637b59		0f1f8000000000			NOPL 0(AX)					
  main.go:140		0x637b60		4180f8ed			CMPL R8, $0xed					
  main.go:140		0x637b64		0f8504020000			JNE 0x637d6e					
  main.go:143		0x637b6a		440fb64221			MOVZX 0x21(DX), R8				
  main.go:143		0x637b6f		450fafc8			IMULL R8, R9					
  main.go:143		0x637b73		4180f9ac			CMPL R9, $0xac					
  main.go:143		0x637b77		0f85ca010000			JNE 0x637d47					
  main.go:145		0x637b7d		440fb64a23			MOVZX 0x23(DX), R9				
  main.go:145		0x637b82		410faff1			IMULL R9, SI					
  main.go:145		0x637b86		4080fe58			CMPL SI, $0x58					
  main.go:145		0x637b8a		0f8594010000			JNE 0x637d24					
  main.go:147		0x637b90		450fafd7			IMULL R15, R10					
  main.go:147		0x637b94		4180fac3			CMPL R10, $0xc3					
  main.go:147		0x637b98		0f8563010000			JNE 0x637d01					
  main.go:148		0x637b9e		0fafcb				IMULL BX, CX					
  main.go:148		0x637ba1		80f916				CMPL CL, $0x16					
  main.go:148		0x637ba4		0f8534010000			JNE 0x637cde					
  main.go:150		0x637baa		440fb654242e			MOVZX 0x2e(SP), R10				
  main.go:150		0x637bb0		450fafe2			IMULL R10, R12					
  main.go:150		0x637bb4		4180fcec			CMPL R12, $0xec					
  main.go:150		0x637bb8		0f85fd000000			JNE 0x637cbb					
  main.go:151		0x637bbe		440fb654242f			MOVZX 0x2f(SP), R10				
  main.go:151		0x637bc4		450fafda			IMULL R10, R11					
  main.go:151		0x637bc8		4180fb41			CMPL R11, $0x41					
  main.go:151		0x637bcc		0f85c6000000			JNE 0x637c98					
  main.go:153		0x637bd2		410fafff			IMULL R15, DI					
  main.go:153		0x637bd6		660f1f840000000000		NOPW 0(AX)(AX*1)				
  main.go:153		0x637bdf		90				NOPL						
  main.go:153		0x637be0		4080ff30			CMPL DI, $0x30					
  main.go:153		0x637be4		0f858b000000			JNE 0x637c75					
  main.go:154		0x637bea		440fb6522c			MOVZX 0x2c(DX), R10				
  main.go:154		0x637bef		0fb65202			MOVZX 0x2(DX), DX				
  main.go:154		0x637bf3		410fafd2			IMULL R10, DX					
  main.go:154		0x637bf7		80faf0				CMPL DL, $0xf0					
  main.go:154		0x637bfa		7556				JNE 0x637c52					
  main.go:154		0x637bfc		0f1f4000			NOPL 0(AX)					
  main.go:156		0x637c00		4180f960			CMPL R9, $0x60					
  main.go:156		0x637c04		7206				JB 0x637c0c					
  main.go:156		0x637c06		4180f860			CMPL R8, $0x60					
  main.go:156		0x637c0a		7323				JAE 0x637c2f					
  main.go:156		0x637c0c		488d05edd70100			LEAQ 0x1d7ed(IP), AX				
  main.go:156		0x637c13		488d1d96a70d00			LEAQ 0xda796(IP), BX				
  main.go:156		0x637c1a		31c9				XORL CX, CX					
  main.go:156		0x637c1c		31ff				XORL DI, DI					
  main.go:156		0x637c1e		4889fe				MOVQ DI, SI					
  main.go:156		0x637c21		e8ba87fbff			CALL github.com/charmbracelet/log.Error(SB)	
  main.go:156		0x637c26		4881c4d8000000			ADDQ $0xd8, SP					
  main.go:156		0x637c2d		5d				POPQ BP						
  main.go:156		0x637c2e		c3				RET						
  main.go:158		0x637c2f		488d05cad70100			LEAQ 0x1d7ca(IP), AX				
  main.go:158		0x637c36		488d1d83a70d00			LEAQ 0xda783(IP), BX				
  main.go:158		0x637c3d		31c9				XORL CX, CX					
  main.go:158		0x637c3f		31ff				XORL DI, DI					
  main.go:158		0x637c41		4889fe				MOVQ DI, SI					
  main.go:158		0x637c44		e8f786fbff			CALL github.com/charmbracelet/log.Info(SB)	
  main.go:160		0x637c49		4881c4d8000000			ADDQ $0xd8, SP					
  main.go:160		0x637c50		5d				POPQ BP						
  main.go:160		0x637c51		c3				RET						
  main.go:154		0x637c52		488d05a7d70100			LEAQ 0x1d7a7(IP), AX				
  main.go:154		0x637c59		488d1d50a70d00			LEAQ 0xda750(IP), BX				
  main.go:154		0x637c60		31c9				XORL CX, CX					
  main.go:154		0x637c62		31ff				XORL DI, DI					
  main.go:154		0x637c64		4889fe				MOVQ DI, SI					
  main.go:154		0x637c67		e87487fbff			CALL github.com/charmbracelet/log.Error(SB)	
  main.go:154		0x637c6c		4881c4d8000000			ADDQ $0xd8, SP					
  main.go:154		0x637c73		5d				POPQ BP						
  main.go:154		0x637c74		c3				RET						
  main.go:153		0x637c75		488d0584d70100			LEAQ 0x1d784(IP), AX				
  main.go:153		0x637c7c		488d1d2da70d00			LEAQ 0xda72d(IP), BX				
  main.go:153		0x637c83		31c9				XORL CX, CX					
  main.go:153		0x637c85		31ff				XORL DI, DI					
  main.go:153		0x637c87		4889fe				MOVQ DI, SI					
  main.go:153		0x637c8a		e85187fbff			CALL github.com/charmbracelet/log.Error(SB)	
  main.go:153		0x637c8f		4881c4d8000000			ADDQ $0xd8, SP					
  main.go:153		0x637c96		5d				POPQ BP						
  main.go:153		0x637c97		c3				RET						
  main.go:151		0x637c98		488d0561d70100			LEAQ 0x1d761(IP), AX				
  main.go:151		0x637c9f		488d1d0aa70d00			LEAQ 0xda70a(IP), BX				
  main.go:151		0x637ca6		31c9				XORL CX, CX					
  main.go:151		0x637ca8		31ff				XORL DI, DI					
  main.go:151		0x637caa		4889fe				MOVQ DI, SI					
  main.go:151		0x637cad		e82e87fbff			CALL github.com/charmbracelet/log.Error(SB)	
  main.go:151		0x637cb2		4881c4d8000000			ADDQ $0xd8, SP					
  main.go:151		0x637cb9		5d				POPQ BP						
  main.go:151		0x637cba		c3				RET						
  main.go:150		0x637cbb		488d053ed70100			LEAQ 0x1d73e(IP), AX				
  main.go:150		0x637cc2		488d1de7a60d00			LEAQ 0xda6e7(IP), BX				
  main.go:150		0x637cc9		31c9				XORL CX, CX					
  main.go:150		0x637ccb		31ff				XORL DI, DI					
  main.go:150		0x637ccd		4889fe				MOVQ DI, SI					
  main.go:150		0x637cd0		e80b87fbff			CALL github.com/charmbracelet/log.Error(SB)	
  main.go:150		0x637cd5		4881c4d8000000			ADDQ $0xd8, SP					
  main.go:150		0x637cdc		5d				POPQ BP						
  main.go:150		0x637cdd		c3				RET						
  main.go:148		0x637cde		488d051bd70100			LEAQ 0x1d71b(IP), AX				
  main.go:148		0x637ce5		488d1dc4a60d00			LEAQ 0xda6c4(IP), BX				
  main.go:148		0x637cec		31c9				XORL CX, CX					
  main.go:148		0x637cee		31ff				XORL DI, DI					
  main.go:148		0x637cf0		4889fe				MOVQ DI, SI					
  main.go:148		0x637cf3		e8e886fbff			CALL github.com/charmbracelet/log.Error(SB)	
  main.go:148		0x637cf8		4881c4d8000000			ADDQ $0xd8, SP					
  main.go:148		0x637cff		5d				POPQ BP						
  main.go:148		0x637d00		c3				RET						
  main.go:147		0x637d01		488d05f8d60100			LEAQ 0x1d6f8(IP), AX				
  main.go:147		0x637d08		488d1da1a60d00			LEAQ 0xda6a1(IP), BX				
  main.go:147		0x637d0f		31c9				XORL CX, CX					
  main.go:147		0x637d11		31ff				XORL DI, DI					
  main.go:147		0x637d13		4889fe				MOVQ DI, SI					
  main.go:147		0x637d16		e8c586fbff			CALL github.com/charmbracelet/log.Error(SB)	
  main.go:147		0x637d1b		4881c4d8000000			ADDQ $0xd8, SP					
  main.go:147		0x637d22		5d				POPQ BP						
  main.go:147		0x637d23		c3				RET						
  main.go:145		0x637d24		488d05d5d60100			LEAQ 0x1d6d5(IP), AX				
  main.go:145		0x637d2b		488d1d7ea60d00			LEAQ 0xda67e(IP), BX				
  main.go:145		0x637d32		31c9				XORL CX, CX					
  main.go:145		0x637d34		31ff				XORL DI, DI					
  main.go:145		0x637d36		4889fe				MOVQ DI, SI					
  main.go:145		0x637d39		e8a286fbff			CALL github.com/charmbracelet/log.Error(SB)	
  main.go:145		0x637d3e		4881c4d8000000			ADDQ $0xd8, SP					
  main.go:145		0x637d45		5d				POPQ BP						
  main.go:145		0x637d46		c3				RET						
  main.go:143		0x637d47		488d05b2d60100			LEAQ 0x1d6b2(IP), AX				
  main.go:143		0x637d4e		488d1d5ba60d00			LEAQ 0xda65b(IP), BX				
  main.go:143		0x637d55		31c9				XORL CX, CX					
  main.go:143		0x637d57		31ff				XORL DI, DI					
  main.go:143		0x637d59		4889fe				MOVQ DI, SI					
  main.go:143		0x637d5c		0f1f4000			NOPL 0(AX)					
  main.go:143		0x637d60		e87b86fbff			CALL github.com/charmbracelet/log.Error(SB)	
  main.go:143		0x637d65		4881c4d8000000			ADDQ $0xd8, SP					
  main.go:143		0x637d6c		5d				POPQ BP						
  main.go:143		0x637d6d		c3				RET						
  main.go:140		0x637d6e		488d058bd60100			LEAQ 0x1d68b(IP), AX				
  main.go:140		0x637d75		488d1d34a60d00			LEAQ 0xda634(IP), BX				
  main.go:140		0x637d7c		31c9				XORL CX, CX					
  main.go:140		0x637d7e		31ff				XORL DI, DI					
  main.go:140		0x637d80		4889fe				MOVQ DI, SI					
  main.go:140		0x637d83		e85886fbff			CALL github.com/charmbracelet/log.Error(SB)	
  main.go:140		0x637d88		4881c4d8000000			ADDQ $0xd8, SP					
  main.go:140		0x637d8f		5d				POPQ BP						
  main.go:140		0x637d90		c3				RET						
  main.go:138		0x637d91		488d0568d60100			LEAQ 0x1d668(IP), AX				
  main.go:138		0x637d98		488d1d11a60d00			LEAQ 0xda611(IP), BX				
  main.go:138		0x637d9f		31c9				XORL CX, CX					
  main.go:138		0x637da1		31ff				XORL DI, DI					
  main.go:138		0x637da3		4889fe				MOVQ DI, SI					
  main.go:138		0x637da6		e83586fbff			CALL github.com/charmbracelet/log.Error(SB)	
  main.go:138		0x637dab		4881c4d8000000			ADDQ $0xd8, SP					
  main.go:138		0x637db2		5d				POPQ BP						
  main.go:138		0x637db3		c3				RET						
  main.go:136		0x637db4		488d0545d60100			LEAQ 0x1d645(IP), AX				
  main.go:136		0x637dbb		488d1deea50d00			LEAQ 0xda5ee(IP), BX				
  main.go:136		0x637dc2		31c9				XORL CX, CX					
  main.go:136		0x637dc4		31ff				XORL DI, DI					
  main.go:136		0x637dc6		4889fe				MOVQ DI, SI					
  main.go:136		0x637dc9		e81286fbff			CALL github.com/charmbracelet/log.Error(SB)	
  main.go:136		0x637dce		4881c4d8000000			ADDQ $0xd8, SP					
  main.go:136		0x637dd5		5d				POPQ BP						
  main.go:136		0x637dd6		c3				RET						
  main.go:133		0x637dd7		488d0522d60100			LEAQ 0x1d622(IP), AX				
  main.go:133		0x637dde		488d1dcba50d00			LEAQ 0xda5cb(IP), BX				
  main.go:133		0x637de5		31c9				XORL CX, CX					
  main.go:133		0x637de7		31ff				XORL DI, DI					
  main.go:133		0x637de9		4889fe				MOVQ DI, SI					
  main.go:133		0x637dec		e8ef85fbff			CALL github.com/charmbracelet/log.Error(SB)	
  main.go:133		0x637df1		4881c4d8000000			ADDQ $0xd8, SP					
  main.go:133		0x637df8		5d				POPQ BP						
  main.go:133		0x637df9		c3				RET						
  main.go:132		0x637dfa		488d05ffd50100			LEAQ 0x1d5ff(IP), AX				
  main.go:132		0x637e01		488d1da8a50d00			LEAQ 0xda5a8(IP), BX				
  main.go:132		0x637e08		31c9				XORL CX, CX					
  main.go:132		0x637e0a		31ff				XORL DI, DI					
  main.go:132		0x637e0c		4889fe				MOVQ DI, SI					
  main.go:132		0x637e0f		e8cc85fbff			CALL github.com/charmbracelet/log.Error(SB)	
  main.go:132		0x637e14		4881c4d8000000			ADDQ $0xd8, SP					
  main.go:132		0x637e1b		5d				POPQ BP						
  main.go:132		0x637e1c		c3				RET						
  main.go:130		0x637e1d		488d05dcd50100			LEAQ 0x1d5dc(IP), AX				
  main.go:130		0x637e24		488d1d85a50d00			LEAQ 0xda585(IP), BX				
  main.go:130		0x637e2b		31c9				XORL CX, CX					
  main.go:130		0x637e2d		31ff				XORL DI, DI					
  main.go:130		0x637e2f		4889fe				MOVQ DI, SI					
  main.go:130		0x637e32		e8a985fbff			CALL github.com/charmbracelet/log.Error(SB)	
  main.go:130		0x637e37		4881c4d8000000			ADDQ $0xd8, SP					
  main.go:130		0x637e3e		5d				POPQ BP						
  main.go:130		0x637e3f		90				NOPL						
  main.go:130		0x637e40		c3				RET						
  main.go:129		0x637e41		488d05b8d50100			LEAQ 0x1d5b8(IP), AX				
  main.go:129		0x637e48		488d1d61a50d00			LEAQ 0xda561(IP), BX				
  main.go:129		0x637e4f		31c9				XORL CX, CX					
  main.go:129		0x637e51		31ff				XORL DI, DI					
  main.go:129		0x637e53		4889fe				MOVQ DI, SI					
  main.go:129		0x637e56		e88585fbff			CALL github.com/charmbracelet/log.Error(SB)	
  main.go:129		0x637e5b		4881c4d8000000			ADDQ $0xd8, SP					
  main.go:129		0x637e62		5d				POPQ BP						
  main.go:129		0x637e63		c3				RET						
  main.go:128		0x637e64		488d0595d50100			LEAQ 0x1d595(IP), AX				
  main.go:128		0x637e6b		488d1d3ea50d00			LEAQ 0xda53e(IP), BX				
  main.go:128		0x637e72		31c9				XORL CX, CX					
  main.go:128		0x637e74		31ff				XORL DI, DI					
  main.go:128		0x637e76		4889fe				MOVQ DI, SI					
  main.go:128		0x637e79		e86285fbff			CALL github.com/charmbracelet/log.Error(SB)	
  main.go:128		0x637e7e		4881c4d8000000			ADDQ $0xd8, SP					
  main.go:128		0x637e85		5d				POPQ BP						
  main.go:128		0x637e86		c3				RET						
  main.go:127		0x637e87		488d0572d50100			LEAQ 0x1d572(IP), AX				
  main.go:127		0x637e8e		488d1d1ba50d00			LEAQ 0xda51b(IP), BX				
  main.go:127		0x637e95		31c9				XORL CX, CX					
  main.go:127		0x637e97		31ff				XORL DI, DI					
  main.go:127		0x637e99		4889fe				MOVQ DI, SI					
  main.go:127		0x637e9c		0f1f4000			NOPL 0(AX)					
  main.go:127		0x637ea0		e83b85fbff			CALL github.com/charmbracelet/log.Error(SB)	
  main.go:127		0x637ea5		4881c4d8000000			ADDQ $0xd8, SP					
  main.go:127		0x637eac		5d				POPQ BP						
  main.go:127		0x637ead		c3				RET						
  main.go:126		0x637eae		488d054bd50100			LEAQ 0x1d54b(IP), AX				
  main.go:126		0x637eb5		488d1df4a40d00			LEAQ 0xda4f4(IP), BX				
  main.go:126		0x637ebc		31c9				XORL CX, CX					
  main.go:126		0x637ebe		31ff				XORL DI, DI					
  main.go:126		0x637ec0		4889fe				MOVQ DI, SI					
  main.go:126		0x637ec3		e81885fbff			CALL github.com/charmbracelet/log.Error(SB)	
  main.go:126		0x637ec8		4881c4d8000000			ADDQ $0xd8, SP					
  main.go:126		0x637ecf		5d				POPQ BP						
  main.go:126		0x637ed0		c3				RET						
  main.go:125		0x637ed1		488d0528d50100			LEAQ 0x1d528(IP), AX				
  main.go:125		0x637ed8		488d1dd1a40d00			LEAQ 0xda4d1(IP), BX				
  main.go:125		0x637edf		31c9				XORL CX, CX					
  main.go:125		0x637ee1		31ff				XORL DI, DI					
  main.go:125		0x637ee3		4889fe				MOVQ DI, SI					
  main.go:125		0x637ee6		e8f584fbff			CALL github.com/charmbracelet/log.Error(SB)	
  main.go:125		0x637eeb		4881c4d8000000			ADDQ $0xd8, SP					
  main.go:125		0x637ef2		5d				POPQ BP						
  main.go:125		0x637ef3		c3				RET						
  main.go:124		0x637ef4		488d0505d50100			LEAQ 0x1d505(IP), AX				
  main.go:124		0x637efb		488d1daea40d00			LEAQ 0xda4ae(IP), BX				
  main.go:124		0x637f02		31c9				XORL CX, CX					
  main.go:124		0x637f04		31ff				XORL DI, DI					
  main.go:124		0x637f06		4889fe				MOVQ DI, SI					
  main.go:124		0x637f09		e8d284fbff			CALL github.com/charmbracelet/log.Error(SB)	
  main.go:124		0x637f0e		4881c4d8000000			ADDQ $0xd8, SP					
  main.go:124		0x637f15		5d				POPQ BP						
  main.go:124		0x637f16		c3				RET						
  main.go:123		0x637f17		488d05e2d40100			LEAQ 0x1d4e2(IP), AX				
  main.go:123		0x637f1e		488d1d8ba40d00			LEAQ 0xda48b(IP), BX				
  main.go:123		0x637f25		31c9				XORL CX, CX					
  main.go:123		0x637f27		31ff				XORL DI, DI					
  main.go:123		0x637f29		4889fe				MOVQ DI, SI					
  main.go:123		0x637f2c		e8af84fbff			CALL github.com/charmbracelet/log.Error(SB)	
  main.go:123		0x637f31		4881c4d8000000			ADDQ $0xd8, SP					
  main.go:123		0x637f38		5d				POPQ BP						
  main.go:123		0x637f39		c3				RET						
  main.go:122		0x637f3a		488d05bfd40100			LEAQ 0x1d4bf(IP), AX				
  main.go:122		0x637f41		488d1d68a40d00			LEAQ 0xda468(IP), BX				
  main.go:122		0x637f48		31c9				XORL CX, CX					
  main.go:122		0x637f4a		31ff				XORL DI, DI					
  main.go:122		0x637f4c		4889fe				MOVQ DI, SI					
  main.go:122		0x637f4f		e88c84fbff			CALL github.com/charmbracelet/log.Error(SB)	
  main.go:122		0x637f54		4881c4d8000000			ADDQ $0xd8, SP					
  main.go:122		0x637f5b		5d				POPQ BP						
  main.go:122		0x637f5c		c3				RET						
  main.go:121		0x637f5d		488d059cd40100			LEAQ 0x1d49c(IP), AX				
  main.go:121		0x637f64		488d1d45a40d00			LEAQ 0xda445(IP), BX				
  main.go:121		0x637f6b		31c9				XORL CX, CX					
  main.go:121		0x637f6d		31ff				XORL DI, DI					
  main.go:121		0x637f6f		4889fe				MOVQ DI, SI					
  main.go:121		0x637f72		e86984fbff			CALL github.com/charmbracelet/log.Error(SB)	
  main.go:121		0x637f77		4881c4d8000000			ADDQ $0xd8, SP					
  main.go:121		0x637f7e		5d				POPQ BP						
  main.go:121		0x637f7f		90				NOPL						
  main.go:121		0x637f80		c3				RET						
  main.go:120		0x637f81		488d0578d40100			LEAQ 0x1d478(IP), AX				
  main.go:120		0x637f88		488d1d21a40d00			LEAQ 0xda421(IP), BX				
  main.go:120		0x637f8f		31c9				XORL CX, CX					
  main.go:120		0x637f91		31ff				XORL DI, DI					
  main.go:120		0x637f93		4889fe				MOVQ DI, SI					
  main.go:120		0x637f96		e84584fbff			CALL github.com/charmbracelet/log.Error(SB)	
  main.go:120		0x637f9b		4881c4d8000000			ADDQ $0xd8, SP					
  main.go:120		0x637fa2		5d				POPQ BP						
  main.go:120		0x637fa3		c3				RET						
  main.go:119		0x637fa4		488d0555d40100			LEAQ 0x1d455(IP), AX				
  main.go:119		0x637fab		488d1dfea30d00			LEAQ 0xda3fe(IP), BX				
  main.go:119		0x637fb2		31c9				XORL CX, CX					
  main.go:119		0x637fb4		31ff				XORL DI, DI					
  main.go:119		0x637fb6		4889fe				MOVQ DI, SI					
  main.go:119		0x637fb9		e82284fbff			CALL github.com/charmbracelet/log.Error(SB)	
  main.go:119		0x637fbe		4881c4d8000000			ADDQ $0xd8, SP					
  main.go:119		0x637fc5		5d				POPQ BP						
  main.go:119		0x637fc6		c3				RET						
  main.go:118		0x637fc7		488d0532d40100			LEAQ 0x1d432(IP), AX				
  main.go:118		0x637fce		488d1ddba30d00			LEAQ 0xda3db(IP), BX				
  main.go:118		0x637fd5		31c9				XORL CX, CX					
  main.go:118		0x637fd7		31ff				XORL DI, DI					
  main.go:118		0x637fd9		4889fe				MOVQ DI, SI					
  main.go:118		0x637fdc		0f1f4000			NOPL 0(AX)					
  main.go:118		0x637fe0		e8fb83fbff			CALL github.com/charmbracelet/log.Error(SB)	
  main.go:118		0x637fe5		4881c4d8000000			ADDQ $0xd8, SP					
  main.go:118		0x637fec		5d				POPQ BP						
  main.go:118		0x637fed		c3				RET						
  main.go:117		0x637fee		488d050bd40100			LEAQ 0x1d40b(IP), AX				
  main.go:117		0x637ff5		488d1db4a30d00			LEAQ 0xda3b4(IP), BX				
  main.go:117		0x637ffc		31c9				XORL CX, CX					
  main.go:117		0x637ffe		31ff				XORL DI, DI					
  main.go:117		0x638000		4889fe				MOVQ DI, SI					
  main.go:117		0x638003		e8d883fbff			CALL github.com/charmbracelet/log.Error(SB)	
  main.go:117		0x638008		4881c4d8000000			ADDQ $0xd8, SP					
  main.go:117		0x63800f		5d				POPQ BP						
  main.go:117		0x638010		c3				RET						
  main.go:116		0x638011		488d05e8d30100			LEAQ 0x1d3e8(IP), AX				
  main.go:116		0x638018		488d1d91a30d00			LEAQ 0xda391(IP), BX				
  main.go:116		0x63801f		31c9				XORL CX, CX					
  main.go:116		0x638021		31ff				XORL DI, DI					
  main.go:116		0x638023		4889fe				MOVQ DI, SI					
  main.go:116		0x638026		e8b583fbff			CALL github.com/charmbracelet/log.Error(SB)	
  main.go:116		0x63802b		4881c4d8000000			ADDQ $0xd8, SP					
  main.go:116		0x638032		5d				POPQ BP						
  main.go:116		0x638033		c3				RET						
  main.go:114		0x638034		488d05c5d30100			LEAQ 0x1d3c5(IP), AX				
  main.go:114		0x63803b		488d1d6ea30d00			LEAQ 0xda36e(IP), BX				
  main.go:114		0x638042		31c9				XORL CX, CX					
  main.go:114		0x638044		31ff				XORL DI, DI					
  main.go:114		0x638046		4889fe				MOVQ DI, SI					
  main.go:114		0x638049		e89283fbff			CALL github.com/charmbracelet/log.Error(SB)	
  main.go:114		0x63804e		4881c4d8000000			ADDQ $0xd8, SP					
  main.go:114		0x638055		5d				POPQ BP						
  main.go:114		0x638056		c3				RET						
  main.go:111		0x638057		488d05a2d30100			LEAQ 0x1d3a2(IP), AX				
  main.go:111		0x63805e		488d1d4ba30d00			LEAQ 0xda34b(IP), BX				
  main.go:111		0x638065		31c9				XORL CX, CX					
  main.go:111		0x638067		31ff				XORL DI, DI					
  main.go:111		0x638069		4889fe				MOVQ DI, SI					
  main.go:111		0x63806c		e86f83fbff			CALL github.com/charmbracelet/log.Error(SB)	
  main.go:111		0x638071		4881c4d8000000			ADDQ $0xd8, SP					
  main.go:111		0x638078		5d				POPQ BP						
  main.go:111		0x638079		c3				RET						
  main.go:119		0x63807a		b82d000000			MOVL $0x2d, AX					
  main.go:119		0x63807f		90				NOPL						
  main.go:119		0x638080		e8fb41e4ff			CALL runtime.panicIndex(SB)			
  main.go:114		0x638085		b828000000			MOVL $0x28, AX					
  main.go:114		0x63808a		e8f141e4ff			CALL runtime.panicIndex(SB)			
  main.go:111		0x63808f		b822000000			MOVL $0x22, AX					
  main.go:111		0x638094		e8e741e4ff			CALL runtime.panicIndex(SB)			
  main.go:111		0x638099		b801000000			MOVL $0x1, AX					
  main.go:111		0x63809e		6690				NOPW						
  main.go:111		0x6380a0		e8db41e4ff			CALL runtime.panicIndex(SB)			
  main.go:108		0x6380a5		4c89c0				MOVQ R8, AX					
  main.go:108		0x6380a8		e8d341e4ff			CALL runtime.panicIndex(SB)			
  main.go:102		0x6380ad		31c0				XORL AX, AX					
  main.go:102		0x6380af		4889c1				MOVQ AX, CX					
  main.go:102		0x6380b2		e8c941e4ff			CALL runtime.panicIndex(SB)			
  main.go:102		0x6380b7		90				NOPL						
  main.go:88		0x6380b8		e8231fe4ff			CALL runtime.morestack_noctxt.abi0(SB)		
  main.go:88		0x6380bd		0f1f00				NOPL 0(AX)					
  main.go:88		0x6380c0		e9fbf5ffff			JMP main.(*program).run(SB)			
