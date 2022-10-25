import json
import numpy as np


def read_filejson(path):
    f = open(path)
    data = json.load(f)
    for i in data:
        print(i)
    f.close()
    return data


def decode_json(msg):
    msg = msg.value.decode('utf-8')
    data = json.loads(msg)
    """    for i in data:
        print(i)"""

    return data


def encode_json(stringa_json):
    msg = stringa_json.encode('utf-8')
    return msg


def GestureRecognition(timestampwear, datafine):
    # return datafine
    gesturedata = []
    # scorro tutti gli elementi in memoria fino a quando ho il primo valore >=a quello passato dal wear
    MAX_PEOPLE_TRACKABLE = 10
    number_people = np.zeros(MAX_PEOPLE_TRACKABLE)
    times_appear = np.zeros(MAX_PEOPLE_TRACKABLE)
    bodies_ids=[]
    result = np.zeros(MAX_PEOPLE_TRACKABLE)
    #print("stampo datafine")
    #print(datafine)
    for frame in datafine:
        #if int(frame["timestamp"]) >= int(timestampwear):#old
        #@to do :
        if True:# al momento evito ma si dovrebbe controllare il tempo di quando è stato shakerato il wear
        #print(str(frame["timestamp"] * 1000 - timestampwear))
        #if frame["timestamp"]*1000-timestampwear>0:
        #print(frame["timestamp"]*1000)
        #print(str(timestampwear))
            numero_thisperson=0

            #print(frame)
            people = frame["bodies"]
            for person in people:  # all people
                abort = False

                #print("Person number: "+person["body_id"])
                if numero_thisperson >= MAX_PEOPLE_TRACKABLE:  # metto un massimo di persone gestibili
                    break

                numero_thisperson=len(bodies_ids)
                if person["body_id"] not in bodies_ids:
                     bodies_ids.append(person["body_id"])
                # print(person["keypoints"])
                joints = person["keypoints"]
                if len(joints)<1:
                    #print("break funge")
                    break
                #print(joints)
                """nose
                                    left_ear
                                    right_ear
                                    left_shoulder
                                    right_shoulder
                                    left_elbow
                                    right_elbow
                                    left_wrist
                                    right_wrist
                                    left_hip
                                    right_hip
                                    left_knee
                                    right_knee
                                    left_ankle
                                    right_ankle
                                    neck
                                    chest
                                    mid_hip"""
                """for joint in joints:
                    if joint=="nose" or joint=="right_wrist":
                #print(joints)"""
                nose = joints["nose"][0]

                right_wrist = joints["right_wrist"][0]
                nose_high = nose["z"]
                right_wrist_high = right_wrist["z"]
                """print("nose")
                print(nose)
                print("wrist")
                print(right_wrist)
                if math.isnan(nose_high):
                    nose = joints["left_ear"][0]
                    nose_high = nose["z"]
                    if math.isnan(nose_high):
                        nose = joints["right_ear"][0]
                        nose_high = nose["z"]
                        if math.isnan(nose_high):
                            nose = joints["left_elbow"][0]
                            nose_high = nose["z"]
                            if math.isnan(nose_high):
                                nose = joints["right_elbow"][0]
                                nose_high = nose["z"]
                                if math.isnan(nose_high):
                                    nose_high = 0
                                    abort = True"""
                if nose_high is None:
                    nose = joints["left_ear"][0]
                    nose_high = nose["z"]
                    if nose_high is None:
                        nose = joints["right_ear"][0]
                        nose_high = nose["z"]
                        if nose_high is None:
                            nose = joints["left_elbow"][0]
                            nose_high = nose["z"]
                            if nose_high is None:
                                nose = joints["right_elbow"][0]
                                nose_high = nose["z"]
                                if nose_high is None:
                                    nose_high = 0
                                    abort = True
                if right_wrist_high is None:
                    right_wrist_high = 0
                    abort = True
                """print(nose_high)
                print("nose")
                print(right_wrist_high)
                print("wrist")
                #print(len(bodies_ids))"""
                if not abort:
                    difference_head_wrist = right_wrist_high - nose_high
                    """number_people[int(person["body_id"])] = number_people[
                                                                int(person["body_id"])] + difference_head_wrist
                    times_appear[int(person["body_id"])] = times_appear[int(person["body_id"])] + 1"""
                    number_people[int(bodies_ids.index(person["body_id"]))] = number_people[
                                                                int(bodies_ids.index(person["body_id"]))] + difference_head_wrist
                    times_appear[int(bodies_ids.index(person["body_id"]))] = times_appear[int(bodies_ids.index(person["body_id"]))] + 1
        """if i == 20:
            break

            for i in range(3):
        head_mean[i] = head_mean[i]/len(datafine)
        right_hand_mean[i] = right_hand_mean[i] / len(datafine)

        if right_hand_mean[0]>head_mean[0]:
        result = "mano sopra la testa"""

    for i in range(len(times_appear)):#deve essere comparso
        # i=0
        # for _ in times_appear:
        # print("indice"+str(i))
        if times_appear[i] != 0:
            head_mean_distance = number_people[i] / times_appear[i]
            if head_mean_distance > 0:
                result[i] = 1
            #   i=i+1

    # print("risultato")
    # print(result)

    return result,bodies_ids