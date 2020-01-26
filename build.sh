#!/bin/bash

project_name=CH559_verify_test
xram_size=0x0800
xram_loc=0x0600
code_size=0xEFFF
dfreq_sys=48000000

sdcc -c -V -mmcs51 --std-sdcc11 --model-large --xram-size $xram_size --xram-loc $xram_loc --code-size $code_size -I/ -DFREQ_SYS=$dfreq_sys  main.c
sdcc main.rel -V -mmcs51 --std-sdcc11 --model-large --xram-size $xram_size --xram-loc $xram_loc --code-size $code_size -I/ -DFREQ_SYS=$dfreq_sys  -o $project_name.ihx
sdobjcopy -I ihex -O binary $project_name.ihx $project_name.bin
python3 scripts/print_bin_size.py -i $project_name.bin

rm $project_name.lk
rm $project_name.map
rm $project_name.mem
rm $project_name.ihx

rm *.asm
rm *.lst
rm *.rel
rm *.rst
rm *.sym


# This tool flashes the bin file directly to the ch559 chip, you need to install the libusb-win32 driver with the zadig( https://zadig.akeo.ie/ ) tool so the tool can access the usb device
# chflasher.exe $project_name.bin
python3 scripts/chflasher.py $project_name.bin
