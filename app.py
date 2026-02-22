from flask import Flask, render_template, request
from model import predict_disease

app = Flask(__name__)

def get_age_group(age):
    age = int(age)
    if age <= 12:
        return "Child"
    elif age <= 30:
        return "Young Adult"
    elif age <= 60:
        return "Adult"
    else:
        return "Senior"

@app.route("/", methods=["GET", "POST"])
def index():
    output = None
    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        gender = request.form["gender"]
        symptoms = request.form["symptoms"]
        age_group = get_age_group(age)
        output = predict_disease(age, gender, age_group, symptoms)

    return render_template("index.html", output=output)

if __name__ == "__main__":
    app.run(debug=True)
