from requests   import get, post
from os         import system, remove

base = "http://10.89.211.86:8000/flatrate/api-"

endpoints = [
    ("post-new-user",       post),
    ("try-login",           get),
    ("create-chore",    post),
    ]

paramses = [
    {
        "fname":    "Jane Mary",
        "sname":    "Doe",
        "email":    "jmdoe@gmail.com",
        "leaseid":  222
    }, {
        "username": "jmdoe@gmail.com"
    }, {
        "type":     1,
        "weight":   15,
        "owner":    "jmdoe@gmail.com"
    }
]

fileses = [
    {
        "pii":      open("/home/bingers/Desktop/fakepassport.png",    "rb"),
        "photo":    open("/home/bingers/Desktop/fakephoto.jpg",       "rb")
    }, {None: None}, {None: None}
]

def main():
    system("clear")
    combined = list(zip(endpoints, paramses, fileses))
    for i in combined:
        end, params, files = i
        url, method = end
        res = None
        if files is not None:
            res = method(f"{base}{url}/", params = params, files = files)
        else:
            res = method(f"{base}{url}/", params = params)
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

    #print(post(f"{base}burn-everything/").text[2:-2])
    system("rm /home/bingers/MICASA/FlatRate/media/* 2>  /dev/null")

if __name__ == "__main__":
    main()
