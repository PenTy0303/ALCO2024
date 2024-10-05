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
    
    
    # response = requests.post(
    #     url = url1,
    #     data=json.dumps({"name":"penguin0000", "pass":"sample"}),
    #     headers={"Content-Type":"application/json"},
    # ).json()
    
    # print(json.dumps(response, indent=2))
    
    
    response = requests.post(
        url = url2,
        headers = {"Content-Type":"application/json"},
        data = json.dumps({"userID":"97e185a1", "pass":"sample"})
    ).json()

    num = 0
    print(str(num) + json.dumps(response, indent=2))
    
    response = requests.post(
        url = url2,
        headers = {"Content-Type":"application/json"},
        data = json.dumps({"userID":"8a54bd87", "pass":"sample"})
    ).json()
    
    num += 1
    print(str(num) + json.dumps(response, indent=2))
    
    
    response = requests.get(
        url = url3 % ("5196c1c8", "381bb412")
    ).json()
    
    num += 1
    print(str(num) + json.dumps(response, indent=2))
    
    response = requests.get(
        url = url4 % ("97e185a1", "aa65486e")
    ).json()
    
    num += 1
    print(str(num) + json.dumps(response, indent=2))
    
    response = requests.put(
        url = url4 % ("97e185a1", "aa65486e")
    ).json()
    
    num += 1
    print(str(num) + json.dumps(response, indent=2))
    
    response = requests.get(
        url = url4 % ("97e185a1", "aa65486e"),
    ).json()
    
    num += 1
    print(str(num) + json.dumps(response, indent=2))


    response = requests.get(
        url = url5 % ("97e185a1", "aa65486e")
    ).json()
    
    num += 1
    print(str(num) + json.dumps(response, indent=2))    
    
    response = requests.post(
        url = url6 % ("97e185a1", "aa65486e"),
        data = json.dumps({"itemID":2, "itemCount":10, "property":900}),
        headers = {"Content-Type":"application/json"},
    ).json()
    
    num += 1
    print(str(num) + json.dumps(response, indent=2)) 
    
    response = requests.put(
        url = url7 % ("97e185a1", "aa65486e"),
        data = json.dumps({"itemID":2, "itemCount":10, "destructionRate":10, "civilizationRate":10, "debuff":10}),
        headers = {"Content-Type":"application/json"},
    ).json()
    
    
    num += 1
    print(str(num) + json.dumps(response, indent=2)) 
    
    response = requests.put(
        url = url8 % ("97e185a1", "aa65486e"),
        data = json.dumps({"unlockedAchievement":[{"id":0, "name":"地球救済マスター"}]}, ensure_ascii=False),
        headers = {"Content-Type":"application/json"},
    ).json()
    
    num += 1
    print(str(num) + json.dumps(response, indent=2)) 
    
    response = requests.get(
        url = url9 % ("97e185a1", "aa65486e")
    ).json()
    
    num += 1
    print(str(num) + json.dumps(response, indent=2))
    
    
    response = requests.get(
        url = url9 % ("8a54bd87", "9b2b619e")
    ).json()
    
    num += 1
    print(str(num) + json.dumps(response, indent=2))
    
    response = requests.put(
        url = url9 % ("97e185a1", "aa65486e"),
        data = json.dumps({"todaySteps":100, "totalSteps":1100, "property":900}, ensure_ascii=False),
        headers = {"Content-Type":"application/json"},
    ).json()
    
    num += 1
    print(str(num) + json.dumps(response, indent=2))
    
    response = requests.get(
        url = url10 % ("5196c1c8", "381bb412", "1")
    ).json()
    
    num += 1
    print(str(num) + json.dumps(response, indent=2))