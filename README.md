# Overview
Assembler that translates English to Assembly code for CS232 Proj 5

# Usage
 `python3 assembler.py [> ...]`

Type in english commands in an input file according to the syntax below.
The program will output the corresponding VHDL statement containing 10-bit codes along with the "when...else..." boilerplate statements, or error message if appropriate. 

The output will be an appropriate VHDL expression designed to be assigned to the `data` signal in the pldrom.vhd file.

The program prints to stdout by default but you can use the pipe function ">" to make it print to a certain output file.

# Syntax

move [[from] [acc/lr] / [bits]] to [dest]

bin [add/sub/shift/xor/and/rotate] [src] [to/from/left/right/with/to] [dest]

branch [to] xxxx

branch [to] xxxx if src == 0
