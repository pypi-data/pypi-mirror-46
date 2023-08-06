import requests
import json
import numpy as np
import cv2
import io

class Algorithm(object):
    def __init__(self, client,token):
        self.token = token
        self.client = client

    def send(self,input_data):
        return self.post_data(input_data)

    def send_url_to_download(self,input_object):
        if isinstance(input_object, (str,)): 
            input_json = input_object.encode('utf-8')
            headers = {'x-access-token': self.token,'content-type':'text/uri-list'}
            return self.return_from_headders(requests.post(self.client, 
                                        data=input_json,
                                        headers=headers, 
                                        params = {'timeout':200}))
        else: 
            raise ValueError("Error: must provide a url to download")

    def post_data(self,input_object):
        if input_object is None:
            input_json = json.dumps(None).encode('utf-8')
            headers = {'x-access-token': self.token,'content-type':'application/json'}
        elif isinstance(input_object, (str,)): 
            input_json = input_object.encode('utf-8')
            headers = {'x-access-token': self.token,'content-type':'text/plain'}
        elif isinstance(input_object, (dict,)):
            for key, value in input_object.items(): 
                if isinstance(value,np.ndarray):
                    input_object[key] = value.tolist()
            input_json = json.dumps(input_object).encode('utf-8')
            headers = {'x-access-token': self.token,'content-type':'application/json'} 
        elif isinstance(input_object, (bytearray, bytes)):
            input_json = bytes(input_object)
            headers = {'x-access-token': self.token,'content-type':'application/octet-stream'}
        else:
            input_json = json.dumps(input_object).encode('utf-8')
            headers = {'x-access-token': self.token,'content-type':'application/json'}
        
        return self.return_from_headders(requests.post(self.client, 
                                    data=input_json,
                                    headers=headers, 
                                    params = {'timeout':200}))
        
    def return_from_headders(self,r):
        if r.headers['content-type'] ==  'application/json':
            if "Error" in  r.json():
                raise ValueError(r.json()["Error"])
            return (r.json())
        elif r.headers['content-type'] ==  'text/plain':     
            return (r.text)
        elif r.headers['content-type'] ==  'application/octet-stream':  
            return (r.content)
        elif r.headers['content-type'] ==  'image/jpg':  
            return (r.content)
        elif r.headers['content-type'] ==  'image/png':  
            return (r.content)
        raise ValueError("Error: unable to call algorithm")


def jpgbytes_to_np(output):
    img = np.asarray(bytearray(output),dtype=np.uint8)
    img = cv2.cvtColor(cv2.imdecode(img,cv2.IMREAD_UNCHANGED),cv2.COLOR_BGR2RGB)
    return img

def jpgbytes_to_list(output):
    img = np.asarray(bytearray(output),dtype=np.uint8)
    img = cv2.cvtColor(cv2.imdecode(img,cv2.IMREAD_UNCHANGED),cv2.COLOR_BGR2RGB).tolist()
    return img
