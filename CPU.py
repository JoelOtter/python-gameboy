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
    self.ct, self.cm = [0]*2

    #Registers
    self.a = 0 # 8 bit
    self.b = 0
    self.c = 0
    self.d = 0
    self.e = 0
    self.h = 0
    self.l = 0
    self.pc, self.sp = [0]*2 # 16 bit
    self.m, self.t = [0]*2   # Last clock

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
    self.m = 1
    self.t = 4

  #0x01 - LD BC, d16
  @opcode
  def ldbc16 (self):
    #do stuff
    return
