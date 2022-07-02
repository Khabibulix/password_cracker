import time
import string
import hashlib
import sys
import argparse
import atexit

def crack_dict(md5, file):
    try:
        found = False
        opened_file = open(file, "r")
        for mot in opened_file.readlines():
            mot = mot.strip("\n").encode("utf8")
            hash = hashlib.md5(mot).hexdigest()
            if hash == md5:
                print("Password found", mot,"--",hash)
                found = True
        if not found:
            print("Not found")
        opened_file.close()

    except FileNotFoundError as fnfe:
        print("File does not exist:", str(fnfe))
        sys.exit(1)


def crack_incr(md5, length, currpass=[]):
    lettres = string.ascii_letters
    pwd = "".join(currpass)

    if length >= 1:
        if len(currpass) == 0:
            currpass = ['a' for _ in range(length)]
            crack_incr(md5, length, currpass)
        else:
            for c in lettres:
                currpass[length - 1] = c
                print("Trying:", pwd)
                if hashlib.md5(pwd.encode("utf8")).hexdigest() == md5:
                    print("Password found", pwd)
                    sys.exit(0)
                else:
                    crack_incr(md5, length - 1, currpass)

def display_time():
    print("Durée :", str(time.time() - debut), "secondes")


parser = argparse.ArgumentParser(description="Password Cracker")
parser.add_argument("-f", "--file", dest="file", help="Path to wordlist file", required=False)
parser.add_argument("-g", "--gen", dest="gen", help="Generate MD5 hash of password",required=False)
parser.add_argument("-md5", dest="md5", help="Hashed Password (MD5)", required=False)
parser.add_argument("-l", dest="plength", help="Password Length", type=int, required=False)

args = parser.parse_args()

debut = time.time()
atexit.register(display_time)

if args.md5:
    print("[CRACKING HASH", args.md5,"]")
    if args.file and not args.plength:
        print("[Using wordlist", args.file,"]")
        crack_dict(args.md5, args.file)
    elif args.plength and not args.file:
        print("[Using incremental mode for", str(args.plength), "letter(s)]")
        crack_incr(args.md5, args.plength)
    else:
        print("Choose either -f or -l argument")
else:
    print("MD5 hash not provided")
    if args.gen:
        print("[MD5 hash of", args.gen, ":", hashlib.md5(args.gen.encode("utf8")).hexdigest())
