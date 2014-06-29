import CPU
import sys

romFile = sys.argv[1]
cpu = CPU.CPU()
cpu.mmu.load(romFile)
