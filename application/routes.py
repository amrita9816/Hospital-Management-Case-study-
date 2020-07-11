from application import app,cursor,conn
from flask import render_template,flash,redirect,request,url_for,session
from application.forms import LoginForm,RegisterForm,CreatePatientForm,UpdatePatient,ShowPatient,DeleteMedicine,DeleteDiagnosis,Diagnosis,Medicine,GetPatientId,ConfirmBill
from wtforms.validators import ValidationError
from application.models import Patient
import sys
from datetime import datetime


#####################################################################################

                    #Login Feature Completed

#####################################################################################
@app.route("/",methods=['GET','POST'])
@app.route("/login",methods=['GET','POST'])
def login():
    if session.get('username') and session.get('usertype')==("rde"):
        return redirect("/create_patient")
    elif session.get('username') and session.get('usertype') == "pha":
        return redirect("/patient_search")
    elif session.get('username') and session.get('usertype')=="dse":
        return redirect("/patient_search2")

    loginForm = LoginForm()
    title = "Login"
    if loginForm.validate_on_submit():
        username = loginForm.username.data
        password = loginForm.password.data
        cursor.execute("""SELECT (`type`) FROM `user_login` WHERE `username` LIKE '{}' AND `password` LIKE '{}'"""
        .format(username,password))
        dataset=cursor.fetchone()
        
        if cursor.rowcount>0:
            flash("Logged in SuccessFully")
            session['username'] = username
            session['usertype'] = dataset[0]
            if dataset[0] == ("rde"):
                return redirect("/create_patient")
            elif dataset[0] == "pha":
                return redirect("/patient_search")
            else:
                return redirect("/patient_search2")
    return render_template("login.html",title=title,form=loginForm)

#####################################################################################

                    #Logout Feature completed

#####################################################################################
@app.route("/logout")
def logout():
    session.pop('username',None)
    session.pop('usertype',None)
    return redirect("/login")

#####################################################################################

                #register Feature Completed

#####################################################################################
@app.route("/register", methods=['GET','POST'])
def register():
    registerForm = RegisterForm()
    title = "Register Here"
    if registerForm.validate_on_submit() :
        department=registerForm.department.data
        username = registerForm.username.data
        password = registerForm.password.data
        cursor.execute("""SELECT (`type`) FROM `user_login` WHERE `username` LIKE '{}' """
        .format(username))
        data=cursor.fetchall()
        if cursor.rowcount>0:
            flash(f"{username} already exist")
            return redirect(url_for('register'))
        else:
            cursor.execute("""INSERT INTO `user_login` (`username`,`password`,`type`) VALUES ('{}','{}','{}')""".format(username,password,department))
            conn.commit()
            return redirect("/login")        

    return render_template("register.html",title=title,form=registerForm)

#######################################################################################

                #Create Patient Feature Completed

#######################################################################################
@app.route("/create_patient",methods=['GET','POST'])
def create_patient():
    if session.get('username'):
        if session.get('usertype')=="rde":
            form = CreatePatientForm()
            if form.validate_on_submit():
                ssn=form.patientid.data
                name= form.patient_name.data
                age=form.patient_age.data
                doj=request.form.get("date")
                bed=form.bed_type.data
                addrs=form.address.data
                state=form.state.data
                city=form.city.data
                adrs=addrs+" , "+city+" , "+state
                cursor.execute("""INSERT INTO `patient` (`ws_ssn`,`ws_pat_name`,`ws_age`,`ws_adrs`,`ws_doj`,`ws_rtype`) VALUES ('{}','{}','{}','{}','{}','{}')"""
                .format(ssn,name,age,adrs,doj,bed))
                conn.commit()
                flash("Patient Detail Saved")
                return redirect("/create_patient")
            return render_template("CreatePatient.html",form=form)

    return redirect("/login")

#######################################################################################

                #diagnose feature in progress

#######################################################################################

