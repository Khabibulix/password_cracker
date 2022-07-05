#!python3
# coding:utf-8

import time, string, hashlib, sys, argparse, atexit

class Color:
    ROUGE = '\033[91m'
    VERT = '\033[92m'
    FIN = '\033[0m'

class Cracker:
    @staticmethod
    def crack_dict(hash_provided, file):
        """
        Cracking using a wordlist
        :param hash_provided: hash to crack
        :param file: wordlist to use
        :return:
        """
        try:
            found = False
            opened_file = open(file, "r")
            for mot in opened_file.readlines():
                mot = mot.strip("\n").encode("utf8")
                hash = hashlib.md5(mot).hexdigest()
                if hash == hash_provided:
                    print(Color.VERT + "Password found", str(mot).replace("b'", "")[:-1], "--", hash + Color.FIN)
                    found = True
            if not found:
                print(Color.ROUGE + "Not found" + Color.FIN)
            opened_file.close()

        except FileNotFoundError as fnfe:
            print(Color.ROUGE + "File does not exist:", str(fnfe) + Color.FIN)
            sys.exit(1)

    @staticmethod
    def crack_incr(hash_provided, length, _currpass=[]):
        """
        Cracking using bruteforce, not really effective
        :param hash_provided: hash md5 to crack
        :param length: length of password to crack
        :param _currpass: temporary list modifying via recursion
        :return:
        """

        lettres = string.ascii_letters
        pwd = "".join(_currpass)

        if length >= 1:
            if len(_currpass) == 0:
                _currpass = ['a' for _ in range(length)]
                crack_incr(hash_provided, length, _currpass)
            else:
                for c in lettres:
                    _currpass[length - 1] = c
                    currhash = hashlib.md5(pwd.encode("utf8")).hexdigest()
                    print("Trying:", pwd, "-->", currhash)
                    if currhash == hash_provided:
                        print(Color.VERT + "Password found", pwd + Color.FIN)
                        sys.exit(0)
                    else:
                        crack_incr(hash_provided, length - 1, _currpass)

    @staticmethod
    def crack_smart(hash_provided, pattern, _index=0):
        """
        :param hash_provided: hash to crack
        :param pattern:
        :param _index: private variable
        :return:
        """
        MAJ = string.ascii_uppercase
        CHIFFRES = string.digits
        MIN = string.ascii_lowercase

        if _index < len(pattern):
            if pattern[_index] in MAJ + CHIFFRES + MIN:
                cracker.crack_smart(hash_provided, pattern, _index+1)
            if "^" == pattern[_index]:
                for c in MAJ:
                    p = pattern.replace("^", c, 1)
                    currhash = hashlib.md5(p.encode("utf8")).hexdigest()
                    if currhash == hash_provided:
                        print(Color.VERT + "Found: " + p + Color.FIN)
                    cracker.crack_smart(hash_provided, p, _index + 1)
            if "*" == pattern[_index]:
                for c in MIN:
                    p = pattern.replace("*", c, 1)
                    currhash = hashlib.md5(p.encode("utf8")).hexdigest()
                    if currhash == hash_provided:
                        print(Color.VERT + "Found: " + p + Color.FIN)
                    cracker.crack_smart(hash_provided, p, _index + 1)
            if "²" == pattern[_index]:
                for c in CHIFFRES:
                    p = pattern.replace("²", c, 1)
                    currhash = hashlib.md5(p.encode("utf8")).hexdigest()
                    if currhash == hash_provided:
                        print(Color.VERT + "Found: " + p + Color.FIN)
                    cracker.crack_smart(hash_provided, p, _index + 1)
        else:
            return

    @staticmethod
    def generate_the_hack(arg, pwd_to_encrypt):
        if arg == 1:
            return hashlib.md5(pwd_to_encrypt.encode("utf8")).hexdigest()
        if arg == 2:
            return hashlib.sha256(pwd_to_encrypt.encode("utf8")).hexdigest()
        else:
            return None

def display_time():
    print("Durée :", str(time.time() - debut), "secondes")

parser = argparse.ArgumentParser(description="Password Cracker")
parser.add_argument("-f", "--file", dest="file", help="Path to wordlist file", required=False)
parser.add_argument("-g", "--gen", dest="gen", help="Choose hashing of password (1 for md5, 2 for sha-256",required=False, type=int)
parser.add_argument("-pwd", "--password", dest="pwd", help="Password to encrypt")
parser.add_argument("-hash", dest="hashed", help="Hashed Password", required=False)
parser.add_argument("-l", dest="plength", help="Password Length", type=int, required=False)
parser.add_argument("-p", dest="pattern", help="Using pattern of password (^=Maj, *=Min, ²=Chiffre)",required=False)

args = parser.parse_args()

debut = time.time()
atexit.register(display_time)

cracker = Cracker()

if args.pwd:
    if args.file and not args.plength:
        print("[Cracking using wordlist", args.file,"]")
        Cracker.crack_dict(args.md5, args.file)
    elif args.plength and not args.file:
        print("[Cracking using incremental mode for", str(args.plength), "letter(s)]")
        Cracker.crack_incr(args.md5, args.plength)
    elif args.pattern:
        print("[Cracking using pattern mode for", str(args.pattern),"]")
        Cracker.crack_smart(args.md5, args.pattern)
    elif args.gen: #if no hash, we create one
        pwd = args.pwd
        args = vars(parser.parse_args())
        if args["gen"] == 1:  # md5
            print("[MD5 hash is:", cracker.generate_the_hack(1, pwd), "]")
        if args["gen"] == 2:  # sha-256
            print("[SHA-256 hash is", cracker.generate_the_hack(2, pwd), "]")
        args = parser.parse_args()

    elif not args.gen:
        while True:
            algo = input(Color.ROUGE, "In which algorithm do you want to encrypt the password?", Color.FIN)
            if algo == 1:
                print("[The MD5 hash is:", cracker.generate_the_hack(1, args.pwd))
                break
            if algo == 2:
                print("[SHA-256 hash is", cracker.generate_the_hack(2, args.pwd))
                break
            else:
                print(Color.ROUGE, "Invalid input, please enter 1 for MD5, or 2 for sha-256)", Color.FIN)
                continue

if args.gen and not args.pwd:
    print(Color.ROUGE + "You must provide a password to encrypt, dummy. Use -pwd for that. Example: -pwd 'password' where password will be encrypted", Color.FIN)

if not args.file and not args.plength and not args.gen:
    print(Color.ROUGE + "Enter -h to display help" + Color.FIN)

