#!python3
# coding:utf-8

import time, string, hashlib, sys, argparse, atexit

class Color:
    ROUGE = '\033[91m'
    VERT = '\033[92m'
    FIN = '\033[0m'

class Cracker:
    @staticmethod
    def crack_dict(md5, file):
        """
        Cracking using a wordlist
        :param md5: hash md5 to crack
        :param file: wordlist to use
        :return:
        """
        try:
            found = False
            opened_file = open(file, "r")
            for mot in opened_file.readlines():
                mot = mot.strip("\n").encode("utf8")
                hash = hashlib.md5(mot).hexdigest()
                if hash == md5:
                    print(Color.VERT + "Password found", str(mot).replace("b'", "")[:-1], "--", hash + Color.FIN)
                    found = True
            if not found:
                print(Color.ROUGE + "Not found" + Color.FIN)
            opened_file.close()

        except FileNotFoundError as fnfe:
            print(Color.ROUGE + "File does not exist:", str(fnfe) + Color.FIN)
            sys.exit(1)

    @staticmethod
    def crack_incr(md5, length, _currpass=[]):
        """
        Cracking using bruteforce
        :param md5: hash md5 to crack
        :param length: length of password to crack
        :param _currpass: temporary list modifying via recursion
        :return:
        """

        lettres = string.ascii_letters
        pwd = "".join(_currpass)

        if length >= 1:
            if len(_currpass) == 0:
                _currpass = ['a' for _ in range(length)]
                crack_incr(md5, length, _currpass)
            else:
                for c in lettres:
                    _currpass[length - 1] = c
                    currhash = hashlib.md5(pwd.encode("utf8")).hexdigest()
                    print("Trying:", pwd, "-->", currhash)
                    if currhash == md5:
                        print(Color.VERT + "Password found", pwd + Color.FIN)
                        sys.exit(0)
                    else:
                        crack_incr(md5, length - 1, _currpass)

    @staticmethod
    def crack_smart(md5, pattern, _index=0):
        """
        :param md5:
        :param pattern:
        :param _index:
        :return:
        """
        MAJ = string.ascii_uppercase
        CHIFFRES = string.digits
        MIN = string.ascii_lowercase

        if _index < len(pattern):
            if pattern[_index] in MAJ + CHIFFRES + MIN:
                cracker.crack_smart(md5, pattern, _index+1)
            if "^" == pattern[_index]:
                for c in MAJ:
                    p = pattern.replace("^", c, 1)
                    currhash = hashlib.md5(p.encode("utf8")).hexdigest()
                    if currhash == md5:
                        print(Color.VERT + "Found: " + p + Color.FIN)
                    cracker.crack_smart(md5, p, _index + 1)
            if "*" == pattern[_index]:
                for c in MIN:
                    p = pattern.replace("*", c, 1)
                    currhash = hashlib.md5(p.encode("utf8")).hexdigest()
                    if currhash == md5:
                        print(Color.VERT + "Found: " + p + Color.FIN)
                    cracker.crack_smart(md5, p, _index + 1)
            if "²" == pattern[_index]:
                for c in CHIFFRES:
                    p = pattern.replace("²", c, 1)
                    currhash = hashlib.md5(p.encode("utf8")).hexdigest()
                    if currhash == md5:
                        print(Color.VERT + "Found: " + p + Color.FIN)
                    cracker.crack_smart(md5, p, _index + 1)
        else:
            return

def display_time():
    print("Durée :", str(time.time() - debut), "secondes")

parser = argparse.ArgumentParser(description="Password Cracker")
parser.add_argument("-f", "--file", dest="file", help="Path to wordlist file", required=False)
parser.add_argument("-g", "--gen", dest="gen", help="Generate MD5 hash of password",required=False)
parser.add_argument("-md5", dest="md5", help="Hashed Password (MD5)", required=False)
parser.add_argument("-l", dest="plength", help="Password Length", type=int, required=False)
parser.add_argument("-p", dest="pattern", help="Using pattern of password (^=Maj, *=Min, ²=Chiffre)",required=False)

args = parser.parse_args()

debut = time.time()
atexit.register(display_time)

cracker = Cracker()

if args.md5:
    print("[Cracking hash:", args.md5,"]")
    if args.file and not args.plength:
        print("[Using wordlist", args.file,"]")
        Cracker.crack_dict(args.md5, args.file)
    elif args.plength and not args.file:
        print("[Using incremental mode for", str(args.plength), "letter(s)]")
        Cracker.crack_incr(args.md5, args.plength)
    elif args.pattern:
        print("[Using pattern mode for", str(args.pattern),"]")
        Cracker.crack_smart(args.md5, args.pattern)
    else:
        print(Color.ROUGE + "Choose either -f or -l argument" + Color.FIN)
else:
    print(Color.ROUGE + "MD5 hash not provided" + Color.FIN)
    if args.gen:
        print("[MD5 hash of", args.gen, ":", hashlib.md5(args.gen.encode("utf8")).hexdigest())
