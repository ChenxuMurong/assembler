# Overview
Assembler that translates English to Assembly code for CS232 Proj 5

# Usage
 `python3 assembler.py`
 
In the standard input, type in english command then hit enter. The program will return the translated 10-bit assembly code, or error message if appropriate.

# Syntax

move [[from] [acc/lr] / [bits]] to [dest]

bin [add/sub/shift/xor/and/rotate] [src] [to/from/left/right/with/to] [dest]

branch [to] xxxx

branch [to] xxxx if src == 0


Input "quit" or "exit" to quit