@app.route('/patient_search2',methods=['GET','POST'])
def search():
    if session.get('username'):
        if session.get('usertype')=="dse":
            return render_template("patient_search2.html")
    return redirect("/login")

@app.route("/view_diagnostics",methods=['GET','POST'])
def view_diagnostics():
    if session.get('username'):
        if session.get('usertype')=="dse":
            p_id=request.form.get("ID")
            cursor.execute("""SELECT * FROM `patient` WHERE `ws_pat_id` LIKE '{}'""".format(p_id))
            detail=cursor.fetchall()
            cursor.execute("SELECT `ws_test_id` FROM `track_diag` WHERE `ws_pat_id` LIKE '{}'".format(p_id))
            all_diag=cursor.fetchall()
            info=list()
            print(all_diag)
            for i in all_diag:
                cursor.execute("SELECT * FROM `diag_master_file` WHERE `ws_test_id` LIKE '{}'".format(i[0]))
                some=cursor.fetchall()
                print(some)
                info.append(some[0])

            return render_template("diagnose1.html",detail=detail,info=info)
    return redirect("/login")

@app.route('/add_diagnostics',methods=['GET','POST'])
def  add_diagnostics():
    if session.get('username'):
        if session.get('usertype')=="dse":
            p_id=request.form.get("ID")
            test_name=request.form.get("name")

            cursor.execute("""SELECT * FROM `patient` WHERE `ws_pat_id` LIKE '{}'""".format(p_id))
            detail=cursor.fetchall()
            cursor.execute("SELECT * FROM `diag_master_file` WHERE `ws_test_name` LIKE '{}'".format(test_name))
            add=cursor.fetchall()
            print(add)

            cursor.execute("INSERT INTO `track_diag` VALUES ('{}','{}')".format(p_id,add[0][0]))
            conn.commit()
            cursor.execute("SELECT `ws_test_id` FROM `track_diag` WHERE `ws_pat_id` LIKE '{}'".format(p_id))
            all_diag=cursor.fetchall()

            info=list()
            print(all_diag)
            for i in all_diag:
                cursor.execute("SELECT * FROM `diag_master_file` WHERE `ws_test_id` LIKE '{}'".format(i[0]))
                some=cursor.fetchall()
                info.append(some[0])

            return render_template("diagnose1.html",detail=detail,info=info,add=add)
    return redirect("/login")

@app.route("/diagnose",methods=['GET','POST'])
def diagnose():
    if session.get('username'):
        if session.get('usertype')=="dse":
            return render_template("diagnose1.html")
    return redirect("/login")        


#######################################################################################

                #Pharmacy feature in progress

#######################################################################################
@app.route("/patient_search",methods=['POST','GET'])
def pharmacy():
    if session.get('username'):
        if session.get('usertype')=="pha":
            return render_template("patient_search.html")
    return redirect("/login")



#######################################################################################

                #View/Issue Medicine feature in progress

#######################################################################################


@app.route('/view_medicines',methods=['POST','GET'])
def view():
    P_id=request.form.get("ID")
    cursor.execute("""SELECT * FROM `patient` WHERE `ws_pat_id` LIKE '{}'""".format(P_id))
    detail=cursor.fetchall()
    print(detail)
    cursor.execute("""SELECT `ws_med_id` FROM `track_medicine` WHERE `ws_pat_id` LIKE '{}'""".format(P_id))
    all_med=cursor.fetchall()
    
    cursor.execute("""SELECT `ws_qty` FROM `track_medicine` WHERE `ws_pat_id` LIKE '{}'""".format(P_id))
    all_qty=cursor.fetchall()
    medicine_name=[]
    medicine_rate=[]
    medicine_amount=[]
    store=[]
    for i in all_med:
        
        cursor.execute("""SELECT `ws_med_name` FROM `master_med_file` WHERE `ws_med_id` LIKE '{}'""".format(i[0]))
        nam=cursor.fetchall()
        medicine_name.append(nam)
        cursor.execute("""SELECT `ws_rate` FROM `master_med_file` WHERE `ws_med_id` LIKE '{}'""".format(i[0]))
        medrate=cursor.fetchall()
        medicine_rate.append(medrate)
    for j in range(len(all_qty)):
        quant=all_qty[j][0]
        perrate=medicine_rate[j][0][0]
        peramount=quant*perrate
        store.append(int(j))

        medicine_amount.append(peramount)
        conn.close()
    return render_template("issue_medicine.html",details=detail,pid=P_id,ALLNAME=medicine_name,ALLQTY=all_qty,ALLRATE=medicine_rate,ALLAMOUNT=medicine_amount,LENGTH=store)


