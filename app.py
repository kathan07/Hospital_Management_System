from flask import Flask, render_template, request,redirect,flash
from flask_sqlalchemy import SQLAlchemy
from datetime import date,datetime

# Connecting database wuth flask app
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///fsql.db"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# db = SQLAlchemy(app)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:kathant@localhost:5432/flasksql'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'secret string'

db = SQLAlchemy(app)


# Creating of tables
class patient(db.Model):
    pat_id = db.Column(db.Integer, primary_key=True)
    pat_first_name = db.Column(db.String(20),nullable = False)
    pat_last_name = db.Column(db.String(20), nullable = False)
    pat_insurance_no = db.Column(db.String(30), nullable = False)
    pat_ph_no = db.Column(db.String(20), nullable = False)
    pat_date = db.Column(db.Date, default = date.today())
    pat_address = db.Column(db.String(40), nullable = False)

    def __repr__(self) -> str:
        return f"{self.pat_id} - {self.pat_first_name} - {self.pat_last_name} - {self.pat_insurance_no} - {self.pat_ph_no} - {self.pat_date} - {self.pat_address}"


class doctor(db.Model):
    doc_id = db.Column(db.Integer, primary_key=True)
    doc_first_name = db.Column(db.String(20),nullable = False)
    doc_last_name = db.Column(db.String(20), nullable = False)
    doc_ph_no = db.Column(db.String(20), nullable = False)
    doc_date = db.Column(db.Date, default = date.today())
    doc_address = db.Column(db.String(40), nullable = False)

    def __repr__(self) -> str:
        return f"{self.doc_id} - {self.doc_first_name} - {self.doc_last_name} - {self.doc_ph_no} - {self.doc_date} - {self.doc_address}"


class nurse(db.Model):
    nur_id = db.Column(db.Integer, primary_key=True)
    nur_first_name = db.Column(db.String(20),nullable = False)
    nur_last_name = db.Column(db.String(20), nullable = False)
    nur_ph_no = db.Column(db.String(20), nullable = False)
    nur_date = db.Column(db.Date, default = date.today())
    nur_address = db.Column(db.String(40), nullable = False)

    def __repr__(self) -> str:
        return f"{self.nur_id} - {self.nur_first_name} - {self.nur_last_name} - {self.nur_ph_no} - {self.nur_date} - {self.nur_address}"


class appointment(db.Model):
    app_id = db.Column(db.Integer, primary_key = True)
    pat_id = db.Column(db.Integer, db.ForeignKey('patient.pat_id'))
    doc_id = db.Column(db.Integer, db.ForeignKey('doctor.doc_id'))
    appointment_date = db.Column(db.Date,nullable = False)
    
    def __repr__(self) -> str:
        return f"{self.app_id} - {self.pat_id} - {self.doc_id} - {self.appointment_date}"



class room(db.Model):
    room_no = db.Column(db.Integer, primary_key = True)
    room_type = db.Column(db.String(20), nullable = False)
    available = db.Column(db.Integer, nullable = False)

    def __repr__(self) -> str:
        return f"{self.room_no} - {self.room_type} - {self.available}"



class medication(db.Model):
    code = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20), nullable = False)
    brand = db.Column(db.String(20), nullable = False)
    description = db.Column(db.String(20))
    
    def __repr__(self) -> str:
        return f"{self.code} - {self.name} - {self.brand} - {self.description}"


class department(db.Model):
    department_id = db.Column(db.Integer, primary_key = True)
    name =  db.Column(db.String(20), nullable = False)
    head_id = db.Column(db.Integer, db.ForeignKey('doctor.doc_id'), nullable = False)

    def __repr__(self) -> str:
        return f"{self.department_id} - {self.name} - {self.head_id}"



class procedure(db.Model):
    code = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20), nullable = False)
    cost = db.Column(db.Integer, nullable = False)
    
    def __repr__(self) -> str:
        return f"{self.code} - {self.name} - {self.cost}"


