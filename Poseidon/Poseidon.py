import gmpy2
import base64
import struct
import hashlib
import requests
import binascii
from PIL import Image
from pwn import *
from pwnlib.util.iters import mbruteforce
from Crypto.Cipher import ARC4
from Crypto.Cipher import AES as aes
from Crypto.Util.number import long_to_bytes, bytes_to_long


def Binary_String(Binary):
    assert(len(Binary) % 8 == 0)
    String = "".join([chr(int(Binary[i:i + 8], 2)) for i in range(0, len(Binary), 8)])
    return String


def Binary_Dec(Binary):
    Dec = str(int(Binary, 2))
    return Dec


def Binary_Hex(Binary):
    Hex = hex(int(Binary, 2))
    return Hex


def Dec_String(Dec):
    String = long_to_bytes(Dec).decode()
    return String


def Dec_Binary(Dec):
    Binary = bin(int(Dec))
    return Binary


def Dec_Hex(Dec):
    Hex = hex(int(Dec))
    return Hex


def Hex_String(Hex):
    assert(len(Hex) % 2 == 0)
    String = "".join([chr(int(Hex[i:i + 2], 16)) for i in range(0, len(Hex), 2)])
    return String


def Hex_Binary(Hex):
    Binary = bin(int(Hex, 16))
    return Binary


def Hex_Dec(Hex):
    Dec = str(int(Hex, 16))
    return Dec


def File_Bytes(Course):
    with open(Course, "rb") as f:
        return f.read()


def Zodiac(Text, Foot=17):
    assert(len(Text) % Foot == 0)
    templist1 = Text[::Foot]
    templist2 = []
    for index in range(Foot):
        temp = ""
        for i in range(0, len(templist1)):
            temp += templist1[i][index]
            index = (index + 2) % Foot
        templist2.append(temp)
    DecryptedText = "".join(templist2)
    return DecryptedText


def Yunying(Text):
    List = Text.split("0")
    DecryptedText = ""
    for i in List:
        Sum = 64
        for j in i:
            Sum += int(j)
        DecryptedText += chr(Sum)
    return DecryptedText


def Morse_Encrypt(Morse):
    MorseCode = {
        "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".", "F": "..-.", "G": "--.",
        "H": "....", "I": "..", "J": ".---", "K": "-.-", "L": ".-..", "M": "--",
        "N": "-.", "O": "---", "P": ".--.", "Q": "--.-", "R": ".-.", "S": "...",
        "T": "-", "U": "..-", "V": "...-", "W": ".--", "X": "-..-", "Y": "-.--",
        "Z": "--..", "a": ".-", "b": "-...", "c": "-.-.", "d": "-..", "e": ".",
        "f": "..-.", "g": "--.", "h": "....", "i": "..", "j": ".---", "k": "-.-",
        "l": ".-..", "m": "--", "n": "-.", "o": "---", "p": ".--.", "q": "--.-",
        "r": ".-.", "s": "...", "t": "-", "u": "..-", "v": "...-", "w": ".--",
        "x": "-..-", "y": "-.--", "z": "--..", "0": "-----", "1": ".----", "2": "..---",
        "3": "...--", "4": "....-", "5": ".....", "6": "-....", "7": "--...", "8": "---..",
        "9": "----.", ".": ".-.-.-", ":": "---...", ",": "--..--", ";": "-.-.-.", "?": "..--..",
        "=": "-...-", "'": ".----.", "/": "-..-.", "!": "-.-.--", "-": "-....-", "_": "..--.-",
        '"': ".-..-.", "(": "-.--.", ")": "-.--.-", "$": "...-..-", "&": ".-...", "@": ".--.-.", "+": ".-.-."
    }
    EncryptedText = "/".join([MorseCode.get(i, "[" + i + "]") for i in Morse])
    return EncryptedText


def Morse_Decrypt(Morse):
    MorseCode = {
        ".-": "a", "-...": "b", "-.-.": "c", "-..": "d", ".": "e", "..-.": "f",
        "--.": "g", "....": "h", "..": "i", ".---": "j", "-.-": "k", ".-..": "l",
        "--": "m", "-.": "n", "---": "o", ".--.": "p", "--.-": "q", ".-.": "r",
        "...": "s", "-": "t", "..-": "u", "...-": "v", ".--": "w", "-..-": "x",
        "-.--": "y", "--..": "z", "-----": "0", ".----": "1", "..---": "2", "...--": "3",
        "....-": "4", ".....": "5", "-....": "6", "--...": "7", "---..": "8", "----.": "9",
        ".-.-.-": ".", "---...": ":", "--..--": ",", "-.-.-.": ";", "..--..": "?", "-...-": "=",
        ".----.": "'", "-..-.": "/", "-.-.--": "!", "-....-": "-", "..--.-": "_", ".-..-.": '"',
        "-.--.": "(", "-.--.-": ")", "...-..-": "$", ".-...": "&", ".--.-.": "@", ".-.-.": "+"
    }
    DecryptedText = "".join([MorseCode.get(i, "[" + i + "]") for i in Morse.split("/")])
    return DecryptedText


