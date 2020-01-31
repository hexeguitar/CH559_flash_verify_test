# Parser for the CH559 usb data sniffed with the Wireshark and exported to JSON
# script will format and comment the transactions
# (c) 2020 by Piotr Zapart www.hexefx.com

import json
import argparse
txt_sep = '--------------------------------------------------------------------------------'

example_text = '''--------------------------------------------------------------------------------
How to generate input data:

 Export USB data from Wireshark using
 File/Export Packet Dissections/As JSON option.
 Use the exported JSON data as the input file:
 python3 usb_parser.py -i USB_data.json -o USB_log.txt
'''


def usage():
    print(txt_sep)
    print(" ")
    print("")
    print("")
    print("usage: usb_parser.py [-h] -i INPUT -o OUTPUT")
    print("Example:")
    print("")


def print_title(title, addr_rng):
    print(txt_sep, file=out_file)
    print(title, file=out_file)
    print("add=" + '|'.join('{:02x}'.format(x) for x in range(addr_rng)), file=out_file)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(prog='usb_parser',
                                     description='Parser for the CH55x USB data packets in json format.',
                                     epilog=example_text,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-i', '--input', type=str, default='', required=True, help="Input JSON file.")
    parser.add_argument('-o', '--output', type=str, default='', required=True, help="Parsed output txt file.")
    args = parser.parse_args()

    input_file = None
    output_file = None

    if args.input:
        input_file = args.input
    if args.output:
        output_file = args.output

    with open(input_file, 'r') as f:
        usb_data = json.load(f)
    
    write_once = False
    verify_once = False

    with open(output_file, 'w') as out_file:
        for key in usb_data:
            if key["_source"]["layers"]["usb"]["usb.src"] == "host":
                oper = "WR: "
            else:
                oper = "RD: "
            data = key["_source"]["layers"]["usb.capdata"]

            if oper == "WR: ":
                if data[0:2] == 'a1':
                    print_title("Detect sequence:", 0x15)
                elif data[0:2] == 'a2':
                    print_title("Reset and run application:", 0x06)
                elif data[0:2] == 'a7':
                    print_title("Read config data:", 0x1E)
                elif data[0:2] == 'a8':
                    print_title("Write config data:", 0x11)
                elif data[0:2] == 'a3':
                    print_title("Send key:", 0x3E)
                elif data[0:2] == 'a4':
                    print_title("Erase chip:", 0x06)
                elif data[0:2] == 'a5' and write_once is False:
                    print_title("Write flash", 0x40)
                    write_once = True
                elif data[0:2] == 'a6' and verify_once is False:
                    print_title("Verify flash", 0x40)
                    verify_once = True
            print(oper, file=out_file, end='')
            print(key["_source"]["layers"]["usb.capdata"], file=out_file)
        print("Log file saved: " + output_file)