class undergoes(db.Model):
    under_id = db.Column(db.Integer, primary_key = True)
    pat_id = db.Column(db.Integer, db.ForeignKey('patient.pat_id'))
    proc_code = db.Column(db.Integer,db.ForeignKey('procedure.code'))
    u_date =  db.Column(db.Date)
    doc_id = db.Column(db.Integer,db.ForeignKey('doctor.doc_id'))
    nur_id = db.Column(db.Integer,db.ForeignKey('nurse.nur_id'))
    room_no = db.Column(db.Integer,db.ForeignKey('room.room_no'))

    def __repr__(self) -> str:
        return f"{self.under_id} - {self.pat_id} - {self.proc_code} - {self.u_date} - {self.doc_id} - {self.nur_id} - {self.room_no}"


class prescribes(db.Model):
    pre_id = db.Column(db.Integer,primary_key=True)
    doc_id = db.Column(db.Integer,db.ForeignKey('doctor.doc_id'))
    pat_id = db.Column(db.Integer, db.ForeignKey('patient.pat_id'))
    med_code = db.Column(db.Integer,db.ForeignKey('medication.code'))
    p_date =  db.Column(db.Date, nullable = False)
    app_id = db.Column(db.Integer,db.ForeignKey('appointment.app_id'))
    dose = db.Column(db.Integer,nullable = False)


    def __repr__(self) -> str:
        return f"{self.pre_id} - {self.doc_id} - {self.pat_id} - {self.med_code} - {self.p_date} - {self.app_id} - {self.dose}"




@app.route("/")
def hello_world():
    return render_template('index.html')


# adding the data to the tables
@app.route("/patient", methods=['GET', 'POST'])
def addpatient():
    if request.method == 'POST':
        pat_id = request.form['pat_id']
        pat_first_name = request.form['pat_first_name']
        pat_last_name = request.form['pat_last_name']
        pat_insurance_no = request.form['pat_insurance_no']
        pat_ph_no = request.form['pat_ph_no']
        pat_date = request.form['pat_date']
        pat_address = request.form['pat_address']
        Patient = patient(pat_id = pat_id, pat_first_name = pat_first_name, pat_last_name = pat_last_name, pat_insurance_no = pat_insurance_no,pat_ph_no = pat_ph_no,pat_date =  pat_date,pat_address =  pat_address)
        db.session.add(Patient)
        db.session.commit()

    allpatient = patient.query.all()
    return render_template('patient.html', allpatient=allpatient)


@app.route("/doctor", methods=['GET', 'POST'])
def adddoctor():
    if request.method == 'POST':
        doc_id = request.form['doc_id']
        doc_first_name = request.form['doc_first_name']
        doc_last_name = request.form['doc_last_name']
        doc_ph_no = request.form['doc_ph_no']
        doc_date = request.form['doc_date']
        doc_address = request.form['doc_address']
        Doctor = doctor(doc_id = doc_id, doc_first_name = doc_first_name, doc_last_name = doc_last_name, doc_ph_no = doc_ph_no, doc_date = doc_date,doc_address =  doc_address)
        db.session.add(Doctor)
        db.session.commit()

    alldoctor = doctor.query.all()
    return render_template('doctor.html', alldoctor=alldoctor)


@app.route("/nurse", methods=['GET', 'POST'])
def addnurse():
    if request.method == 'POST':
        nur_id = request.form['nur_id']
        nur_first_name = request.form['nur_first_name']
        nur_last_name = request.form['nur_last_name']
        nur_ph_no = request.form['nur_ph_no']
        nur_date = request.form['nur_date']
        nur_address = request.form['nur_address']
        Nurse = nurse(nur_id = nur_id, nur_first_name  = nur_first_name, nur_last_name = nur_last_name,nur_ph_no  = nur_ph_no, nur_date = nur_date, nur_address = nur_address)
        db.session.add(Nurse)
        db.session.commit()

    allnurse = nurse.query.all()
    return render_template('nurse.html', allnurse=allnurse)


@app.route("/appointment", methods=['GET', 'POST'])
def addappoitment():
    if request.method == 'POST':
        app_id = request.form['app_id']
        pat_id = request.form['pat_id']
        doc_id = request.form['doc_id']
        appointment_date = request.form['appointment_date']
        Appointment = appointment(app_id=app_id,pat_id = pat_id, doc_id=doc_id, appointment_date=appointment_date)
        db.session.add(Appointment)
        db.session.commit()

    allappointment = appointment.query.all()
    return render_template('appointment.html', allappointment=allappointment)


