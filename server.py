# This is server code to send video and audio frames over UDP

import cv2, imutils, socket

import time
import base64
import  wave, pyaudio,pickle,struct

import queue
import os

q = queue.Queue(maxsize=10)

filename =  'yellow.mp4'
command = "ffmpeg -i {} -ab 160k -ac 2 -ar 44100 -vn {}".format(filename,'temp.wav')#audio bitrate,audio channle, auido sample rate
os.system(command)#uses poweshell and ffmpeg

BUFF_SIZE = 65536# 2 power 16, 16 bit
server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)#af_inet for ipv4, sock.datagram for UDP datagram, server_socket is the object
server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)#set socket output, the size speciefied for recieve buffer
host_name = socket.gethostname()
host_ip = '192.168.206.1'#  socket.gethostbyname(host_name)
print(host_ip)
port = 10006
socket_address = (host_ip,port)
server_socket.bind(socket_address)
print('Listening at:',socket_address)

vid = cv2.VideoCapture(filename)#captures video frame data
FPS = vid.get(cv2.CAP_PROP_FPS)
global TS
TS = (0.5/FPS)#ts i timestamp
BREAK=False
print('FPS:',FPS,TS)
totalNoFrames = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
durationInSeconds = float(totalNoFrames) / float(FPS)
d=vid.get(cv2.CAP_PROP_POS_MSEC)
print(durationInSeconds,d)

def video_stream_gen():#This is a Python function that generates a video stream from a file using OpenCV and imutils libraries.
   
    WIDTH=400#width is 400 pixel
    while(vid.isOpened()):
        try:
            _,frame = vid.read()#frrame contains data,_ return value
            frame = imutils.resize(frame,width=WIDTH)#used with opencv,resize the frame
            q.put(frame)
        except:
            os._exit(1)
    print('Player closed')
    BREAK=True
    vid.release()#this function reads frames from a video file, resizes them to a specified width using the imutils library, and adds them to a queue for further processing or transmission.

def video_stream():#This is a Python function that sends a video stream over a network using OpenCV, base64 encoding, and socket programming.
    global TS
    fps,st,frames_to_count,cnt = (0,0,1,0)
    cv2.namedWindow('TRANSMITTING VIDEO')        
    cv2.moveWindow('TRANSMITTING VIDEO', 10,30) 
    while True:
        msg,client_addr = server_socket.recvfrom(BUFF_SIZE)
        print('GOT connection from ',client_addr)
        WIDTH=400
        
        while(True):
            frame = q.get()
            encoded,buffer = cv2.imencode('.jpeg',frame,[cv2.IMWRITE_JPEG_QUALITY,80])
            message = base64.b64encode(buffer)
            server_socket.sendto(message,client_addr)
            frame = cv2.putText(frame,'FPS: '+str(round(fps,1)),(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
            if cnt == frames_to_count:
                try:
                    fps = (frames_to_count/(time.time()-st))
                    st=time.time()
                    cnt=0
                    if fps>FPS:
                        TS+=0.001#ts is transmission speed
                    elif fps<FPS:
                        TS-=0.001
                    else:
                        pass
                except:
                    pass
            cnt+=1
            
            
            
            cv2.imshow('TRANSMITTING VIDEO', frame)
            key = cv2.waitKey(int(1000*TS)) & 0xFF	
            if key == ord('q'):
                os._exit(1)
                TS=False
                break	
                

def audio_stream():
    s = socket.socket()
    s.bind((host_ip, (port-1)))

    s.listen(5)
    CHUNK = 1024
    wf = wave.open("temp.wav", 'rb')
    p = pyaudio.PyAudio()
    print('server listening at',(host_ip, (port-1)))
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    input=True,
                    frames_per_buffer=CHUNK)

    client_socket,addr = s.accept()#accept client request

    while True:
        if client_socket:
            while True:
                data = wf.readframes(CHUNK)
                a = pickle.dumps(data)
                message = struct.pack("Q",len(a))+a#binary message
                client_socket.sendall(message)
                

from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=3) as executor:
    executor.submit(audio_stream)
    executor.submit(video_stream_gen)
    executor.submit(video_stream)
