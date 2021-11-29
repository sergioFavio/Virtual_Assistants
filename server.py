# ... server_with_record.py

import socket,pickle,struct,time
import pyshine as ps
import threading
import tempfile
import soundfile as sf
filename = tempfile.mktemp(prefix='output',suffix='.wav',dir='')

mode =  'get'
name = 'SERVER RECEIVING AUDIO'
audio,context= ps.audioCapture(mode=mode)
#ps.showPlot(context,name)

# Socket Create
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_ip = '192.168.1.10'
port = 4982
backlog = 5
socket_address = (host_ip,port)
print('STARTING SERVER AT',socket_address,'...')
server_socket.bind(socket_address)
server_socket.listen(backlog)


def listen_client(addr,client_socket):
    try:
        print('CLIENT {} CONNECTED!'.format(addr))
        if client_socket: # if a client socket exists
            data = b""
            payload_size = struct.calcsize("Q")
            while True:
                while len(data) < payload_size:
                    packet = client_socket.recv(4*1024) # 4K
                    if not packet: break
                    data+=packet
                packed_msg_size = data[:payload_size]
                data = data[payload_size:]
                msg_size = struct.unpack("Q",packed_msg_size)[0]

                while len(data) < msg_size:
                    data += client_socket.recv(4*1024)
                frame_data = data[:msg_size]
                data  = data[msg_size:]
                frame = pickle.loads(frame_data)
                audio.put(frame)
            
            client_socket.close()
    except Exception as e:
        print(f"CLINET {addr} DISCONNECTED")
        pass

while True:
    client_socket,addr = server_socket.accept()
    thread = threading.Thread(target=listen_client, args=(addr,client_socket))
    thread.start()
    print("TOTAL CLIENTS ",threading.activeCount() - 1)
    with sf.SoundFile(filename, mode='x', samplerate=44100,channels=2) as file:
        while True:
            file.write(audio.get())