@app.route("/room", methods=['GET', 'POST'])
def addroom():
    if request.method == 'POST':
        room_no =  request.form['room_no']
        room_type = request.form['room_type']
        available = request.form['available']
        Room = room(room_no = room_no, room_type = room_type, available = available)
        db.session.add(Room)
        db.session.commit()

    allroom = room.query.all()
    return render_template('room.html', allroom=allroom)


@app.route("/medication", methods=['GET', 'POST'])
def addmedication():
    if request.method == 'POST':
        code = request.form['code']
        name = request.form['name']
        brand = request.form['brand']
        description = request.form['description']

        Medication = medication(code=code, name=name, brand=brand, description=description)
        db.session.add(Medication)
        db.session.commit()

    allmedication = medication.query.all()
    return render_template('medication.html', allmedication=allmedication)


@app.route("/department", methods=['GET', 'POST'])
def adddepartment():
    if request.method == 'POST':
        department_id = request.form['department_id']
        name = request.form['name']
        head_id = request.form['head_id']
        Department = department(department_id = department_id, name = name, head_id = head_id)
        db.session.add(Department)
        db.session.commit()

    alldepartment = department.query.all()
    return render_template('department.html', alldepartment=alldepartment)


@app.route("/procedure", methods=['GET', 'POST'])
def addprocedure():
    if request.method == 'POST':
        code =  request.form['code']
        name = request.form['name']
        cost = request.form['cost']
        Procedure = procedure(code=code, name=name, cost=cost)
        db.session.add(Procedure)
        db.session.commit()

    allprocedure = procedure.query.all()
    return render_template('procedure.html', allprocedure=allprocedure)


@app.route("/undergoes", methods=['GET', 'POST'])
def addundergoes():
    if request.method == 'POST':
        under_id = request.form['under_id']
        pat_id = request.form['pat_id']
        proc_code = request.form['proc_code']
        u_date = request.form['u_date']
        doc_id = request.form['doc_id']
        nur_id = request.form['nur_id']
        room_no = request.form['room_no']
        Undergoes = undergoes(under_id = under_id, pat_id = pat_id, proc_code = proc_code, u_date = u_date, doc_id = doc_id, nur_id = nur_id, room_no = room_no)
        db.session.add(Undergoes)
        db.session.commit()

    allundergoes = undergoes.query.all()
    return render_template('undergoes.html', allundergoes=allundergoes)

@app.route("/prescribes", methods=['GET', 'POST'])
def addprescribes():
    if request.method == 'POST':
        pre_id = request.form['pre_id']
        doc_id = request.form['doc_id']
        pat_id = request.form['pat_id']
        med_code = request.form['med_code']
        p_date = request.form['p_date']
        app_id = request.form['app_id']
        dose = request.form['dose']
        Prescribes = prescribes(pre_id = pre_id, doc_id = doc_id , pat_id = pat_id , med_code = med_code, p_date = p_date,app_id = app_id, dose = dose)
        db.session.add(Prescribes)
        db.session.commit()

    allprescribes = prescribes.query.all()
    return render_template('prescribes.html', allprescribes=allprescribes)








# Updates all the tables

@app.route('/updatepatient/<int:pat_id>', methods=['GET', 'POST'])
def updatepatient(pat_id):
    if request.method == 'POST':
        pat_first_name = request.form['pat_first_name']
        pat_last_name = request.form['pat_last_name']
        pat_insurance_no = request.form['pat_insurance_no']
        pat_ph_no = request.form['pat_ph_no']
        pat_date = request.form['pat_date']
        pat_address = request.form['pat_address']
        Patient = patient.query.filter_by(pat_id=pat_id).first()
        Patient.pat_first_name = pat_first_name
        Patient.pat_last_name = pat_last_name
        Patient.pat_insurance_no = pat_insurance_no
        Patient.pat_ph_no = pat_ph_no
        Patient.pat_date = pat_date
        Patient.pat_address = pat_address
        db.session.add(Patient)
        db.session.commit()
        return redirect("/patient")

    allpatient = patient.query.filter_by(pat_id=pat_id).first()
    values = []
    for i in list(map(str,str(allpatient).split("-"))):
        values.append(i.strip())
    p = {
        "pat_id":values[0],
        "pat_first_name":values[1],
        "pat_last_name":values[2],
        "pat_insurance_no":values[3],
        "pat_ph_no":values[4],
        "pat_date":datetime.strptime(values[7] + '-' + values[6] + '-' + values[5],'%d-%m-%Y').date(),
        "pat_address":values[8]
    }
    return render_template('updatepatient.html', p=p)