@app.route('/issue_medicine',methods=['POST','GET'])
def issue():
    P_id=request.form.get('pt_id')
    
    cursor.execute("""SELECT * FROM `patient` WHERE `ws_pat_id` LIKE '{}'""".format(P_id))
    detail=cursor.fetchall()
    med_name=request.form.get('name')
    med_qty=int(request.form.get('quantity'))
    cursor.execute("""SELECT `ws_rate`  FROM `master_med_file` WHERE `ws_med_name` LIKE '{}'""".format(med_name))
    rate=cursor.fetchall()
    amt=med_qty*rate[0][0]
    cursor.execute("""SELECT `ws_med_id`  FROM `master_med_file` WHERE `ws_med_name` LIKE '{}'""".format(med_name))
    mid=cursor.fetchall()
    med_id=mid[0][0]
    print(med_id)
    
    ####### reduce quantity from master_med_file #####
    cursor.execute("""SELECT `ws_qty_av`  FROM `master_med_file` WHERE `ws_med_name` LIKE '{}'""".format(med_name))
    quant_to_update=cursor.fetchall()
    new_quant=quant_to_update[0][0]-med_qty
    if new_quant<0:
        msg=" medicine is not available"
    else:
        cursor.execute("""INSERT INTO `track_medicine` (`ws_pat_id`,`ws_med_id`,`ws_qty`) VALUES ('{}','{}','{}')""".format(P_id,med_id,med_qty))
        conn.commit()
        cursor.execute("""UPDATE `master_med_file` SET `ws_qty_av`='{}' WHERE `ws_med_name` LIKE '{}'""".format(new_quant,med_name))
        conn.commit()
        msg= None
    print(new_quant)
    
    
    ####### patient medicines issued #######
    cursor.execute("""SELECT `ws_med_id` FROM `track_medicine` WHERE `ws_pat_id` LIKE '{}'""".format(P_id))
    all_med=cursor.fetchall()
    
    cursor.execute("""SELECT `ws_qty` FROM `track_medicine` WHERE `ws_pat_id` LIKE '{}'""".format(P_id))
    all_qty=cursor.fetchall()
    medicine_name=[]
    medicine_rate=[]
    medicine_amount=[]
    store=[]
    for i in all_med:
        
        cursor.execute("""SELECT `ws_med_name` FROM `master_med_file` WHERE `ws_med_id` LIKE '{}'""".format(i[0]))
        nam=cursor.fetchall()
        medicine_name.append(nam)
        cursor.execute("""SELECT `ws_rate` FROM `master_med_file` WHERE `ws_med_id` LIKE '{}'""".format(i[0]))
        medrate=cursor.fetchall()
        medicine_rate.append(medrate)
    for j in range(len(all_qty)):
        quant=all_qty[j][0]
        perrate=medicine_rate[j][0][0]
        peramount=quant*perrate
        store.append(int(j))

        medicine_amount.append(peramount)
    
    return render_template("issue_medicine.html",details=detail,name=med_name,qty=med_qty,rate=rate[0][0],amt=amt,pid=P_id,ALLNAME=medicine_name,ALLQTY=all_qty,ALLRATE=medicine_rate,ALLAMOUNT=medicine_amount,LENGTH=store,message=msg)

