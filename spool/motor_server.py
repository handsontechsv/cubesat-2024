import RPi.GPIO as GPIO
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
from io import BytesIO

host_name = '192.168.1.55' # IP Address of Raspberry Pi
host_port = 8000

direction = "forward"
step_count = 200


class MyServer(BaseHTTPRequestHandler):

    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def _redirect(self, path):
        self.send_response(303)
        self.send_header('Content-type', 'text/html')
        self.send_header('Location', path)
        self.end_headers()

    def do_GET(self):
        html = '''
           <html>
           <body 
            style="width:960px; margin: 20px auto;">
           <h1>Welcome to my Raspberry Pi</h1>
           <form action="/" method="POST">
               Move Direction: 
               <input type="submit" name="submit" value="Forward">
               <input type="submit" name="submit" value="Backward"><br>
               <input type="submit" name="submit" value="Move">
               <input type="submit" name="submit" value="Stop">
            
           </form>
           </body>
           </html>
        '''
        self.do_HEAD()
        self.wfile.write(html.format().encode("utf-8"))
        
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
 #       body = self.rfile.read(content_length)
        post_data = self.rfile.read(content_length).decode("utf-8")

        s = post_data.replace('%40','')
        l = s.split('&')
        print(l)
 #       post_data = post_data.split("=")[1]
        direction = l[0].split("=")[1]
        step_count = eval(l[1].split("=")[1])
 
        print("direction is {}".format(direction))
        print("step_count is {}".format(step_count))
        
#        return

        self.move(direction,step_count)
        self._redirect('/')  # Redirect back to the root url
        
        
    def move(self, direction,step_count):
            out1 = 17
            out2 = 18
            out3 = 27
            out4 = 22

            step_sleep = 0.007

    #        step_count = 600
   
            GPIO.setmode( GPIO.BCM )
            GPIO.setup( out1, GPIO.OUT )
            GPIO.setup( out2, GPIO.OUT )
            GPIO.setup( out3, GPIO.OUT )
            GPIO.setup( out4, GPIO.OUT )

            # initializing
            GPIO.output( out1, GPIO.LOW )
            GPIO.output( out2, GPIO.LOW )
            GPIO.output( out3, GPIO.LOW )
            GPIO.output( out4, GPIO.LOW )


            def cleanup():
                GPIO.output( out1, GPIO.LOW )
                GPIO.output( out2, GPIO.LOW )
                GPIO.output( out3, GPIO.LOW )
                GPIO.output( out4, GPIO.LOW )
                GPIO.cleanup()



            # the meat

            try:
                if direction == "forward":
                    i = 0
                    for i in range(step_count):
 
                        if i%4==0:
                                GPIO.output( out4, GPIO.HIGH )
                                GPIO.output( out3, GPIO.LOW )
                                GPIO.output( out2, GPIO.LOW )
                                GPIO.output( out1, GPIO.LOW )
                        elif i%4==1:
                                GPIO.output( out4, GPIO.LOW )
                                GPIO.output( out3, GPIO.LOW )
                                GPIO.output( out2, GPIO.HIGH )
                                GPIO.output( out1, GPIO.LOW )
                        elif i%4==2:
                                GPIO.output( out4, GPIO.LOW )
                                GPIO.output( out3, GPIO.HIGH )
                                GPIO.output( out2, GPIO.LOW )
                                GPIO.output( out1, GPIO.LOW )
                        elif i%4==3:
                                GPIO.output( out4, GPIO.LOW )
                                GPIO.output( out3, GPIO.LOW )
                                GPIO.output( out2, GPIO.LOW )
                                GPIO.output( out1, GPIO.HIGH )

                        time.sleep( step_sleep )
 
                elif direction == "backward":
                    i = 0
                    for i in range(step_count):
 
                        if i%4==0:
                                GPIO.output( out4, GPIO.HIGH )
                                GPIO.output( out3, GPIO.LOW )
                                GPIO.output( out2, GPIO.LOW )
                                GPIO.output( out1, GPIO.LOW )
                        elif i%4==1:
                                GPIO.output( out4, GPIO.LOW )
                                GPIO.output( out3, GPIO.LOW )
                                GPIO.output( out2, GPIO.LOW )
                                GPIO.output( out1, GPIO.HIGH )
                        elif i%4==2:
                                GPIO.output( out4, GPIO.LOW )
                                GPIO.output( out3, GPIO.HIGH )
                                GPIO.output( out2, GPIO.LOW )
                                GPIO.output( out1, GPIO.LOW )
                        elif i%4==3:
                                GPIO.output( out4, GPIO.LOW )
                                GPIO.output( out3, GPIO.LOW )
                                GPIO.output( out2, GPIO.HIGH )
                                GPIO.output( out1, GPIO.LOW )

                        time.sleep( step_sleep ) 
  

            except KeyboardInterrupt:
                cleanup()
                exit( 1 )
            
            cleanup()
            Status = "Stopped"
        
# # # # # Main # # # # #

if __name__ == '__main__':
    http_server = HTTPServer((host_name, host_port), MyServer)
    print("Server Starts - %s:%s" % (host_name, host_port))

    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()