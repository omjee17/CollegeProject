import os
import numpy as np
from flask import Flask, render_template, request, send_from_directory
import pickle


# template_dir = os.path.abspath('/templates/index.html')#


app=Flask(__name__, static_folder='Static')
model=pickle.load(open('model.pkl','rb'))


@app.route("/")
@app.route("/frontPage.html")
def hello():
    return render_template('frontPage.html')

@app.route("/index.html")
def helloSymptoms():
    return render_template('index.html')

@app.route("/sub",methods=['POST'])
def submit():
    if request.method=="POST": 

        sym1=request.form.get("symptom1")
        sym2=request.form.get("symptom2")
        sym3=request.form.get("symptom3")
        sym4=request.form.get("symptom4")
        sym5=request.form.get("symptom5")
        sym6=request.form.get("symptom6")
        # print(sym1,sym2,sym3,sym4,sym5,sym6)

        first_symptom=int(sym1[0:2])
        second_symptom=int(sym2[0:2])
        third_symptom=int(sym3[0:2])
        fourth_symptom=int(sym4[0:2])
        fivth_symptom=int(sym5[0:2])
        sixth_symptom=int(sym6[0:2])

        li=[0]*70

        if first_symptom!=0:
            li[first_symptom-1]=1
        if second_symptom!=0:
            li[second_symptom-1]=1
        if third_symptom!=0:    
            li[third_symptom-1]=1
        if fourth_symptom!=0:
            li[fourth_symptom-1]=1
        if fivth_symptom!=0:
            li[fivth_symptom-1]=1
        if sixth_symptom!=0:
            li[sixth_symptom-1]=1
       

        final_features=[np.array(li)]
        output=model.predict(final_features)

    # lists=output.tolist()
    # json_str=json.dumps(lists)
    # return json_str

    
    return render_template("submit.html",s=output)