def Caesar_Encrypt(Text, Move=3):
    EncryptedText = ""
    for i in Text:
        if i.isupper():
            EncryptedText += chr((ord(i) - ord('A') + int(Move)) % 26 + ord('A'))
        elif i.islower():
            EncryptedText += chr((ord(i) - ord('a') + int(Move)) % 26 + ord('a'))
        else:
            EncryptedText += i
    return EncryptedText


def Caesar_Decrypt(Text, Move=3):
    DecryptedText = ""
    for i in Text:
        if i.isupper():
            DecryptedText += chr((ord(i) - ord('A') - int(Move)) % 26 + ord('A'))
        elif i.islower():
            DecryptedText += chr((ord(i) - ord('a') - int(Move)) % 26 + ord('a'))
        else:
            DecryptedText += i
    return DecryptedText


def Caesar_Attack(Text):
    Result = [Caesar_Decrypt(Text, i) for i in range(0, 26)]
    return Result


def Bacon_Encrypt(Bacon):
    BaconCode = {
        "a": "aaaaa", "b": "aaaab", "c": "aaaba", "d": "aaabb", "e": "aabaa", "f": "aabab", "g": "aabba",
        "h": "aabbb", "i": "abaaa", "j": "abaab", "k": "ababa", "l": "ababb", "m": "abbaa", "n": "abbab",
        "o": "abbba", "p": "abbbb", "q": "baaaa", "r": "baaab", "s": "baaba", "t": "baabb",
        "u": "babaa", "v": "babab", "w": "babba", "x": "babbb", "y": "bbaaa", "z": "bbaab",
    }
    EncryptedText = "".join([BaconCode.get(i, "[" + i + "]") for i in Bacon.lower()]).upper()
    return EncryptedText


def Bacon_Decrypt(Bacon):
    BaconCode = {
        "aaaaa": "a", "aaaab": "b", "aaaba": "c", "aaabb": "d", "aabaa": "e", "aabab": "f", "aabba": "g",
        "aabbb": "h", "abaaa": "i", "abaab": "j", "ababa": "k", "ababb": "l", "abbaa": "m", "abbab": "n",
        "abbba": "o", "abbbb": "p", "baaaa": "q", "baaab": "r", "baaba": "s", "baabb": "t",
        "babaa": "u", "babab": "v", "babba": "w", "babbb": "x", "bbaaa": "y", "bbaab": "z",
    }
    assert(len(Bacon) % 5 == 0)
    DecryptText = "".join([BaconCode.get(i, "[" + i + "]") for i in Bacon.lower()[:: 5]]).upper()
    return DecryptText


def Affine_Encrypt(Text, a, b):
    A = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]
    assert(a in A)
    List = []
    for i in Text:
        if i.isupper():
            List.append(chr((a * (ord(i) - ord('A')) + b) % 26 + ord('A')))
        elif i.islower():
            List.append(chr((a * (ord(i) - ord('a')) + b) % 26 + ord('a')))
        else:
            List.append(i)
    EncryptedText = "".join(List)
    return EncryptedText


def Affine_Decrypt(Text, a, b):
    A = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]
    assert(a in A)
    List = []
    n = 1
    while (n * a) % 26 != 1:
        n = n + 1
    for i in Text:
        if i.isupper():
            List.append(chr(n * (ord(i) - ord('A') - b) % 26 + ord('A')))
        elif i.islower():
            List.append(chr(n * (ord(i) - ord('a') - b) % 26 + ord('a')))
        else:
            List.append(i)
    DecryptedText = "".join(List)
    return DecryptedText


def Affine_Attack(Text):
    A = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]
    Result = []
    for a in A:
        for b in range(26):
            Result.append((a, b, Affine_Decrypt(Text, a, b)))
    return Result


