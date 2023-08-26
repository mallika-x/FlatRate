from requests   import get, post
from os         import system, remove
from sys        import argv

base = "http://10.89.211.86:8000/flatrate/api-"

endpoints = [
    ("post-new-user",   post),
    ("post-new-user",   post),
    ("resolve-address", post),
    ("resolve-address", post),
    ("try-login",       get),
    ("create-chore",    post),
    ("create-chore",    post),
    ("create-chore",    post),
    ("get-user-chores", get),
    ]

paramses = [
    {
        "fnames":   "Jane Mary",
        "sname":    "Doe",
        "email":    "jmdoe@gmail.com",
        "leaseid":  0
    }, {
        "fnames":   "John",
        "sname":    "Smith",
        "email":    "jsmith@outlook.com",
        "leaseid":  0
    }, {
        "uname":    "jmdoe@gmail.com",
        "address":  "123 Cringe Street, Inala"
    }, {
        "uname":    "jsmith@outlook.com",
        "address":  "123 Cringe Street, Inala"
    }, {
        "username": "jmdoe@gmail.com"
    }, {
        "type":     1,
        "weight":   15,
        "owner":    "jmdoe@gmail.com",
        "expiry":   "18:30:00 2/11/2023"
    }, {
        "type":     4,
        "weight":   15,
        "owner":    "jmdoe@gmail.com",
        "expiry":   "18:30:00 2/11/2023"
    }, {
        "type":     7,
        "weight":   5,
        "owner":    "jsmith@outlook.com",
        "expiry":   "18:30:00 2/11/2023"
    }, {
        "uname":    "jmdoe@gmail.com"
    }
]

def main():
    system("clear")
    combined = list(zip(endpoints, paramses))
    for i in combined:
        #print(i)
        end, params = i
        url, method = end
        if method == get:
            res = method(f"{base}{url}/", params = params)
        else:
            res = method(f"{base}{url}/", data = params)
        if (res.status_code == 200):
            print(url + "\tpassed", res.text)
            try:
                remove(f"{url}.html")
            except:
                # idc
                pass
        else:
            print(url + "\tfailed")
            f = open(f"{url}.html", "w")
            f.write(res.text)
            f.close

    if argv[1] == "kill":
        print(post(f"{base}burn-everything/").text[2:-2])
    system("rm /home/bingers/MICASA/FlatRate/media/* 2>  /dev/null")

if __name__ == "__main__":
    main()