@app.route('/master_medicine')
def master_medicine():
    cursor.execute("TRUNCATE TABLE master_med_file")
    conn.commit()
    cursor.execute("""INSERT INTO `master_med_file` (`ws_med_id`,`ws_med_name`,`ws_qty_av`,`ws_rate`) VALUES ('01','acetaminophen','400','20')""")
    conn.commit()
    cursor.execute("""INSERT INTO `master_med_file` (`ws_med_id`,`ws_med_name`,`ws_qty_av`,`ws_rate`) VALUES ('02','aspirin','500','15')""")
    conn.commit()
    cursor.execute("""INSERT INTO `master_med_file` (`ws_med_id`,`ws_med_name`,`ws_qty_av`,`ws_rate`) VALUES ('03','decongestant','350','30')""")
    conn.commit()
    cursor.execute("""INSERT INTO `master_med_file` (`ws_med_id`,`ws_med_name`,`ws_qty_av`,`ws_rate`) VALUES ('04','insofurane','400','40')""")
    conn.commit()
    cursor.execute("""INSERT INTO `master_med_file` (`ws_med_id`,`ws_med_name`,`ws_qty_av`,`ws_rate`) VALUES ('05','paracetamol','600','10')""")
    conn.commit()
    return "success"









#######################################################################################

                #search patient feature completed

#######################################################################################
@app.route("/search_patient",methods=['GET','POST'])
def search_patient():
    if session.get('username'):
        if session.get('usertype')=="rde":
            pform = GetPatientId()
            if pform.validate_on_submit():
                ssn = pform.patientid.data
                cursor = conn.cursor(buffered=True)
                cursor.execute("""SELECT (`*`) FROM `patient` WHERE `ws_ssn` LIKE '{}'"""
                .format(ssn))
                if cursor.rowcount>0:
                    return redirect(url_for('show_patient',patientid=ssn))
                else:
                    flash("Patient Not Found")
                    return redirect(url_for('search_patient'))
            return render_template("search_patient.html",pform = pform)
    return redirect("/login")
@app.route("/search_patiente",methods=['GET','POST'])
def show_patient():
    if session.get('username'):
        if session.get('usertype')=="rde":
            patientData = {}
            patientid = request.args.get("patientid")
            if patientid:
                cursor.execute("""SELECT (`*`) FROM `patient` WHERE `ws_ssn` LIKE '{}' """
                .format(patientid))
                patientData=cursor.fetchone()
                #Splitting the address in to Street State and City
                getCompleteAddress = patientData[4].__str__()
                splittedAddress = getCompleteAddress.split(" , ",2)
                street = splittedAddress[0]
                State  = splittedAddress[1]
                city   = splittedAddress[2]
                patient = Patient(patientData[0],patientData[2],patientData[3],patientData[6],street,State,city)
            else:
                flash("No patient found")
                return redirect("/search_patient")
            form = ShowPatient(obj=patient)
            form.populate_obj(patient)
            if form.validate_on_submit():
                return redirect("/create_patient")
            return render_template("search_patient.html",form=form)
    return redirect("/login")

#######################################################################################

                    #update patient feature completed

#######################################################################################

@app.route("/update_patient",methods=['GET','POST'])
def update_patient():
    if session.get('username'):
        if session.get('usertype')=="rde":
            pform = GetPatientId()
            if pform.validate_on_submit():
                ssn = pform.patientid.data
                cursor = conn.cursor(buffered=True)
                cursor.execute("""SELECT (`*`) FROM `patient` WHERE `ws_ssn` LIKE '{}'"""
                .format(ssn))
                if cursor.rowcount>0:
                    return redirect(url_for('fetch_to_update',patientid=ssn))
                else:
                    
                    flash("Patient Not Found")
                    return redirect(url_for('update_patient'))
            return render_template("update_patient.html",pform=pform)
    return redirect("/login")

