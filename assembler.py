#Anish Sinha
#Assembler for EC327
#Built with Python

comParam1s = {'inc':'11000'}
comParam2s = {'add':'0001', 'sub':'0010', 'xor':'0011', 'cmp':'0100',}

comMovs = {'mov1': '0101', 'mov2':'0110', 'mov3':'0111', 'mov4':'1000'}

comJumps = {'jmp':'11001', 'jne':'11010', 'je':'11011'}

#converts from binary to hexadecimal
def hexConvert(binary):   
    #binary parameter should be astring
    result = hex(int(binary, 2))[2:]
    if len(result) < 4:
        diff = 4-len(result)
        result = ('0')*diff + result
    return result

#converts commands/instructions to binary (except mov)
def binCom(com):
    if com in comParam1s:
        return comParam1s[com]
    if com in comParam2s:
        return comParam2s[com]
    if com in comMovs:
        return comMovs[com]
    if com in comJumps:
        return comJumps[com]

def com1or2(com, inputStr, comBin):
    param1 = ''
    param2 = ''
    if com in comParam1s:
        param1 = inputStr[3:]
    elif com in comParam2s:
        param1 = inputStr[3:5]
        param2 = inputStr[5:]

    if ('r' in param1):
        param1bin = bin(int(param1[1:]))[2:]
    else:
        param1bin = bin(int(param1))[2:]

    if param2 != '':
        if ('r' in param2):
            param2bin = bin(int(param2[1:]))[2:]
        else:
            param2bin = bin(int(param2))[2:]
        
        if len(param2bin) < 6:
            diff = 6 - len(param2bin)
            param2bin = diff*('0') + param2bin
        if len(param1bin) < 6:
            diff = 6 - len(param1bin)
            param1bin = diff*('0') + param1bin
        #print(param1bin)
        #print(param2bin)
        return hexConvert(comBin+param1bin+param2bin)
    else:
        if len(param1bin) < 11:
            diff = 11 - len(param1bin)
            param1bin = diff*('0') + param1bin
        return hexConvert(comBin+param1bin)

def whichMov(inputStr):
    param1 = inputStr[3:5]
    if '[' in param1:
        return 'mov3'
    param2 = inputStr[5:]
    if '[' in param2:
        return 'mov4'
    elif 'r' in param2:
        return 'mov2'
    else:
        return 'mov1'

def comInMovs(com, inputStr, comBin):
    inputStr = inputStr.replace('[','').replace(']','')
    param1 = inputStr[3:5]
    param2 = inputStr[5:]
    #print(param1)
    if ('r' in param1):
        param1bin = bin(int(param1[1:]))[2:]
    else:
        param1bin = bin(int(param1))[2:]

    if ('r' in param2):
        param2bin = bin(int(param2[1:]))[2:]
    else:
        param2bin = bin(int(param2))[2:]
    
    if len(param2bin) < 6:
        diff = 6 - len(param2bin)
        param2bin = diff*('0') + param2bin
    if len(param1bin) < 6:
        diff = 6 - len(param1bin)
        param1bin = diff*('0') + param1bin
    #print(param1bin)
    #print(param2bin)
    return hexConvert(comBin+param1bin+param2bin)

def comInJumps(com, inputStr, comBin):
    if com == 'je':
        param1 = inputStr[2:]
    else:
        param1 = inputStr[3:]
    
    firstDigit = '0'

    if int(param1) < 0:
        firstDigit = '1'
        diff = 1024+(int(param1))
        lastDigs = bin(diff)[2:]
        if len(lastDigs) < 10:
            diff1 = 10 - len(lastDigs)
            lastDigs = ('0')*diff1 + lastDigs
    else:
        firstDigit = '0'
        lastDigs = bin(int(param1))[2:]
        if len(lastDigs) < 10:
            diff1 = 10 - len(lastDigs)
            lastDigs = ('0')*diff1 + lastDigs
    
    print(comBin + firstDigit + lastDigs)
    return hexConvert(comBin + firstDigit + lastDigs)


def ask():
    com = ''
    param1 = ''
    param2 = ''

    inputStr = input("Enter Code: ").replace(' ','').replace('(','').replace(')','').replace(',','').lower()

    if(inputStr[:4] == 'halt'):
        com = 'halt'
        return hexConvert('0')
    elif(inputStr[:2] == 'je'):
        com = 'je'
    elif(inputStr[:3] == 'mov'):
        com = whichMov(inputStr)
    else:
        com = inputStr[:3]
    
    comBin = binCom(com)

    if com in comParam1s or com in comParam2s:
        return com1or2(com, inputStr, comBin)
    if com in comMovs:
        return comInMovs(com, inputStr, comBin)
    if com in comJumps:
        return comInJumps(com, inputStr, comBin)
    

#Main
str = ''
x = ask()
print('Hexadecimal: 0x' + x)
print()
str = str + x
while x != '0000':
    x = ask()
    print('Hexadecimal: 0x' + x)
    print()
    str = str + x
    if x == '0000':
        print('DONE')
        print('Final Machine Code: ' + str)