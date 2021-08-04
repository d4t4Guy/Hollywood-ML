from flask import Flask, render_template, request
#import sklearn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
# from sklearn.externals 
import joblib

# Import model
#with open('static/model/rf.joblib', 'rb') as f:
with open('assets/model/model.joblib', 'rb') as f:
  model=joblib.load(f)  

# lookup table for user selection on genre:
genre_dict ={
"action": [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
"adventure": [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
"animation": [0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
"biography": [0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
"comedy": [0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
"crime": [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
"drama": [0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
"family": [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0],
"fantasy": [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
"history": [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
"horror": [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],
"music": [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0],
"musical": [0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
"mystery": [0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],
"romance": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0],
"scifi": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0],
"sport": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
"thriller": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0],
"war": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
"western": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1]
}


# lookup table for user selection on language:
language_dict= {
"arabic": [1,0,0,0,0,0,0,0,0,0,0],
"chinese": [0,1,0,0,0,0,0,0,0,0,0],
"english": [0,0,1,0,0,0,0,0,0,0,0],
"french": [0,0,0,1,0,0,0,0,0,0,0],
"german": [0,0,0,0,1,0,0,0,0,0,0],
"italian": [0,0,0,0,0,1,0,0,0,0,0],
"japanese": [0,0,0,0,0,0,1,0,0,0,0],
"korean": [0,0,0,0,0,0,0,1,0,0,0],
"other": [0,0,0,0,0,0,0,0,1,0,0],
"russian": [0,0,0,0,0,0,0,0,0,1,0],
"spanish": [0,0,0,0,0,0,0,0,0,0,1]
}


# Create an instance of our Flask app.
app = Flask(__name__)

# Set route
@app.route('/', methods=["GET"])
def index():
  return render_template("index.html")


@app.route('/predict', methods=["GET", "POST"])
def predict():
  
  if request.method == 'POST':   
     
    numerics = []
    formData = request.form

    for each_field in formData:
      if each_field=='genre':
        genre_key=formData[each_field]
        genre_value=genre_dict[genre_key]
        for i in genre_value:
          numerics.append(i)
      elif each_field=='language':
        language_key=formData[each_field]
        language_value = language_dict[language_key]
        for i in language_value:
          numerics.append(i)
      else:
        each_field = int(formData[each_field])
        numerics.append(each_field)
    numerics.append(0) # need to check model n_features -??
    
    #print(numerics)       
    
    #prediction=model.predict([[duration, budget, month, genre_value, language_value]])    

    prediction=model.predict([numerics])    
    
    output=prediction[0]
    
    return render_template('index.html', prediction_text="The predicted gross income is ${}".format(output))

  else:
    return render_template('index.html')

  
if __name__ == "__main__":  
  app.run()