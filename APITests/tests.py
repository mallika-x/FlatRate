from requests   import get, post
from os         import remove

base = "http://10.89.211.86:8000/flatrate/api-"

endpoints = [
    ("post-new-user/", post)
    ]

paramses = [
    {
        "fname":    "Jane Mary",
        "sname":    "Doe",
        "email":    "jmdoe@gmail.com"
    }
]

fileses = [
    {
        "pii":      open("/home/bingers/Desktop/fakepassport.png",    "rb"),
        "photo":    open("/home/bingers/Desktop/fakephoto.jpg",       "rb")
    }
]

def main():
    combined = list(zip(endpoints, paramses, fileses))
    for i in combined:
        end, params, files = i
        url, method = end
        res = method(base + url, params = params, files = files)
        if (res.status_code == 200):
            print(url + " passed")
            remove(f"{url[:-1]}.html")
        else:
            print(url + " failed")
            f = open(f"{url[:-1]}.html", "w")
            f.write(res.text)
            f.close


if __name__ == "__main__":
    main()
