#!/usr/bin/python

# this short tool can flash the CH55x series with bootloader version 1.1 and 2.31
# usage:

# to check if the chip is detected and see the bootloader version:
# python3 chflasher.py -d

# to flash an example blink.bin file:
# python3 chflasher.py -w -i blink.bin

# to erase the flash:
# python3 chflasher.py -e

# to verify the flash against the blink.bin file
# python3 chflasher.py -v -i blink.bin

# In addition, a log of usb tx and rx packets can be written for all operations, simply add --log option:
# python3 chflasher.py --log=<logfilename> -w -i blink.bin

# support for: CH551, CH552, CH554, CH558 and CH559

# Copyright by https://ATCnetz.de (Aaron Christophel) you can edit and use this code as you want if you mention me :)

# now works with Python 2.7 or Python 3 thanks to adlerweb
# you need to install pyusb to use this flasher install it via pip install pyusb
# on linux run: sudo apt-get install python-pip and sudo pip install pyusb
# on windows you need the zadig tool https://zadig.akeo.ie/ to install the right driver
# click on Options and List all devices to show the USB Module, then install the libusb-win32 driver

# Rewritten and upgraded by Piotr Zapart / www.hexefx.com on Jan 2020
# things changed / added:
# 1. Moved all funtcions into a class and restructured the code, fixed pycharm warnings
# 2. Added __name__ test condition
# 3. Added help and info options
# 4. Added options to detect the chip, erase or verify the flash only
# 5. Optional usb data logging: use the option --log. It will create a
#    new log file with all the usb operations logged.
#    If the logger is enabled, the ship will not exit the bootloader mode.
#


import usb.core
import usb.util
import sys
import os
import getopt
import traceback
import platform
from time import localtime, strftime


