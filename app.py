import os
from flask import Flask, render_template, session, request, send_file, Response, redirect, url_for, flash
from werkzeug.utils import secure_filename
from flask_session import Session

try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import cv2
import re

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

app.secret_key = "hello there"

nishant = {
    "name": "Nishant Ray",
    "num_absences": 0,
    "id": 0
}

stacey = {
    "name": "Stacey Jaehnig",
    "num_absences": 0,
    "id": 1
}

anoop = {
    "name": "Anoop Bhat",
    "num_absences": 0,
    "id": 2
}

allan = {
    "name": "Allan Zhu",
    "num_absences": 0,
    "id": 3
}

anand = {
    "name": "Anand Menon",
    "num_absences": 0,
    "id": 4
}

anusha = {
    "name": "Anusha Singhai",
    "num_absences": 0,
    "id": 5
}

ashvin = {
    "name": "Ashvin Loghashankar",
    "num_absences": 0,
    "id": 6
}

bhuvana = {
    "name": "Bhuvana Betini",
    "num_absences": 0,
    "id": 7
}

chloe = {
    "name": "Chloe Cui",
    "num_absences": 0,
    "id": 8
}

daniel = {
    "name": "Daniel Chen",
    "num_absences": 0,
    "id": 9
}

dylan = {
    "name": "Dylan Adal",
    "num_absences": 0,
    "id": 10
}

erin = {
    "name": "Erin Kim",
    "num_absences": 0,
    "id": 11
}

garima = {
    "name": "Garima Bansal",
    "num_absences": 0,
    "id": 12
}

hanzhang = {
    "name": "Hanzhang Luo",
    "num_absences": 0,
    "id": 13
}

hanzhang = {
    "name": "Hanzhang Luo",
    "num_absences": 0,
    "id": 13
}

tristan = {
    "name": "Tristan Liu",
    "num_absences": 0,
    "id": 14
}

adrian = {
    "name": "Adrian Liu",
    "num_absences": 0,
    "id": 15
}

manu = {
    "name": "Manu Bhat",
    "num_absences": 0,
    "id": 16
}

michael = {
    "name": "Michael Chian",
    "num_absences": 0,
    "id": 17
}

loden = {
    "name": "Loden Campbell",
    "num_absences": 0,
    "id": 18
}

pranav = {
    "name": "Pranav Harakere",
    "num_absences": 0,
    "id": 19
}

roster = [nishant, stacey, anoop, anand, anusha, ashvin, bhuvana, chloe, daniel, dylan, erin, hanzhang, tristan, adrian, manu, michael, loden, pranav]

# absence1 = {
#     "absentee": tristan,
#     "day": "April 1st, 2020"
# }

# absence2 = {
#     "absentee": adrian,
#     "day": "February 22nd, 2020"
# }

absences = [] # [absence1, absence2]

data = {
    "date": "",
    "presentees": []
}

