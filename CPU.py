from MMU import MMU

opcodes = []
def opcode (func):
  opcodes.append(func)
  return func

class CPU:
  
  ###############
  #INTERNAL STATE
  ###############

  def __init__ (self):
    #Clock
    self.ct = 0

    #Registers
    self.a = 0 # 8 bit
    self.b = 0
    self.c = 0
    self.d = 0
    self.e = 0
    self.h = 0
    self.l = 0
    self.pc, self.sp = [0]*2 # 16 bit
    self.m = 0               # Last clock

    #Flags
    self.fZero = False
    self.fSubtract = False
    self.fHalfCarry = False
    self.fCarry = False

    #MMU
    self.mmu = MMU(self)
  
  ###############
  #OPERATIONS
  ###############

  #0x00 - NOP
  @opcode
  def nop (self):
    print "NOP"
    self.m = 1

  #0x01 - LD BC, d16 TODO
  @opcode
  def ldbc16 (self):
    print "LD BC, d16"
    self.m = 3

  #0x02 - LD (BC) A TODO
  @opcode
  def ldbca (self):
    print "LD BC A"
    self.m = 2

  #0x03 - INC BC TODO
  @opcode
  def incbc (self):
    print "INC BC"
    self.m = 2

  #0x04 - INC B TODO
  @opcode
  def incb (self):
    print "INC B"
    self.m = 1

  #0x05 - DEC B TODO
  @opcode
  def decb (self):
    print "DEC B"
    self.m = 1

  #0x06 - LD B, d8 TODO
  @opcode
  def ldb8 (self):
    print "LD B, d8"
    self.m = 2

  #0x07 - RLCA TODO
  @opcode
  def rlca (self):
    print "RLCA"
    self.m = 1

  #0x08 - LD (a16), SP TODO
  @opcode
  def lda16sp (self):
    print "LD (a16), SP"
    self.m = 5

  #0x09 - ADD HL, BC
  @opcode
  def addhlbc (self):
    print "ADD HL, BC"
    self.m = 2

  #0x0A - LD A, (BC)
  @opcode
  def ldabc (self):
    print "LD A, (BC)"
    self.m = 2
