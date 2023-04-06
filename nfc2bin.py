#!/usr/bin/env python3
import argparse
import os

def write_output(name: str, data: bytes, output_dir: str):
    with open(os.path.join(output_dir, f"{name}.bin"), "wb") as f:
        f.write(data)

def convert_data(input_file: str, output_path: str):
    input_extension = os.path.splitext(input_file)[1]
    if input_extension == ".nfc":
        with open(input_file, "rt") as file:
            contents = file.read()
            name = os.path.basename(input_file)
            data_init = contents[contents.find("Block 0"):].split(sep="\n")
            buff = bytes.fromhex(''.join([line[line.find(":")+2:].replace(" ", "") for line in data_init]))
            write_output(os.path.splitext(name)[0], buff, output_path)

def process(path: str, output_path: str):
    if os.path.isfile(path):
        convert_data(path, output_path)
    else:
        for filename in os.listdir(path):
            new_path = os.path.join(path, filename)
            if os.path.isfile(new_path):
                convert_data(new_path, output_path)
            else:
                process(new_path, output_path)

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input-file",
        required=True,
        help="File to convert",
    )
    parser.add_argument(
        "-o",
        "--output-path",
        required=False,
        help="Output path, if not specified, the output .bin file will be created in the same directory as the input file.",
    )
    parser.add_argument(
        "-n",
        "--no-ascii",
        required=False,
        action="store_true",
        help="Do not print ascii art.",
    )
    
    args = parser.parse_args()
    return args

def main():
    args = get_args()
    
    if args.no_ascii:
      pass
    else:        
        print("""
        ****++*******++++*+=++**+*****
        *+*****++++++*****+----+*+****
        **++====++**+==+=++----:=*++**
        +=+*##%%%%***##*++=-==-=:++***
        =#@@@@@@@*-*%%%%%%#-=+=***+++*
        @@@%**+**=+@##@####**%@%*=::+*
        @@#+*--.:#**@%####%@@#-   -+**
        @@+*+ .  :*=##%%@@@#:  .=****+
        *+=+*-+#%%%@@@@@@#:   -+*++=+*
        +====@@@@@@@@%#+:-*##*++*#**=+
        @@@@@@@@@@%%%#*+*%@@@@@%%%#++*
        @@@@@@@@@@@@@@@@@@@##**+++++**
        @@@@@@@@@@@@@@@@*:   =++****+*
        @@@@@@@@@@@@@@@@@%#*-****+****
        @@@@@@@@@@@@@@@@@@@%=*+*******
                ____      ___    __     _      
        ____   / __/_____|__ \  / /_   (_)____ 
       / __ \ / /_ / ___/__/ / / __ \ / // __ \\
      / / / // __// /__ / __/ / /_/ // // / / /
     /_/ /_//_/   \___//____//_.___//_//_/ /_/                                                             
    _____________________________________________
        """)

    if os.path.isfile(args.input_file):
        if not args.output_path:
            args.output_path = os.path.dirname(args.input_file)

    process(args.input_file, args.output_path)
    print("\n[-] Converting from .nfc to .bin format")
    
if __name__ == "__main__":
    main()
    print("[+] Conversion Completed!")
