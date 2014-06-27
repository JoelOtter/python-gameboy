class MMU:

  def __init__ (self, cpu):
    self.inBios = True
    self.bios = []
    self.rom = []
    self.wram = []
    self.eram = []
    self.zram = []
    self.cpu = cpu

  def rb (self, addr):
    #Read 8 bits
    index = addr & 0xF000
    if (index == 0x0000):
      if (self.inBios):
        if (addr < 0x0100):
          return self.bios[addr]
        elif (cpu.pc == 0x0100):
          self.inBios = False
      return self.rom[addr]

    #others

  def rw (self, addr):
    #Read 16 bits
    print "rw"

  def wb (self, addr, val):
    #Write 8 bits
    print "wb"

  def ww (self, addr, val):
    #Write 16 bits
    print "ww"
