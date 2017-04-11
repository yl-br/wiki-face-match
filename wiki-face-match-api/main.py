import cv2
import imghdr
import pandas
import tempfile
import numpy as np
from flask import Flask,request,jsonify,Response
from flask_cors import CORS, cross_origin
from image_parser import ImageParser
from representation_store import RepresentationStore
from image_matcher import ImageMatcher

import os, sys
import json

project_path = os.path.dirname(os.path.realpath(__file__))


with open(os.path.join(project_path,'config.json')) as config_file:
    config = json.load(config_file)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = int(config['max_image_upload_size_mb']) * 1024 * 1024 # MB
CORS(app)

wiki_meta_df = pandas.read_csv(os.path.join(project_path,config['wiki_meta_csv_path']), index_col=0)
imdb_meta_df = pandas.read_csv(os.path.join(project_path,config['imdb_meta_csv_path']), index_col=0)

image_parser = ImageParser(config['open_face_models_dir_path'])
image_parser.init()

representation_store = RepresentationStore(image_parser)
representation_store.load_representations(os.path.join(project_path,config['representations_file_path']))

image_matcher = ImageMatcher(representation_store)

representation_count = len(representation_store.get_representations())


@app.route('/randomImages', methods=['GET'])
def get_random_images():
    out_paths = [row['full_path'] for index, row in imdb_meta_df.sample(12).iterrows()]
    return json.dumps(out_paths)


@app.route('/findMatches', methods=['POST'])
def upload_image():
    image_file = request.files['file']
    if image_file is None:
        message = 'No image file found.'
        return (jsonify({'message':message}),400)
    file_ext = imghdr.what(image_file)

    image_array = np.asarray(bytearray(image_file.read()), dtype="uint8")
    img = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    bounding_box = image_parser.get_face_bounding_box(rgb_img)
    if bounding_box is None:
        message = 'Failed detecting a face in image.'
        return (jsonify({'message': message}), 400)

    try:
        image_representation = image_parser.get_face_representation(rgb_img, bounding_box)
        image_id_distances, max_distance = image_matcher.get_top_faces_matches(image_representation, top_limit=3)
    except Exception as e:
        message = 'An error accord during image processing.'
        return (jsonify({'message': message}), 500)


    out_res_data = {'result':[],'scanned_image_count':representation_count,'boxed_image':None}
    for image_id, distance in image_id_distances:
        matched_row = wiki_meta_df.ix[[image_id]]
        image_path = matched_row['full_path'].values[0]
        name = matched_row['name'].values[0]
        score = 1 - distance/max_distance
        image_res = {'image_path':image_path, 'distance':distance, 'name':name, 'score':score}
        out_res_data['result'].append(image_res)

    with tempfile.NamedTemporaryFile(suffix='.{}'.format(file_ext)) as temp_file:
        cv2.rectangle(img, (bounding_box.left(), bounding_box.top()), (bounding_box.right(), bounding_box.bottom()), (255, 0, 0), 10)
        cv2.imwrite(temp_file.name, img)
        out_res_data['boxed_image'] = temp_file.read().encode('base64')

    return json.dumps(out_res_data)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)