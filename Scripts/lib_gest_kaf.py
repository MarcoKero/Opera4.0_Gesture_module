import json
import numpy as np
from kafka import KafkaConsumer, KafkaProducer
import keyboard



def read_filejson(path):
    f = open(path)
    data = json.load(f)
    for i in data:
        print(i)
    f.close()
    return data

def decode_json(msg):
    msg=msg.value.decode('utf-8')
    data = json.loads(msg)
    """    for i in data:
        print(i)"""

    return data

def encode_json(stringa_json):
    msg=stringa_json.encode('utf-8')
    return msg

def GestureRecognition(timestampwear,datafine):
    return datafine
    gesturedata=[]
    #scorro tutti gli elementi in memoria fino a quando ho il primo valore >=a quello passato dal wear
    i=0

    joint_right_hand = []
    joint_head = []
    right_hand_mean = np.zeros(3)
    head_mean = np.zeros(3)
    result = "non gesture"
    for frame in datafine:#{"timestamp": 1654607356927.583, "body": [{"body_id": 0, "event": [], "keypoints": {"nose": {"x": NaN, "y": NaN, "z": NaN}, "left_ear": {"x": NaN, "y": NaN, "z": NaN}, "right_ear": {"x": NaN, "y": NaN, "z": NaN}, "left_shoulder": {"x": NaN, "y": NaN, "z": NaN}, "right_shoulder": {"x": NaN, "y": NaN, "z": NaN}, "left_elbow": {"x": NaN, "y": NaN, "z": NaN}, "right_elbow": {"x": NaN, "y": NaN, "z": NaN}, "left_wrist": {"x": NaN, "y": NaN, "z": NaN}, "right_wrist": {"x": NaN, "y": NaN, "z": NaN}, "left_hip": {"x": 10.851959228515625, "y": -4.4818196296691895, "z": -0.900795578956604}, "right_hip": {"x": 10.782848358154297, "y": -4.492856979370117, "z": -0.9190366268157959}, "left_knee": {"x": NaN, "y": NaN, "z": NaN}, "right_knee": {"x": 10.482959747314453, "y": -4.294037342071533, "z": -0.881792426109314}, "left_ankle": {"x": NaN, "y": NaN, "z": NaN}, "right_ankle": {"x": NaN, "y": NaN, "z": NaN}, "neck": {"x": NaN, "y": NaN, "z": NaN}, "chest": {"x": NaN, "y": NaN, "z": NaN}, "mid_hip": {"x": 10.817403793334961, "y": -4.487338066101074, "z": -0.9099161028862}}}]}
        if frame["timestamp"] >=timestampwear:
            people=frame["body"]
            for person in people:  # all people
                print(person["body_id"])
                #frame['body']
                #for frame in dati_befine:
                #posso aggiungere i punti in una lista che mi serve
                #joint_right_hand.append(frame['right_hand'])
                #joint_head.append(frame['head'])
                """right_hand_mean[0] = right_hand_mean[0] + frame['right_hand']['x']
                right_hand_mean[1] = right_hand_mean[1] + frame['right_hand']['y']
                right_hand_mean[2] = right_hand_mean[2] + frame['right_hand']['z']
    
                head_mean[0] = head_mean[0] + frame['head_mean']['x']
                head_mean[1] = head_mean[1] + frame['head_mean']['y']
                head_mean[2] = head_mean[2] + frame['head_mean']['z']
                i=i+1"""

        if i==20:
            break

    for i in range(3):
        head_mean[i] = head_mean[i]/len(dati_befine)
        right_hand_mean[i] = right_hand_mean[i] / len(dati_befine)

    if right_hand_mean[0]>head_mean[0]:
        result = "mano sopra la testa"

    return result

