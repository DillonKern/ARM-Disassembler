import sys
import os

for i in range(len(sys.argv)):
    if (sys.argv[i] == '-i' and i < (len(sys.argv) - 1)):
        inputFileName = sys.argv[i + 1]
    elif (sys.argv[i] == '-o' and i < (len(sys.argv) - 1)):
        outputFileName = sys.argv[i + 1]

specialMask = 0x1FFFFF

rnMask = 0x3E0
rmMask = 0x1F0000
rdMask = 0x1F
imMask = 0x3FFC00
shmtMask = 0xFC00
addrMask = 0x1FF000
addrCBMask = 0xFFFFE0
imsftMask = 0x600000
imdataMask = 0x1FFFE0

opcodeStr = []
validStr = []
instrSpaced = []
arg1 = []
arg2 = []
arg3 = []
arg1Str = []
arg2Str = []
arg3Str = []
mem = []
opcode = []
instructions = []
data = []
dataPrint = []
registers = [0] * 32
i = 0
j = 0
memoryLocationDis = 96
memoryLocationSim = 96
memoryLocationData = 96
cycle = 1

class Disassembler:

    def run(self):
        global opcodeStr
        global validStr
        global arg1
        global arg2
        global arg3
        global arg1Str
        global arg2Str
        global arg3Str
        global mem
        global opcode
        global instructions
        global i
        global data
        global memoryLocationData

        global specialMask
        global rnMask
        global rmMask
        global rdMask
        global imMask
        global shmtMask
        global addrMask
        global addrCBMask
        global imsftMask
        global imdataMask

        opcode.append(binaryToDecimal(instructions[0:11]))

        def printBinaryandMemory(instructions):
            global memoryLocationDis
            global i

            instrSpaced.append(instructions[0:8] + ' ' + instructions[8:11] + ' ' + instructions[11:16] + ' ' +
                               instructions[16:21] + ' ' + instructions[21:26] + ' ' + instructions[26:32] + '\t')


            mem.append(str(memoryLocationDis) + '\t')
            outFileDis.write(str(instrSpaced[i]) + str(mem[i]))

            memoryLocationDis += 4

        printBinaryandMemory(instructions)

        if opcode[i] >= 160 and opcode[i] <= 191:
            opcodeStr.append('B')
            validStr.append('Y')

            if (instructions[6] == '0'):
                arg1.append((int(instructions, base=2) & specialMask))
                arg2.append((int(instructions, base=2) & specialMask))
                arg3.append((int(instructions, base=2) & specialMask))
                arg1Str.append('\t#' + str(arg3[i]) + '\n')
                arg2Str.append('\t#' + str(arg1[i]) + '\n')
                arg3Str.append('\t#' + str(arg2[i]) + '\n')

            elif (instructions[6] == '1'):
                address = instructions[6:32]
                value = twosComplement(int(address, 2), len(address))

                arg1.append(value)
                arg2.append(value)
                arg3.append(value)
                arg1Str.append('\t#' + str(arg3[i]) + '\n')
                arg2Str.append('\t#' + str(arg1[i]) + '\n')
                arg3Str.append('\t#' + str(arg2[i]) + '\n')

            data.append(0)
            dataPrint.append(0)
            outFileDis.write(opcodeStr[i] + "   " + arg1Str[i])

        elif opcode[i] == 1104:
            opcodeStr.append('AND')
            validStr.append('Y')

            arg1.append((int(instructions, base=2) & rnMask) >> 5)
            arg2.append((int(instructions, base=2) & rmMask) >> 16)
            arg3.append((int(instructions, base=2) & rdMask) >> 0)
            arg1Str.append('\tR' + str(arg3[i]))
            arg2Str.append(', R' + str(arg1[i]))
            arg3Str.append(', R' + str(arg2[i]) + '\n')

            data.append(0)
            dataPrint.append(0)
            outFileDis.write(opcodeStr[i] + " " + arg1Str[i] + arg2Str[i] + arg3Str[i])

        elif opcode[i] == 1112:
            opcodeStr.append('ADD')
            validStr.append('Y')

            arg1.append((int(instructions, base=2) & rnMask) >> 5)
            arg2.append((int(instructions, base=2) & rmMask) >> 16)
            arg3.append((int(instructions, base=2) & rdMask) >> 0)
            arg1Str.append('\tR' + str(arg3[i]))
            arg2Str.append(', R' + str(arg1[i]))
            arg3Str.append(', R' + str(arg2[i]) + '\n')

            data.append(0)
            dataPrint.append(0)
            outFileDis.write(opcodeStr[i] + " " + arg1Str[i] + arg2Str[i] + arg3Str[i])

        elif opcode[i] >= 1160 and opcode[i] <= 1161:
            opcodeStr.append('ADDI')
            validStr.append('Y')

            if (instructions[10] == '0'):
                arg1.append((int(instructions, base=2) & rnMask) >> 5)
                arg2.append((int(instructions, base=2) & imMask) >> 10)
                arg3.append((int(instructions, base=2) & rdMask) >> 0)
                arg1Str.append('\tR' + str(arg3[i]))
                arg2Str.append(', R' + str(arg1[i]))
                arg3Str.append(', #' + str(arg2[i]) + '\n')

            elif (instructions[10] == '1'):
                immediate = instructions[10:22]
                value = twosComplement(int(immediate, 2), len(immediate))

                arg1.append((int(instructions, base=2) & rnMask) >> 5)
                arg2.append(value)
                arg3.append((int(instructions, base=2) & rdMask) >> 0)
                arg1Str.append('\tR' + str(arg3[i]))
                arg2Str.append(', R' + str(arg1[i]))
                arg3Str.append(', #' + str(arg2[i]) + '\n')

            data.append(0)
            dataPrint.append(0)
            outFileDis.write(opcodeStr[i] + arg1Str[i] + arg2Str[i] + arg3Str[i])

        elif opcode[i] == 1360:
            opcodeStr.append('ORR')
            validStr.append('Y')

            arg1.append((int(instructions, base=2) & rnMask) >> 5)
            arg2.append((int(instructions, base=2) & rmMask) >> 16)
            arg3.append((int(instructions, base=2) & rdMask) >> 0)
            arg1Str.append('\tR' + str(arg3[i]))
            arg2Str.append(', R' + str(arg1[i]))
            arg3Str.append(', R' + str(arg2[i]) + '\n')

            data.append(0)
            dataPrint.append(0)
            outFileDis.write(opcodeStr[i] + " " + arg1Str[i] + arg2Str[i] + arg3Str[i])

        elif opcode[i] >= 1440 and opcode[i] <= 1447:
            opcodeStr.append('CBZ')
            validStr.append('Y')

            if (instructions[8] == '0'):
                arg1.append((int(instructions, base=2) & addrCBMask) >> 5)
                arg2.append((int(instructions, base=2) & addrCBMask) >> 5)
                arg3.append((int(instructions, base=2) & rdMask) >> 0)
                arg1Str.append('\tR' + str(arg3[i]))
                arg2Str.append(', #' + str(arg1[i]) + '\n')
                arg3Str.append('' + str(arg2[i]) + '\n')

            elif (instructions[8] == '1'):
                address = instructions[8:27]
                value = twosComplement(int(address, 2), len(address))

                arg1.append(value)
                arg2.append(value)
                arg3.append((int(instructions, base=2) & rdMask) >> 0)
                arg1Str.append('\tR' + str(arg3[i]))
                arg2Str.append(', #' + str(arg1[i]) + '\n')
                arg3Str.append('' + str(arg2[i]) + '\n')

            data.append(0)
            dataPrint.append(0)
            outFileDis.write(opcodeStr[i] + " " + arg1Str[i] + arg2Str[i])

        elif opcode[i] >= 1448 and opcode[i] <= 1455:
            opcodeStr.append('CBNZ')
            validStr.append('Y')

            if (instructions[8] == '0'):
                arg1.append((int(instructions, base=2) & addrCBMask) >> 5)
                arg2.append((int(instructions, base=2) & addrCBMask) >> 5)
                arg3.append((int(instructions, base=2) & rdMask) >> 0)
                arg1Str.append('\tR' + str(arg3[i]))
                arg2Str.append(', #' + str(arg1[i]) + '\n')
                arg3Str.append('' + str(arg2[i]) + '\n')

            elif (instructions[8] == '1'):
                address = instructions[8:27]
                value = twosComplement(int(address, 2), len(address))

                arg1.append(value)
                arg2.append(value)
                arg3.append((int(instructions, base=2) & rdMask) >> 0)
                arg1Str.append('\tR' + str(arg3[i]))
                arg2Str.append(', #' + str(arg1[i]) + '\n')
                arg3Str.append('' + str(arg2[i]) + '\n')

            data.append(0)
            dataPrint.append(0)
            outFileDis.write(opcodeStr[i] + arg1Str[i] + arg2Str[i])

        elif opcode[i] == 1624:
            opcodeStr.append('SUB')
            validStr.append('Y')

            arg1.append((int(instructions, base=2) & rnMask) >> 5)
            arg2.append((int(instructions, base=2) & rmMask) >> 16)
            arg3.append((int(instructions, base=2) & rdMask) >> 0)
            arg1Str.append('\tR' + str(arg3[i]))
            arg2Str.append(', R' + str(arg1[i]))
            arg3Str.append(', R' + str(arg2[i]) + '\n')

            data.append(0)
            dataPrint.append(0)
            outFileDis.write(opcodeStr[i] + " " + arg1Str[i] + arg2Str[i] + arg3Str[i])

        elif opcode[i] >= 1672 and opcode[i] <= 1673:
            opcodeStr.append('SUBI')
            validStr.append('Y')

            if (instructions[10] == '0'):
                arg1.append((int(instructions, base=2) & rnMask) >> 5)
                arg2.append((int(instructions, base=2) & imMask) >> 10)
                arg3.append((int(instructions, base=2) & rdMask) >> 0)
                arg1Str.append('\tR' + str(arg3[i]))
                arg2Str.append(', R' + str(arg1[i]))
                arg3Str.append(', #' + str(arg2[i]) + '\n')
            elif (instructions[10] == '1'):
                immediate = instructions[10:22]
                value = twosComplement(int(immediate, 2), len(immediate))

                arg1.append((int(instructions, base=2) & rnMask) >> 5)
                arg2.append(value)
                arg3.append((int(instructions, base=2) & rdMask) >> 0)
                arg1Str.append('\tR' + str(arg3[i]))
                arg2Str.append(', R' + str(arg1[i]))
                arg3Str.append(', #' + str(arg2[i]) + '\n')

            data.append(0)
            dataPrint.append(0)
            outFileDis.write(opcodeStr[i] + arg1Str[i] + arg2Str[i] + arg3Str[i])

        elif opcode[i] >= 1684 and opcode[i] <= 1687:
            opcodeStr.append('MOVZ')
            validStr.append('Y')

            arg1.append((int(instructions, base=2) & imdataMask) >> 5)
            arg2.append(((int(instructions, base=2) & imsftMask) >> 21) * 16)
            arg3.append((int(instructions, base=2) & rdMask) >> 0)
            arg1Str.append('\tR' + str(arg3[i]))
            arg2Str.append(', ' + str(arg1[i]))
            arg3Str.append(', LSL ' + str(arg2[i]) + '\n')

            data.append(0)
            dataPrint.append(0)
            outFileDis.write(opcodeStr[i] + arg1Str[i] + arg2Str[i] + arg3Str[i])

        elif opcode[i] >= 1940 and opcode[i] <= 1943:
            opcodeStr.append('MOVK')
            validStr.append('Y')

            arg1.append((int(instructions, base=2) & imdataMask) >> 5)
            arg2.append(((int(instructions, base=2) & imsftMask) >> 21) * 16)
            arg3.append((int(instructions, base=2) & rdMask) >> 0)
            arg1Str.append('\tR' + str(arg3[i]))
            arg2Str.append(', ' + str(arg1[i]))
            arg3Str.append(', LSL ' + str(arg2[i]) + '\n')

            data.append(0)
            dataPrint.append(0)
            outFileDis.write(opcodeStr[i] + arg1Str[i] + arg2Str[i] + arg3Str[i])

        elif opcode[i] == 1690:
            opcodeStr.append('LSR')
            validStr.append('Y')

            arg1.append((int(instructions, base=2) & rnMask) >> 5)
            arg2.append((int(instructions, base=2) & shmtMask) >> 10)
            arg3.append((int(instructions, base=2) & rdMask) >> 0)
            arg1Str.append('\tR' + str(arg3[i]))
            arg2Str.append(', R' + str(arg1[i]))
            arg3Str.append(', #' + str(arg2[i]) + '\n')

            data.append(0)
            dataPrint.append(0)
            outFileDis.write(opcodeStr[i] + " " + arg1Str[i] + arg2Str[i] + arg3Str[i])

        elif opcode[i] == 1691:
            opcodeStr.append('LSL')
            validStr.append('Y')

            arg1.append((int(instructions, base=2) & rnMask) >> 5)
            arg2.append((int(instructions, base=2) & shmtMask) >> 10)
            arg3.append((int(instructions, base=2) & rdMask) >> 0)
            arg1Str.append('\tR' + str(arg3[i]))
            arg2Str.append(', R' + str(arg1[i]))
            arg3Str.append(', #' + str(arg2[i]) + '\n')

            data.append(0)
            dataPrint.append(0)
            outFileDis.write(opcodeStr[i] + " " + arg1Str[i] + arg2Str[i] + arg3Str[i])

        elif opcode[i] == 1692:
            opcodeStr.append('ASR')
            validStr.append('Y')

            arg1.append((int(instructions, base=2) & rnMask) >> 5)
            arg2.append((int(instructions, base=2) & shmtMask) >> 10)
            arg3.append((int(instructions, base=2) & rdMask) >> 0)
            arg1Str.append('\tR' + str(arg3[i]))
            arg2Str.append(', R' + str(arg1[i]))
            arg3Str.append(', #' + str(arg2[i]) + '\n')

            data.append(0)
            dataPrint.append(0)
            outFileDis.write(opcodeStr[i] + " " + arg1Str[i] + arg2Str[i] + arg3Str[i])

        elif opcode[i] == 1984:
            opcodeStr.append('STUR')
            validStr.append('Y')

            arg1.append((int(instructions, base=2) & rnMask) >> 5)
            arg2.append((int(instructions, base=2) & addrMask) >> 12)
            arg3.append((int(instructions, base=2) & rdMask) >> 0)
            arg1Str.append('\tR' + str(arg3[i]))
            arg2Str.append(', [R' + str(arg1[i]))
            arg3Str.append(', #' + str(arg2[i]) + ']\n')

            data.append(0)
            dataPrint.append(0)
            outFileDis.write(opcodeStr[i] + arg1Str[i] + arg2Str[i] + arg3Str[i])

        elif opcode[i] == 1986:
            opcodeStr.append('LDUR')
            validStr.append('Y')

            arg1.append((int(instructions, base=2) & rnMask) >> 5)
            arg2.append((int(instructions, base=2) & addrMask) >> 12)
            arg3.append((int(instructions, base=2) & rdMask) >> 0)
            arg1Str.append('\tR' + str(arg3[i]))
            arg2Str.append(', [R' + str(arg1[i]))
            arg3Str.append(', #' + str(arg2[i]) + ']\n')

            data.append(0)
            dataPrint.append(0)
            outFileDis.write(opcodeStr[i] + arg1Str[i] + arg2Str[i] + arg3Str[i])

        elif opcode[i] == 1872:
            opcodeStr.append('EOR')
            validStr.append('Y')

            arg1.append((int(instructions, base=2) & rnMask) >> 5)
            arg2.append((int(instructions, base=2) & rmMask) >> 16)
            arg3.append((int(instructions, base=2) & rdMask) >> 0)
            arg1Str.append('\tR' + str(arg3[i]))
            arg2Str.append(', R' + str(arg1[i]))
            arg3Str.append(', R' + str(arg2[i]) + '\n')

            data.append(0)
            dataPrint.append(0)
            outFileDis.write(opcodeStr[i] + " " + arg1Str[i] + arg2Str[i] + arg3Str[i])

        elif int(instructions,2) == 0:
            opcodeStr.append('NOP\n')
            validStr.append('Y')

            arg1.append('')
            arg2.append('')
            arg3.append('')
            arg1Str.append(str(arg3[i]))
            arg2Str.append(str(arg1[i]))
            arg3Str.append(str(arg2[i]))

            data.append(0)
            dataPrint.append(0)
            outFileDis.write(opcodeStr[i])

        elif opcode[i] == 2038:
            opcodeStr.append('BREAK')
            validStr.append('Y')

            arg1.append('')
            arg2.append('')
            arg3.append('')
            arg1Str.append(str(arg3[i]))
            arg2Str.append(str(arg1[i]))
            arg3Str.append(str(arg2[i]) + '\n')

            data.append(0)
            dataPrint.append(0)
            memoryLocationData = memoryLocationDis
            outFileDis.write(opcodeStr[i] + '\n')

        else:
            opcodeStr.append('Data\n')
            validStr.append('N')

            arg1.append('')
            arg2.append('')
            arg3.append('')
            arg1Str.append(str(arg3[i]))
            arg2Str.append(str(arg1[i]))
            arg3Str.append(str(arg2[i]))

            if int(instructions,2) >> 31 == 1:
                twosComp = (0xFFFFFFFF ^ int(instructions,2)) + 1
                value = int(twosComp) * -1
                data.append(value)
                dataPrint.append(value)

            elif int(instructions,2) >> 31 == 0:
                data.append(int(instructions,2))
                dataPrint.append(int(instructions,2))

            outFileDis.write(str(data[i]) + '\n')

        i += 1

