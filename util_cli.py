import os
import pickle
import face_recognition
from anti_spoof.anti_spoof_predict import AntiSpoofPredict
import cv2

def is_spoof(img, model_path):
    device_id = 0
    anti_spoof_predictor = AntiSpoofPredict(device_id)
    result = anti_spoof_predictor.predict(img, model_path)
    return result[0][0] < result[0][1]

def recognize(img):
    db_path = './db'
    embeddings_unknown = face_recognition.face_encodings(img)
    if len(embeddings_unknown) == 0:
        return 'no_persons_found'
    else:
        embeddings_unknown = embeddings_unknown[0]

    db_dir = sorted(os.listdir(db_path))
    match = False
    j = 0
    while not match and j < len(db_dir):
        path_ = os.path.join(db_path, db_dir[j])
        file = open(path_, 'rb')
        embeddings = pickle.load(file)
        match = face_recognition.compare_faces([embeddings], embeddings_unknown)[0]
        j += 1

    if match:
        return db_dir[j - 1][:-7]
    else:
        return 'unknown_person'

def register_user(name, capture):
    db_dir = './db'
    if not os.path.exists(db_dir):
        os.mkdir(db_dir)

    embeddings = face_recognition.face_encodings(capture)[0]
    file = open(os.path.join(db_dir, '{}.pickle'.format(name)), 'wb')
    pickle.dump(embeddings, file)

def capture_face():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    return frame