def Vigenere_Encrypt(Text, Key):
    Key = Key[:len(Text)]
    Temp = Key
    index = 0
    while(len(Key) < len(Text)):
        if(index != len(Temp)):
            Key += Temp[index]
            index += 1
        else:
            index = 0
            Key += Temp[index]
            index += 1
    EncryptedText = ""
    for i in range(len(Text)):
        if i.isupper():
            EncryptedText += chr((ord(Text[i]) + ord(Key[i].upper()) - 2 * ord('A')) % 26 + ord('A'))
        elif i.islower():
            EncryptedText += chr((ord(Text[i]) + ord(Key[i].lower()) - 2 * ord('a')) % 26 + ord('a'))
        else:
            EncryptedText += Text[i]
    return EncryptedText


def Vigenere_Decrypt(Text, Key):
    Key = Key[:len(Text)]
    Temp = Key
    index = 0
    while(len(Key) < len(Text)):
        if(index != len(Temp)):
            Key = Key + Temp[index]
            index = index + 1
        else:
            index = 0
            Key = Key + Temp[index]
            index = index + 1
    DecryptedText = ""
    for i in range(len(Text)):
        if i.isupper():
            DecryptedText += chr((ord(Text[i]) - ord(Key[i].upper())) % 26 + ord('A'))
        elif i.islower():
            DecryptedText += chr((ord(Text[i]) - ord(Key[i].lower())) % 26 + ord('a'))
        else:
            DecryptedText += Text[i]
    return DecryptedText


def Fence_Encrypt(Text, Fence):
    assert(len(Text) % Fence == 0)
    templist = []
    for i in range(Fence):
        temp = ""
        for j in Text[::Fence]:
            temp += j[i]
        templist.append(temp)
    EncryptedText = "".join(templist)
    return EncryptedText


def Fence_Decrypt(Text, Fence):
    assert(len(Text) % Fence == 0)
    templist = ["" for _ in range(Fence)]
    for i in Text[::Fence]:
        for j in range(Fence):
            templist[j] = templist[j] + i[j]
    DecryptedText = "".join(templist)
    return DecryptedText


def Fence_Attack(Text):
    Factors = [factor for factor in range(2, len(Text)) if len(Text) % factor == 0]
    Result = [(i, Fence_Decrypt(Text, i)) for i in Factors]
    return Result


def WFence_Generate(Text, Fence):
    Matrix = [['.'] * len(Text) for _ in range(Fence)]
    Row = 0
    Up = False
    for Column in range(len(Text)):
        Matrix[Row][Column] = Text[Column]
        if Row == Fence - 1:
            Up = True
        if Row == 0:
            Up = False
        if Up:
            Row -= 1
        else:
            Row += 1
    return Matrix


def WFence_Encrypt(Text, Fence):
    Matrix = WFence_Generate(Text, Fence)
    EncryptedText = ""
    for Row in range(Fence):
        for Column in range(len(Text)):
            if Matrix[Row][Column] != '.':
                EncryptedText += Matrix[Row][Column]
    return EncryptedText


def WFence_Decrypt(Text, Fence):
    Matrix = WFence_Generate(Text, Fence)
    index = 0
    for Row in range(Fence):
        for Column in range(len(Text)):
            if Matrix[Row][Column] != '.':
                Matrix[Row][Column] = Text[index]
                index += 1
    DecryptedText = ""
    for Column in range(len(Text)):
        for Row in range(Fence):
            if Matrix[Row][Column] != '.':
                DecryptedText += Matrix[Row][Column]
    return DecryptedText


def WFence_Attack(Text):
    Result = [(i, WFence_Decrypt(Text, i)) for i in range(2, len(Text))]
    return Result


def RC4_Encrypt(Text, Key):
    RC4 = ARC4.new(Key.encode())
    EncryptedText = base64.b64encode(RC4.encrypt(Text.encode())).decode()
    return EncryptedText


def RC4_Decrypt(Text, Key):
    RC4 = ARC4.new(Key.encode())
    DecryptedText = RC4.decrypt(base64.b64decode(Text.encode())).decode()
    return DecryptedText


def AES_Fill(Text):
    Fill = Text.encode()
    while len(Fill) % 16 != 0:
        Fill += b'\x00'
    return Fill


def AES_Encrypt(Text, Key, Mode=aes.MODE_ECB):
    AES = aes.new(AES_Fill(Key), Mode)
    EncryptedText = base64.b64encode(AES.encrypt(AES_Fill(Text))).decode()
    return EncryptedText


def AES_Decrypt(Text, Key, Mode=aes.MODE_ECB):
    AES = aes.new(AES_Fill(Key), Mode)
    DecryptedText = AES.decrypt(base64.b64decode(AES_Fill(Text))).decode()
    return DecryptedText


