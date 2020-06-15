__version__ = '0.1.0'

import requests

ept=''

def main():
    while True:
        callEndpoint(ept)

def callEndpoint(endpoint):
    req = requests.post("http://localhost:3000"+endpoint)
    res = req.text
    status = req.status_code

if __name__=="__main__":
    main()