@app.route('/updatedoctor/<int:doc_id>', methods=['GET', 'POST'])
def updatedoctor(doc_id):
    if request.method == 'POST':
        doc_first_name = request.form['doc_first_name']
        doc_last_name = request.form['doc_last_name']
        doc_ph_no = request.form['doc_ph_no']
        doc_date = request.form['doc_date']
        doc_address = request.form['doc_address']
        Doctor = doctor.query.filter_by(doc_id=doc_id).first()
        Doctor.doc_first_name = doc_first_name
        Doctor.doc_last_name = doc_last_name
        Doctor.doc_ph_no = doc_ph_no
        Doctor.doc_date = doc_date
        Doctor.doc_address = doc_address
        db.session.add(Doctor)
        db.session.commit()
        return redirect("/doctor")

    alldoctor = doctor.query.filter_by(doc_id=doc_id).first()
    values = []
    for i in list(map(str,str(alldoctor).split("-"))):
        values.append(i.strip())
    d = {
        "doc_id":values[0],
        "doc_first_name":values[1],
        "doc_last_name":values[2],
        "doc_ph_no":values[3],
        "doc_date":datetime.strptime(values[6] + '-' + values[5] + '-' + values[4],'%d-%m-%Y').date(),
        "doc_address":values[7]
    }

    return render_template('updatedoctor.html', d=d)


@app.route('/updatenurse/<int:nur_id>', methods=['GET', 'POST'])
def updatenurse(nur_id):
    if request.method == 'POST':
        nur_first_name = request.form['nur_first_name']
        nur_last_name = request.form['nur_last_name']
        nur_ph_no = request.form['nur_ph_no']
        nur_date = request.form['nur_date']
        nur_address = request.form['nur_address']
        Nurse = nurse.query.filter_by(nur_id=nur_id).first()
        Nurse.nur_first_name = nur_first_name
        Nurse.nur_last_name = nur_last_name
        Nurse.nur_ph_no = nur_ph_no
        Nurse.nur_date = nur_date
        Nurse.nur_address = nur_address
        db.session.add(Nurse)
        db.session.commit()
        return redirect("/nurse")

    allnurse = nurse.query.filter_by(nur_id=nur_id).first()
    print("allnurse",allnurse)
    values = []
    for i in list(map(str,str(allnurse).split("-"))):
        values.append(i.strip())
    n = {
        "nur_id":values[0],
        "nur_first_name":values[1],
        "nur_last_name":values[2],
        "nur_ph_no":values[3],
        "nur_date":datetime.strptime(values[6] + '-' + values[5] + '-' + values[4],'%d-%m-%Y').date(),
        "nur_address":values[7]
    }
    return render_template('updatenurse.html', n=n)


@app.route('/updateappointment/<int:app_id>', methods=['GET', 'POST'])
def updateappointment(app_id):
    if request.method == 'POST':
        pat_id = request.form['pat_id']
        doc_id = request.form['doc_id']
        appointment_date = request.form['appointment_date']
        Appointment = appointment.query.filter_by(app_id=app_id).first()
        Appointment.pat_id = pat_id
        Appointment.doc_id = doc_id
        Appointment.appointment_date = appointment_date
        db.session.add(Appointment)
        db.session.commit()
        return redirect("/appointment")

    allappointment = appointment.query.filter_by(app_id=app_id).first()

    values = []
    for i in list(map(str,str(allappointment).split("-"))):
        values.append(i.strip())
    a = {
        "app_id":values[0],
        "pat_id":values[1],
        "doc_id":values[2],
        "appointment_date":datetime.strptime(values[5] + '-' + values[4] + '-' + values[3],'%d-%m-%Y').date(),
    }
    return render_template('updateappointment.html', a=a)


