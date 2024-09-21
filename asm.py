import sys
import subprocess
import os

program = []
eformat = None

label_counter = 0

def translate_to_nasm(line):
    global eformat, label_counter
    if line.startswith('\t') or line.startswith('    '):
        program.append("\t")
    line = line.strip()
    if line.startswith("."):
        program.append("section " + line)
    elif line.startswith("format: "):
        eformat = line[8:].strip()
    elif line.startswith("entry "):
        program.append("global " + line[6:].strip())
    elif line.strip() == "scall":
        program.append("syscall")
    elif line.startswith("cle "):
        v = line[4:].strip()
        program.append("xor " + v + ", " + v)
    elif line.endswith(":"):
        label_counter += 1
        program.append(line)
    else:
        program.append(line)

# Step 1: Read the custom assembly code from a file
with open(sys.argv[1], 'r') as file:
    for line in file:
        translate_to_nasm(line)

# Step 2: Create the output file
output_file = sys.argv[2]
os.close(os.open(output_file, os.O_CREAT | os.O_WRONLY))
if '.' in output_file:
    i = output_file.index('.')
    output_file = output_file[:i]
# Step 3: Write the translated NASM code to the output file
with open(output_file, 'w') as file:
    for line in program:
        if line == "\t":
            file.write('\t')
            continue
        file.write(line + '\n')

subprocess.run(['nasm', '-f', eformat, '-o', output_file + '.o', output_file])
subprocess.run(['ld', '-o', output_file + '.bin', output_file + '.o'])