def RSA_Encrypt(Text, p, q, e=65537):
    m = bytes_to_long(Text.encode())
    c = gmpy2.powmod(m, e, p * q)
    EncryptedText = base64.b64encode(long_to_bytes(c)).decode()
    return EncryptedText


def RSA_Base64_Decrypt(Base64, p, q, e=65537):
    c = bytes_to_long(base64.b64decode(Base64.encode()))
    d = gmpy2.invert(e, (p - 1) * (q - 1))
    m = gmpy2.powmod(c, d, p * q)
    DecryptedText = long_to_bytes(m).decode()
    return DecryptedText


def RSA_Long_Decrypt(Long, p, q, e=65537):
    d = gmpy2.invert(e, (p - 1) * (q - 1))
    m = gmpy2.powmod(Long, d, p * q)
    DecryptedText = long_to_bytes(m).decode()
    return DecryptedText


def SHA1(Text):
    Hash = hashlib.sha1().update(Text.encode()).hexdigest()
    return Hash


def SHA256(Text):
    Hash = hashlib.sha256().update(Text.encode()).hexdigest()
    return Hash


def SHA512(Text):
    Hash = hashlib.sha512().update(Text.encode()).hexdigest()
    return Hash


def MD5(Text):
    Hash = hashlib.md5().update(Text.encode()).hexdigest()
    return Hash


def ProofOfWork_SHA256(Url, Port=80, Bit=4, HashBegin=":", SendAfter=">"):
    Connection = remote(Url, Port)
    Connection.recvuntil(HashBegin)
    Hash = Connection.recvuntil('\n', drop=True).decode().strip()
    Charset = string.printable
    Proof = mbruteforce(lambda x: hashlib.sha256((x).encode()).hexdigest() == Hash, Charset, Bit, method='fixed')
    Connection.sendlineafter(SendAfter, Proof)
    Connection.interactive()


def ProofOfWork_MD5(Url, Port=80, Bit=4, HashBegin=":", SendAfter=">"):
    Connection = remote(Url, Port)
    Connection.recvuntil(HashBegin)
    Hash = Connection.recvuntil('\n', drop=True).decode().strip()
    Charset = string.printable
    Proof = mbruteforce(lambda x: hashlib.md5((x).encode()).hexdigest() == Hash, Charset, Bit, method='fixed')
    Connection.sendlineafter(SendAfter, Proof)
    Connection.interactive()


def Base64_Encrypt(Text):
    try:
        EncryptedText = base64.b64encode(Text.encode()).decode()
        return EncryptedText
    except:
        return "[Base64]加密错误"


def Base64_Decrypt(Text):
    try:
        DecryptedText = base64.b64decode(Text.encode()).decode()
        return DecryptedText
    except:
        return "[Base64]解密错误"


def Base64_Stego_Decrypt(Base64List):
    Base64Code = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    Binary = ""
    for line in Base64List:
        if "==" in line:
            temp = bin(Base64Code.find(line[-3]) & 15)[2:]  # 通过按位与&15运算取出二进制数后4位 [2:]的作用是将0b过滤掉
            Binary += "0" * (4 - len(temp)) + temp  # 高位补0
        elif "=" in line:
            temp = bin(Base64Code.find(line[-2]) & 3)[2:]  # 通过按位与&3运算取出二进制数后2位
            Binary += "0" * (2 - len(temp)) + temp  # 高位补0
    Text = ""
    if(len(Binary) % 8 != 0):  # 最终得到的隐写数据二进制位数不一定都是8的倍数，为了避免数组越界，加上一个判断
        print("[Base64隐写]将进行不完整解析")
        for i in range(0, len(Binary), 8):
            if(i + 8 > len(Binary)):
                Text += " 剩余位:" + Binary[i:]
                return Text
            else:
                Text += chr(int(Binary[i:i + 8], 2))
    else:
        Text = "".join([chr(int(Binary[i:i + 8], 2)) for i in range(0, len(Binary), 8)])
        return Text


def Base32_Encrypt(Text):
    try:
        EncryptedText = base64.b32encode(Text.upper().encode()).decode()
        return EncryptedText
    except:
        return "[Base32]加密错误"


def Base32_Decrypt(Text):
    try:
        DecryptedText = base64.b32decode(Text.upper().encode()).decode()
        return DecryptedText
    except:
        return "[Base32]解密错误"


def Base16_Encrypt(Text):
    try:
        EncryptedText = base64.b16encode(Text.upper().encode()).decode()
        return EncryptedText
    except:
        return "[Base16]加密错误"


def Base16_Decrypt(Text):
    try:
        DecryptedText = base64.b16decode(Text.upper().encode()).decode()
        return DecryptedText
    except:
        return "[Base16]解密错误"


