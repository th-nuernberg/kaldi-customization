import requests
import threading
import multiprocessing

def make_request(method, url, data):
    print("Started to make " + str(method) + "Request to " + url)
    if(method == "GET"):
        response = requests.get(url=url)
        print(response)
        return
    if(method == "POST"):
        response = requests.post(url=url,data=data)
        print(response)
        return
    print("Unknown Method (" + method + ")")

def make_async_request(method, url, data=None):
    p = multiprocessing.current_process()
    name = "callback worker" + str(p.pid)
    cc = multiprocessing.Process(name=name, target=make_request,args=(method,url,data,))
    cc.daemon = False
    cc.start()