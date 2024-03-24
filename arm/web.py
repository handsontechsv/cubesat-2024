from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
from urllib.parse import urlparse
import raspArmS
import time
import json
import cgi

currPos = [0, 0, 0, 0]

""" because i am an idiot here is the information on how to use the api
basically: Servo_A, Servo_B, Servo_C all move singular servos
curl --data "oxxoxxoxx" http://192.168.1.40:8080/multiple
where xx = number, o = 0 or -

"""

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    
    def send_Status_200(self,content):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(bytes(content, "utf-8"))
        pass
        
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    
    def get_Status(self,content):
        self.send_Status_200(content)
        pass
    
    def post_Reset(self):
        self.send_Status_200("reset")
        ras = raspArmS.RaspArmS()
        ras.servoAngInput([0, 0, 0, 0])
        pass

    def get_ServoA(self):
        self.send_Status_200("servoA")
        self.wfile.write(bytes(str(currPos[0]), "utf-8"))
        pass

    def get_ServoB(self):
        self.send_Status_200("servoB")
        self.wfile.write(bytes(str(currPos[1]), "utf-8"))
        pass
        
    def get_ServoC(self):
        self.send_Status_200("servoC")
        self.wfile.write(bytes(str(currPos[2]), "utf-8"))
        pass
        
    def get_BottomFlat(self):
        
        pass
    
    def post_ServoA(self, angle):
        ras = raspArmS.RaspArmS()
        currPos[0] = angle
        ras.servoAngInput(currPos)
        pass

    def post_ServoB(self, angle):
        ras = raspArmS.RaspArmS()
        currPos[1] = angle/2
        ras.servoAngInput(currPos)
        pass
    
    def post_ServoC(self, angle):
        ras = raspArmS.RaspArmS()
        currPos[2] = angle
        ras.servoAngInput(currPos)
        pass
    
    def post_Multiple(self, body):
        ang1 = int(body[0:3])
        ang2 = int(body[3:6])
        ang3 = int(body[6:9])
        ras = raspArmS.RaspArmS()
        currPos[0] = ang1
        currPos[1] = ang2
        currPos[2] = ang3
        ras.servoAngInput(currPos)
    def post_BottomFlat(self):
        pass
    
    
    def do_default(self):
        self.send_response(400)
        self.end_headers()
        self.wfile.write(bytes("INVALID", "utf-8"))
    
    def do_GET(self):
        parsed = urlparse(self.path)
        query_string = parsed.query
        path_string = parsed.path
        if path_string == "/status":
            self.get_Status(path_string)
        elif path_string == "/Servo_A":
            self.get_ServoA()
        elif path_string == "/Servo_B":
            self.get_ServoB()
        elif path_string == "/Servo_C":
            self.get_ServoC()
        elif path_string == "/BottomFlat":
            self.get_BottomFlat()
        else:
            self.do_default()
        
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        parsed = urlparse(self.path)
        query_string = parsed.query
        path_string = parsed.path
        if path_string == "/Servo_A":
            self.post_ServoA(int(body))
        elif path_string == "/Servo_B":
            self.post_ServoB(int(body))
        elif path_string == "/Servo_C":
            self.post_ServoC(int(body))
        elif path_string == "/BottomFlat":
            self.post_BottomFlat(body)
        elif path_string == "/reset":
            self.post_Reset()
        elif path_string == "/multiple":
            self.post_Multiple(body)
        else:
            self.do_default()
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(b'This is POST request. ')
        response.write(b'Recieved: ')
        response.write(body)
        self.wfile.write(response.getvalue())
        
httpd = HTTPServer(('0.0.0.0', 8080), SimpleHTTPRequestHandler)
httpd.serve_forever()
