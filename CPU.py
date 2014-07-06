from MMU import MMU

opcodes = []

def opcode(func):
    opcodes.append(func)
    return func


class CPU:
    
    ###############
    #INTERNAL STATE
    ###############

    def __init__(self):
        #Clock
        self.cm = 0

        #Registers
        self.a = 0 # 8 bit
        self.b = 0
        self.c = 0
        self.d = 0
        self.e = 0
        self.hl = 0
        self.pc, self.sp = [0]*2 # 16 bit
        self.m = 0 # Last clock

        #Flags
        self.f_zero = False
        self.f_subtract = False
        self.f_half_carry = False
        self.f_carry = False

        #MMU
        self.mmu = MMU(self)

        #Other state things
        self.stopped = False
    
    ###############
    #OPERATIONS
    ###############

    #0x00 - NOP
    @opcode
    def nop(self):
        self.m = 1
        print "NOP"

    #0x01 - LD BC d16
    @opcode
    def ldbcd16(self):
        print "LD BC d16"
        self.c = self.mmu.rb(self.pc)
        self.b = self.mmu.rb(self.pc + 1)
        self.pc += 2
        self.m = 3

    #0x02 - LD (BC) A
    @opcode
    def ldbca(self):
        print "LD (BC) A"
        self.mmu.wb((self.b << 8) | self.c, self.a)
        self.m = 2

    #0x03 - INC BC
    @opcode
    def incbc(self):
        print "INC BC"
        temp = ((self.b << 8) | self.c) + 1
        self.b = (temp >> 8) & 0xFF
        self.c = temp & 0xFF
        self.m = 2

    #0x04 - INC B
    @opcode
    def incb(self):
        print "INC B"
        self.b = (self.b + 1) & 0xFF
        self.m = 1
        self.f_zero = (self.b == 0)
        self.f_half_carry = ((self.b & 0xF) == 0)
        self.f_subtract = False

    #0x05 - DEC B
    @opcode
    def decb(self):
        print "DEC B"
        self.b = (self.b - 1) & 0xFF
        self.m = 1
        self.f_zero = (self.b == 0)
        self.f_half_carry = ((self.b & 0xF) == 0xF)
        self.f_subtract = True

    #0x06 - LD B d8
    @opcode
    def ldbd8(self):
        print "LD B d8"
        self.b = self.mmu.rb(self.pc)
        self.m = 2
        self.pc += 1

    #0x07 - RLCA
    @opcode
    def rlca(self):
        print "RLCA"
        self.f_carry = (self.a > 0x7F)
        self.a = ((self.a << 1) & 0xFF) | (self.a >> 7)
        self.f_zero = False
        self.f_half_carry = False
        self.f_subtract = False
        self.m = 1

    #0x08 - LD (a16) SP
    # Bytes: 3
    # Flags ZHNC: - - - - 
    # Cycles: 5
    # TODO
    @opcode
    def lda16sp(self):
        print "LD (a16) SP"

    #0x09 - ADD HL BC
    @opcode
    def addhlbc(self):
        print "ADD HL BC"
        temp = self.hl + ((self.b << 8) | self.c)
        self.f_half_carry = ((self.hl & 0xFFF) > (temp & 0xFFF))
        self.f_carry = (temp > 0xFFFF)
        self.f_subtract = False
        self.hl = temp & 0xFFFF
        self.m = 2

    #0x0a - LD A (BC)
    @opcode
    def ldabc(self):
        print "LD A (BC)"
        self.a = (self.b << 8) | self.c
        self.m = 2

    #0x0b - DEC BC
    @opcode
    def decbc(self):
        print "DEC BC"
        temp = (((self.b << 8) | self.c) - 1) & 0xFFFF
        self.b = temp >> 8
        self.c = temp & 0xFF
        self.m = 2

    #0x0c - INC C
    @opcode
    def incc(self):
        print "INC C"
        self.c = (self.c + 1) & 0xFF
        self.m = 1
        self.f_zero = (self.c == 0)
        self.f_half_carry = ((self.c & 0xF) == 0)
        self.f_subtract = False

    #0x0d - DEC C
    @opcode
    def decc(self):
        print "DEC C"
        self.c = (self.c - 1) & 0xFF
        self.m = 1
        self.f_zero = (self.c == 0)
        self.f_half_carry = ((self.c & 0xF) == 0xF)
        self.f_subtract = True

    #0x0e - LD C d8
    @opcode
    def ldcd8(self):
        print "LD C d8"
        self.c = self.mmu.rb(self.pc)
        self.pc += 1
        self.m = 2

    #0x0f - RRCA
    @opcode
    def rrca(self):
        print "RRCA"
        self.a = (self.a >> 1) | ((self.a & 1) << 7)
        self.f_carry = (self.a > 0x7F)
        self.f_half_carry = False
        self.f_zero = False
        self.f_subtract = False
        self.m = 1

    #0x10 - STOP 0
    @opcode
    def stop0(self):
        print "STOP 0"
        self.stopped = True
        self.m = 1

    #0x11 - LD DE d16
    @opcode
    def ldded16(self):
        print "LD DE d16"
        self.mmu.wb((self.d << 8) | self.e, self.a)
        self.m = 3

    #0x12 - LD (DE) A
    @opcode
    def lddea(self):
        print "LD (DE) A"
        self.mmu.wb((self.d << 8) | self.e, self.a)
        self.m = 2

    #0x13 - INC DE
    @opcode
    def incde(self):
        print "INC DE"
        temp = ((self.d << 8) | self.e) + 1
        self.d = (temp >> 8) & 0xFF
        self.e = temp & 0xFF
        self.m = 2


    #0x14 - INC D
    @opcode
    def incd(self):
        print "INC D"
        self.d = (self.d + 1) & 0xFF
        self.m = 1
        self.f_zero = (self.d == 0)
        self.f_half_carry = ((self.d & 0xF) == 0)
        self.f_subtract = False

    #0x15 - DEC D
    @opcode
    def decd(self):
        print "DEC D"
        self.d = (self.d - 1) & 0xFF
        self.m = 1
        self.f_zero = (self.d == 0)
        self.f_half_carry = ((self.d & 0xF) == 0xF)
        self.f_subtract = True

    #0x16 - LD D d8
    @opcode
    def lddd8(self):
        print "LD D d8"
        self.d = self.mmu.rb(self.pc)
        self.m = 2
        self.pc += 1

    #0x17 - RLA
    @opcode
    def rla(self):
        print "RLA"
        carry = 1 if self.f_carry else 0
        self.f_carry = (self.a > 0x7F)
        self.a = ((self.a << 1) & 0xFF) | carry
        self.f_zero = False
        self.f_half_carry = False
        self.f_subtract = False
        self.m = 1
        
    #0x18 - JR r8
    @opcode
    def jrr8(self):
        print "JR r8"
        self.pc = (self.pc + ((self.mmu.rb(self.pc) << 24) >> 24) + 1) & 0xFFFF
        self.m = 3

    #0x19 - ADD HL DE
    @opcode
    def addhlde(self):
        print "ADD HL DE"
        temp = self.hl + ((self.d << 8) | self.e)
        self.f_half_carry = ((self.hl & 0xFFF) > (temp & 0xFFF))
        self.f_carry = (temp > 0xFFFF)
        self.hl = temp & 0xFFFF
        self.f_subtract = False

    #0x1a - LD A (DE)
    @opcode
    def ldade(self):
        print "LD A (DE)"
        self.a = self.mmu.rb((self.d << 8) | self.e)
        self.m = 2

    #0x1b - DEC DE
    @opcode
    def decde(self):
        print "DEC DE"
        temp = (((self.d << 8) | self.e) - 1) & 0xFFFF
        self.d = temp >> 8
        self.e = temp & 0xFF
        self.m = 2

    #0x1c - INC E
    @opcode
    def ince(self):
        print "INC E"
        self.e = (self.e + 1) & 0xFF
        self.m = 1
        self.f_zero = (self.e == 0)
        self.f_half_carry = ((self.e & 0xF) == 0)
        self.f_subtract = False

    #0x1d - DEC E
    @opcode
    def dece(self):
        print "DEC E"
        self.e = (self.e - 1) & 0xFF
        self.m = 1
        self.f_zero = (self.e == 0)
        self.f_half_carry = ((self.e & 0xF) == 0xF)
        self.f_subtract = True

    #0x1e - LD E d8
    @opcode
    def lded8(self):
        print "LD E d8"
        self.e = self.mmu.rb(self.pc)
        self.m = 2
        self.pc += 1

    #0x1f - RRA
    @opcode
    def rra(self):
        print "RRA"
        carry = 0x80 if self.f_carry else 0
        self.f_carry = ((self.a & 1) == 1)
        self.a = (self.a >> 1) | carry
        self.f_zero = False
        self.f_half_carry = False
        self.f_subtract = False

    #0x20 - JR NZ r8
    @opcode
    def jrnzr8(self):
        print "JR NZ r8"
        if (!self.f_zero):
            self.pc = (self.pc + ((self.mmu.rb(self.pc) << 24) >> 24) + 1) & 0xFFFF
            self.m = 3
        else:
            self.pc = (self.pc + 1) & 0xFFFF
            self.m = 2

    #0x21 - LD HL d16
    # Bytes: 3
    # Flags ZHNC: - - - - 
    # Cycles: 3
    # TODO
    @opcode
    def ldhld16(self):
        print "LD HL d16"

    #0x22 - LD (HL+) A
    # Bytes: 1
    # Flags ZHNC: - - - - 
    # Cycles: 2
    # TODO
    @opcode
    def ldhla(self):
        print "LD (HL+) A"

    #0x23 - INC HL
    # Bytes: 1
    # Flags ZHNC: - - - - 
    # Cycles: 2
    # TODO
    @opcode
    def inchl(self):
        print "INC HL"

    #0x24 - INC H
    # Bytes: 1
    # Flags ZHNC: Z 0 H - 
    # Cycles: 1
    # TODO
    @opcode
    def inch(self):
        print "INC H"

    #0x25 - DEC H
    # Bytes: 1
    # Flags ZHNC: Z 1 H - 
    # Cycles: 1
    # TODO
    @opcode
    def dech(self):
        print "DEC H"

    #0x26 - LD H d8
    # Bytes: 2
    # Flags ZHNC: - - - - 
    # Cycles: 2
    # TODO
    @opcode
    def ldhd8(self):
        print "LD H d8"

    #0x27 - DAA
    # Bytes: 1
    # Flags ZHNC: Z - 0 C 
    # Cycles: 1
    # TODO
    @opcode
    def daa(self):
        print "DAA"

    #0x28 - JR Z r8
    # Bytes: 2
    # Flags ZHNC: - - - - 
    # Cycles: 3/2/
    # TODO
    @opcode
    def jrzr8(self):
        print "JR Z r8"

    #0x29 - ADD HL HL
    # Bytes: 1
    # Flags ZHNC: - 0 H C 
    # Cycles: 2
    # TODO
    @opcode
    def addhlhl(self):
        print "ADD HL HL"

    #0x2a - LD A (HL+)
    # Bytes: 1
    # Flags ZHNC: - - - - 
    # Cycles: 2
    # TODO
    @opcode
    def ldahl(self):
        print "LD A (HL+)"

    #0x2b - DEC HL
    # Bytes: 1
    # Flags ZHNC: - - - - 
    # Cycles: 2
    # TODO
    @opcode
    def dechl(self):
        print "DEC HL"

    #0x2c - INC L
    # Bytes: 1
    # Flags ZHNC: Z 0 H - 
    # Cycles: 1
    # TODO
    @opcode
    def incl(self):
        print "INC L"

    #0x2d - DEC L
    # Bytes: 1
    # Flags ZHNC: Z 1 H - 
    # Cycles: 1
    # TODO
    @opcode
    def decl(self):
        print "DEC L"

    #0x2e - LD L d8
    # Bytes: 2
    # Flags ZHNC: - - - - 
    # Cycles: 2
    # TODO
    @opcode
    def ldld8(self):
        print "LD L d8"

    #0x2f - CPL
    # Bytes: 1
    # Flags ZHNC: - 1 1 - 
    # Cycles: 1
    # TODO
    @opcode
    def cpl(self):
        print "CPL"

    #0x30 - JR NC r8
    # Bytes: 2
    # Flags ZHNC: - - - - 
    # Cycles: 3/2/
    # TODO
    @opcode
    def jrncr8(self):
        print "JR NC r8"

    #0x31 - LD SP d16
    # Bytes: 3
    # Flags ZHNC: - - - - 
    # Cycles: 3
    # TODO
    @opcode
    def ldspd16(self):
        print "LD SP d16"

    #0x32 - LD (HL-) A
    # Bytes: 1
    # Flags ZHNC: - - - - 
    # Cycles: 2
    # TODO
    @opcode
    def ldhla(self):
        print "LD (HL-) A"

    #0x33 - INC SP
    # Bytes: 1
    # Flags ZHNC: - - - - 
    # Cycles: 2
    # TODO
    @opcode
    def incsp(self):
        print "INC SP"

    #0x34 - INC (HL)
    # Bytes: 1
    # Flags ZHNC: Z 0 H - 
    # Cycles: 3
    # TODO
    @opcode
    def inchl(self):
        print "INC (HL)"

    #0x35 - DEC (HL)
    # Bytes: 1
    # Flags ZHNC: Z 1 H - 
    # Cycles: 3
    # TODO
    @opcode
    def dechl(self):
        print "DEC (HL)"

    #0x36 - LD (HL) d8
    # Bytes: 2
    # Flags ZHNC: - - - - 
    # Cycles: 3
    # TODO
    @opcode
    def ldhld8(self):
        print "LD (HL) d8"

    #0x37 - SCF
    # Bytes: 1
    # Flags ZHNC: - 0 0 1 
    # Cycles: 1
    # TODO
    @opcode
    def scf(self):
        print "SCF"

    #0x38 - JR C r8
    # Bytes: 2
    # Flags ZHNC: - - - - 
    # Cycles: 3/2/
    # TODO
    @opcode
    def jrcr8(self):
        print "JR C r8"

    #0x39 - ADD HL SP
    # Bytes: 1
    # Flags ZHNC: - 0 H C 
    # Cycles: 2
    # TODO
    @opcode
    def addhlsp(self):
        print "ADD HL SP"

    #0x3a - LD A (HL-)
    # Bytes: 1
    # Flags ZHNC: - - - - 
    # Cycles: 2
    # TODO
    @opcode
    def ldahl(self):
        print "LD A (HL-)"

    #0x3b - DEC SP
    # Bytes: 1
    # Flags ZHNC: - - - - 
    # Cycles: 2
    # TODO
    @opcode
    def decsp(self):
        print "DEC SP"

    #0x3c - INC A
    # Bytes: 1
    # Flags ZHNC: Z 0 H - 
    # Cycles: 1
    # TODO
    @opcode
    def inca(self):
        print "INC A"

    #0x3d - DEC A
    # Bytes: 1
    # Flags ZHNC: Z 1 H - 
    # Cycles: 1
    # TODO
    @opcode
    def deca(self):
        print "DEC A"

    #0x3e - LD A d8
    # Bytes: 2
    # Flags ZHNC: - - - - 
    # Cycles: 2
    # TODO
    @opcode
    def ldad8(self):
        print "LD A d8"

    #0x3f - CCF
    # Bytes: 1
    # Flags ZHNC: - 0 0 C 
    # Cycles: 1
    # TODO
    @opcode
    def ccf(self):
        print "CCF"

    #0x40 - LD B B
    @opcode
    def ldbb(self):
        print "LD B B"
        m = 1

    #0x41 - LD B C
    @opcode
    def ldbc(self):
        print "LD B C"
        self.b = self.c
        self.m = 1

    #0x42 - LD B D
    @opcode
    def ldbd(self):
        print "LD B D"
        self.b = self.d
        self.m = 1

    #0x43 - LD B E
    @opcode
    def ldbe(self):
        print "LD B E"
        self.b = self.e
        self.m = 1

    #0x44 - LD B H
    @opcode
    def ldbh(self):
        print "LD B H"
        self.b = (self.hl >>    8)
        self.m = 1

    #0x45 - LD B L
    @opcode
    def ldbl(self):
        print "LD B L"
        self.b = (self.hl & 0xFF)
        self.m = 1

    #0x46 - LD B (HL)
    # Bytes: 1
    # Flags ZHNC: - - - - 
    # Cycles: 2
    # TODO
    @opcode
    def ldbhl(self):
        print "LD B (HL)"

    #0x47 - LD B A
    @opcode
    def ldba(self):
        print "LD B A"
        self.b = self.a
        self.m = 1

    #0x48 - LD C B
    @opcode
    def ldcb(self):
        print "LD C B"
        self.c = self.b
        self.m = 1

    #0x49 - LD C C
    @opcode
    def ldcc(self):
        print "LD C C"
        self.m = 1

    #0x4a - LD C D
    @opcode
    def ldcd(self):
        print "LD C D"
        self.c = self.d
        self.m = 1

    #0x4b - LD C E
    @opcode
    def ldce(self):
        print "LD C E"
        self.c = self.e
        self.m = 1

    #0x4c - LD C H
    # Bytes: 1
    # Flags ZHNC: - - - - 
    # Cycles: 1
    # TODO
    @opcode
    def ldch(self):
        print "LD C H"

    #0x4d - LD C L
    # Bytes: 1
    # Flags ZHNC: - - - - 
    # Cycles: 1
    # TODO
    @opcode
    def ldcl(self):
        print "LD C L"

    #0x4e - LD C (HL)
    # Bytes: 1
    # Flags ZHNC: - - - - 
    # Cycles: 2
    # TODO
    @opcode
    def ldchl(self):
        print "LD C (HL)"

    #0x4f - LD C A
    @opcode
    def ldca(self):
        print "LD C A"
        self.c = self.a
        self.m = 1

    #0x50 - LD D B
    @opcode
    def lddb(self):
        print "LD D B"
        self.d = self.b
        self.m = 1

    #0x51 - LD D C
    @opcode
    def lddc(self):
        print "LD D C"
        self.d = self.c
        self.m = 1

    #0x52 - LD D D
    @opcode
    def lddd(self):
        print "LD D D"
        self.m = 1

    #0x53 - LD D E
    @opcode
    def ldde(self):
        print "LD D E"
        self.d = self.e
        self.m = 1

    #0x54 - LD D H
    # Bytes: 1
    # Flags ZHNC: - - - - 
    # Cycles: 1
    # TODO
    @opcode
    def lddh(self):
        print "LD D H"

    #0x55 - LD D L
    # Bytes: 1
    # Flags ZHNC: - - - - 
    # Cycles: 1
    # TODO
    @opcode
    def lddl(self):
        print "LD D L"

    #0x56 - LD D (HL)
    # Bytes: 1
    # Flags ZHNC: - - - - 
    # Cycles: 2
    # TODO
    @opcode
    def lddhl(self):
        print "LD D (HL)"

    #0x57 - LD D A
    @opcode
    def ldda(self):
        print "LD D A"
        self.d = self.a
        self.m = 1

    #0x58 - LD E B
    @opcode
    def ldeb(self):
        print "LD E B"
        self.e = self.b
        self.m = 1

    #0x59 - LD E C
    @opcode
    def ldec(self):
        print "LD E C"
        self.e = self.c
        self.m = 1

    #0x5a - LD E D
    @opcode
    def lded(self):
        print "LD E D"
        self.e = self.d
        self.m = 1

    #0x5b - LD E E
    @opcode
    def ldee(self):
        print "LD E E"
        self.m = 1

    #0x5c - LD E H
    # Bytes: 1
    # Flags ZHNC: - - - - 
    # Cycles: 1
    # TODO
    @opcode
    def ldeh(self):
        print "LD E H"

    #0x5d - LD E L
    # Bytes: 1
    # Flags ZHNC: - - - - 
    # Cycles: 1
    # TODO
    @opcode
    def ldel(self):
        print "LD E L"

    #0x5e - LD E (HL)
    # Bytes: 1
    # Flags ZHNC: - - - - 
    # Cycles: 2
    # TODO
    @opcode
    def ldehl(self):
        print "LD E (HL)"

    #0x5f - LD E A
    @opcode
    def ldea(self):
        print "LD E A"
        self.e = self.a
        self.m = 1

    #0x60 - LD H B
    # Bytes: 1
    # Flags ZHNC: - - - - 
    # Cycles: 1
    # TODO
    @opcode
    def ldhb(self):
        print "LD H B"

    #0x61 - LD H C
    # Bytes: 1
    # Flags ZHNC: - - - - 
    # Cycles: 1
    # TODO
    @opcode
    def ldhc(self):
        print "LD H C"

    #0x62 - LD H D
    # Bytes: 1
    # Flags ZHNC: - - - - 
    # Cycles: 1
    # TODO
    @opcode
    def ldhd(self):
        print "LD H D"

    #0x63 - LD H E
    # Bytes: 1
    # Flags ZHNC: - - - - 
    # Cycles: 1
    # TODO
    @opcode
    def ldhe(self):
        print "LD H E"

    #0x64 - LD H H
    @opcode
    def ldhh(self):
        print "LD H H"
        self.m = 1

    #0x65 - LD H L
    # Bytes: 1
    # Flags ZHNC: - - - - 
    # Cycles: 1
    # TODO
    @opcode
    def ldhl(self):
        print "LD H L"

    #0x66 - LD H (HL)
    # Bytes: 1
    # Flags ZHNC: - - - - 
    # Cycles: 2
    # TODO
    @opcode
    def ldhhl(self):
        print "LD H (HL)"

    #0x67 - LD H A
    # Bytes: 1
    # Flags ZHNC: - - - - 
    # Cycles: 1
    # TODO
    @opcode
    def ldha(self):
        print "LD H A"

    #0x68 - LD L B
    # Bytes: 1
    # Flags ZHNC: - - - - 
    # Cycles: 1
    # TODO
    @opcode
    def ldlb(self):
        print "LD L B"

    #0x69 - LD L C
    # Bytes: 1
    # Flags ZHNC: - - - - 
    # Cycles: 1
    # TODO
    @opcode
    def ldlc(self):
        print "LD L C"

    #0x6a - LD L D
    # Bytes: 1
    # Flags ZHNC: - - - - 
    # Cycles: 1
    # TODO
    @opcode
    def ldld(self):
        print "LD L D"

    #0x6b - LD L E
    # Bytes: 1
    # Flags ZHNC: - - - - 
    # Cycles: 1
    # TODO
    @opcode
    def ldle(self):
        print "LD L E"

    #0x6c - LD L H
    # Bytes: 1
    # Flags ZHNC: - - - - 
    # Cycles: 1
    # TODO
    @opcode
    def ldlh(self):
        print "LD L H"

    #0x6d - LD L L
    # Bytes: 1
    # Flags ZHNC: - - - - 
    # Cycles: 1
    # TODO
    @opcode
    def ldll(self):
        print "LD L L"

    #0x6e - LD L (HL)
    # Bytes: 1
    # Flags ZHNC: - - - - 
    # Cycles: 2
    # TODO
    @opcode
    def ldlhl(self):
        print "LD L (HL)"

    #0x6f - LD L A
    # Bytes: 1
    # Flags ZHNC: - - - - 
    # Cycles: 1
    # TODO
    @opcode
    def ldla(self):
        print "LD L A"

    #0x70 - LD (HL) B
    # Bytes: 1
    # Flags ZHNC: - - - - 
    # Cycles: 2
    # TODO
    @opcode
    def ldhlb(self):
        print "LD (HL) B"

    #0x71 - LD (HL) C
    # Bytes: 1
    # Flags ZHNC: - - - - 
    # Cycles: 2
    # TODO
    @opcode
    def ldhlc(self):
        print "LD (HL) C"

    #0x72 - LD (HL) D
    # Bytes: 1
    # Flags ZHNC: - - - - 
    # Cycles: 2
    # TODO
    @opcode
    def ldhld(self):
        print "LD (HL) D"

    #0x73 - LD (HL) E
    # Bytes: 1
    # Flags ZHNC: - - - - 
    # Cycles: 2
    # TODO
    @opcode
    def ldhle(self):
        print "LD (HL) E"

    #0x74 - LD (HL) H
    # Bytes: 1
    # Flags ZHNC: - - - - 
    # Cycles: 2
    # TODO
    @opcode
    def ldhlh(self):
        print "LD (HL) H"

    #0x75 - LD (HL) L
    # Bytes: 1
    # Flags ZHNC: - - - - 
    # Cycles: 2
    # TODO
    @opcode
    def ldhll(self):
        print "LD (HL) L"

    #0x76 - HALT
    # Bytes: 1
    # Flags ZHNC: - - - - 
    # Cycles: 1
    # TODO
    @opcode
    def halt(self):
        print "HALT"

    #0x77 - LD (HL) A
    # Bytes: 1
    # Flags ZHNC: - - - - 
    # Cycles: 2
    # TODO
    @opcode
    def ldhla(self):
        print "LD (HL) A"

    #0x78 - LD A B
    @opcode
    def ldab(self):
        print "LD A B"
        self.a = self.b
        self.m = 1

    #0x79 - LD A C
    @opcode
    def ldac(self):
        print "LD A C"
        self.a = self.c
        self.m = 1

    #0x7a - LD A D
    @opcode
    def ldad(self):
        print "LD A D"
        self.a = self.d
        self.m = 1

    #0x7b - LD A E
    @opcode
    def ldae(self):
        print "LD A E"
        self.a = self.e
        self.m = 1

    #0x7c - LD A H
    # Bytes: 1
    # Flags ZHNC: - - - - 
    # Cycles: 1
    # TODO
    @opcode
    def ldah(self):
        print "LD A H"

    #0x7d - LD A L
    # Bytes: 1
    # Flags ZHNC: - - - - 
    # Cycles: 1
    # TODO
    @opcode
    def ldal(self):
        print "LD A L"

    #0x7e - LD A (HL)
    # Bytes: 1
    # Flags ZHNC: - - - - 
    # Cycles: 2
    # TODO
    @opcode
    def ldahl(self):
        print "LD A (HL)"

    #0x7f - LD A A
    @opcode
    def ldaa(self):
        print "LD A A"
        self.m = 1

    #0x80 - ADD A B
    @opcode
    def addab(self):
        print "ADD A B"
        temp = self.a + self.b
        self.f_half_carry = ((temp & 0xF) < (self.a & 0xF))
        self.f_carry = (temp > 0xFF)
        self.a = temp & 0xFF
        self.f_zero = (self.a == 0)
        self.f_subtract = False
        self.m = 1

    #0x81 - ADD A C
    @opcode
    def addac(self):
        print "ADD A C"
        temp = self.a + self.c
        self.f_half_carry = ((temp & 0xF) < (self.a & 0xF))
        self.f_carry = (temp > 0xFF)
        self.a = temp & 0xFF
        self.f_zero = (self.a == 0)
        self.f_subtract = False
        self.m = 1

    #0x82 - ADD A D
    @opcode
    def addad(self):
        print "ADD A D"
        temp = self.a + self.d
        self.f_half_carry = ((temp & 0xF) < (self.a & 0xF))
        self.f_carry = (temp > 0xFF)
        self.a = temp & 0xFF
        self.f_zero = (self.a == 0)
        self.f_subtract = False
        self.m = 1

    #0x83 - ADD A E
    @opcode
    def addae(self):
        print "ADD A E"
        temp = self.a + self.e
        self.f_half_carry = ((temp & 0xF) < (self.a & 0xF))
        self.f_carry = (temp > 0xFF)
        self.a = temp & 0xFF
        self.f_zero = (self.a == 0)
        self.f_subtract = False
        self.m = 1

    #0x84 - ADD A H
    # Bytes: 1
    # Flags ZHNC: Z 0 H C 
    # Cycles: 1
    # TODO
    @opcode
    def addah(self):
        print "ADD A H"

    #0x85 - ADD A L
    # Bytes: 1
    # Flags ZHNC: Z 0 H C 
    # Cycles: 1
    # TODO
    @opcode
    def addal(self):
        print "ADD A L"

    #0x86 - ADD A (HL)
    # Bytes: 1
    # Flags ZHNC: Z 0 H C 
    # Cycles: 2
    # TODO
    @opcode
    def addahl(self):
        print "ADD A (HL)"

    #0x87 - ADD A A
    # Bytes: 1
    # Flags ZHNC: Z 0 H C 
    # Cycles: 1
    # TODO
    @opcode
    def addaa(self):
        print "ADD A A"
        self.f_half_carry = ((self.a & 0x8) == 0x8);
        self.f_carry = (self.a > 0x7F);
        self.a = (self.a << 1) & 0xFF;
        self.f_zero = (self.a == 0);
        self.f_subtract = False;

    #0x88 - ADC A B
    # Bytes: 1
    # Flags ZHNC: Z 0 H C 
    # Cycles: 1
    # TODO
    @opcode
    def adcab(self):
        print "ADC A B"

    #0x89 - ADC A C
    # Bytes: 1
    # Flags ZHNC: Z 0 H C 
    # Cycles: 1
    # TODO
    @opcode
    def adcac(self):
        print "ADC A C"

    #0x8a - ADC A D
    # Bytes: 1
    # Flags ZHNC: Z 0 H C 
    # Cycles: 1
    # TODO
    @opcode
    def adcad(self):
        print "ADC A D"

    #0x8b - ADC A E
    # Bytes: 1
    # Flags ZHNC: Z 0 H C 
    # Cycles: 1
    # TODO
    @opcode
    def adcae(self):
        print "ADC A E"

    #0x8c - ADC A H
    # Bytes: 1
    # Flags ZHNC: Z 0 H C 
    # Cycles: 1
    # TODO
    @opcode
    def adcah(self):
        print "ADC A H"

    #0x8d - ADC A L
    # Bytes: 1
    # Flags ZHNC: Z 0 H C 
    # Cycles: 1
    # TODO
    @opcode
    def adcal(self):
        print "ADC A L"

    #0x8e - ADC A (HL)
    # Bytes: 1
    # Flags ZHNC: Z 0 H C 
    # Cycles: 2
    # TODO
    @opcode
    def adcahl(self):
        print "ADC A (HL)"

    #0x8f - ADC A A
    # Bytes: 1
    # Flags ZHNC: Z 0 H C 
    # Cycles: 1
    # TODO
    @opcode
    def adcaa(self):
        print "ADC A A"

    #0x90 - SUB B
    # Bytes: 1
    # Flags ZHNC: Z 1 H C 
    # Cycles: 1
    # TODO
    @opcode
    def subb(self):
        print "SUB B"

    #0x91 - SUB C
    # Bytes: 1
    # Flags ZHNC: Z 1 H C 
    # Cycles: 1
    # TODO
    @opcode
    def subc(self):
        print "SUB C"

    #0x92 - SUB D
    # Bytes: 1
    # Flags ZHNC: Z 1 H C 
    # Cycles: 1
    # TODO
    @opcode
    def subd(self):
        print "SUB D"

    #0x93 - SUB E
    # Bytes: 1
    # Flags ZHNC: Z 1 H C 
    # Cycles: 1
    # TODO
    @opcode
    def sube(self):
        print "SUB E"

    #0x94 - SUB H
    # Bytes: 1
    # Flags ZHNC: Z 1 H C 
    # Cycles: 1
    # TODO
    @opcode
    def subh(self):
        print "SUB H"

    #0x95 - SUB L
    # Bytes: 1
    # Flags ZHNC: Z 1 H C 
    # Cycles: 1
    # TODO
    @opcode
    def subl(self):
        print "SUB L"

    #0x96 - SUB (HL)
    # Bytes: 1
    # Flags ZHNC: Z 1 H C 
    # Cycles: 2
    # TODO
    @opcode
    def subhl(self):
        print "SUB (HL)"

    #0x97 - SUB A
    # Bytes: 1
    # Flags ZHNC: Z 1 H C 
    # Cycles: 1
    # TODO
    @opcode
    def suba(self):
        print "SUB A"

    #0x98 - SBC A B
    # Bytes: 1
    # Flags ZHNC: Z 1 H C 
    # Cycles: 1
    # TODO
    @opcode
    def sbcab(self):
        print "SBC A B"

    #0x99 - SBC A C
    # Bytes: 1
    # Flags ZHNC: Z 1 H C 
    # Cycles: 1
    # TODO
    @opcode
    def sbcac(self):
        print "SBC A C"

    #0x9a - SBC A D
    # Bytes: 1
    # Flags ZHNC: Z 1 H C 
    # Cycles: 1
    # TODO
    @opcode
    def sbcad(self):
        print "SBC A D"

    #0x9b - SBC A E
    # Bytes: 1
    # Flags ZHNC: Z 1 H C 
    # Cycles: 1
    # TODO
    @opcode
    def sbcae(self):
        print "SBC A E"

    #0x9c - SBC A H
    # Bytes: 1
    # Flags ZHNC: Z 1 H C 
    # Cycles: 1
    # TODO
    @opcode
    def sbcah(self):
        print "SBC A H"

    #0x9d - SBC A L
    # Bytes: 1
    # Flags ZHNC: Z 1 H C 
    # Cycles: 1
    # TODO
    @opcode
    def sbcal(self):
        print "SBC A L"

    #0x9e - SBC A (HL)
    # Bytes: 1
    # Flags ZHNC: Z 1 H C 
    # Cycles: 2
    # TODO
    @opcode
    def sbcahl(self):
        print "SBC A (HL)"

    #0x9f - SBC A A
    # Bytes: 1
    # Flags ZHNC: Z 1 H C 
    # Cycles: 1
    # TODO
    @opcode
    def sbcaa(self):
        print "SBC A A"

    #0xa0 - AND B
    # Bytes: 1
    # Flags ZHNC: Z 0 1 0 
    # Cycles: 1
    # TODO
    @opcode
    def andb(self):
        print "AND B"

    #0xa1 - AND C
    # Bytes: 1
    # Flags ZHNC: Z 0 1 0 
    # Cycles: 1
    # TODO
    @opcode
    def andc(self):
        print "AND C"

    #0xa2 - AND D
    # Bytes: 1
    # Flags ZHNC: Z 0 1 0 
    # Cycles: 1
    # TODO
    @opcode
    def andd(self):
        print "AND D"

    #0xa3 - AND E
    # Bytes: 1
    # Flags ZHNC: Z 0 1 0 
    # Cycles: 1
    # TODO
    @opcode
    def ande(self):
        print "AND E"

    #0xa4 - AND H
    # Bytes: 1
    # Flags ZHNC: Z 0 1 0 
    # Cycles: 1
    # TODO
    @opcode
    def andh(self):
        print "AND H"

    #0xa5 - AND L
    # Bytes: 1
    # Flags ZHNC: Z 0 1 0 
    # Cycles: 1
    # TODO
    @opcode
    def andl(self):
        print "AND L"

    #0xa6 - AND (HL)
    # Bytes: 1
    # Flags ZHNC: Z 0 1 0 
    # Cycles: 2
    # TODO
    @opcode
    def andhl(self):
        print "AND (HL)"

    #0xa7 - AND A
    # Bytes: 1
    # Flags ZHNC: Z 0 1 0 
    # Cycles: 1
    # TODO
    @opcode
    def anda(self):
        print "AND A"

    #0xa8 - XOR B
    # Bytes: 1
    # Flags ZHNC: Z 0 0 0 
    # Cycles: 1
    # TODO
    @opcode
    def xorb(self):
        print "XOR B"

    #0xa9 - XOR C
    # Bytes: 1
    # Flags ZHNC: Z 0 0 0 
    # Cycles: 1
    # TODO
    @opcode
    def xorc(self):
        print "XOR C"

    #0xaa - XOR D
    # Bytes: 1
    # Flags ZHNC: Z 0 0 0 
    # Cycles: 1
    # TODO
    @opcode
    def xord(self):
        print "XOR D"

    #0xab - XOR E
    # Bytes: 1
    # Flags ZHNC: Z 0 0 0 
    # Cycles: 1
    # TODO
    @opcode
    def xore(self):
        print "XOR E"

    #0xac - XOR H
    # Bytes: 1
    # Flags ZHNC: Z 0 0 0 
    # Cycles: 1
    # TODO
    @opcode
    def xorh(self):
        print "XOR H"

    #0xad - XOR L
    # Bytes: 1
    # Flags ZHNC: Z 0 0 0 
    # Cycles: 1
    # TODO
    @opcode
    def xorl(self):
        print "XOR L"

    #0xae - XOR (HL)
    # Bytes: 1
    # Flags ZHNC: Z 0 0 0 
    # Cycles: 2
    # TODO
    @opcode
    def xorhl(self):
        print "XOR (HL)"

    #0xaf - XOR A
    # Bytes: 1
    # Flags ZHNC: Z 0 0 0 
    # Cycles: 1
    # TODO
    @opcode
    def xora(self):
        print "XOR A"

    #0xb0 - OR B
    # Bytes: 1
    # Flags ZHNC: Z 0 0 0 
    # Cycles: 1
    # TODO
    @opcode
    def orb(self):
        print "OR B"

    #0xb1 - OR C
    # Bytes: 1
    # Flags ZHNC: Z 0 0 0 
    # Cycles: 1
    # TODO
    @opcode
    def orc(self):
        print "OR C"

    #0xb2 - OR D
    # Bytes: 1
    # Flags ZHNC: Z 0 0 0 
    # Cycles: 1
    # TODO
    @opcode
    def ord(self):
        print "OR D"

    #0xb3 - OR E
    # Bytes: 1
    # Flags ZHNC: Z 0 0 0 
    # Cycles: 1
    # TODO
    @opcode
    def ore(self):
        print "OR E"

    #0xb4 - OR H
    # Bytes: 1
    # Flags ZHNC: Z 0 0 0 
    # Cycles: 1
    # TODO
    @opcode
    def orh(self):
        print "OR H"

    #0xb5 - OR L
    # Bytes: 1
    # Flags ZHNC: Z 0 0 0 
    # Cycles: 1
    # TODO
    @opcode
    def orl(self):
        print "OR L"

    #0xb6 - OR (HL)
    # Bytes: 1
    # Flags ZHNC: Z 0 0 0 
    # Cycles: 2
    # TODO
    @opcode
    def orhl(self):
        print "OR (HL)"

    #0xb7 - OR A
    # Bytes: 1
    # Flags ZHNC: Z 0 0 0 
    # Cycles: 1
    # TODO
    @opcode
    def ora(self):
        print "OR A"

    #0xb8 - CP B
    # Bytes: 1
    # Flags ZHNC: Z 1 H C 
    # Cycles: 1
    # TODO
    @opcode
    def cpb(self):
        print "CP B"

    #0xb9 - CP C
    # Bytes: 1
    # Flags ZHNC: Z 1 H C 
    # Cycles: 1
    # TODO
    @opcode
    def cpc(self):
        print "CP C"

    #0xba - CP D
    # Bytes: 1
    # Flags ZHNC: Z 1 H C 
    # Cycles: 1
    # TODO
    @opcode
    def cpd(self):
        print "CP D"

    #0xbb - CP E
    # Bytes: 1
    # Flags ZHNC: Z 1 H C 
    # Cycles: 1
    # TODO
    @opcode
    def cpe(self):
        print "CP E"

    #0xbc - CP H
    # Bytes: 1
    # Flags ZHNC: Z 1 H C 
    # Cycles: 1
    # TODO
    @opcode
    def cph(self):
        print "CP H"

    #0xbd - CP L
    # Bytes: 1
    # Flags ZHNC: Z 1 H C 
    # Cycles: 1
    # TODO
    @opcode
    def cpl(self):
        print "CP L"

    #0xbe - CP (HL)
    # Bytes: 1
    # Flags ZHNC: Z 1 H C 
    # Cycles: 2
    # TODO
    @opcode
    def cphl(self):
        print "CP (HL)"

    #0xbf - CP A
    # Bytes: 1
    # Flags ZHNC: Z 1 H C 
    # Cycles: 1
    # TODO
    @opcode
    def cpa(self):
        print "CP A"

    #0xc0 - RET NZ
    # Bytes: 1
    # Flags ZHNC: - - - - 
    # Cycles: 5/2/
    # TODO
    @opcode
    def retnz(self):
        print "RET NZ"

    #0xc1 - POP BC
    # Bytes: 1
    # Flags ZHNC: - - - - 
    # Cycles: 3
    # TODO
    @opcode
    def popbc(self):
        print "POP BC"

    #0xc2 - JP NZ a16
    # Bytes: 3
    # Flags ZHNC: - - - - 
    # Cycles: 4/3/
    # TODO
    @opcode
    def jpnza16(self):
        print "JP NZ a16"

    #0xc3 - JP a16
    # Bytes: 3
    # Flags ZHNC: - - - - 
    # Cycles: 4
    # TODO
    @opcode
    def jpa16(self):
        print "JP a16"

    #0xc4 - CALL NZ a16
    # Bytes: 3
    # Flags ZHNC: - - - - 
    # Cycles: 6/3/
    # TODO
    @opcode
    def callnza16(self):
        print "CALL NZ a16"

    #0xc5 - PUSH BC
    # Bytes: 1
    # Flags ZHNC: - - - - 
    # Cycles: 4
    # TODO
    @opcode
    def pushbc(self):
        print "PUSH BC"

    #0xc6 - ADD A d8
    # Bytes: 2
    # Flags ZHNC: Z 0 H C 
    # Cycles: 2
    # TODO
    @opcode
    def addad8(self):
        print "ADD A d8"

    #0xc7 - RST 00H
    # Bytes: 1
    # Flags ZHNC: - - - - 
    # Cycles: 4
    # TODO
    @opcode
    def rst00h(self):
        print "RST 00H"

    #0xc8 - RET Z
    # Bytes: 1
    # Flags ZHNC: - - - - 
    # Cycles: 5/2/
    # TODO
    @opcode
    def retz(self):
        print "RET Z"

    #0xc9 - RET
    # Bytes: 1
    # Flags ZHNC: - - - - 
    # Cycles: 4
    # TODO
    @opcode
    def ret(self):
        print "RET"

    #0xca - JP Z a16
    # Bytes: 3
    # Flags ZHNC: - - - - 
    # Cycles: 4/3/
    # TODO
    @opcode
    def jpza16(self):
        print "JP Z a16"

    #0xcb - PREFIX CB
    # Bytes: 1
    # Flags ZHNC: - - - - 
    # Cycles: 1
    # TODO
    @opcode
    def prefixcb(self):
        print "PREFIX CB"

    #0xcc - CALL Z a16
    # Bytes: 3
    # Flags ZHNC: - - - - 
    # Cycles: 6/3/
    # TODO
    @opcode
    def callza16(self):
        print "CALL Z a16"

    #0xcd - CALL a16
    # Bytes: 3
    # Flags ZHNC: - - - - 
    # Cycles: 6
    # TODO
    @opcode
    def calla16(self):
        print "CALL a16"

    #0xce - ADC A d8
    # Bytes: 2
    # Flags ZHNC: Z 0 H C 
    # Cycles: 2
    # TODO
    @opcode
    def adcad8(self):
        print "ADC A d8"

    #0xcf - RST 08H
    # Bytes: 1
    # Flags ZHNC: - - - - 
    # Cycles: 4
    # TODO
    @opcode
    def rst08h(self):
        print "RST 08H"

    #0xd0 - RET NC
    # Bytes: 1
    # Flags ZHNC: - - - - 
    # Cycles: 5/2/
    # TODO
    @opcode
    def retnc(self):
        print "RET NC"

    #0xd1 - POP DE
    # Bytes: 1
    # Flags ZHNC: - - - - 
    # Cycles: 3
    # TODO
    @opcode
    def popde(self):
        print "POP DE"

    #0xd2 - JP NC a16
    # Bytes: 3
    # Flags ZHNC: - - - - 
    # Cycles: 4/3/
    # TODO
    @opcode
    def jpnca16(self):
        print "JP NC a16"

    #0xd3 - undefined
    @opcode
    def undef1(self):
        print "undefined"

    #0xd4 - CALL NC a16
    # Bytes: 3
    # Flags ZHNC: - - - - 
    # Cycles: 6/3/
    # TODO
    @opcode
    def callnca16(self):
        print "CALL NC a16"

    #0xd5 - PUSH DE
    # Bytes: 1
    # Flags ZHNC: - - - - 
    # Cycles: 4
    # TODO
    @opcode
    def pushde(self):
        print "PUSH DE"

    #0xd6 - SUB d8
    # Bytes: 2
    # Flags ZHNC: Z 1 H C 
    # Cycles: 2
    # TODO
    @opcode
    def subd8(self):
        print "SUB d8"

    #0xd7 - RST 10H
    # Bytes: 1
    # Flags ZHNC: - - - - 
    # Cycles: 4
    # TODO
    @opcode
    def rst10h(self):
        print "RST 10H"

    #0xd8 - RET C
    # Bytes: 1
    # Flags ZHNC: - - - - 
    # Cycles: 5/2/
    # TODO
    @opcode
    def retc(self):
        print "RET C"

    #0xd9 - RETI
    # Bytes: 1
    # Flags ZHNC: - - - - 
    # Cycles: 4
    # TODO
    @opcode
    def reti(self):
        print "RETI"

    #0xda - JP C a16
    # Bytes: 3
    # Flags ZHNC: - - - - 
    # Cycles: 4/3/
    # TODO
    @opcode
    def jpca16(self):
        print "JP C a16"

    #0xdb - undefined
    @opcode
    def undef2(self):
        print "undefined"

    #0xdc - CALL C a16
    # Bytes: 3
    # Flags ZHNC: - - - - 
    # Cycles: 6/3/
    # TODO
    @opcode
    def callca16(self):
        print "CALL C a16"

    #0xdd - undefined
    @opcode
    def undef3(self):
        print "undefined"

    #0xde - SBC A d8
    # Bytes: 2
    # Flags ZHNC: Z 1 H C 
    # Cycles: 2
    # TODO
    @opcode
    def sbcad8(self):
        print "SBC A d8"

    #0xdf - RST 18H
    # Bytes: 1
    # Flags ZHNC: - - - - 
    # Cycles: 4
    # TODO
    @opcode
    def rst18h(self):
        print "RST 18H"

    #0xe0 - LDH (a8) A
    # Bytes: 2
    # Flags ZHNC: - - - - 
    # Cycles: 3
    # TODO
    @opcode
    def ldha8a(self):
        print "LDH (a8) A"

    #0xe1 - POP HL
    # Bytes: 1
    # Flags ZHNC: - - - - 
    # Cycles: 3
    # TODO
    @opcode
    def pophl(self):
        print "POP HL"

    #0xe2 - LD (C) A
    # Bytes: 2
    # Flags ZHNC: - - - - 
    # Cycles: 2
    # TODO
    @opcode
    def ldca(self):
        print "LD (C) A"

    #0xe3 - undefined
    @opcode
    def undef4(self):
        print "undefined"

    #0xe4 - undefined
    @opcode
    def undef5(self):
        print "undefined"

    #0xe5 - PUSH HL
    # Bytes: 1
    # Flags ZHNC: - - - - 
    # Cycles: 4
    # TODO
    @opcode
    def pushhl(self):
        print "PUSH HL"

    #0xe6 - AND d8
    # Bytes: 2
    # Flags ZHNC: Z 0 1 0 
    # Cycles: 2
    # TODO
    @opcode
    def andd8(self):
        print "AND d8"

    #0xe7 - RST 20H
    # Bytes: 1
    # Flags ZHNC: - - - - 
    # Cycles: 4
    # TODO
    @opcode
    def rst20h(self):
        print "RST 20H"

    #0xe8 - ADD SP r8
    # Bytes: 2
    # Flags ZHNC: 0 0 H C 
    # Cycles: 4
    # TODO
    @opcode
    def addspr8(self):
        print "ADD SP r8"

    #0xe9 - JP (HL)
    # Bytes: 1
    # Flags ZHNC: - - - - 
    # Cycles: 1
    # TODO
    @opcode
    def jphl(self):
        print "JP (HL)"

    #0xea - LD (a16) A
    # Bytes: 3
    # Flags ZHNC: - - - - 
    # Cycles: 4
    # TODO
    @opcode
    def lda16a(self):
        print "LD (a16) A"

    #0xeb - undefined
    @opcode
    def undef6(self):
        print "undefined"

    #0xec - undefined
    @opcode
    def undef7(self):
        print "undefined"

    #0xed - undefined
    @opcode
    def undef8(self):
        print "undefined"

    #0xee - XOR d8
    # Bytes: 2
    # Flags ZHNC: Z 0 0 0 
    # Cycles: 2
    # TODO
    @opcode
    def xord8(self):
        print "XOR d8"

    #0xef - RST 28H
    # Bytes: 1
    # Flags ZHNC: - - - - 
    # Cycles: 4
    # TODO
    @opcode
    def rst28h(self):
        print "RST 28H"

    #0xf0 - LDH A (a8)
    # Bytes: 2
    # Flags ZHNC: - - - - 
    # Cycles: 3
    # TODO
    @opcode
    def ldhaa8(self):
        print "LDH A (a8)"

    #0xf1 - POP AF
    # Bytes: 1
    # Flags ZHNC: Z N H C 
    # Cycles: 3
    # TODO
    @opcode
    def popaf(self):
        print "POP AF"

    #0xf2 - LD A (C)
    # Bytes: 2
    # Flags ZHNC: - - - - 
    # Cycles: 2
    # TODO
    @opcode
    def ldac(self):
        print "LD A (C)"

    #0xf3 - DI
    # Bytes: 1
    # Flags ZHNC: - - - - 
    # Cycles: 1
    # TODO
    @opcode
    def di(self):
        print "DI"

    #0xf4 - undefined
    @opcode
    def undef9(self):
        print "undefined"

    #0xf5 - PUSH AF
    # Bytes: 1
    # Flags ZHNC: - - - - 
    # Cycles: 4
    # TODO
    @opcode
    def pushaf(self):
        print "PUSH AF"

    #0xf6 - OR d8
    # Bytes: 2
    # Flags ZHNC: Z 0 0 0 
    # Cycles: 2
    # TODO
    @opcode
    def ord8(self):
        print "OR d8"

    #0xf7 - RST 30H
    # Bytes: 1
    # Flags ZHNC: - - - - 
    # Cycles: 4
    # TODO
    @opcode
    def rst30h(self):
        print "RST 30H"

    #0xf8 - LD HL SP+r8
    # Bytes: 2
    # Flags ZHNC: 0 0 H C 
    # Cycles: 3
    # TODO
    @opcode
    def ldhlspr8(self):
        print "LD HL SP+r8"

    #0xf9 - LD SP HL
    # Bytes: 1
    # Flags ZHNC: - - - - 
    # Cycles: 2
    # TODO
    @opcode
    def ldsphl(self):
        print "LD SP HL"

    #0xfa - LD A (a16)
    # Bytes: 3
    # Flags ZHNC: - - - - 
    # Cycles: 4
    # TODO
    @opcode
    def ldaa16(self):
        print "LD A (a16)"

    #0xfb - EI
    # Bytes: 1
    # Flags ZHNC: - - - - 
    # Cycles: 1
    # TODO
    @opcode
    def ei(self):
        print "EI"

    #0xfc - undefined
    @opcode
    def undef10(self):
        print "undefined"

    #0xfd - undefined
    @opcode
    def undef11(self):
        print "undefined"

    #0xfe - CP d8
    # Bytes: 2
    # Flags ZHNC: Z 1 H C 
    # Cycles: 2
    # TODO
    @opcode
    def cpd8(self):
        print "CP d8"

    #0xff - RST 38H
    # Bytes: 1
    # Flags ZHNC: - - - - 
    # Cycles: 4
    # TODO
    @opcode
    def rst38h(self):
        print "RST 38H"
