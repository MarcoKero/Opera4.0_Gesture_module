#!/usr/bin/env python3

# import threading
# import keyboard  # using module keyboard

__VERSION__ = '0.0.1'

import json

from kafka import KafkaConsumer, KafkaProducer

from lib_gest_kaf import read_filejson, decode_json, GestureRecognition

def kafka_gesture_reader():
    path = "data_config_gestures.json"
    config_info = read_filejson(path)
    consumer = KafkaConsumer(config_info["consumer_gesture_recognition_name"],
                             bootstrap_servers=config_info["bootstrapservers"],
                             security_protocol=config_info["security_protocol"],
                             sasl_mechanism=config_info["sasl_mechanism"],
                             sasl_plain_username=config_info["sasl_plain_username"],
                             sasl_plain_password=config_info["sasl_plain_password"])

    for msg in consumer:
        print(msg)

def main():
    path = "data_config_gestures.json"
    config_info = read_filejson(path)
    datafine = []

    print(f'Gesture recognition node {__VERSION__}')
    consumer = KafkaConsumer(config_info["consumer_wearable_event_name"], config_info["consumer_pose_aggreagator_name"],
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

    modalita_debug = False
    if modalita_debug:
        MAXFRAMES = 20
    else:
        MAXFRAMES = config_info["max_frames_number"]

    for msg in consumer:

        # print(msg)
        if (msg.topic == config_info["consumer_wearable_event_name"]):  # check wearable is shaked
            wear_data = decode_json(msg)
            #print(msg)
            #print("shake")
            if wear_data["is_shaking"]:
                stringa_json = "shaking device: " + str(wear_data["id"]), " timestamp: " + str(wear_data["timestamp"])
                print(stringa_json)
                result,bodies_ids = GestureRecognition(wear_data["timestamp"]-config_info["delay"], datafine)
                j = 0
                for elem in result:
                    if elem == 1:
                        # print(result[j])
                        print("person " + str(j) + " raised arm")
                        senddata = {
                            config_info["gesture_aggregator_body_id"]: bodies_ids[j],
                            config_info["gesture_timestamp"]: wear_data["timestamp"],
                            config_info["gesture_wear_id"]: wear_data["id"],
                            config_info["gesture_name"]: "Raised right hand"
                        }
                        print(senddata)
                        sendKafka = json.dumps(senddata)

                        producer_gesture.send("opera_data_gesture_recognition", sendKafka.encode())
                        print("done 1")

                    j = j + 1
                print(result)
        else:
            # msg = read_filejson("GestureRecKafkaDocker/data/befine_no_collision_1_zed/1.json")
            # print(msg)
            datasample = decode_json(msg)
            '''
            # print("done 2")
            # datafine = [datasample, datasample, datasample]
            # print(datasample)
            # for msg in consumer:
            # print("befine")
            # print(msg)
            # {"timestamp": 1654607356927.583, "body": [{"body_id": 0, "event": [], "keypoints": {"nose": {"x": NaN, "y": NaN, "z": NaN}, "left_ear": {"x": NaN, "y": NaN, "z": NaN}, "right_ear": {"x": NaN, "y": NaN, "z": NaN}, "left_shoulder": {"x": NaN, "y": NaN, "z": NaN}, "right_shoulder": {"x": NaN, "y": NaN, "z": NaN}, "left_elbow": {"x": NaN, "y": NaN, "z": NaN}, "right_elbow": {"x": NaN, "y": NaN, "z": NaN}, "left_wrist": {"x": NaN, "y": NaN, "z": NaN}, "right_wrist": {"x": NaN, "y": NaN, "z": NaN}, "left_hip": {"x": 10.851959228515625, "y": -4.4818196296691895, "z": -0.900795578956604}, "right_hip": {"x": 10.782848358154297, "y": -4.492856979370117, "z": -0.9190366268157959}, "left_knee": {"x": NaN, "y": NaN, "z": NaN}, "right_knee": {"x": 10.482959747314453, "y": -4.294037342071533, "z": -0.881792426109314}, "left_ankle": {"x": NaN, "y": NaN, "z": NaN}, "right_ankle": {"x": NaN, "y": NaN, "z": NaN}, "neck": {"x": NaN, "y": NaN, "z": NaN}, "chest": {"x": NaN, "y": NaN, "z": NaN}, "mid_hip": {"x": 10.817403793334961, "y": -4.487338066101074, "z": -0.9099161028862}}}]}
            '''
            if len(datafine) >= MAXFRAMES:
                datafine.pop(0)
                if modalita_debug:
                    result,bodies_ids = GestureRecognition(1654607356927.583- config_info["delay"], datafine)

                    # print(result)
                    j = 0
                    for elem in result:
                        if elem == 1:
                            # print(result[j])
                            print("person " + str(j) + " raised arm")

                            """ mod debug
                            senddata = datafine
                            senddata["BodyId"] = j"""

                            senddata = {
                                config_info["gesture_aggregator_body_id"]: j,
                                config_info["gesture_timestamp"]: 1654607356927.583,
                                config_info["gesture_wear_id"]: j,
                                config_info["gesture_name"]: "Raised right hand"
                            }
                            print(senddata)
                            datajson = json.dumps(senddata)

                            producer_gesture.send("opera_data_gesture_recognition", datajson.encode())
                            print("done 2")

                        j = j + 1
            datafine.append(datasample)


if __name__ == '__main__':
    main()