from flask_wtf import FlaskForm
import email_validator
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError,email_validator,Email,Regexp, NumberRange
from wtforms import StringField, SelectField, PasswordField, SubmitField,IntegerField,TextAreaField,DateField,BooleanField,RadioField




class RegisterForm(FlaskForm):
    department = SelectField(label="Dapartment",validators=[DataRequired()],choices=[("rde","Registration/Admission Desk Executive"),("pha","Pharmacist"),("dse","Diagnostic Service Executive")],render_kw={"id":"department"})
    username   = StringField("Username", validators=[DataRequired(message="Username is Required"),Length(message='UserName should be Minimun 4 characters.',
                          min=4) ] )
    password = PasswordField("Password", validators=[DataRequired(message="Password is Required"),Length(message='Password should be of 5 characters.',
                          min=5),Regexp(message=' Password should contain 5 characters including one special character, one upper case, one numeric.',
                          regex=r'^(?=.*[A-Z])(?=.*\d)(?=.*[\W\_])[A-Za-z\d\W\_]*$'), ] )
    #password_cnf = PasswordField(label="Confirm Password",validators=[DataRequired(),EqualTo('password',message="Password do not match")])
    submit = SubmitField(label="Register Now")


class CreatePatientForm(FlaskForm):
    patientid = IntegerField(label="SSN ID",validators=[DataRequired(),NumberRange(message='ID should be exactly 9', min=100000000, max=999999999)],render_kw={"id":"ssn_id"})
    patient_name = StringField(label="Patient Name",validators=[DataRequired()],render_kw={"id":"p_name","placeholder":"Name"})
    patient_age  = IntegerField(label="Patient Age",validators=[DataRequired()],render_kw={"id":"p_age","placeholder":"Age"})
    bed_type = SelectField(label="Type Of Bed",validators=[DataRequired()],choices=[("General Ward","General Ward"),("Semi Sharing","Semi Sharing"),("Single Room","Single Room")],render_kw={"id":"bed_type"})
    address = TextAreaField(label="Address",validators=[DataRequired()],render_kw={"id":"address"})
    state   = StringField(label="State",validators=[DataRequired()])
    city = StringField(label="City",validators=[DataRequired()])
    submit = SubmitField(label="Submit",validators=[DataRequired()])




class LoginForm(FlaskForm):
    username   = StringField("Username", validators=[DataRequired(message="Username is Required"),Length(message='UserName should be Minimun 4 characters.',
                          min=4) ] )
    password = PasswordField("Password", validators=[DataRequired(message="Password is Required"),Length(message='Password should be and 5 characters.',
                          min=5),Regexp(message=' Password should contain 5 characters including one special character, one upper case, one numeric.',
                          regex=r'^(?=.*[A-Z])(?=.*\d)(?=.*[\W\_])[A-Za-z\d\W\_]*$'), ] )
    submit = SubmitField(label="Log In")



class UpdatePatient(FlaskForm):
    patientid = IntegerField(label="SSN ID",validators=[DataRequired(),NumberRange(message='ID should be exactly 9', min=100000000, max=999999999)],render_kw={"id":"ssn_id","readonly":"readonly"})
    patient_name = StringField(label="Patient Name",validators=[DataRequired()],render_kw={"id":"p_name","placeholder":"Name"})
    patient_age  = IntegerField(label="Patient Age",validators=[DataRequired()],render_kw={"id":"p_age","placeholder":"Age"})
    bed_type = SelectField(label="Type Of Bed",validators=[DataRequired()],choices=[("General Ward","General Ward"),("Semi Sharing","Semi Sharing"),("Single Room","Single Room")],render_kw={"id":"bed_type"})
    address = TextAreaField(label="Address",validators=[DataRequired()],render_kw={"id":"address"})
    state   = StringField(label="State",validators=[DataRequired()])
    city = StringField(label="City",validators=[DataRequired()])
    submit = SubmitField(label="Update",validators=[DataRequired()])


class GetPatientId(FlaskForm):
    patientid = IntegerField(label="SSN ID",validators=[DataRequired(),NumberRange(message='ID should be exactly 9', min=100000000, max=999999999)],render_kw={"id":"ssn_id"})
    submit = SubmitField(label="Submit",validators=[DataRequired()])



class ShowPatient(FlaskForm):
    patientid = IntegerField(label="SSN ID",validators=[DataRequired(),NumberRange(message='ID should be exactly 9', min=100000000, max=999999999)],render_kw={"id":"ssn_id","readonly":"readonly"})
    patient_name = StringField(label="Patient Name",render_kw={"id":"p_name","placeholder":"Name"})
    patient_age  = IntegerField(label="Patient Age",render_kw={"id":"p_age","placeholder":"Age"})
    bed_type = SelectField(label="Type Of Bed",choices=[("General Ward","General Ward"),("Semi Sharing","Semi Sharing"),("Single Room","Single Room")],render_kw={"id":"bed_type"})
    address = TextAreaField(label="Address",render_kw={"id":"address"})
    state   = StringField(label="State")
    city = StringField(label="City")
    submit = SubmitField(label="Delete")

class ConfirmBill(FlaskForm):
    submit = SubmitField(label="Confirm")

class Medicine(FlaskForm):
    quantity = IntegerField("Quantity", validators=[DataRequired(message="Quantity is Required"), NumberRange(message='Minimum 1', min=1, max=999999999 ) ])
    rate = IntegerField("Rate", validators=[DataRequired(message="Rate is Required"), NumberRange(message='Minimum 1', min=1, max=999999999 ) ])
    medicinename = StringField("Name", validators=[ DataRequired(message="Name is Required") ])

class DeleteMedicine(FlaskForm):
    medicinename = StringField("Name", validators=[ DataRequired(message="Name is Required") ])

class Diagnosis(FlaskForm):
    rate = IntegerField("Rate", [DataRequired(message="Rate is Required"), NumberRange(message='Minimum 1', min=1, max=999999999 ) ])
    diagnosisname = StringField("Name", validators=[ DataRequired(message="Name is Required") ])

class DeleteDiagnosis(FlaskForm):
    diagnosisname = StringField("Name", validators=[ DataRequired(message="Name is Required") ])