from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField, TextAreaField,BooleanField, SelectField,DateField, URLField,TelField,RadioField,FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from flask_login import current_user
from flask_wtf.file import FileField , FileAllowed,FileRequired
from flask import jsonify
# from wtforms.fields.html5 import DateField,DateTimeField


class Register(FlaskForm):

    name = StringField('name', validators=[DataRequired(),Length(min=2,max=24)])
    email = StringField('email', validators=[DataRequired(),Email()])
    password = PasswordField('password', validators=[DataRequired(), Length(min=8, max=64)])
    confirm = PasswordField('confirm', validators=[DataRequired(),EqualTo('password'), Length(min=8, max=64)])
    admin_bool = BooleanField('Register as Admin?')

    submit = SubmitField('Create Account!')

    def validate_email(self,email):
        from app import db, User, app

        # with db.init_app(app):
        user_email = User.query.filter_by(email = self.email.data).first()
        if user_email:
            print("CHECKING EMAIL: " , user_email)
            return user_email


class UserAccountForm(FlaskForm):

    address = StringField('Physical Address')
    contacts = TelField('Phone Number', validators=[DataRequired()])
    church_local = StringField('Local Church', validators=[DataRequired()])
    church_zone = StringField('Zone', validators=[DataRequired()])
    church_mission = SelectField('Mission Station', validators=[DataRequired()],choices=[("Manzini", "Manzini"),("Mankayane", "Mankayane"),("Mbabane", "Mbabane")
                                                                                 ,("Ebenezer", "Ebenezer"),("Mpaka", "Mpaka"),("Mankayane", "Mankayane"),("Mbabane", "Mbabane"),
                                                                                 ("Mayiwane", "Mayiwane")])
    gender = SelectField('Gender',choices=[("Male", "Male"),("Female", "Female")])
    # pastor = SelectField('Are You a Pastor?',choices=[("None", "None"),("Pastor", "Pastor"),("Reverend", "Reverend")])
    age_group = SelectField('Group',choices=[("Youth", "Youth"),("Young Adults", "Young Adults"),("Women", "Women"),("Men", "Men"),("Sunday School", "Sunday School")])
    other = StringField('')
    other2 = StringField('')
    other3 = StringField('')
    image = FileField('Profile Picture',validators=[FileAllowed(['jpg', 'png', 'webp'], 'Images only!')])
    next_of_kin = StringField('Emergency Contact Person')
    next_of_kin_no = TelField('Their Contacts')
    employ_status = SelectField('Mission Station', validators=[Optional()],choices=[("Entreprenuer", "Entreprenuer/Self-Employed"),("Working", "Working"),("Un-employed","No Job")])
    employer = StringField('Employer (If Working)')
    skills = StringField('Skills')
    qualifications = StringField('Qualifications (If Applicable)')
    experience = StringField('Experience')
    submit = SubmitField('Update')


class AdminAccountForm(FlaskForm):

    address = StringField('Physical Address')
    contacts = TelField('Phone Number', validators=[DataRequired()])
    age_group = SelectField('Group',choices=[("Youth", "Youth"),("Young Adults", "Young Adults"),("Women", "Women"),("Men", "Men"),("Sunday School", "Sunday School")])
    church_local = StringField('Local Church', validators=[DataRequired()])
    church_zone = StringField('Zone', validators=[DataRequired()])
    church_mission = SelectField('Mission Station', validators=[DataRequired()],choices=[("Manzini", "Manzini"),("Mankayane", "Mankayane"),("Mbabane", "Mbabane")
                                                                                 ,("Ebenezer", "Ebenezer"),("Mpaka", "Mpaka"),("Mankayane", "Mankayane"),("Mbabane", "Mbabane"),
                                                                                 ("Mayiwane", "Mayiwane"),])
    gender = SelectField('Gender',choices=[("Male", "Male"),("Female", "Female")])
    pastor = SelectField('Are You a Pastor?',choices=[("None", "None"),("Pastor", "Pastor"),("Reverend", "Reverend")])
    senior_pastor = BooleanField('Senior Pastor?',validators=[Optional()])
    committee_local_group=SelectField('Local Committee Group',choices=[("None", "None"),("Deacons", "Deacons"),("Elders", "Elders"),
                                                                          ("Youth Committee", "Youth Committee"),("Brothers Committee", "Brothers Committee"),("Sisters Committee", "Sisters Committee"),("Fathers Committee", "Fathers Committee"),("Womens Committee", "Womens Commiittee")
                                                                          ,("Sunday School", "Sunday School")])
    committee_local_pos=SelectField('Local Committee Membership',choices=[("None", "None"),("Chairman", "Chairman"),("Vice-Chairman", "Vice-Chairman"),
                                                                          ("Secretary", "Secretary"),("Vice-Secretary", "Vice-Secretary"),("Treasurer", "Treasurer")
                                                                          ,("Add Member", "Add Member"),("Sunday School Teacher", " Sunday School Teacher")])
    committee_mission_grp=SelectField('Mission Committee Group',choices=[("None", "None"),("MSAC Committee", "MSAC Committee"),("MYC Committee", "MYC Committee")
                                                                          ,("CYC Committee", "CYC Committee")])
    committee_mission_pos=SelectField('Mission Committee Membership',choices=[("None", "None"),("Chairman", "Chairman"),("Vice-Chairman", "Vice-Chairman"),
                                                                          ("Secretary", "Secretary"),("Vice-Secretary", "Vice-Secretary"),("Treasurer", "Treasurer")
                                                                          ,("Add Member", "Add Member")])
    other = StringField('')
    other2 = StringField('')
    other3 = StringField('')
    next_of_kin = StringField('Emergency Contact Person')
    next_of_kin_no = StringField('Their Contacts')
    employ_status = SelectField('Mission Station', validators=[Optional()],choices=[("Entreprenuer", "Entreprenuer/Self-Employed"),("Working", "Working"),("Employed","No Job")])
    employer = StringField('Employer (If Working)')
    skills = StringField('Skills')
    qualifications = StringField('Qualifications (If Applicable)')
    experience = StringField('Experience')
    submit = SubmitField('Update')
    image = FileField('Profile Picture',validators=[FileAllowed(['jpg', 'png', 'webp'], 'Images only!')])
    submit = SubmitField('Update')


