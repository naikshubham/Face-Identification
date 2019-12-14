from flask import Flask, request, Response
import jsonpickle
import numpy as np 
import cv2 
from PIL import Image

# initialize flask app
app = Flask(__name__)

# route http posts to this method
@app.route('/api/test', methods=['POST'])
def test():
    f = request.files['file']
    f.save(f.filename)

    # print('nparr->', nparr)
    # decode image
    img = cv2.imread(f.filename, cv2.IMREAD_COLOR)
    # img = Image.fromarray(nparr)

    # build a response dict to send back to client
    response = {'message':'image received. size={}x{}'.format(img.shape[1], img.shape[0])}

    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)

    return Response(response=response_pickled, status=200, mimetype='application/json')

# start flask app
app.run(host="127.0.0.1", port=8080, debug=True)