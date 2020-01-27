# CH559_flash_verify_test
Quick project to test the verify function of the wchflasher python script.

A python script generates variable length uint8_t arrays with random numbers to test different sizes of the output bin file.
Another python script prints out the size of the file after the compilaion is done.

### Assuming that sdcc is installed and in PATH.

## Test procedure (linux):

1. Generate the random byte array by using the following command:  
`pytnon3 scripts/gen_data.py -l <array length> -o rndata.h`  
Example:  
`pytnon3 scripts/gen_data.py -l 12000 -o rndata.h`  
generates an array of size 12000 populated with random 8bit values.  
2. Run build script:  
`./build.sh`  
3. Script will compile the test main.c and will try to upload it to the chip using the modded chflasher.py script.
4. Script will also write a log file showing all the addresses where the verify failed, including the chip reply and the sent data packet.  

The errors (are they errors or maybe just another status reply?) appear to be 56bytes spaced. Exactly the flash data packe size.  

## Observations:
1. To make the testing easier i created two additional test scripts: test_pass.sh and test_fail.sh.  
2. test_pass.sh will generate a firmware bin file that verifies ok.  
`./test_pass.sh`  
3. test_fail.sh will generate a bin file that generates 0xf5 reply from the bootloader.  
`./test_fail.sh` 
4. fail/pass results impact the working of the stdio library and the printf function.     

![write.log][pic1]  


[pic1]: ch55x_flash3.png



