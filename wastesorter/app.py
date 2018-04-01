from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from watson_developer_cloud import VisualRecognitionV3
from flask_uploads import UploadSet, configure_uploads, IMAGES
import json
import os


vr = VisualRecognitionV3(
    "2016-05-20",
    api_key="fa0da0f5958dfe0b4cfd40c677757648a6fd3e52")

    
classifier_id = "WasterSorter_356924497"

app = Flask (__name__) #creates the application instance

photos = UploadSet('photos', IMAGES) #gets images variable

app.config.from_object(__name__) #load configuraiton fom the file
app.config['UPLOADED_PHOTOS_DEST'] = 'static/img' #load config of immages 
configure_uploads(app, photos)


app.config.update(dict(
    SECRET_KEY='development key',
    PHOTO_DB="static/image"
))

#need to do following in command line
#pip install FLask-Uploads to get python dictionary

app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
configure_uploads(app, photos)

#pulls the layout 
@app.route('/')
def welcome(): 
    return render_template('layout.html')

#this function is for the uploads
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        return filename
    return render_template('layout.html') #change this to the right url 


@app.route('/classify', methods=['GET', 'POST'])
def classify():
    with open('static/img/test.jpg', 'rb') as images_file:
        classes = vr.classify(images_file, parameters=json.dumps({
                'classifier_ids': [classifier_id],
                'threshold': 0
                }))
        print(json.dumps(classes, indent=2))

        #code here to display and hold scores in a list
        #this code should store the values in a list? 
        #this is nathan li's code 
    results = classes['images'][0]['classifiers'][0]['classes']
    top_3 = []
    max_score = {"class":"","score":0}
    max_index=0
    while len(top_3) <2:
        count = 0
        for i in results:
            if i["score"] > max_score["score"]:
                max_score = i
                max_index = count
            count += 1
        top_3.append(max_score)
        max_score = {"class":"","score":0}
        del results[max_index]
    return render_template('layout.html', data=top_3)
    #this is the end of nathan's code 

#runs locally - taken from welcome.py 
port = os.getenv('PORT', '5000')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(port), debug=True)

