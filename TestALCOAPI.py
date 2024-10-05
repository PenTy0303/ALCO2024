if(__name__ == "__main__"): 
    import os
    import random
    import datetime
    import json
    import requests
    import time

    users = ["inamori", "inagawa", "imoto", "imazato", "takatosi", "Xx_fps_shake_xX", "takemoto", "banndou", "uwano", "ishimizu", "mori"]
    passwords = ["sample", "sample", "sample", "sample","sample","sample", "sample", "sample", "sample", "sample"]


    sel = 1
    domain  = ["127.0.0.1:5000", "alco2024.sakura.ne.jp/ALCOAPI/v2.0.0"]
    
    
    url1 = "http://" + domain[sel] + "/CreateUser"
    url2 = "http://" + domain[sel] + "/AuthUser"
    url3 = "http://" + domain[sel] + "/UseSession/%s?sessionID=%s"
    url4 = "http://" + domain[sel] + "/InterfereTime/%s?sessionID=%s"
    url5 = "http://" + domain[sel] + "/IsRelief/%s?sessionID=%s"
    url6 = "http://" + domain[sel] + "/FetchItem/%s?sessionID=%s"
    url7 = "http://" + domain[sel] + "/FetchItem/%s?sessionID=%s"
    url8 = "http://" + domain[sel] + "/FetchAchievement/%s?sessionID=%s"
    url9 = "http://" + domain[sel] + "/FetchUserData/%s?sessionID=%s"
    url10 = "http://" + domain[sel] + "/GetUserRanking/%s?sessionID=%s&num=%s"
    
    
    response = requests.post(
        url = url1,
        data=json.dumps({"name":"penguin0005", "pass":"sample"}),
        headers={"Content-Type":"application/json"},
    ).json()
    
    print(json.dumps(response, indent=2))
    
    
    response = requests.post(
        url = url2,
        headers = {"Content-Type":"application/json"},
        data = json.dumps({"userID":"d1dbd082", "pass":"sample"})
    ).json()

    num = 0
    print(str(num) + json.dumps(response, indent=2))
    
    response = requests.get(
        url = url3 % ("d1dbd082", "90d423e6")
    ).json()
    
    num += 1
    print(str(num) + json.dumps(response, indent=2))
    
    response = requests.get(
        url = url4 % ("d1dbd082", "90d423e6")
    ).json()
    
    num += 1
    print(str(num) + json.dumps(response, indent=2))
    
    response = requests.put(
        url = url4 % ("d1dbd082", "90d423e6")
    ).json()
    
    num += 1
    print(str(num) + json.dumps(response, indent=2))
    
    response = requests.get(
        url = url4 % ("d1dbd082", "90d423e6"),
    ).json()
    
    num += 1
    print(str(num) + json.dumps(response, indent=2))


    response = requests.get(
        url = url5 % ("d1dbd082", "90d423e6")
    ).json()
    
    num += 1
    print(str(num) + json.dumps(response, indent=2))    
    
    response = requests.post(
        url = url6 % ("d1dbd082", "90d423e6"),
        data = json.dumps({"itemID":2, "itemCount":10, "property":900}),
        headers = {"Content-Type":"application/json"},
    ).json()
    
    num += 1
    print(str(num) + json.dumps(response, indent=2)) 
    
    response = requests.put(
        url = url7 % ("d1dbd082", "90d423e6"),
        data = json.dumps({"itemID":2, "itemCount":10, "destructionRate":10, "civilizationRate":10, "debuff":100}),
        headers = {"Content-Type":"application/json"},
    ).json()
    
    
    num += 1
    print(str(num) + json.dumps(response, indent=2)) 
    
    response = requests.put(
        url = url8 % ("d1dbd082", "90d423e6"),
        data = json.dumps({"unlockedAchievement":[{"id":0, "name":"地球救済マスター"}]}, ensure_ascii=False),
        headers = {"Content-Type":"application/json"},
    ).json()
    
    num += 1
    print(str(num) + json.dumps(response, indent=2)) 
    
    response = requests.get(
        url = url9 % ("d1dbd082", "90d423e6")
    ).json()
    
    num += 1
    print(str(num) + json.dumps(response, indent=2))
    
    
    response = requests.get(
        url = url9 % ("d1dbd082", "90d423e6")
    ).json()
    
    num += 1
    print(str(num) + json.dumps(response, indent=2))
    
    response = requests.put(
        url = url9 % ("d1dbd082", "90d423e6"),
        data = json.dumps({"todaySteps":100, "totalSteps":1100, "property":900}, ensure_ascii=False),
        headers = {"Content-Type":"application/json"},
    ).json()
    
    num += 1
    print(str(num) + json.dumps(response, indent=2))
    
    response = requests.get(
        url = url10 % ("d1dbd082", "90d423e6", "1")
    ).json()
    
    num += 1
    print(str(num) + json.dumps(response, indent=2))