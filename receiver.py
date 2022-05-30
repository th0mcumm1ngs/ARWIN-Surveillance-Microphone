from flask import Flask
import waitress

app = Flask(__name__)

@app.route("/")
def main():
    pass

if __name__ == "__main__":
    waitress.serve(app = app, host='192.168.1.159', port=8080)