import random

from flask import Flask, render_template, request, redirect, session
import json

app = Flask(__name__)
app.secret_key = "secret123"  # nötig für session


def load_questions():
    with open("questions.json", "r", encoding="utf-8") as file:
        return json.load(file)


@app.route("/")
def start():
    questions = load_questions()
    random.shuffle(questions)
    session["questions"] = questions
    session["current_index"] = 0
    session["score"] = 0
    session["wrong_answers"] = []
    return redirect("/question")


@app.route("/question")
def question():
    questions = session.get("questions", [])
    index = session.get("current_index", 0)

    if not questions or index >= len(questions):
        return redirect("/result")

    q = questions[index]
    return render_template("question.html", question=q, index=index, total=len(questions))


@app.route("/answer", methods=["POST"])
def answer():
    questions = session.get("questions", [])
    index = session.get("current_index", 0)

    selected = request.form.get("option")

    if selected is not None and index < len(questions):
        selected = int(selected)
        q = questions[index]

        if selected == q["correct_option"]:
            session["score"] = session.get("score", 0) + 1
        else:
            wrong = session.get("wrong_answers", [])
            wrong.append({
                "question": q["question"],
                "your_answer": q["options"][selected],
                "correct_answer": q["options"][q["correct_option"]]
            })
            session["wrong_answers"] = wrong

    session["current_index"] = index + 1
    return redirect("/question")


@app.route("/result")
def result():
    score = session.get("score", 0)
    questions = session.get("questions", [])
    wrong_answers = session.get("wrong_answers", [])

    return render_template(
        "result.html",
        score=score,
        total=len(questions),
        wrong_answers=wrong_answers
    )


if __name__ == "__main__":
    app.run(debug=True)
