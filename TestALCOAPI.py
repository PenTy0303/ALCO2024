if(__name__ == "__main__"): 
    import os
    import random
    import datetime
    import json
    import requests

    users = ["inamori", "inagawa", "imoto", "imazato", "takatosi", "Xx_fps_shake_xX", "takemoto", "banndou", "uwano", "ishimizu", "mori"]
    passwords = ["sample", "sample", "sample", "sample","sample","sample", "sample", "sample", "sample", "sample"]
    userIDs = ["1242f353", "e09e6a90", "fbd9f8b6", "94e49b24", "1e50b217", "8e016722", "2ec60030", "ec02f7be", "a14451b3", "15d35444"]


    url1 = "http://127.0.0.1:5000/ALCOAPI/v2.0.0/CreateUser"
    url2 = "http://127.0.0.1:5000/ALCOAPI/v2.0.0/AuthUser"
    
    
    

    for u,p, id in zip(users, passwords, userIDs):
        payload = {"name":str(u), "pass": str(p)}
        response1 = requests.post(
            url1, 
            headers={"Content-Type": "application/json"}, 
            data=json.dumps(payload)
            ).json()
        
        print(response1)
        if("userID" in response1.keys()):
            payload = {"userID":str(response1["userID"]), "pass": p}
            
            
            response2 = requests.post(
                url2, 
                headers = {"Content-Type": "application/json"},
                data=json.dumps(payload)
                ).json()
            
            print(response2)
        else:
            payload = {"userID":id, "pass": p}
            response2 = requests.post(
                url2, 
                headers = {"Content-Type": "application/json"}, 
                data=json.dumps(payload)
                ).json()
            
            print(response2)
        
          
        
    # CE = CreateEngine()
    # session = MakeSession(CE).getSession()
    
    # for u,p in zip(users, passwords):
    #     user = session.query(USER).filter(USER.name == u).all()
    #     userDataID = user[0].userDataID
        
    #     data = session.query(USERData).filter(USERData.userDataID == userDataID).all()
    #     data = data[0]
        
    #     steps = [random.randint(10, 10000) for _ in range(7)]
        
    #     data.totalSteps = sum(steps)
    #     data.todaySteps = steps[0]
    #     data.point = random.randint(0, 100)
    #     data.favorableRate = random.randint(0, 100)
    #     data.reloadedDate = datetime.datetime.now()
    #     data.weekSteps = json.dumps(dict([("0"+str(i+1), steps[i]) for i in range(7)]))
        
    #     session.flush()
        
    
    # session.commit()
    
    # session.close()


        