@app.route('/updateroom/<int:room_no>', methods=['GET', 'POST'])
def updateroom(room_no):
    print('updateroom',room_no)
    if request.method == 'POST':
        room_type = request.form['room_type']
        available = request.form['available']
        Room = room.query.filter_by(room_no=room_no).first()
        Room.room_type = room_type
        Room.available = available
        db.session.add(Room)
        db.session.commit()
        return redirect("/room")

    allroom = room.query.filter_by(room_no=room_no).first()
    # print("allroom",allroom)
    # print(list(map(str,str(allroom).strip().split("-"))))
    values = []
    for i in list(map(str,str(allroom).split("-"))):
        values.append(i.strip())
    r = {
        "room_no":values[0],
        "room_type":values[1],
        "available":values[2]
    }
    return render_template('updateroom.html', r=r)



@app.route('/updatemedication/<int:code>', methods=['GET', 'POST'])
def updatemedication(code):
    if request.method == 'POST':
        name = request.form['name']
        brand = request.form['brand']
        description = request.form['description']
        Medication = medication.query.filter_by(code=code).first()
        Medication.name = name
        Medication.brand = brand
        Medication.description = description
        db.session.add(Medication)
        db.session.commit()
        return redirect("/medication")

    allmedication = medication.query.filter_by(code=code).first()
    values = []
    for i in list(map(str,str(allmedication).split("-"))):
        values.append(i.strip())
    m = {
        "code":values[0],
        "name":values[1],
        "brand":values[2],
        "description":values[3]
    }
    return render_template('updatemedication.html', m=m)

@app.route('/updatedepartment/<int:department_id>', methods=['GET', 'POST'])
def updatedepartment(department_id):
    if request.method == 'POST':
        name = request.form['name']
        head_id = request.form['head_id']
        Department = department.query.filter_by(department_id=department_id).first()
        Department.name = name
        Department.head_id = head_id
        db.session.add(Department)
        db.session.commit()
        return redirect("/department")

    alldepartment = department.query.filter_by(department_id=department_id).first()

    values = []
    for i in list(map(str,str(alldepartment).split("-"))):
        values.append(i.strip())
    de = {
        "department_id":values[0],
        "name":values[1],
        "head_id":values[2],
    }
    return render_template('updatedepartment.html', de=de)

@app.route('/updateprocedure/<int:code>', methods=['GET', 'POST'])
def updateprocedure(code):
    if request.method == 'POST':
        name = request.form['name']
        cost = request.form['cost']
        Procedure = procedure.query.filter_by(code=code).first()
        Procedure.name = name
        Procedure.cost = cost
        db.session.add(Procedure)
        db.session.commit()
        return redirect("/procedure")

    allprocedure = procedure.query.filter_by(code=code).first()

    values = []
    for i in list(map(str,str(allprocedure).split("-"))):
        values.append(i.strip())
    p = {
        "code":values[0],
        "name":values[1],
        "cost":values[2],
    }
    return render_template('updateprocedure.html', p=p)



@app.route('/updateundergoes/<int:under_id>', methods=['GET', 'POST'])
def updateundergoes(under_id):
    if request.method == 'POST':
        pat_id = request.form['pat_id']
        proc_code = request.form['proc_code']
        u_date = request.form['u_date']
        doc_id = request.form['doc_id']
        nur_id = request.form['nur_id']
        room_no = request.form['room_no']
        Undergoes= undergoes.query.filter_by(under_id=under_id).first()
        Undergoes.pat_id = pat_id 
        Undergoes.proc_code = proc_code
        Undergoes.u_date = u_date
        Undergoes.doc_id = doc_id
        Undergoes.nur_id = nur_id
        Undergoes.room_no = room_no
        db.session.add(Undergoes)
        db.session.commit()
        return redirect("/undergoes")

    allundergoes = undergoes.query.filter_by(under_id=under_id).first()

    values = []
    for i in list(map(str,str(allundergoes).split("-"))):
        values.append(i.strip())
    u = {
        "under_id":values[0],
        "pat_id":values[1],
        "proc_code":values[2],
        "u_date":datetime.strptime(values[5] + '-' + values[4] + '-' + values[3],'%d-%m-%Y').date(),
        "doc_id":values[6],
        "nur_id":values[7],
        "room_no":values[8],
    }
    return render_template('updateundergoes.html', u=u)

