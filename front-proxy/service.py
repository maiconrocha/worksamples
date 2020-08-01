from flask import Flask
import socket

app = Flask(__name__)

@app.route('/service')
def hello():
    return ('Hello from behind Envoy! hostname: {}\n'.format(socket.gethostname()))
    
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)
