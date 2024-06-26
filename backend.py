from flask import Flask, request, render_template, jsonify
import random
import json
import time 
import socket
from math import sqrt
import asyncio


# Create a UDP socket i website1
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Server address and port
address = ('127.0.0.1', 8148)
try:
    client_socket.bind(('127.0.0.1', 8148))
except:
    print("wtf")

client_socket.settimeout(1)

client_socket2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Server address and port
address = ('127.0.0.1', 8011)
try:
    client_socket2.bind(('127.0.0.1', 8011))
except:
    print("wtf")

client_socket2.settimeout(20)

game_start = 0

data_file = 'data.json'

def load_data():
    try:
        with open(data_file, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"numbers": [], "tilt_angles": []}

def save_data(data):
    with open(data_file, 'w') as file:
        json.dump(data, file) 

def flush_socket(sock):
    try:
        while True:
            data = sock.recv(1024)
            if not data:
                break
    except BlockingIOError:
        pass

def website():
    global client_socket
    print("started backend")
    app = Flask(__name__)
    @app.route('/')
    def index():
        return render_template('forside.html')
    
    @app.route('/forside.html')
    def forside():
        return render_template('forside.html')
    
    @app.route('/glass.html')
    def glass_view():
        return render_template('glass.html')

    @app.route('/graf.html')
    def graf_view():
        return render_template('graf.html')

    @app.route('/pasient.html')
    def pasient():
        return render_template('pasient.html')
    
    @app.route('/behandler.html')
    def behandler_view():
        return render_template('behandler.html')

    @app.route('/grafBehandler.html')
    def graf_behandler(): 
        return render_template('grafBehandler.html')
    
    @app.route('/3dglass.html')
    def glass_3d():
        return render_template('3dglass.html')

    @app.route('/api/hello', methods=['POST'])
    def hello():
        print('Hello, World!')
        return '', 200

    @app.route('/api/name', methods=['POST'])
    def handle_text():
        text_data = request.form['text']  # Assuming the data is sent as form data
        print(text_data)  # Print the received text to the console
        return 'Text received', 200  # Respond to the client that the text was received

    @app.route('/api/newbutton', methods=['GET'])
    def init():
    #    try:
        #flush_socket(client_socket)
        try:
            a, adress = client_socket.recvfrom(1024)
            a = a.decode("utf-8")
            a = a.split(' ')
            print(a)
            #tilt = str(sqrt((float((a[0]))/100)**2+(float((a[2]))/100)**2))
            graph = a[8]
            #tilt_angle = tilt
            if int(a[7]) != 1:
                print("returning 0 to numbers")
                return jsonify({
                    "tiltAngleX": float(a[0])/100,
                    "tiltAngleY": float(a[1])/100,
                    "tiltAngleZ": float(a[2])/100,
                    "numbers": 0
                })
            else:
                print("returning graph to numbers")
                return jsonify({
                    "tiltAngleX": float(a[0])/100,
                    "tiltAngleY": float(a[1])/100,
                    "tiltAngleZ": float(a[2])/100,
                    "numbers": float(graph)
                })
        except Exception as errormessage:
            print(errormessage) 
        
    '''
        except Exception as errormessage:
            print(errormessage)
            print("returning nothing")
            return jsonify({
                    "tiltAngleX": 0,
                    "tiltAngleY": 0,
                    "tiltAngleZ": 0,
                    "numbers": 0
                })
        
    '''
    #        print("Harm done") 
    #        return ""

    @app.route('/api/game_start', methods=['POST'])
    def game_start():
        data = request.json
        print("data json: " + str(data))
        address = ('127.0.0.1', 8004)
        Reading = "1 pasient1"
        Reading = str.encode(Reading) #codek register encoding
        for i in range(1):
            print("sending")
            client_socket2.sendto(Reading, address) 
            time.sleep(1)
        return "Button clicked"

    @app.route('/api/newbutton2', methods=['GET'])
    def data():
        numbers = [random.randint(0,100) for _ in range(10)]
        tilt_angles = [random.randint(-100,100) for _ in range(10)]
        time = [random.randint(0,100) for _ in range(10)]
        acceleration = [random.randint(0,100) for _ in range(10)]
        return jsonify({
            "numbers": numbers,
            "tilt_angles": tilt_angles,
            "time": time,
            "acceleration": acceleration
        })

    if __name__ == '__main__':
        app.run(debug=False, host="10.42.0.1", port="5000")
        #app.run(debug=True, host=address[0], port=address[1])

    
'''
def website2(address):
    app = Flask(__name__)

    # Create a UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    @app.route('/')
    def index():
        return render_template('forside.html')

    @app.route('/glass.html')
    def glass_view():
        return render_template('glass.html')

    @app.route('/graf.html')
    def graf_view():
        return render_template('graf.html')

    @app.route('/pasient.html')
    def pasient():
        return render_template('pasient.html')

    @app.route('/api/hello', methods=['POST'])
    def hello():
        print('Hello, World!')
        return '', 200

    @app.route('/api/name', methods=['POST'])
    def handle_text():
        text_data = request.form['text']  # Assuming the data is sent as form data
        print(text_data)  # Print the received text to the console
        return 'Text received', 200  # Respond to the client that the text was received

    @app.route('/api/newbutton', methods=['GET'])
    def init():
        print(str(client_socket.recvfrom(1024)))
        messagereicived = client_socket.recvfrom(1024)

        a = messagereicived[0]
        a = a.split(' ')
        tilt = sqrt(int(a[0])^2 + int(a[1])^2 + int(a[2])^2)
        graph = sqrt(int(a[3])^2 + int(a[4])^2 + int(a[5])^2)
        tilt_angle = a[2]
        graph_number = a[4] 
        return jsonify({
            "tilt": tilt_angle,
            "number": graph_number
        })


    if __name__ == '__main__':
        app.run(debug=True, host=address[0], port=address[1])

if __name__ == '__main__':
    website2(('127.0.0.1', 8009))

'''
website()
