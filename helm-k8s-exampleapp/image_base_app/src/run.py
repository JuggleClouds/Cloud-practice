#!flask/bin/python
from flipflop import WSGIServer
from app import app

if __name__ == '__main__':
    WSGIServer(app).run(host='0.0.0.0', debug=True)

    #app.run(host='0.0.0.0', debug=True)
