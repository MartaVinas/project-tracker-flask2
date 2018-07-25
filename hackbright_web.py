"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template, session, redirect, flash
import hackbright

import hackbright

app = Flask(__name__)

app.secret_key = "This is a secret."

@app.route("/student")
def get_student():
    """Show information about a student."""

    # import pdb; pdb.set_trace();
    if 'new_student' in session:
        github = session['new_student'][2]

        first_name, last_name, github = hackbright.get_student_by_github(github)

        html = render_template("student_info.html",
                       first=first_name,
                       last=last_name,
                       github=github)
        return html
    else:
        return redirect("/student-add-form")


@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")


@app.route("/student-add-form")
def student_add_form():
    """Show form for adding a student."""

    return render_template("add_student.html")


@app.route("/student-add", methods=['POST'])
def student_add():
    """Add a student."""
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    github = request.form.get('github')

    hackbright.make_new_student(first_name,last_name,github)

    html = render_template("show_added_student.html",
                            first_name=first_name,
                            last_name=last_name,
                            github=github)

    session['new_student'] = (first_name, last_name, github)
    # flash("")

    return html



if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)

