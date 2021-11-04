#step1
from flask import Flask, jsonify


#############################
# Flask Setup
#############################
#step2
app = Flask(__name__)





# step 3 Run code from command line
if __name__ == '__main__':
    app.run(debug=True)