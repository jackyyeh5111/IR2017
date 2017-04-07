#!/bin/bash
# Put your command below to execute your program.
# Replace "./my-program" with the command that can execute your program.
# Remember to preserve " $@" at the end, which will be the program options we give you.
source env/bin/activate

python create_file-list_tb.py $@
python create_inverted-file_tb.py $@
python create_vocab_tb.py $@

python main.py $@
