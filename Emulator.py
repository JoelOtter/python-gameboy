import CPU
import sys

rom_file = sys.argv[1]
cpu = CPU.CPU()
cpu.mmu.load(rom_file)
while (True):
    cpu.pc += 1
    op = cpu.mmu.rb(cpu.pc)
    CPU.opcodes[op](cpu)
    cpu.pc &= 65535
    cpu.cm += cpu.m
