# Opera4.0_Gesture_module

Prende come INPUT tutti i dati del thread "opera_data_human_pose_aggregator"(json) mantenendo in memoria gli ultimi "max_frames_number"(json). Il metodo di riconoscimento si avvia quando arriva un evento "opera_data_wearable"["is_shaking"](json). 

Se è stata riconosciuta una gesture, invia come OUTPUT al thread "opera_data_gesture_recognition"(json): 
  "gesture_aggregator_body_id": id del poseaggregator 
  "gesture_timestamp": tempo dello shake 
  "gesture_wear_id": id del wearable  
  "gesture_name": gesture eseguita 
  
La funzione GestureRecognition(timestampwear, datafine) ha un limite massimo di persone trackabili (MAX_PEOPLE_TRACKABLE). 

Al momento non è importante il timestamp del wearable ma si può attivare un controllo per evitare scheletri "vecchi" scommentando riga 44 (if frame["timestamp"]*1000-timestampwear>0). 

Dal momento che befine non vede sempre i joint, ho dovuto effettuare dei controlli a cascata: se non vede il naso, cerca orecchia destra, sopracciglia sinistra e così via. Ho eseguito questo controllo per avere un punto da identificare come testa, necessario per verificare che il joint manodestra sia sotto o sopra di esso 
