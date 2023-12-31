from requests   import get, post
from os         import system, remove
from sys        import argv
from random     import randint

base = "http://10.89.211.86:8000/flatrate/api-"

endpoints = [
    #("post-new-user",       post),
    #("post-new-user",       post),
    ("post-new-user",       post),
    #("resolve-address",     post),
    ("try-login",           get),
    ("create-chore",        post),
    ("create-chore",        post),
    ("create-chore",        post),
    ("create-chore",        post),
    ("get-user-chores",     get),
    ("get-others-chores",   get),
    ("get-flatmates",       get),
    ("get-tallies",         get),
    ("get-socialcredits",   get),
    ("change-lease",        post),
    ("change-lease",        post),
    ("change-lease",        post),
    ]

paramses = [
    {
#        "fnames":   "Jane Mary",
#        "sname":    "Doe",
#        "email":    "jmdoe@gmail.com",
#        "leaseid":  222
#    }, {
#        "fnames":   "John",
#        "sname":    "Smith",
#        "email":    "jsmith@outlook.com",
#        "leaseid":  222
#    }, {
        "fnames":   "Homeowner",
        "sname":    "Person",
        "email":    "a@gmail.com",
        "leaseid":  0,
        "address":  "123 Cringe Street, Inala"
    }, {
        "username": "jmdoe@gmail.com"
    }, {
        "type":     1,
        "weight":   20,
        "owner":    "jmdoe@gmail.com",
        "expiry":   "18:30:00 2/11/2023"
    }, {
        "type":     4,
        "weight":   20,
        "owner":    "jmdoe@gmail.com",
        "expiry":   "18:30:00 2/11/2023"
    }, {
        "type":     7,
        "weight":   10,
        "owner":    "jsmith@outlook.com",
        "expiry":   "18:30:00 2/11/2023"
    }, {
        "type":     17,
        "weight":   30,
        "owner":    "a@gmail.com",
        "expiry":   "18:30:00 2/11/2023"
    }, {
        "uname":    "jmdoe@gmail.com"
    }, {
        "leaseid":  222,
        "exclude":  "jsmith@outlook.com"
    }, {
        "uname":    "jsmith@outlook.com"
    }, {
        "leaseid":  222
    }, {
        "uname":    "jsmith@outlook.com"
    }, {
        "uname":    "jsmith@outlook.com",
        "leaseid":  "0",
        "address":  "123 cringe street, inala"
    }, {
        "uname":    "jsmith@outlook.com",
        "leaseid":  "0",
        "address":  f"deleteme {str(randint(0, 1000000))}"
    }, {
        "uname":    "jsmith@outlook.com",
        "leaseid":  222,
        "address":  "shouldn't matter"
    }
]

def main():
    #system("clear")
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
            if "allies" not in url:
                print(url + "\tpassed", res.text)
            else:
                print(url + "\tpassed")
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
    #system("rm /home/bingers/MICASA/FlatRate/media/* 2>  /dev/null")

if __name__ == "__main__":
    main()