@app.route("/update_patiente",methods=['GET','POST'])
def fetch_to_update():
    if session.get('username'):
        if session.get('usertype')=="rde":
            patientData = {}
            patientid = request.args.get("patientid")
            if patientid:
                cursor.execute("""SELECT (`*`) FROM `patient` WHERE `ws_ssn` LIKE '{}' """
                .format(patientid))
                patientData=cursor.fetchone()
                #Splitting the address in to Street State and City
                getCompleteAddress = patientData[4].__str__()
                splittedAddress = getCompleteAddress.split(" , ",2)
                street = splittedAddress[0]
                State  = splittedAddress[1]
                city   = splittedAddress[2]
                #completeAddress = street +" , "+State+" , "+city
                patient = Patient(patientData[0],patientData[2],patientData[3],patientData[6],street,State,city)
            else:
                flash("No patient found")
                return redirect("/update_patient")
            form = UpdatePatient(obj=patient)
            form.populate_obj(patient)
            if form.validate_on_submit():
                ssn = form.patientid.data
                name= form.patient_name.data
                age=form.patient_age.data
                bed=form.bed_type.data
                addrs=form.address.data
                state=form.state.data
                city=form.city.data
                adrs=addrs+" , "+city+" , "+state
                cursor.execute("UPDATE patient SET ws_pat_name = %s, ws_adrs = %s, ws_age = %s, ws_rtype = %s where ws_ssn = %s", ( name, adrs, age, bed, ssn))
                conn.commit()
                flash("Patient Detail Updated")
                return redirect("/create_patient")
            return render_template("update_patient.html",form=form)
    return redirect("/login")

#######################################################################################

                    #delete patient feature completed

#######################################################################################
@app.route("/delete_patient",methods=['GET','POST'])
def delete_patient():
    if session.get('username'):
        if session.get('usertype')=="rde":
            pform = GetPatientId()
            if pform.validate_on_submit():
                ssn = pform.patientid.data
                cursor = conn.cursor(buffered=True)
                cursor.execute("""SELECT (`*`) FROM `patient` WHERE `ws_ssn` LIKE '{}'"""
                .format(ssn))
                if cursor.rowcount>0:
                    return redirect(url_for('fetch_To_delete',patientid=ssn))
                else:
                    flash("Patient Not Found")
                    return redirect(url_for('delete_patient'))
            return render_template("delete_patient.html",pform = pform)
    return redirect("/login")

@app.route("/delete_patiente",methods=['GET','POST'])
def fetch_To_delete():
    if session.get('username'):
        if session.get('usertype')=="rde":
            patientData = {}
            patientid = request.args.get("patientid")
            if patientid:
                cursor.execute("""SELECT (`*`) FROM `patient` WHERE `ws_ssn` LIKE '{}' """
                .format(patientid))
                patientData=cursor.fetchone()
                #Splitting the address in to Street State and City
                getCompleteAddress = patientData[4].__str__()
                splittedAddress = getCompleteAddress.split(" , ",2)
                street = splittedAddress[0]
                State  = splittedAddress[1]
                city   = splittedAddress[2]
                patient = Patient(patientData[0],patientData[2],patientData[3],patientData[6],street,State,city)
            else:
                flash("No patient found")
                return redirect("/update_patient")
            form = ShowPatient(obj=patient)
            form.populate_obj(patient)
            if form.validate_on_submit():
                cursor.execute("DELETE FROM `patient` WHERE `ws_ssn` LIKE '{}' """
                .format(patientid))
                conn.commit()
                flash("Patient Deleted Successfully")
                return redirect("/create_patient")
            return render_template("delete_patient.html",form=form)
            
    return redirect("/login")

#######################################################################################

                        #view patient feature completed

#######################################################################################
@app.route("/view_patient",methods=['GET','POST'])
def view_patient():
    if session.get('username'):
        if session.get('usertype')=="rde":
            cursor.execute("""SELECT * FROM `patient`""")
            val=cursor.fetchall()
            print(val[0])
            return render_template("viewPatient.html",value=val)

