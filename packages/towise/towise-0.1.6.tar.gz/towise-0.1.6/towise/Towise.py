import requests
import re

class Towise:
    def __init__(self,app_id,app_key):
        self.headers = {
            "appid":app_id,
            "appkey":app_key,
            'accept': 'application/json'
        }
        self._baseURL= "https://api.towise.io"
        self._detect = {
                "face":"/detect/face",
                "body":"/detect/person",
                "emotion":"/detect/emotion"
        }
        self._recognize = {
                "face":"/recognize/face"
        }
        self._persons = "/persons/"
        self._faces = "/faces/"

    def checkImage(self,image):
        res = {}
        if(re.match("(data:image)",image)):
            res['image_base64'] = image
        else:
            res['image_url'] = image
        
        return res
    
    def faceDetect(self,image):
        data = self.checkImage(image)
        res = requests.post(url = self._baseURL + self._detect['face'], headers=self.headers, data = data)
        return res.json()

    def bodyDetect(self,image):
        data = self.checkImage(image)
        res = requests.post(url = self._baseURL + self._detect['body'], headers=self.headers, data = data)
        return res.json()
    
    def emotionDetect(self,image):
        data = self.checkImage(image)
        res = requests.post(url = self._baseURL + self._detect['emotion'], headers=self.headers, data = data)
        return res.json()

    def faceComparing(self,image):
        data = self.checkImage(image)
        res = requests.post(url = self._baseURL + self._recognize['face'], headers=self.headers, data = data)
        return res.getjson()
    
    def getAllPerson(self):
        res = requests.get(url = self._baseURL + self._persons, headers=self.headers)
        return res.json()
    
    def getPerson(self,person_id):
        params = {"person_id":person_id}
        res = requests.get(url = self._baseURL + self._persons, headers=self.headers, params = params)
        return res.json()
    
    def addPerson(self,name):
        data = {"name":name}
        res = requests.post(url = self._baseURL + self._persons, headers=self.headers, data = data)
        return res.json()

    def removePerson(self,person_id):
        data = {"person_id":person_id}
        res = requests.delete(url = self._baseURL + self._persons, headers=self.headers, data = data)
        return res.json()
    
    def getAllFace(self,person_id):
        params = {"person_id":person_id}
        res = requests.get(url = self._baseURL + self._faces, headers=self.headers, params = params)
        return res.json()

    def getFace(self,face_id):
        params = {"face_id":face_id}
        res = requests.get(url = self._baseURL + self._faces, headers=self.headers, params = params)
        return res.json()
    
    
    def addFace(self,image,person_id,save):
        data = self.checkImage(image)
        data["person_id"] = person_id
        data["save_image"] = save
        res = requests.post(url = self._baseURL + self._faces, headers=self.headers, data = data)
        return res.json()
    
    def removeFace(self, face_id):
        data = {"face_id":face_id}
        res = requests.delete(url = self._baseURL + self._faces, headers=self.headers, data = data)
        return res.json()