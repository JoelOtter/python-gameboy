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
    index = addr & 0xF000

    # BIOS (256b)/ROM0
    if (index == 0x0000):
      if (self.inBios):
        if (addr < 0x0100):
          return self.bios[addr]
        elif (cpu.pc == 0x0100):
          self.inBios = False
      return self.rom[addr]

    # ROM0 + ROM1 (unbanked, 16k)
    elif (index <= 0x7000):
      return self.rom[addr]

    # VRAM (8k)
    elif (index <= 0x9000):
      #TODO gpu stuff
      return

    # External RAM (8k)
    elif (index <= 0xB000):
      return self.eram[addr & 0x1FFF]

    # Working RAM (8k) and Shadow
    elif (index <= 0xE000):
      return self.wram[addr & 0x1FFF]

    # Shadow, I/O, zero-page
    else:
      sIndex = addr & 0x0F00

      # Working RAM shadow
      if (sIndex <= 0xD00):
        return self.wram[addr & 0x1FFF]

      # Graphics: Object Attribute Memory
      # 160b, rest is 0
      elif (sIndex <= 0xE00):
        if (addr < 0xFEA0):
          #TODO return gpu stuff
          return
        else:
          return 0

      # Zero-page
      else:
        if (addr >= 0xFF80):
          return self.zram[addr & 0x7F]
        else: #TODO I/O stuff
          return 0

  def rw (self, addr):
    return self.rb(addr) + (self.rb(addr+1) << 8)

  def wb (self, addr, val):
    #Write 8 bits
    print "wb"

  def ww (self, addr, val):
    #Write 16 bits
    print "ww"
