from vidstream import AudioSender ,   AudioReceiver  , ScreenShareClient , CameraClient , StreamingServer 
import tkinter as tk
import socket #getting for private ip address
import threading  # for many many connectings , audio video receiving and sending

# 192.168.43.187

host_name = socket.gethostname()
local_ip_address = socket.gethostbyname(host_name)
print("local_ip_address ",host_name,  local_ip_address )

#for public ip address
# import requests 
# public_ip_address = requests.get('https://api.ipify.org')
# print(public_ip_address)

server = StreamingServer(local_ip_address , 7777)
receiver = AudioReceiver(local_ip_address , 6666)

print()

def start_listening():
    t1 = threading.Thread(target=server.start_server)
    t2 = threading.Thread(target=receiver.start_server)
    t1.start()
    t2.start()


def start_camera_stream():
    camera_client = CameraClient(text_target_ip.get(1.0 , 'end-1c') , 9999)
    t3 = threading.Thread(target=camera_client.start_stream)
    t3.start()


def start_screan_sharing():
    screen_client = ScreenShareClient(text_target_ip.get(1.0 , 'end-1c') , 9999)
    t4 = threading.Thread(target=screen_client.start_stream)
    t4.start()



def start_audio_stream():
    audio_sender = AudioSender(text_target_ip.get(1.0 , 'end-1c') , 8888)
    t5 = threading.Thread(target=audio_sender.start_stream)
    t5.start()






#gui
window = tk.Tk();
window.title('People AI Meet')
window.geometry('300x200')

label_target_ip = tk.Label(window , text = 'target ip')
label_target_ip.pack()

text_target_ip = tk.Text(window , height = 1)
text_target_ip.pack()

btn_listen = tk.Button(window , text= 'start listening' , width=50 , command=start_listening)
btn_listen.pack(anchor=tk.CENTER , expand=True)

btn_camera = tk.Button(window , text= 'start camera stream' , width=50 ,  command=start_camera_stream)
btn_camera.pack(anchor=tk.CENTER , expand=True)

# btn_screen = tk.Button(window , text= 'start screen sharing' , width=50 ,  command=start_screan_sharing)
# btn_screen.pack(anchor=tk.CENTER , expand=True)

btn_audio = tk.Button(window , text= 'start audio stream' , width=50 , command=start_audio_stream)
btn_audio.pack(anchor=tk.CENTER , expand=True)

window.mainloop()

# window.


''' 
host_name => DESKTOP-20HI0QT
IPv4 Address. = local_ip_address => 192.168.43.187


'''