class OpenEventForm(FlaskForm):

    start_date = DateField('Start Date (Event)',validators=[DataRequired()])
    end_date = DateField('End Date',validators=[DataRequired()])
    event_title = StringField('Services Title', validators=[DataRequired()])
    event_abbr = StringField('Abbreviation (Optional)')#
    event_theme = StringField('Services Theme (Optional)')
    event_venue = StringField('Venue', validators=[DataRequired()])#
    registration_group1 = SelectField('Select Group',
                            choices=[("VIP", "VIP"),("Adults", "Adults"),("Working Youth", "Working Youth"),("Non Working Youth", "Non Working Youth"),("Children", "Children")])
    reg_fee_amnt1 = FloatField("Amount", validators=[Optional()])
    registration_group2 = SelectField('Select Group',
                            choices=[("VIP", "VIP"),("Adults", "Adults"),("Working Youth", "Working Youth"),("Non Working Youth", "Non Working Youth"),("Children", "Children")])
    reg_fee_amnt2 = FloatField("Amount", validators=[Optional()])
    registration_group3 = SelectField('Select Group',
                            choices=[("VIP", "VIP"),("Adults", "Adults"),("Working Youth", "Working Youth"),("Non Working Youth", "Non Working Youth"),("Children", "Children")])
    reg_fee_amnt3 = FloatField("Amount", validators=[Optional()])
    registration_group4 = SelectField('Select Group',
                            choices=[("VIP", "VIP"),("Adults", "Adults"),("Working Youth", "Working Youth"),("Non Working Youth", "Non Working Youth"),("Children", "Children")])
    reg_fee_amnt4 = FloatField("Amount", validators=[Optional()])
    registration_group5 = SelectField('Select Group',
                            choices=[("VIP", "VIP"),("Adults", "Adults"),("Working Youth", "Working Youth"),("Non Working Youth", "Non Working Youth"),("Children", "Children")])
    reg_fee_amnt5 = FloatField("Amount", validators=[Optional()])
    registration_group6 = SelectField('Select Group',
                            choices=[("VIP", "VIP"),("Adults", "Adults"),("Working Youth", "Working Youth"),("Non Working Youth", "Non Working Youth"),("Children", "Children")])
    reg_fee_amnt6 = FloatField("Amount", validators=[Optional()])
    event_other_info = StringField('Other Info')
    submit = SubmitField('Submit')


class RegistrationsForm(FlaskForm):

    transaction_id = StringField('Transaction Reference No.')
    pop_image = FileField('Upload Proof of Payment')
    pop_image_comp = FileField('Upload Proof of Payment')
    no_pop = BooleanField('None')
    payment_platform = SelectField('Payment Platform?',
                                  choices=[("Mobile Money", "Mobile Money"),("FNB", "FNB"),("Standard Bank", "Standard Bank"),("NedBank", "NedBank")
                                           ,("Eswatini Bank", "Eswatini Bank"),("Swaziland Building Society", "Swaziland Building Society")])
    registration = SelectField('Registration',
                            choices=[("VIP", "VIP"),("Adults", "Adults"),("Working Youth", "Working Youth"),("Non Working Youth", "Non Working Youth"),("Children", "Children")])
    special_diet_bool = RadioField('Special Diet?',choices=[(0, "No"),(1, "Yes")], validators=[Optional()])
    special_diet = StringField('Please Specify')
    accommodation_bool = BooleanField('Accommodation Required?')
    # accommodation_add_info = RadioField('Accommodation (Will you be staying at the conference venue?")',choices=[(0, "No"),(1, "Yes")],default=0)
    submit = SubmitField('Submit')


class AddChildrenForm(FlaskForm):
    child_name_1 = StringField('Child Name')
    child_name_2 = StringField('Child Name')
    child_name_3 = StringField('Child Name')
    child_name_4 = StringField('Child Name')
    child_name_5 = StringField('Child Name')
    child_name_6 = StringField('Child Name')

    submit = SubmitField('Submit')

    

class Login(FlaskForm):
    email = StringField('email', validators=[DataRequired(),Email()])
    password = PasswordField('password', validators=[DataRequired(), Length(min=8, max=64)])
    submit = SubmitField('Login')


class Contact_Form(FlaskForm):

    name = StringField('name')
    email = StringField('email', validators=[DataRequired(),Email()])
    contact = TelField('contact')
    subject = StringField("subject")
    message = TextAreaField("Message",validators=[Length(min=8, max=255)])
    submit = SubmitField("Send")


class Reset(FlaskForm):

    new_password = PasswordField('New password', validators=[DataRequired(), Length(min=8, max=64)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('new_password'), Length(min=8, max=64)])

    reset = SubmitField('Reset')


class Reset_Request(FlaskForm):

    email = StringField('email', validators=[DataRequired(), Email()])
    reset = SubmitField('Submit')

    # def validate_email(self,email):
    #     user = user.query.filter_by