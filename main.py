from flask import Flask, render_template, request, redirect, session
from users import Users  # Assuming you have a Users class for user authentication
from employees import Employee  # Assuming you have an Employee class for employee operations

app = Flask(__name__)
app.secret_key = "chaka"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check-user', methods=['POST'])
def check_user():
    username = request.form["username"]
    password = request.form["password"]

    result = Users.check_user(username, password)

    if result:
        return redirect('/employee-list')
    else:
        return render_template('index.html')

@app.route('/employee-list')
def employee_list():
    employees = Employee.get_all()

    if "message" not in session:
        session["message"] = ""

    return render_template('employee_list.html', employees=employees, message=session.pop('message'))

@app.route('/add-form')
def add_form():
    return render_template('add_employee.html')

@app.route('/add-employee', methods=["POST"])
def add_employee():
    emp_id = request.form["emp_id"]
    lname = request.form["lname"]
    fname = request.form["fname"]
    mname = request.form["mname"]

    success = Employee.add_employee(emp_id, lname, fname, mname)

    if success:
        session["message"] = "Successfully added"
    else:
        session["message"] = "Failed to add employee"

    return redirect("/employee-list")

@app.route('/update-employee/<int:emp_id>', methods=["GET", "POST"])
def update_employee(emp_id):
    if request.method == "GET":
        employee = Employee.get_by_id(emp_id)
        if employee:
            return render_template('update_employee.html', employee=employee)
        else:
            session["message"] = "Employee not found"
            return redirect("/employee-list")
    elif request.method == "POST":
        lname = request.form["lname"]
        fname = request.form["fname"]
        mname = request.form["mname"]

        success = Employee.update_employee(emp_id, lname, fname, mname)

        if success:
            session["message"] = "Successfully updated"
        else:
            session["message"] = "Failed to update employee"

        return redirect("/employee-list")


@app.route('/delete-employee/<emp_id>')
def delete_employee(emp_id):
    success = Employee.delete_employee(emp_id)

    if success:
        session["message"] = "Successfully deleted"
    else:
        session["message"] = "Failed to delete employee"

    return redirect("/employee-list")

if __name__ == '__main__':
    app.run(debug=True)
