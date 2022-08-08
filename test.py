import base64
import codecs

string = "46726f6d4e6f774f6e4950726f6d697365494c4c5472794e6f74546f486174654d7973656c660d0a"

# split_strings = []
# n = 2
# for index in range(0, len(string), n):
#     split_strings.append(string[index : index + n])
#
# new_string = ''.join([f'\\x{i}' for i in split_strings])
# print(new_string)
# print(base64.decode())

print(bytes.fromhex(string))
