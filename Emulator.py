import CPU
import sys

romFile = sys.argv[1]
cpu = CPU.CPU()
cpu.mmu.load(romFile)
while (True):
  cpu.pc += 1
  op = cpu.mmu.rb(cpu.pc)
  print "Op: " + str(op)
  CPU.opcodes[op](cpu)
  cpu.pc &= 65535
  cpu.cm += cpu.m
  cpu.ct += cpu.t
