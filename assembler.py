'''
Author Baron Wang
Assembler that translates English to Assembly code for CS232 Proj 5

Usage: 

python3 assembler.py [> ...]

Type in english commands in an input file according to the syntax below.
The program will output the corresponding VHDL statement containing 10-bit codes along with the "when...else..." boilerplate statements, or error message if appropriate. 

The output will be an appropriate VHDL expression designed to be assigned to the data signal in the pldrom.vhd file.

The program prints to stdout by default but you can use the pipe function ">" to make it print to a certain output file.


Syntax:

move [[from] [acc/lr] / [bits]] to [dest]
bin [add/sub/shift/xor/and/rotate] [src] [to/from/left/right/with] [dest]
branch [to] xxxx
branch [to] xxxx if src == 0


Known Issue

The current assembler can only concatenate the "when...else..." boilerplate statement with the 10-bit assembly code. It doesn't know when to stop using the boilerplate and put a semicolon after the assembly code.
Please make sure to cut out the trailing "when ... else" statement and replace it with a semicolon in compliance with VHDL standard.
'''


def raiseError(message):
    print(f"error: {message}")
    exit()


def translate(line):

    words = line.split(' ')

    op = words[0]
    ans = ""
    if op == "move":
        '''syntax: 
        move [[from] [acc/lr] / [bits]] to [dest] '''
        # check how many words are in here
        if len(words) > 5 or len(words) < 4:
            raiseError("wrong number of args. check syntax in move.")
        
        ans += "00"
        vals = "0000"

        if words[-1] == "acc":
            ans += "00"
        elif words[-1] == "lr":
            ans += "01"
        elif words[-1] == "acclo":
            ans += "10"
        elif words[-1] == "acchi":
            ans += "11"
        else: 
            raiseError(f"invalid destination {words[-1]} in move")
        
        src = words[1]
        if words[1] == "from":
            src = words[2]
        
        if src == "acc":
            ans += "00"
        elif src == "lr":
            ans += "01"
        elif src == "all1s":
            ans += "11"
        elif len(src) == 4 and src.isnumeric():
            for dig in src:
                if dig != '0' and dig != '1':
                    raiseError(f"invalid source {src} in move")
            ans += "10"
            vals = src
        else:
            raiseError(f"invalid source {src} in move")

        ans += vals
        return ans        

    elif op == "bin":
        '''bin syntax:
            bin [add/sub/shift/xor/and/rotate] [src] [to/from/left/right/with] [dest]'''
        if len(words) != 5:
            raiseError("wrong number of args. check syntax in bin.")
    
        ans += "01"
        vals = "00"
        operation = words[1]
        src = words[2]
        preposition = words[3]
        dest = words[4]

        if operation == "add":
            ans += "000"
        elif operation == "sub":
            ans += "001"
        elif operation == "shift":
            ans += "01"
            if preposition == "left":
                ans += "0"
            elif preposition == "right":
                ans += "1"
            else:
                raiseError(f"Wrong preposition {preposition} with operation {operation}")
        elif operation == "xor":
            ans += "100"
        elif operation == "and":
            ans += "101"
        elif operation == "rotate":
            ans += "11"
            if preposition == "left":
                ans += "0"
            elif preposition == "right":
                ans += "1"
            else:
                raiseError(f"Wrong preposition {preposition} with operation {operation}")
        else: 
            raiseError(f"invalid operation {words[1]} in bin")
        
        if src == "acc":
            ans += "00"
        elif src == "lr":
            ans += "01"
        elif src == "all1s":
            ans += "11"
        elif len(src) == 2 and src.isnumeric():
            for dig in src:
                if dig != '0' and dig != '1':
                    raiseError(f"invalid source {src} in bin")
            ans += "10"
            vals = src
        else:
            raiseError(f"invalid source {src} in bin")
        
        if dest == "acc":
            ans += "0"
        elif dest == "lr":
            ans += "1"
        else: 
            raiseError(f"invalid destination {dest} in bin")

        ans += vals
        return ans

    elif op == "branch":
        '''branch syntax
        branch [to] xxxx
        branch [to] xxxx if src == 0'''
        # branch or conditional branch
        ans += "1"

        addr = words[1]
        if words[1] == "to":
            addr = words[2]
        
        if len(addr) == 2 and addr.isnumeric():
            for dig in addr:
                if dig != '0' and dig != '1':
                    raiseError(f"invalid source {addr} in branch")

        if "if" in words:
            ans += "1"
            # word after if
            idx = words.index("if")
            src = words[idx + 1]

            if src == "acc":
                ans += "0"
            elif src == "lr":
                ans += "1"
            else:
                raiseError(f"invalid source {src} in conditional branch")

            ans += "000" # padding bits
            ans += addr

        else:
            ans += "00000" # 0 for unconditional branch, the rest for padding
            ans += addr
        return ans

    else:
        raiseError(f"invalid op {op}")


def main():
    with open("assemblyinput.txt") as file:

        line = file.readline().strip()
        code = ""
        lineNum = 0
        while len(line) != 0:
            # addr number padded to 4 digits
            code += "\"" +  translate(line) + "\"" + " when addr = \"{0:0<4b}\" else".format(lineNum)
            # add annotation to code
            code += " -- " + line + "\n"
            line = file.readline().strip()
            lineNum += 1

        print(code)


if __name__ == "__main__":
    main()