class CHflasher:

    chip_v1 = {
        "detect_seq": (
            0xa2, 0x13, 0x55, 0x53, 0x42, 0x20, 0x44, 0x42, 0x47, 0x20, 0x43, 0x48, 0x35, 0x35, 0x39,
            0x20, 0x26, 0x20, 0x49, 0x53, 0x50, 0x00),
        "exit_bootloader": (0xa5, 0x02, 0x01, 0x00),
        "mode_write": 0xa8,
        "mode_verify": 0xa7
    }
    chip_v2 = {
        "detect_seq": (
            0xa1, 0x12, 0x00, 0x52, 0x11, 0x4d, 0x43, 0x55, 0x20, 0x49, 0x53, 0x50, 0x20, 0x26, 0x20,
            0x57, 0x43, 0x48, 0x2e, 0x43, 0x4e),
        "exit_bootloader": (0xa2, 0x01, 0x00, 0x01),
        "read_config": (0xa7, 0x02, 0x00, 0x1f, 0x00),
        "mode_write": 0xa5,
        "mode_verify": 0xa6
    }
    txt_sep = '-----------------------------------------------------------------------------------------'
    version = '1.01'

    device_erase_size = 8
    device_flash_size = 16
    chipid = 0
    log_file = None
    bootloader_ver = None

    def __init__(self):
        dev = usb.core.find(idVendor=0x4348, idProduct=0x55e0)
        if dev is None:
            print('No CH55x device found, check driver please')
            sys.exit()
        try:
            dev.set_configuration()
        except usb.core.USBError as ex:
            print('Could not access USB Device')

            if str(ex).startswith('[Errno 13]') and platform.system() == 'Linux':
                print('No access to USB Device, configure udev or execute as root (sudo)')
                print('For udev create /etc/udev/rules.d/99-ch55x.rules')
                print('with one line:')
                print('---')
                print('SUBSYSTEM=="usb", ATTR{idVendor}=="4348", ATTR{idProduct}=="55e0", MODE="666"')
                print('---')
                print('Restart udev: sudo service udev restart')
                print('Reconnect device, should work now!')
                print('Alternativey use the included script:')
                print('sudo ./linux_ch55x_install_udev_rules.sh')
                sys.exit(2)

            traceback.print_exc()
            sys.exit(2)
        cfg = dev.get_active_configuration()
        intf = cfg[(0, 0)]
        self.epout = usb.util.find_descriptor(intf, custom_match=lambda e: usb.util.endpoint_direction(
            e.bEndpointAddress) == usb.util.ENDPOINT_OUT)
        self.epin = usb.util.find_descriptor(intf, custom_match=lambda e: usb.util.endpoint_direction(
            e.bEndpointAddress) == usb.util.ENDPOINT_IN)

        assert self.epout is not None
        assert self.epin is not None

    def set_logger(self, setting, logfile):
        if setting:
            print("Transaction logger ON: " + logfile)
            self.log_file = open(logfile, "w")        # open log file for writing
            print(self.txt_sep, file=self.log_file)
            time = strftime("%a, %d %b %Y %X +0000", localtime())
            print(time, file=self.log_file)
            print(self.txt_sep, file=self.log_file, end="\r\n")

    def close_logger(self):
        if self.log_file is not None:
            self.log_file.close();

    @staticmethod
    def usage():
        print("Usage:")
        print("python3 chflasher.py [options] -i <inputfile.bin>")
        print("Options:")
        print("\t-h\t\tshow help")
        print("\t--version\tshow version")
        print("\t-d\t\tidentify chip")
        print("\t-e\t\terase flash")
        print("\t-i <input file>\tinput bin file")
        print("\t-w\t\twrite bin file to flash")
        print("\t-v\t\tverify the flash against the bin file")
        print("\t--log\t\twrite diagnostic log file")
        print("Example:")
        print("python3 chflasher.py --log -w -i blink.bin")
        print("will write the blink.bin file, verify it and log the usb operations")
        print("in usb_trx.log file")

    @classmethod
    def show_info(cls):
        print(cls.txt_sep)
        print("CH55x USB bootloader flash tool, version " + cls.version)
        print("Copyright 2020 by https://ATCnetz.de (Aaron Christophel)")
        print("Rewitten and upgraded by Piotr Zapart www.hexefx.com")
        print("Supported chips: CH551, CH552, CH554, CH558 and CH559")
        print(cls.txt_sep)

    def show_version(self):
        print("version " + self.version)

    def __print_buffers(self, tx, rx):
        txl = len(tx)
        rxl = len(rx)
        length = max(len(tx), len(rx))
        print("add= " + '|'.join('{:02x}'.format(x) for x in range(max(txl, rxl))),
              file=self.log_file)
        if txl:
            print("tx = " + ':'.join('{:02x}'.format(x) for x in tx), file=self.log_file)
        if rxl:
            print("rx = " + ':'.join('{:02x}'.format(x) for x in rx), file=self.log_file)

    # better formatting for visual inspection
    def __print_buffer_errors(self, tx, rx, address):
        if rx[4] != 0x00:
            msg = "ERR"
        else:
            msg = "OK "
        print('0x{:>04x}'.format(address) + ":" + msg + ":", file=self.log_file, end='')
        if len(rx):
            print(':'.join('{:02x}'.format(x) for x in tx), file=self.log_file)

    def __errorexit(self, errormsg):
        print(self.txt_sep)
        print('Error: ' + errormsg)
        print(self.txt_sep)
        if self.log_file is not None:
            print(self.txt_sep, file=self.log_file)
            print(errormsg, file=self.log_file)
            self.log_file.close()
        sys.exit()

    def __sendcmd(self, cmd):
        self.epout.write(cmd)
        b = self.epin.read(64)
        return b

    def __detect_bootloader_ver(self):
        ver = None
        reply = self.__sendcmd(self.chip_v2["detect_seq"])
        if self.log_file is not None:
            print("Detecting bootloader version:", file=self.log_file)
            self.__print_buffers(self.chip_v2["detect_seq"], reply)
        if len(reply) == 0:
            self.__errorexit('Bootloader detect: USB Error')
        if len(reply) == 2:
            ver = '1.1'
        else:
            ver = '2.3'
        return ver

    def __erasechipv1(self):
        self.__sendcmd((0xa6, 0x04, 0x00, 0x00, 0x00, 0x00))
        for x in range(self.device_flash_size):
            buffer = self.__sendcmd((0xa9, 0x02, 0x00, x*4))
            if buffer[0] != 0x00:
                self.__errorexit('Erase Failed')
        print('Flash Erased')

    def __erasechipv2(self):
        tx = (0xa4, 0x01, 0x00, self.device_erase_size)
        reply = self.__sendcmd(tx)
        if self.log_file is not None:
            print(self.txt_sep, file=self.log_file)
            print("Erasing flash:", file=self.log_file)
            self.__print_buffers(tx, reply)
        if reply[4] != 0x00:
            self.__errorexit('Erase Failed')
        print('Flash Erased')

    def __exitbootloaderv1(self):
        self.epout.write(self.chip_v1["exit_bootloader"])
        if self.log_file is not None:
            print(self.txt_sep, file=self.log_file)
            print("Starting application:", file=self.log_file)
            self.__print_buffers(self.chip_v1["exit_bootloader"], "")

    def exitbootloaderv2(self):
        self.epout.write(self.chip_v1["exit_bootloader"])
        if self.log_file is not None:
            print(self.txt_sep, file=self.log_file)
            print("Starting application:", file=self.log_file)
            self.__print_buffers(self.chip_v2["exit_bootloader"], "")

    def __identchipv1(self):
        reply = self.__sendcmd(self.chip_v1["detect_seq"])
        if len(reply) == 2:
            self.chipid = reply[0]
            print('Found CH5'+str(self.chipid-30))
            if self.chipid == 0x58:
                self.device_flash_size = 64
                self.device_erase_size = 11
            elif self.chipid == 0x59:
                self.device_flash_size = 64
                self.device_erase_size = 11
        else:
            self.__errorexit('Unknown chip')
        cfganswer = self.__sendcmd((0xbb, 0x00))
        if len(cfganswer) == 2:
            print('Bootloader version: ' + str((cfganswer[0] >> 4)) + '.' + str((cfganswer[0] & 0xf)))
        else:
            self.__errorexit('Unknown bootloader')

    def __identchipv2(self):
        reply = self.__sendcmd(self.chip_v2["detect_seq"])
        if self.log_file is not None:
            print(self.txt_sep, file=self.log_file)
            print("Chip identification:", file=self.log_file)
            self.__print_buffers(self.chip_v1["detect_seq"], reply)
        if len(reply) == 6:
            self.chipid = reply[4]

            print('Found CH5'+str(self.chipid-30))
            if self.chipid == 0x58:
                self.device_flash_size = 64
                self.device_erase_size = 11
            elif self.chipid == 0x59:
                self.device_flash_size = 64
                self.device_erase_size = 11
        else:
            self.__errorexit('Unknown chip')
        read_cfg_reply = self.__sendcmd(self.chip_v2["read_config"])
        if self.log_file is not None:
            print(self.txt_sep, file=self.log_file)
            print("Config read:", file=self.log_file)
            self.__print_buffers(self.chip_v2["read_config"], read_cfg_reply)
        if len(read_cfg_reply) == 30:
            print('Bootloader version: ' + str(read_cfg_reply[19]) + '.' + str(read_cfg_reply[20]) +
                  str(read_cfg_reply[21]))
            self.__keyinputv2(read_cfg_reply)
        else:
            self.__errorexit('Unknown bootloader')

    def __keyinputv2(self, cfganswer):
        outbuffer = bytearray(64)
        outbuffer[0] = 0xa3
        outbuffer[1] = 0x30
        outbuffer[2] = 0x00
        checksum = cfganswer[22]
        checksum += cfganswer[23]
        checksum += cfganswer[24]
        checksum += cfganswer[25]
        for x in range(0x30):
            outbuffer[x+3] = checksum & 0xff
        self.__sendcmd(outbuffer)
        if self.log_file is not None:
            print(self.txt_sep, file=self.log_file)
            print("Key input:", file=self.log_file)
            self.__print_buffers(outbuffer, '')

    def __writefilev1(self, file_name, mode):
        with open(file_name, 'rb') as input_file:
            bytes_to_send = os.path.getsize(bytes(input_file))
            if mode == self.chip_v1["mode_write"]:
                print('Filesize: '+str(bytes_to_send)+' bytes')
            curr_addr = 0
            pkt_length = 0
            while curr_addr < bytes_to_send:
                outbuffer = bytearray(64)
                if bytes_to_send >= 0x3c:
                    pkt_length = 0x3c
                else:
                    pkt_length = bytes_to_send
                outbuffer[0] = mode
                outbuffer[1] = pkt_length
                outbuffer[2] = (curr_addr & 0xff)
                outbuffer[3] = ((curr_addr >> 8) & 0xff)
                for x in range(pkt_length):
                    outbuffer[x+4] = input_file.seek(curr_addr+x)
                buffer = self.__sendcmd(outbuffer)
                curr_addr += pkt_length
                bytes_to_send -= pkt_length
                if buffer is not None:
                    if buffer[0] != 0x00:
                        if mode == self.chip_v1["mode_write"]:
                            self.__errorexit('Write Failed!!!')
                        elif mode == self.chip_v1["mode_verify"]:
                            self.__errorexit('Verify Failed!!!')
            if mode == self.chip_v1["mode_write"]:
                print('Writing success')
            elif mode == self.chip_v1["mode_verify"]:
                print('Verify success')

    def __writefilev2(self, file_name, mode):
        input_file = list(open(file_name, 'rb').read())
        bytes_to_send = len(input_file)
        if mode == self.chip_v2["mode_write"]:
            print('Filesize: ' + str(bytes_to_send) + ' bytes')
            if self.log_file is not None:
                print(self.txt_sep, file=self.log_file)
                print("Writing " + str(bytes_to_send) + " bytes to Flash.", file=self.log_file)
                print("add=       " + '|'.join('{:02x}'.format(x) for x in range(64)),
                      file=self.log_file)
        if mode == self.chip_v2["mode_verify"]:
            if self.log_file is not None:
                print(self.txt_sep, file=self.log_file)
                print("Veryfing " + str(bytes_to_send) + " bytes of Flash.", file=self.log_file)
                print("add=       " + '|'.join('{:02x}'.format(x) for x in range(64)),
                      file=self.log_file)
        if bytes_to_send < 256:
            self.__errorexit('Firmware bin file possibly corrupt.')
        curr_addr = 0
        pkt_length = 0
        while curr_addr < bytes_to_send:
            outbuffer = bytearray(64)
            if bytes_to_send >= 0x38:
                pkt_length = 0x38
            else:
                pkt_length = bytes_to_send
            outbuffer[0] = mode
            outbuffer[1] = (pkt_length+5)
            outbuffer[2] = 0x00
            outbuffer[3] = (curr_addr & 0xff)
            outbuffer[4] = ((curr_addr >> 8) & 0xff)
            outbuffer[5] = 0x00
            outbuffer[6] = 0x00
            outbuffer[7] = bytes_to_send & 0xff
            for x in range(pkt_length):
                outbuffer[x+8] = input_file[curr_addr + x]
            for x in range(pkt_length+8):
                if x % 8 == 7:
                    outbuffer[x] ^= self.chipid
            buffer = self.__sendcmd(outbuffer)
            # --- logger ---
            if self.log_file is not None:
                self.__print_buffer_errors(outbuffer, buffer, curr_addr)
            curr_addr += pkt_length
            bytes_to_send -= pkt_length
            if buffer is not None:
                if buffer[4] != 0x00 and buffer[4] != 0xfe:
                    if mode == self.chip_v2["mode_write"]:
                        self.__errorexit('Write Failed at address ' + str(curr_addr))
                    elif mode == self.chip_v2["mode_verify"]:
                        # if the logger is ON, do not exit on verify fail, check all the adresses
                        if self.log_file is not None:
                            print("Verify failed at " + '0x{:>04x}'.format(curr_addr))
                        else:
                            self.__errorexit('Verify Faile at address ' + str(curr_addr))
        if mode == self.chip_v2["mode_write"]:
            print('Writing success')
        elif mode == self.chip_v2["mode_verify"]:
            print('Verify success')

    def write(self, firmware_bin):
        bt_version = self.__detect_bootloader_ver()
        if bt_version == '1.1':
            self.__identchipv1()
            self.__erasechipv1()
            self.__writefilev1(firmware_bin, self.chip_v1["mode_write"])
            self.__writefilev1(firmware_bin, self.chip_v1["mode_verify"])
            if self.log_file is None:
                self.__exitbootloaderv1()
        if bt_version == '2.3':
            self.__identchipv2()
            self.__erasechipv2()
            self.__writefilev2(firmware_bin, self.chip_v2["mode_write"])
            self.__writefilev2(firmware_bin, self.chip_v2["mode_verify"])
            if self.log_file is None:
                self.exitbootloaderv2()

    def verify(self, firmware_bin):
        bt_version = self.__detect_bootloader_ver()
        if bt_version == '1.1':
            self.__identchipv1()
            self.__writefilev1(firmware_bin, self.chip_v1["mode_verify"])
            if self.log_file is None:
                self.__exitbootloaderv1()
        if bt_version == '2.3':
            self.__identchipv2()
            self.__writefilev2(firmware_bin, self.chip_v2["mode_verify"])
            if self.log_file is None:
                self.exitbootloaderv2()

    # erase: stay in bootloader mode?
    def erase(self):
        bt_version = self.__detect_bootloader_ver()
        if bt_version == '1.1':
            self.__identchipv1()
            self.__erasechipv1()
        if bt_version == '2.3':
            self.__identchipv2()
            self.__erasechipv2()

    def detect(self):
        bt_version = self.__detect_bootloader_ver()
        if bt_version == '1.1':
            self.__identchipv1()
        if bt_version == '2.3':
            self.__identchipv2()


