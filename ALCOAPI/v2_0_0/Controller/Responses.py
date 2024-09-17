import datetime
import time

class Responses():
    _Status_200 = {}
    _Status_401 = {}
    _Status_404 = {}
    
    
    def get_200(self, acceptedTime, body={}):
        self._Status_200["status"] = "successful"
        self._Status_200["acceptedTime"] = "-".join(str(datetime.datetime.fromtimestamp(int(acceptedTime))).split(" ")).replace(":", "-")
        self._Status_200["responsedTime"] = "-".join(str(datetime.datetime.fromtimestamp(int(time.time()))).split(" ")).replace(":", "-")
        self._Status_200["responses"] = body
        
        return self._Status_200
    
    def get_401(self, acceptedTime, message="you can not be autholized with your userID and sessionID."):
        self._Status_401["status"] = "faild"
        self._Status_401["acceptedTime"] = "-".join(str(datetime.datetime.fromtimestamp(int(acceptedTime))).split(" ")).replace(":", "-")
        self._Status_401["responsedTime"] = "-".join(str(datetime.datetime.fromtimestamp(int(time.time()))).split(" ")).replace(":", "-")
        self._Status_401["body"] = {"message": message}
        
        return self._Status_401
        
    def get_404(self, acceptedTime, message="you can not get your data."):
        self._Status_401["status"] = "faild"
        self._Status_401["acceptedTime"] = "-".join(str(datetime.datetime.fromtimestamp(int(acceptedTime))).split(" ")).replace(":", "-")
        self._Status_401["responsedTime"] = "-".join(str(datetime.datetime.fromtimestamp(int(time.time()))).split(" ")).replace(":", "-")
        self._Status_401["body"] = {"message": message}
        
        return self._Status_404