import shutil
from flask import Flask,render_template,request
import os
import cv2
import openai
from datetime import datetime

app = Flask(__name__)

@app.route("/")
@app.route("/home")
@app.route("/Stack-Solver")
def home():
    return render_template("home.html")

@app.route("/Stack-Solver-Answer", methods=["POST","GET"])
def answer():
    if request.method == "POST":
        code = request.form.get("code")

        prompt = "this code have error, find it and write my code again into correct:" + str(code)

        openai.api_key = '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'

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        Chatgpt_answer = response['choices'][0]['message']['content']

        return render_template("answer.html", answer=Chatgpt_answer)
    
@app.route("/Stack-Resizer")
def resizer():
    return render_template("resizer.html")

@app.route("/Stack-Resizer-finish", methods=["POST","GET"])
def resizer_finish():
    if 'img' in request.files:
        image = request.files['img']
        img_name = image.filename

        sizew = int(request.form.get("sizew"))
        sizeh = int(request.form.get("sizeh"))

        if image.filename != '':
            image.save(os.path.join(os.getcwd(), image.filename))
            
            cvimg = cv2.imread(img_name)
            resized_cvimg = cv2.resize(cvimg, (sizew, sizeh))
            resized_cvimg_name =  "stack_resizer_" + str(img_name)
            cv2.imwrite(resized_cvimg_name, resized_cvimg)
            os.remove(img_name)

            current_time = datetime.now().time()
            formatted_time = str(current_time.strftime("%H%M%S"))

            name_the_file =  'VS-' + formatted_time + resized_cvimg_name
            os.rename(resized_cvimg_name, name_the_file)

            shutil.move(name_the_file, './templates')

            return render_template("resizer_finish.html", file_path=str(name_the_file))

    else:
        return render_template("resizer.html")
    
if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0')

