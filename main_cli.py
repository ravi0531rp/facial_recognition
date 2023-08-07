import os.path
import datetime
import pickle
import cv2
import face_recognition
import util_cli

def main():
    while True:
        print("1. Login")
        print("2. Logout")
        print("3. Register New User")
        print("4. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            login()
        elif choice == '2':
            logout()
        elif choice == '3':
            register_new_user()
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

def login():
    capture = util_cli.capture_face()
    model_path = 'anti_spoof/anti_spoof_models/anti_spoof_model.pth'

    if util_cli.is_spoof(capture, model_path):
        print('Hey, you are a spoofer! You are fake!')
        return
    
    name = util_cli.recognize(capture)
    if name in ['unknown_person', 'no_persons_found']:
        print('Unknown user. Please register new user or try again.')
    else:
        print('Welcome, {}.'.format(name))
        log_event(name, 'in')

def logout():
    capture = util_cli.capture_face()
    model_path = 'anti_spoof/anti_spoof_models/anti_spoof_model.pth'
    if util_cli.is_spoof(capture, model_path):
        print('Hey, you are a spoofer! You are fake!')
        return
    name = util_cli.recognize(capture)

    if name in ['unknown_person', 'no_persons_found']:
        print('Unknown user. Please register new user or try again.')
    else:
        print('Goodbye, {}.'.format(name))
        log_event(name, 'out')

def register_new_user():
    capture = util_cli.capture_face()
    name = input("Please input username: ")
    util_cli.register_user(name, capture)
    print('User was registered successfully!')

def log_event(name, event):
    log_path = './log.txt'
    with open(log_path, 'a') as f:
        f.write('{},{},{}\n'.format(name, datetime.datetime.now(), event))

if __name__ == "__main__":
    main()