#######################################################################################

                        #Generate bill feature in Completed

#######################################################################################
@app.route("/generate_bill",methods=['GET','POST'])
def generate_bill():
    if session.get('username'):
        if session.get('usertype')=="rde":
            pform = GetPatientId()
            if pform.validate_on_submit():
                ssn = pform.patientid.data
                return redirect(url_for('generate_bille',patientid=ssn))
            return render_template("patient_bill.html",pform=pform)
    return redirect("/login")
@app.route("/generate_bille",methods=['GET','POST'])
def generate_bille():
    if session.get('username'):
        if session.get('usertype')=="rde":
            patientData = {}
            med_detail  = {}
            diag_detail = {}
            todaysDate = datetime.now().strftime("%m/%d/%Y")
            totalRoomCost = 0
            doj =0
            patientid = request.args.get("patientid")
            if patientid:
                cursor.execute("""SELECT (`*`) FROM `patient` WHERE `ws_pat_id` LIKE '{}' """
                .format(patientid))
                patientData=cursor.fetchone()
                cursor.execute("""SELECT track_medicine.ws_qty, master_med_file.ws_med_name,master_med_file.ws_rate FROM `master_med_file` INNER JOIN `track_medicine` ON master_med_file.ws_med_id=track_medicine.ws_med_id WHERE track_medicine.ws_pat_id LIKE '{}'""".format(patientid))
                med_detail=cursor.fetchall()

                cursor.execute("""SELECT diag_master_file.ws_test_rate,diag_master_file.ws_test_name FROM `diag_master_file` INNER JOIN `track_diag` ON diag_master_file.ws_test_id=track_diag.ws_test_id WHERE track_diag.ws_pat_id LIKE '{}'""".format(patientid))
                
                diag_detail = cursor.fetchall()

                totalMed = 0
                totalDiag = 0

                for med in med_detail:
                    totalMed +=(int(med[2])*int(med[0]))

                
                for diag in diag_detail:
                    totalDiag += (int(diag[0]))
                 
                #Splitting the address in to Street State and City
                getCompleteAddress = patientData[4].__str__()
                splittedAddress = getCompleteAddress.split(" , ",2)
                street = splittedAddress[0]
                State  = splittedAddress[1]
                city   = splittedAddress[2]
                patient = Patient(patientData[0],patientData[2],patientData[3],patientData[6],street,State,city)                
            else:
                flash("No patient found")
                return redirect("/generate_bill")
            form = ConfirmBill()
            if form.validate_on_submit():
                cursor.execute("UPDATE `patient` SET `ws_status`='{}' WHERE `ws_pat_id` LIKE '{}'""".format("Discharged",patientid))
                conn.commit()
                flash("Patient Discharged")
                return redirect("/view_patient")
        #calculate how many days patient stayed
            doj = patientData[5].__str__()
            doj = doj[0:10]
            doj = doj.split("-",2)
            dojy= int(doj[0])
            dojm=int(doj[1])
            dojd=int(doj[2])
            totalDays = datetime.today() - datetime(dojy,dojm,dojd)
            totalDays = totalDays.__str__()
            totalDays = totalDays[:2]
            totalDays = int(totalDays)

            totalRoomCost = getRoomPrice(patientData[6])*int(totalDays)

            grandTotal = totalMed+totalDiag+totalRoomCost
            return render_template("patient_bill.html",patientData=patientData,totalDays=totalDays,todaysDate=todaysDate,totalRoomCost=totalRoomCost,roomPrice = getRoomPrice(patientData[6]),med_detail=med_detail,diag_detail=diag_detail,totalMed=totalMed,totalDiag=totalDiag,grandTotal=grandTotal,form=form)
    return redirect("/login")



def getRoomPrice(roomtype):
    if roomtype == "General Ward":
        return 2000
    elif roomtype == "Semi Sharing":
        return 4000
    else:
        return 8000
#######################################################################################