def CRC_Burst(Course):
    Binary = open(Course, "rb").read()
    if(int(Binary[0:8].hex(), 16) != int("0x89504e470d0a1a0a", 16)):
        print("[CRC爆破]检测到[文件头错误]，请修改第[1-8]个字节为:89 50 4E 47 0D 0A 1A 0A")
    if(int(Binary[8:12].hex(), 16) != int("0x0000000d", 16)):
        print("[CRC爆破]检测到[数据块长度错误]，请修改第[9-12]个字节为:00 00 00 0D")
    if(int(Binary[12:16].hex(), 16) != int("0x49484452", 16)):
        print("[CRC爆破]检测到[数据块标识错误]，请修改第[13-16]个字节为:49 48 44 52")
    Code = binascii.crc32(Binary[12:29]) & 0xffffffff
    CRC = int(Binary[29:33].hex(), 16)
    if(Code == CRC):
        print("[CRC爆破]CRC校验码匹配")
    else:
        print("[CRC爆破]CRC校验码不匹配 即将进行[宽度]爆破")
        for i in range(1, 4097):
            temp = struct.pack(">i", i)
            Code = binascii.crc32(bytes("IHDR", "ascii") + temp + Binary[20:29]) & 0xffffffff
            if(Code == CRC):
                print("图片正确宽度为:{} Hex:{}".format(i, hex(i)))
                return
        print("[CRC爆破][宽度]爆破失败 即将进行[高度]爆破")
        for i in range(1, 4097):
            temp = struct.pack(">i", i)
            Code = binascii.crc32(bytes("IHDR", "ascii") + Binary[16:20] + temp + Binary[24:29]) & 0xffffffff
            if(Code == CRC):
                print("图片正确高度为:{} Hex:{}".format(i, hex(i)))
                return
        print("[CRC爆破][宽高单项爆破]失败 即将进行[宽高联合爆破]")
        for i in range(4097):
            width = struct.pack(">i", i)
            for j in range(4097):
                height = struct.pack(">i", j)
                Code = binascii.crc32(bytes("IHDR", "ascii") + width + height + Binary[24:29]) & 0xffffffff
                if(Code == CRC):
                    print("[CRC爆破]宽度为:{} 高度为:{} Hex:{} {}".format(i, j, hex(i), hex(j)))
                    return
        print("[CRC爆破]爆破失败 请判断异常情况")


def BinaryToQRCode(BinaryList):
    X = Y = len(BinaryList)
    for i in range(X):
        assert(X == len(BinaryList[i]))
    image = Image.new('RGB', (X, Y))
    white = (255, 255, 255)
    black = (0, 0, 0)
    for i in range(X):
        line = BinaryList[i]
        for j in range(Y):
            if line[j] == '1':
                image.putpixel((i, j), black)
            elif line[j] == '0':
                image.putpixel((i, j), white)
    image.save("BinaryToQRCodeResult.png")
    image.show()


def RGBToImage(RGBList, X, Y, Mode="Column"):
    Board = Image.new("RGB", (X, Y))
    if Mode == "Column":
        for i in range(X):
            for j in range(Y):
                Index = i * Y + j
                Board.putpixel((i, j), tuple(eval(RGBList[Index])))
    elif Mode == "Row":
        for i in range(Y):
            for j in range(X):
                Index = i * X + j
                Board.putpixel((j, i), tuple(eval(RGBList[Index])))
    Board.save("RGBToImageResult.png")
    Board.show()


def ImageToRGB(ImageCourse, Mode="Column"):
    image = Image.open(ImageCourse)
    X = image.size[0]
    Y = image.size[1]
    imageRGB = image.convert("RGB")
    Result = []
    if Mode == "Column":
        for i in range(X):
            for j in range(Y):
                Result.append(imageRGB.getpixel((i, j)))
    elif Mode == "Row":
        for i in range(Y):
            for j in range(X):
                Result.append(imageRGB.getpixel((j, i)))
    return Result


def Request(Url, Method="GET", Headers=None, Params=None, Data=None):
    Response = requests.request(Method, Url, headers=Headers, params=Params, data=Data)
    StatusCode = Response.status_code
    ResponseHeaders = Response.headers
    Cookies = Response.cookies
    Response.encoding = Response.apparent_encoding
    ResponseText = Response.text
    ReText = Response.text.replace("\n", "").replace(" ", "")
    Result = {"StatusCode": StatusCode, "ResponseHeaders": ResponseHeaders, "Cookies": Cookies, "ResponseText": ResponseText, "ReText": ReText}
    return Result