@app.route('/updateprescribes/<int:pre_id>', methods=['GET', 'POST'])
def updateprescribes(pre_id):
    if request.method == 'POST':
        doc_id = request.form['doc_id']
        pat_id = request.form['pat_id']
        med_code = request.form['med_code']
        p_date = request.form['p_date']
        app_id = request.form['app_id']
        dose = request.form['dose']
        Prescribes = prescribes.query.filter_by(pre_id=pre_id).first()
        Prescribes.doc_id = doc_id
        Prescribes.pat_id = pat_id
        Prescribes.med_code = med_code
        Prescribes.p_date = p_date
        Prescribes.app_id = app_id
        Prescribes.dose = dose
        db.session.add(Prescribes)
        db.session.commit()
        return redirect("/prescribes")

    allprescribes = prescribes.query.filter_by(pre_id=pre_id).first()

    values = []
    for i in list(map(str,str(allprescribes).split("-"))):
        values.append(i.strip())
    pr = {
        "pre_id":values[0],
        "doc_id":values[1],
        "pat_id":values[2],
        "med_code":values[3],
        "p_date":datetime.strptime(values[6] + '-' + values[5] + '-' + values[4],'%d-%m-%Y').date(),
        "app_id":values[7],
        "dose":values[8],
    }
    return render_template('updateprescribes.html', pr=pr)




# Delete entries from the database
@app.route('/deletepatient/<int:pat_id>')
def deletepatient(pat_id):
    Patient = patient.query.filter_by(pat_id=pat_id).first()
    db.session.delete(Patient)
    db.session.commit()
    return redirect("/patient")

@app.route('/deletedoctor/<int:doc_id>')
def deletedoctor(doc_id):
    Doctor = doctor.query.filter_by(doc_id=doc_id).first()
    db.session.delete(Doctor)
    db.session.commit()
    return redirect("/doctor")

@app.route('/deletenurse/<int:nur_id>')
def deletenurse(nur_id):
    Nurse = nurse.query.filter_by(nur_id=nur_id).first()
    db.session.delete(Nurse)
    db.session.commit()
    return redirect("/nurse")

@app.route('/deleteappointment/<int:app_id>')
def deleteappointment(app_id):
    Appointment = appointment.query.filter_by(app_id=app_id).first()
    db.session.delete(Appointment)
    db.session.commit()
    return redirect("/appointment")

@app.route('/deleteroom/<int:room_no>')
def deleteroom(room_no):
    Room = room.query.filter_by(room_no=room_no).first()
    db.session.delete(Room)
    db.session.commit()
    return redirect("/room")

@app.route('/deletemedication/<int:code>')
def deletemedication(code):
    Medication = medication.query.filter_by(code=code).first()
    db.session.delete(Medication)
    db.session.commit()
    return redirect("/medication")

@app.route('/deletedepartment/<int:department_id>')
def deletedepartment(department_id):
    Department = department.query.filter_by(department_id=department_id).first()
    db.session.delete(Department)
    db.session.commit()
    return redirect("/department")

@app.route('/deleteprocedure/<int:code>')
def deleteprocedure(code):
    Procedure = procedure.query.filter_by(code=code).first()
    db.session.delete(Procedure)
    db.session.commit()
    return redirect("/procedure")

@app.route('/deleteundergoes/<int:under_id>')
def deleteundergoes(under_id):
    Undergoes = undergoes.query.filter_by(under_id=under_id).first()
    db.session.delete(Undergoes)
    db.session.commit()
    return redirect("/undergoes")

@app.route('/deleteprescribes/<int:pre_id>')
def deleteprescribes(pre_id):
    Prescribes = prescribes.query.filter_by(pre_id=pre_id).first()
    db.session.delete(Prescribes)
    db.session.commit()
    return redirect("/prescribes")



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    app.run()
    