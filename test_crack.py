from crack import *
import pytest


def test_crack_dict_with_md5():
    assert cracker.crack_dict("95fa9d10dd5aed2c42004a915de00c8d", "wordlist.txt") == True


def test_crack_dict_with_sha_256():
    assert cracker.crack_dict("c6841067cb3a30ee869659fe47e50f9a59cd68ada7d3cac07ae985dee34871dc", "wordlist.txt") == True


def test_crack_smart_with_md5_with_lower_case():
    assert cracker.crack_smart("d9d7dbddc29177b121a6aa1bb09d15fd", "*a*") == True


def test_generate_the_hack_for_md5():
    assert cracker.generate_the_hack(1, "abruti") == "95fa9d10dd5aed2c42004a915de00c8d"


def test_generate_the_hack_for_sha_256():
    assert cracker.generate_the_hack(2, "abruti") == "c6841067cb3a30ee869659fe47e50f9a59cd68ada7d3cac07ae985dee34871dc"


def test_md5_length():
    x = cracker.generate_the_hack(1, "testingthatshit")
    y = cracker.generate_the_hack(1, "testingthatothershit")
    assert (len(x) + len(y)) / 2 == 32
    #should be 32

def test_sha_256_length():
    x = cracker.generate_the_hack(2, "testingthatshit")
    y = cracker.generate_the_hack(2, "testingthatothershit")
    assert (len(x) + len(y)) / 2 == 64
    #should be 64


