import utils.transport
import utils.session
from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)

FILE_NAME = "students.json"


# ------------------ File Handling ------------------
def load_students():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    return []


def save_students(students):
    with open(FILE_NAME, "w") as file:
        json.dump(students, file, indent=4)


def generate_id(students):
    if not students:
        return 1
    return max(s["id"] for s in students) + 1


# ------------------ Routes ------------------

@app.route("/")
def index():
    students = load_students()
    return render_template("index.html", students=students)


@app.route("/add", methods=["POST"])
def add_student():
    students = load_students()

    name = request.form["name"]
    age = request.form["age"]

    student = {
        "id": generate_id(students),
        "name": name,
        "age": age
    }

    students.append(student)
    save_students(students)

    return redirect("/")


@app.route("/delete/<int:id>")
def delete_student(id):
    students = load_students()
    students = [s for s in students if s["id"] != id]
    save_students(students)

    return redirect("/")


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_student(id):
    students = load_students()

    student = next((s for s in students if s["id"] == id), None)

    if not student:
        return "Student not found"

    if request.method == "POST":
        student["name"] = request.form["name"]
        student["age"] = request.form["age"]

        save_students(students)
        return redirect("/")

    return render_template("edit.html", student=student)


# ------------------ Run App ------------------
if __name__ == "__main__":
    app.run(debug=True)