class Simulator:

    def run(self):
        global opcodeStr
        global arg1
        global arg2
        global arg3
        global arg1Str
        global arg2Str
        global arg3Str
        global instructions
        global registers
        global j
        global dataPrint
        global cycle
        global memoryLocationSim

        def dataForSim():
            global memoryLocationData

            if not dataPrint:
                outFileSim.write('\n')
                return

            if dataPrint:
                memoryLocationInitial = memoryLocationData

                outFileSim.write(str(memoryLocationData) + ':\t')

                minOfDataArray = 0
                maxOfDataArray = 8
                lengthOfDataArray = len(dataPrint)

                while lengthOfDataArray != 0 and lengthOfDataArray > 0:
                    if lengthOfDataArray > 8:
                        for x in range(minOfDataArray, maxOfDataArray):
                            outFileSim.write(str(dataPrint[x]) + '\t')
                            x += 1
                        minOfDataArray += 8
                        maxOfDataArray += 8
                        lengthOfDataArray -= 8
                        memoryLocationData += 32
                        outFileSim.write('\n' + str(memoryLocationData) + ':\t')
                    else:
                        for x in range(minOfDataArray, len(dataPrint)):
                            outFileSim.write(str(dataPrint[x]) + '\t')
                            x += 1
                        lengthOfDataArray -= 8

            memoryLocationData = memoryLocationInitial

            outFileSim.write('\n\n')

        memoryLocationSim = 96

        while True:

            j = (memoryLocationSim - 96)/4

            if opcodeStr[j] == 'BREAK':
                outFileSim.write('====================\n' + 'cycle:' + str(cycle) + '\t' + str(memoryLocationSim) + '\t')
                outFileSim.write(str(opcodeStr[j]) + '\n')
                outFileSim.write('\nregisters:')
                outFileSim.write('\nr00:\t')
                for x in range(0, 8):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1
                outFileSim.write('\nr08:\t')
                for x in range(8, 16):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1
                outFileSim.write('\nr16:\t')
                for x in range(16, 24):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1
                outFileSim.write('\nr24:\t')
                for x in range(24, 32):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1

                outFileSim.write('\n\ndata:' + '\n')
                dataForSim()
                break

            elif opcodeStr[j] == 'B':
                outFileSim.write('====================\n' + 'cycle:' + str(cycle) + '\t' + str(memoryLocationSim) + '\t')
                outFileSim.write(str(opcodeStr[j]) + str(arg1Str[j]))
                outFileSim.write('\nregisters:')
                outFileSim.write('\nr00:\t')
                for x in range(0, 8):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1
                outFileSim.write('\nr08:\t')
                for x in range(8, 16):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1
                outFileSim.write('\nr16:\t')
                for x in range(16, 24):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1
                outFileSim.write('\nr24:\t')
                for x in range(24, 32):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1

                outFileSim.write('\n\ndata:' + '\n')
                dataForSim()

                addrValue = arg1[j]
                memoryLocationSim += (addrValue * 4)

            elif opcodeStr[j] == 'AND':
                rnValue = arg1[j]
                rmValue = arg2[j]
                rdValue = arg3[j]

                registers[rdValue] = registers[rnValue] & registers[rmValue]

                outFileSim.write('====================\n' + 'cycle:' + str(cycle) + '\t' + str(memoryLocationSim) + '\t')
                outFileSim.write(str(opcodeStr[j]) + str(arg1Str[j]) + str(arg2Str[j]) + str(arg3Str[j]))
                outFileSim.write('\nregisters:')
                outFileSim.write('\nr00:\t')
                for x in range(0, 8):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1
                outFileSim.write('\nr08:\t')
                for x in range(8, 16):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1
                outFileSim.write('\nr16:\t')
                for x in range(16, 24):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1
                outFileSim.write('\nr24:\t')
                for x in range(24, 32):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1

                outFileSim.write('\n\ndata:' + '\n')
                dataForSim()

                memoryLocationSim += 4

            elif opcodeStr[j] == 'ADD':
                rnValue = arg1[j]
                rmValue = arg2[j]
                rdValue = arg3[j]

                registers[rdValue] = registers[rnValue] + registers[rmValue]

                outFileSim.write('====================\n' + 'cycle:' + str(cycle) + '\t' + str(memoryLocationSim) + '\t')
                outFileSim.write(str(opcodeStr[j]) + str(arg1Str[j]) + str(arg2Str[j]) + str(arg3Str[j]))
                outFileSim.write('\nregisters:')
                outFileSim.write('\nr00:\t')
                for x in range(0, 8):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1
                outFileSim.write('\nr08:\t')
                for x in range(8, 16):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1
                outFileSim.write('\nr16:\t')
                for x in range(16, 24):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1
                outFileSim.write('\nr24:\t')
                for x in range(24, 32):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1

                outFileSim.write('\n\ndata:' + '\n')
                dataForSim()

                memoryLocationSim += 4

            elif opcodeStr[j] == 'ADDI':
                rnValue = arg1[j]
                imValue = arg2[j]
                rdValue = arg3[j]

                registers[rdValue] = registers[rnValue] + imValue

                outFileSim.write('====================\n' + 'cycle:' + str(cycle) + '\t' + str(memoryLocationSim) + '\t')
                outFileSim.write(str(opcodeStr[j]) + str(arg1Str[j]) + str(arg2Str[j]) + str(arg3Str[j]))
                outFileSim.write('\nregisters:')
                outFileSim.write('\nr00:\t')
                for x in range(0, 8):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1
                outFileSim.write('\nr08:\t')
                for x in range(8, 16):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1
                outFileSim.write('\nr16:\t')
                for x in range(16, 24):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1
                outFileSim.write('\nr24:\t')
                for x in range(24, 32):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1

                outFileSim.write('\n\ndata:' + '\n')
                dataForSim()

                memoryLocationSim += 4

            elif opcodeStr[j] == 'ORR':
                rnValue = arg1[j]
                rmValue = arg2[j]
                rdValue = arg3[j]

                registers[rdValue] = registers[rnValue] | registers[rmValue]

                outFileSim.write('====================\n' + 'cycle:' + str(cycle) + '\t' + str(memoryLocationSim) + '\t')
                outFileSim.write(str(opcodeStr[j]) + str(arg1Str[j]) + str(arg2Str[j]) + str(arg3Str[j]))
                outFileSim.write('\nregisters:')
                outFileSim.write('\nr00:\t')
                for x in range(0, 8):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1
                outFileSim.write('\nr08:\t')
                for x in range(8, 16):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1
                outFileSim.write('\nr16:\t')
                for x in range(16, 24):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1
                outFileSim.write('\nr24:\t')
                for x in range(24, 32):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1

                outFileSim.write('\n\ndata:' + '\n')
                dataForSim()

                memoryLocationSim += 4

            elif opcodeStr[j] == 'CBZ':
                outFileSim.write('====================\n' + 'cycle:' + str(cycle) + '\t' + str(memoryLocationSim) + '\t')
                outFileSim.write(str(opcodeStr[j]) + str(arg1Str[j]) + str(arg2Str[j]))
                outFileSim.write('\nregisters:')
                outFileSim.write('\nr00:\t')
                for x in range(0, 8):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1
                outFileSim.write('\nr08:\t')
                for x in range(8, 16):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1
                outFileSim.write('\nr16:\t')
                for x in range(16, 24):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1
                outFileSim.write('\nr24:\t')
                for x in range(24, 32):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1

                outFileSim.write('\n\ndata:' + '\n')
                dataForSim()

                rdValue = arg3[j]
                addrValue = arg1[j]

                if registers[rdValue] == 0:
                    memoryLocationSim += (addrValue * 4)
                else:
                    memoryLocationSim += 4

            elif opcodeStr[j] == 'CBNZ':
                rdValue = arg3[j]
                addrValue = arg1[j]

                outFileSim.write('====================\n' + 'cycle:' + str(cycle) + '\t' + str(memoryLocationSim) + '\t')
                outFileSim.write(str(opcodeStr[j]) + str(arg1Str[j]) + str(arg2Str[j]))
                outFileSim.write('\nregisters:')
                outFileSim.write('\nr00:\t')
                for x in range(0, 8):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1
                outFileSim.write('\nr08:\t')
                for x in range(8, 16):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1
                outFileSim.write('\nr16:\t')
                for x in range(16, 24):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1
                outFileSim.write('\nr24:\t')
                for x in range(24, 32):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1

                outFileSim.write('\n\ndata:' + '\n')
                dataForSim()

                if registers[rdValue] != 0:
                    memoryLocationSim += (addrValue * 4)
                else:
                    memoryLocationSim += 4

            elif opcodeStr[j] == 'SUB':
                rnValue = arg1[j]
                rmValue = arg2[j]
                rdValue = arg3[j]

                registers[rdValue] = registers[rnValue] - registers[rmValue]

                outFileSim.write('====================\n' + 'cycle:' + str(cycle) + '\t' + str(memoryLocationSim) + '\t')
                outFileSim.write(str(opcodeStr[j]) + str(arg1Str[j]) + str(arg2Str[j]) + str(arg3Str[j]))
                outFileSim.write('\nregisters:')
                outFileSim.write('\nr00:\t')
                for x in range(0, 8):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1
                outFileSim.write('\nr08:\t')
                for x in range(8, 16):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1
                outFileSim.write('\nr16:\t')
                for x in range(16, 24):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1
                outFileSim.write('\nr24:\t')
                for x in range(24, 32):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1

                outFileSim.write('\n\ndata:' + '\n')
                dataForSim()

                memoryLocationSim += 4

            elif opcodeStr[j] == 'SUBI':
                rnValue = arg1[j]
                imValue = arg2[j]
                rdValue = arg3[j]

                registers[rdValue] = registers[rnValue] - imValue

                outFileSim.write('====================\n' + 'cycle:' + str(cycle) + '\t' + str(memoryLocationSim) + '\t')
                outFileSim.write(str(opcodeStr[j]) + str(arg1Str[j]) + str(arg2Str[j]) + str(arg3Str[j]))
                outFileSim.write('\nregisters:')
                outFileSim.write('\nr00:\t')
                for x in range(0, 8):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1
                outFileSim.write('\nr08:\t')
                for x in range(8, 16):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1
                outFileSim.write('\nr16:\t')
                for x in range(16, 24):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1
                outFileSim.write('\nr24:\t')
                for x in range(24, 32):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1

                outFileSim.write('\n\ndata:' + '\n')
                dataForSim()

                memoryLocationSim += 4

            elif opcodeStr[j] == 'MOVZ':
                imdataValue = arg1[j]
                imsftValue = arg2[j]
                rdValue = arg3[j]

                registers[rdValue] = imdataValue << imsftValue

                outFileSim.write('====================\n' + 'cycle:' + str(cycle) + '\t' + str(memoryLocationSim) + '\t')
                outFileSim.write(str(opcodeStr[j]) + str(arg1Str[j]) + str(arg2Str[j]) + str(arg3Str[j]))
                outFileSim.write('\nregisters:')
                outFileSim.write('\nr00:\t')
                for x in range(0, 8):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1
                outFileSim.write('\nr08:\t')
                for x in range(8, 16):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1
                outFileSim.write('\nr16:\t')
                for x in range(16, 24):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1
                outFileSim.write('\nr24:\t')
                for x in range(24, 32):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1

                outFileSim.write('\n\ndata:' + '\n')
                dataForSim()

                memoryLocationSim += 4

            elif opcodeStr[j] == 'MOVK':
                imdataValue = arg1[j]
                imsftValue = arg2[j]
                rdValue = arg3[j]

                mask = 0xFFFF << imsftValue
                registers[rdValue] = registers[rdValue] & ~mask
                registers[rdValue] = registers[rdValue] | (imdataValue << imsftValue)

                outFileSim.write('====================\n' + 'cycle:' + str(cycle) + '\t' + str(memoryLocationSim) + '\t')
                outFileSim.write(str(opcodeStr[j]) + str(arg1Str[j]) + str(arg2Str[j]) + str(arg3Str[j]))
                outFileSim.write('\nregisters:')
                outFileSim.write('\nr00:\t')
                for x in range(0, 8):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1
                outFileSim.write('\nr08:\t')
                for x in range(8, 16):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1
                outFileSim.write('\nr16:\t')
                for x in range(16, 24):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1
                outFileSim.write('\nr24:\t')
                for x in range(24, 32):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1

                outFileSim.write('\n\ndata:' + '\n')
                dataForSim()

                memoryLocationSim += 4

            elif opcodeStr[j] == 'LSR':
                rnValue = arg1[j]
                shmtValue = arg2[j]
                rdValue = arg3[j]

                if rnValue < 0:
                    binrep = '{0:b}'.format(-1 * registers[rnValue])
                    lenrep = len(binrep)
                    mask = "1" * shmtValue + "0" * (lenrep - shmtValue)
                    registers[rdValue] = -((int(binrep, 2) >> shmtValue) | int(mask, 2))
                else:
                    binrep = '{0:b}'.format(registers[arg2[j]])
                    registers[rdValue] = (registers[rnValue] >> shmtValue)

                outFileSim.write('====================\n' + 'cycle:' + str(cycle) + '\t' + str(memoryLocationSim) + '\t')
                outFileSim.write(str(opcodeStr[j]) + str(arg1Str[j]) + str(arg2Str[j]) + str(arg3Str[j]))
                outFileSim.write('\nregisters:')
                outFileSim.write('\nr00:\t')
                for x in range(0, 8):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1
                outFileSim.write('\nr08:\t')
                for x in range(8, 16):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1
                outFileSim.write('\nr16:\t')
                for x in range(16, 24):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1
                outFileSim.write('\nr24:\t')
                for x in range(24, 32):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1

                outFileSim.write('\n\ndata:' + '\n')
                dataForSim()

                memoryLocationSim += 4

            elif opcodeStr[j] == 'LSL':
                rnValue = arg1[j]
                shmtValue = arg2[j]
                rdValue = arg3[j]

                registers[rdValue] = registers[rnValue] << shmtValue

                outFileSim.write('====================\n' + 'cycle:' + str(cycle) + '\t' + str(memoryLocationSim) + '\t')
                outFileSim.write(str(opcodeStr[j]) + str(arg1Str[j]) + str(arg2Str[j]) + str(arg3Str[j]))
                outFileSim.write('\nregisters:')
                outFileSim.write('\nr00:\t')
                for x in range(0, 8):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1
                outFileSim.write('\nr08:\t')
                for x in range(8, 16):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1
                outFileSim.write('\nr16:\t')
                for x in range(16, 24):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1
                outFileSim.write('\nr24:\t')
                for x in range(24, 32):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1

                outFileSim.write('\n\ndata:' + '\n')
                dataForSim()

                memoryLocationSim += 4

            elif opcodeStr[j] == 'ASR':
                rnValue = arg1[j]
                shmtValue = arg2[j]
                rdValue = arg3[j]

                registers[rdValue] = registers[rnValue] >> shmtValue

                outFileSim.write('====================\n' + 'cycle:' + str(cycle) + '\t' + str(memoryLocationSim) + '\t')
                outFileSim.write(str(opcodeStr[j]) + str(arg1Str[j]) + str(arg2Str[j]) + str(arg3Str[j]))
                outFileSim.write('\nregisters:')
                outFileSim.write('\nr00:\t')
                for x in range(0, 8):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1
                outFileSim.write('\nr08:\t')
                for x in range(8, 16):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1
                outFileSim.write('\nr16:\t')
                for x in range(16, 24):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1
                outFileSim.write('\nr24:\t')
                for x in range(24, 32):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1

                outFileSim.write('\n\ndata:' + '\n')
                dataForSim()

                memoryLocationSim += 4

            elif opcodeStr[j] == 'STUR':
                outFileSim.write('====================\n' + 'cycle:' + str(cycle) + '\t' + str(memoryLocationSim) + '\t')
                outFileSim.write(str(opcodeStr[j]) + str(arg1Str[j]) + str(arg2Str[j]) + str(arg3Str[j]))
                outFileSim.write('\nregisters:')
                outFileSim.write('\nr00:\t')
                for x in range(0, 8):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1
                outFileSim.write('\nr08:\t')
                for x in range(8, 16):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1
                outFileSim.write('\nr16:\t')
                for x in range(16, 24):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1
                outFileSim.write('\nr24:\t')
                for x in range(24, 32):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1

                outFileSim.write('\n\ndata:' + '\n')

                rnValue = arg1[j]
                addrValue = arg2[j]

                temp = (addrValue * 4) + registers[rnValue]

                if temp < (memoryLocationData + 32):
                    y = temp - memoryLocationData
                    y = y / 4
                else:
                    y = temp - (memoryLocationData + 32)
                    y = y / 4

                for x in range(0, y):
                    dataPrint.append(0)
                    x += 1
                    if x == y:
                        dataPrint.append(registers[rnValue])
                        for i in range(y, 7):
                            dataPrint.append(0)

                dataForSim()
                memoryLocationSim += 4

            elif opcodeStr[j] == 'LDUR':
                rdValue = arg3[j]
                rnValue = arg1[j]

                registers[rdValue] = registers[rnValue]

                outFileSim.write('====================\n' + 'cycle:' + str(cycle) + '\t' + str(memoryLocationSim) + '\t')
                outFileSim.write(str(opcodeStr[j]) + str(arg1Str[j]) + str(arg2Str[j]) + str(arg3Str[j]))
                outFileSim.write('\nregisters:')
                outFileSim.write('\nr00:\t')
                for x in range(0, 8):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1
                outFileSim.write('\nr08:\t')
                for x in range(8, 16):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1
                outFileSim.write('\nr16:\t')
                for x in range(16, 24):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1
                outFileSim.write('\nr24:\t')
                for x in range(24, 32):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1

                outFileSim.write('\n\ndata:' + '\n')
                dataForSim()

                memoryLocationSim += 4

            elif opcodeStr[j] == 'EOR':
                rnValue = arg1[j]
                rmValue = arg2[j]
                rdValue = arg3[j]

                registers[rdValue] = registers[rnValue] ^ registers[rmValue]

                outFileSim.write('====================\n' + 'cycle:' + str(cycle) + '\t' + str(memoryLocationSim) + '\t')
                outFileSim.write(str(opcodeStr[j]) + str(arg1Str[j]) + str(arg2Str[j]) + str(arg3Str[j]))
                outFileSim.write('\nregisters:')
                outFileSim.write('\nr00:\t')
                for x in range(0, 8):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1
                outFileSim.write('\nr08:\t')
                for x in range(8, 16):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1
                outFileSim.write('\nr16:\t')
                for x in range(16, 24):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1
                outFileSim.write('\nr24:\t')
                for x in range(24, 32):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1

                outFileSim.write('\n\ndata:' + '\n')
                dataForSim()

                memoryLocationSim += 4

            elif opcodeStr[j] == 'NOP\n':
                outFileSim.write('====================\n' + 'cycle:' + str(cycle) + '\t' + str(memoryLocationSim) + '\t')
                outFileSim.write(str(opcodeStr[j]))
                outFileSim.write('\nregisters:')
                outFileSim.write('\nr00:\t')
                for x in range(0, 8):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1
                outFileSim.write('\nr08:\t')
                for x in range(8, 16):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1
                outFileSim.write('\nr16:\t')
                for x in range(16, 24):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1
                outFileSim.write('\nr24:\t')
                for x in range(24, 32):
                    outFileSim.write(str(registers[x]) + '\t')
                    x += 1

                outFileSim.write('\n\ndata:' + '\n')
                dataForSim()

                memoryLocationSim += 4

            elif opcodeStr[j] == 'Data\n':
                break

            cycle += 1

def twosComplement(value, bits):
    if (value & (1 << (bits - 1))) != 0:
        value = value - (1 << bits)
    return value

def binaryToDecimal(instructions):
    decimal = int(instructions, 2)
    return decimal

inFileDis = open(inputFileName, 'r')
outFileDis = open(outputFileName + "_dis.txt", 'w')
outFileSim = open(outputFileName + "_sim.txt", 'w')

while True:
    instructions = inFileDis.readline()
    if instructions == '':
        break
    dissme = Disassembler()
    dissme.run()

while 0 in dataPrint:
    dataPrint.remove(0)

simul = Simulator()
simul.run()

inFileDis.close()
outFileDis.close()
outFileSim.close()