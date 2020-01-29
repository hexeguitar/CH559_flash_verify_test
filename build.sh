#!/bin/bash 

project_name=CH559_verify_test
xram_size=0x0800
xram_loc=0x0600
code_size=0xEFFF
dfreq_sys=48000000

if ! [ -x "$(command -v sdcc)" ]; then
  echo 'Error: sdcc is not installed.' >&2
  exit 1
fi

sdcc -c -V --verbose -mmcs51 --std-sdcc11 --model-large --xram-size $xram_size --xram-loc $xram_loc --code-size $code_size -DFREQ_SYS=$dfreq_sys  main.c
sdcc main.rel -V --verbose -mmcs51 --std-sdcc11 --model-large --xram-size $xram_size --xram-loc $xram_loc --code-size $code_size -DFREQ_SYS=$dfreq_sys -o $project_name.ihx
sdobjcopy -I ihex -O binary $project_name.ihx $project_name.bin
python3 scripts/print_bin_size.py -i $project_name.bin

rm *.lk *.mem *.ihx *.asm *.lst *.rel *.rst *.sym 2>/dev/null
# rm *.map 2>/dev/null

if [ "$1" == "-f" ]; then
    if [ -z "$2" ]; then
        python3 scripts/chflasher.py -w -i $project_name.bin
    else
        python3 scripts/chflasher.py --log="$2" -w -i $project_name.bin
    fi
fi