def main(argv, flash):
    try:
        opts, args = getopt.getopt(argv, "hwvdei:", ["version", "log="])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)
    firmware_bin = None

    operation = 'none'
    for opt, arg in opts:
        if opt == '-h':
            flash.show_info()
            flash.usage()
            sys.exit()
        elif opt in '--version':
            flash.show_version()
            sys.exit()
        elif opt in '--log':
            logfile = str(arg)
            flash.set_logger(True, logfile)
        elif opt in '-i':
            firmware_bin = arg
        elif opt in '-w':
            operation = 'write'
        elif opt in '-v':
            operation = 'verify'
        elif opt in '-r':
            operation = 'read'
        elif opt in '-d':
            operation = 'detect'
        elif opt in "-e":
            operation = 'erase'
        else:
            assert False, "unhandled option"

    if operation == 'write':
        flash.write(firmware_bin)
    elif operation == 'verify':
        flash.verify(firmware_bin)
    elif operation == 'detect':
        flash.detect()
    elif operation == 'erase':
        flash.erase()

    # close log file if used
    flash.close_logger()


if __name__ == "__main__":

    flasher = CHflasher()

    if len(sys.argv) < 2:
        print('Error: too few arguments!')
        flasher.show_info()
        flasher.show_version()
        flasher.usage()
        sys.exit(2)
    else:
        main(sys.argv[1:], flasher)
