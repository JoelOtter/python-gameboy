from MMU import MMU

class CPU:
  
  ###############
  #INTERNAL STATE
  ###############

  #Clock
  ct, cm = [0]*2

  #Registers
  a, b, c, d, e, h, l, f = [0]*8 # 8  bit
  pc, sp = [0]*2                 # 16 bit
  m, t = [0]*2                   # Last clock

  #MMU
  mmu = MMU()
  
  ###############
  #OPERATIONS
  ###############
