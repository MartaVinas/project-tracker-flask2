"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template, session, redirect, flash
import hackbright

import hackbright

app = Flask(__name__)

app.secret_key = "This is a secret."

@app.route("/student")
def get_student():
    """Show information about a student."""
    student_github = request.args.get('github')
    # import pdb; pdb.set_trace();

    # Use if/else statements to determine if a student is already in
    # the session OR already in the database OR if it is a new student
    if 'new_student' in session and student_github == session['new_student'][2]:
        # If the student is already in the session and the github that is input
        # into the search bar is the same as the one in the session, then we want 
        # to gather the session information, to be displayed in student_info.html
        github = session['new_student'][2]

        first_name, last_name, github = hackbright.get_student_by_github(github)

        project_grades = hackbright.get_grades_by_github(github)
        # print(project_grades)

    elif student_github in db:
        # If the student IS NOT in the session, we will check if they are in the
        # database. If the student is in the database (checked by their github),
        # then we want to gather the info from the database, to be displayed in 
        # student_info.html
    else:
        # If the student is not in the session AND not in the database, we will
        # send user to the /student-add-form page, where a function will add
        # the student to the database
        return redirect("/student-add-form")
    
    # If student is in session or in database, will render the student_info.html
    html = render_template("student_info.html",
                   first=first_name,
                   last=last_name,
                   github=github,
                   projects=project_grades)
    return html


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