@app.route("/", methods=["POST", "GET"])
def index():
    global roster, absences, data

    if request.method == "POST":

        target = os.path.join(APP_ROOT, "screenshots/")
        print(target)

        if not os.path.isdir(target):
            os.mkdir(target)

        for file in request.files.getlist("file"):
            filename = file.filename
            destination = "/".join([target, filename])
            file.save(destination)

        pytesseract.pytesseract.tesseract_cmd = r'C:\\\Program Files\\\Tesseract-OCR\\\tesseract.exe'

        greyImage = cv2.threshold(cv2.cvtColor(cv2.imread('screenshots/Test.png'), cv2.COLOR_BGR2GRAY), 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        text = pytesseract.image_to_string(greyImage)
        nameList = list(filter(("").__ne__, text.split("\n")))
        for x in range(0, len(nameList)):
            name = " ".join(re.findall("[a-zA-Z]+", nameList[x])).split(" ")
            try:
                nameList[x] = name[0] + " " + name[1]
            except IndexError:
                pass
        
        data = {
            "date": formatDate(request.form["date"]),
            "presentees": nameList
        }

        return redirect(url_for('results'))
    else:
        return render_template("index.html")

@app.route("/results")
def results():
    global roster, absences, data
    
    absentees = []

    formattedAbsentees = ""

    present = False

    for student in roster:
        present = False
        for person in data["presentees"]:
            if ''.join(e for e in person.lower() if e.isalnum()) == ''.join(e for e in student["name"].lower() if e.isalnum()):
                present = True

        if not present:

            student["num_absences"] = student["num_absences"] + 1

            new_absence = {
                "absentee": student,
                "day": data["date"]
            }

            absentees.append(student)
            absences.insert(0, new_absence)
            formattedAbsentees = formattedAbsentees + student["name"] + ", "
    
    if len(absentees) == 2:
        formattedAbsentees = formattedAbsentees[0:formattedAbsentees.find(",")] + " and " + formattedAbsentees[formattedAbsentees.find(",") + 2:len(formattedAbsentees) - 2]
    else:
        formattedAbsentees = formattedAbsentees[0:formattedAbsentees.rindex(",", 0, formattedAbsentees.rindex(",")) + 1] + " and " + formattedAbsentees[formattedAbsentees.rindex(",", 0, formattedAbsentees.rindex(",")) + 2:len(formattedAbsentees) - 2]

    results = {
        "num_present": len(data["presentees"]),
        "num_absent":  len(absentees),
        "absent": absentees,
        "absent_list": formattedAbsentees,
        "day": data["date"]
    }

    return render_template("results.html", results=results)

@app.route("/stats", methods=["POST", "GET"])
def stats():
    global roster, absences

    return render_template("stats.html")

@app.route("/settings", methods=["POST", "GET"])
def settings():
    global roster, absences

    if request.method == "POST":

        if "name" in request.form:

            name = request.form["name"]

            for c in name:
                if str(c) == "_":
                    name = name[0:name.find(c)] + " " + name[name.find(c) + 1:]
                    break

            new_student = {
                "name": name,
                "num_absences": 0,
                "id": len(roster)
            }

            roster.append(new_student)
        elif "az" in request.form:
            roster.sort(key = sortAlphabet)
    else:
        roster.sort(key = sortAbsences, reverse = True)

    return render_template("settings.html")

def sortAlphabet(person):
    return person["name"][ :person["name"].find(' ')]

def sortAbsences(person):
    return person["num_absences"]

@app.route("/delete:<id>")
def delete(id):
    global roster

    for student in roster:
        if student["id"] == int(id):
            roster.remove(student)

    return redirect(url_for("settings"))

def formatDate(date):
    #date = "2020-02-22"

    formatted = ""

    year = date[0:4]
    month = int(date[5:7])
    day = int(date[8:])

    if month == 1:
        formatted = "January"
    elif month == 2:
        formatted = "February"
    elif month == 3:
        formatted = "March"
    elif month == 4:
        formatted = "April"
    elif month == 5:
        formatted = "May"
    elif month == 6:
        formatted = "June"
    elif month == 7:
        formatted = "July"
    elif month == 8:
        formatted = "August"
    elif month == 9:
        formatted = "September"
    elif month == 10:
        formatted = "Octobor"
    elif month == 11:
        formatted = "November"
    elif month == 12:
        formatted = "December"

    formatted = formatted + " " + str(day)

    if day % 10 == 1:
        formatted = formatted + "st, "
    elif day % 10 == 2:
        formatted = formatted + "nd, "
    elif day % 10 == 3:
        formatted = formatted + "rd, "
    else:
        formatted = formatted + "th, "

    formatted = formatted + year

    return formatted

@app.context_processor
def context_processor():

    session.modified = True

    return dict(roster=roster, absences=absences)

if __name__ == "__main__":
    app.run(debug=True)