def wear_thread(thread_name,config_info):
    print(config_info)
    consumer = KafkaConsumer(thread_name,
                            bootstrap_servers=config_info["bootstrapservers"],
                            security_protocol=config_info["security_protocol"],
                            sasl_mechanism=config_info["sasl_mechanism"],
                            sasl_plain_username=config_info["sasl_plain_username"],
                            sasl_plain_password=config_info["sasl_plain_password"])

    producer_gesture = KafkaProducer(bootstrap_servers=config_info["bootstrapservers"],
                                     security_protocol=config_info["security_protocol"],
                                     sasl_mechanism=config_info["sasl_mechanism"],
                                     sasl_plain_username=config_info["sasl_plain_username"],
                                     sasl_plain_password=config_info["sasl_plain_password"])
    for msg in consumer:

        # check wearable is shaked
        wear_data = decode_json(msg)
        if wear_data["is_shaking"]:
            stringa_json = "shaking device: " + str(wear_data["id"]), " timestamp: " + str(wear_data["timestamp"])
            print(stringa_json)

            # dati_befine=[]
            result=GestureRecognition(wear_data["timestamp"])
            print(result)
            """stringa_json={
                id: str(wear_data["id"]),
                timestamp: str(wear_data["timestamp"],
                gesture: result
            }"""
            #future = producer_gesture.send("opera_data_gesture_recognition", "ciao".encode())
            print("done")
            #result = future.get(timeout=60)

def pose_thread(thread_name,config_info):
    global datafine
    msg=read_filejson("GestureRecKafkaDocker/data/befine_no_collision_1_zed/1.json")
    datasample = decode_json(msg)
    datafine=[datasample,datasample,datasample]
    print(datafine)
    print(config_info)
    consumer = KafkaConsumer(thread_name,
                            bootstrap_servers=config_info["bootstrapservers"],
                            security_protocol=config_info["security_protocol"],
                            sasl_mechanism=config_info["sasl_mechanism"],
                            sasl_plain_username=config_info["sasl_plain_username"],
                            sasl_plain_password=config_info["sasl_plain_password"],
                            value_deserializer=lambda x: json.loads(x.decode('utf-8')))#forse ultimo no

    for msg in consumer:
        print("befine")
        print(msg)#{"timestamp": 1654607356927.583, "body": [{"body_id": 0, "event": [], "keypoints": {"nose": {"x": NaN, "y": NaN, "z": NaN}, "left_ear": {"x": NaN, "y": NaN, "z": NaN}, "right_ear": {"x": NaN, "y": NaN, "z": NaN}, "left_shoulder": {"x": NaN, "y": NaN, "z": NaN}, "right_shoulder": {"x": NaN, "y": NaN, "z": NaN}, "left_elbow": {"x": NaN, "y": NaN, "z": NaN}, "right_elbow": {"x": NaN, "y": NaN, "z": NaN}, "left_wrist": {"x": NaN, "y": NaN, "z": NaN}, "right_wrist": {"x": NaN, "y": NaN, "z": NaN}, "left_hip": {"x": 10.851959228515625, "y": -4.4818196296691895, "z": -0.900795578956604}, "right_hip": {"x": 10.782848358154297, "y": -4.492856979370117, "z": -0.9190366268157959}, "left_knee": {"x": NaN, "y": NaN, "z": NaN}, "right_knee": {"x": 10.482959747314453, "y": -4.294037342071533, "z": -0.881792426109314}, "left_ankle": {"x": NaN, "y": NaN, "z": NaN}, "right_ankle": {"x": NaN, "y": NaN, "z": NaN}, "neck": {"x": NaN, "y": NaN, "z": NaN}, "chest": {"x": NaN, "y": NaN, "z": NaN}, "mid_hip": {"x": 10.817403793334961, "y": -4.487338066101074, "z": -0.9099161028862}}}]}
        if len(datafine)>=100:
            datafine.pop(0)
        datafine.add(msg)


    """ while True:
            #print(msg)
            if keyboard.is_pressed('a'):  # if key 'q' is pressed
                datafine.append("eccoci")
                #print(datafine)"""

def prova():
    msg=read_filejson(r"data/formatonuovo.json")
    #print(msg["timestamp"])
    data=[]
    bodies=msg["body"]
    #print(bodies)
    for person in bodies:#all people
        print(person["body_id"])
        #data = json.load(person)

    #datasample = decode_json(msg)
    #datafine=[datasample,datasample,datasample]