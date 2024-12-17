
from flask import Flask,render_template,url_for,redirect,request,flash,jsonify,session
from flask_login import login_user, LoginManager,current_user,logout_user, login_required
from Forms import *
from models import *
from flask_bcrypt import Bcrypt
import secrets
# import MySQLdb
import time
import os
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message
# from bs4 import BeautifulSoup as bs
from flask_colorpicker import colorpicker
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
import itsdangerous
from sqlalchemy.exc import IntegrityError
from authlib.integrations.flask_client import OAuth
import json
from sqlalchemy import inspect
# import logging





#Change App
app = Flask(__name__)
app.config['SECRET_KEY'] = "sdsdjfe832j2rj_32j"
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///techxicons_db.db"
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:tmazst41@localhost/fea_registration_db"
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://techtlnf_tmaz:!Tmazst41#@localhost/techtlnf_fea_db"
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle':280}
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOADED"] = 'static/uploads'

oauth = OAuth(app)
db.init_app(app)

application = app

login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Log in
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

ALLOWED_EXTENSIONS = {"txt", "xlxs", 'docx', 'pdf', 'png', 'jpg', 'jpeg', 'gif',"JPG"}

if os.path.exists('client.json'):
    # Load secrets from JSON file
    with open('client.json') as f:
        creds = json.load(f)

def allowed_files(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# # Set up logging configuration
# logging.basicConfig(level=logging.INFO)

# # Suppress Werkzeug logger
# werkzeug_logger = logging.getLogger('werkzeug')
# werkzeug_logger.setLevel(logging.ERROR)

# # Create a logs directory and setup the log file path
# log_dir = os.path.join(os.path.dirname(__file__), 'logs')
# if not os.path.exists(log_dir):
#     os.makedirs(log_dir)
    
# # Configure logger for SQLAlchemy
# sqlalchemy_logger = logging.getLogger('sqlalchemy.engine')
# sqlalchemy_logger.setLevel(logging.INFO)
# sqlalchemy_logger.propagate = False

# # File handler for SQL logs (user entries)
# file_handler = logging.FileHandler(os.path.join(log_dir, 'user_queries.log'))
# file_handler.setLevel(logging.INFO)
# file_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
# sqlalchemy_logger.addHandler(file_handler)

from authlib.integrations.base_client.errors import MismatchingStateError

@app.errorhandler(MismatchingStateError)
def handle_mismatching_state_error(error):
    return "Authentication is Terminated due to Security Measures, Please Go Back To Login Again.", 400


class user_class:
    s = None

    def get_reset_token(self, c_user_id):

        s = Serializer(app.config['SECRET_KEY'])
        return s.dumps({'user_id': c_user_id, 'expiration_time': time.time() + 300}).encode('utf-8')

    @staticmethod
    def verify_reset_token(token, expires=1800):

        s = Serializer(app.config['SECRET_KEY'], )

        try:
            user_id = s.loads(token, max_age=300)['user_id']
        except itsdangerous.SignatureExpired:
           return f'Token has expired!, Please Create a New Token'
        except itsdangerous.BadSignature:
            return f'Token has expired, Please Create a New Token'
        except:
            return f'Something Went Wrong'
         
        return user_id

if os.path.exists('client.json'):
    appConfig = {

        "OAUTH2_CLIENT_ID" : creds['clientid'],
        "OAUTH2_CLIENT_SECRET":creds['clientps'],
        "OAUTH2_META_URL":"",
        "FLASK_SECRET":"sdsdjsdsdjfe832j2rj_32jfesdsdjfe832j2rj32j832",
        "FLASK_PORT": 5000  
    }


    oauth.register("fearegistra",
                client_id = appConfig.get("OAUTH2_CLIENT_ID"),
                client_secret = appConfig.get("OAUTH2_CLIENT_SECRET"),
                    api_base_url='https://www.googleapis.com/',
                    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo', 
                client_kwargs={ "scope" : "openid email profile"},
                server_metadata_url= 'https://accounts.google.com/.well-known/openid-configuration',
                jwks_uri = "https://www.googleapis.com/oauth2/v3/certs"
                )


def process_file(file):

        filename = secure_filename(file.filename)

        _img_name, _ext = os.path.splitext(filename)
        gen_random = secrets.token_hex(8)
        new_file_name = gen_random + _ext

        if file.filename == '':
            return 'No selected file'

        print("DEBUG FILE NAME: ", file.filename)
        file_saved = file.save(os.path.join("static/images",new_file_name))
        flash(f"File Upload Successful!!", "success")
        return new_file_name



def process_pop_file(file,usr_id):

        filename = secure_filename(file.filename)

        _img_name, _ext = os.path.splitext(filename)
        gen_random = secrets.token_hex(8)
        new_file_name = gen_random + str(usr_id) + _ext

        if file.filename == '':
            return 'No selected file'

        if file.filename:
            file_saved = file.save(os.path.join(app.config["UPLOADED"],new_file_name))
            # flash(f"File Upload Successful!!", "success")
            return new_file_name

        else:
            return f"Allowed are [.txt, .xls,.docx, .pdf, .png, .jpg, .jpeg, .gif] only"


def createall(db_):
    db_.create_all()

encry_pw = Bcrypt()

@app.context_processor
def inject_ser():
    event = open_event.query.filter_by(event_closed=False).first()
    user_no_base=User.query.all()

    return dict(event_details=event,pop_transts=pop_transactions,user_no_base=user_no_base)


@app.route("/", methods=['POST','GET'])
def home():

    with app.app_context():
       db.create_all()

    event_details=None

    if open_event.query.filter_by(event_closed=False).first():
        event_details = open_event.query.filter_by(event_closed=False).first()
    
    return render_template("index.html", event_details=event_details)


#Admins Opening & Closing Registrations
@app.route("/open_event_form", methods=["POST", "GET"])
def open_event_form():

    open_reg_form = OpenEventForm()
    event_details=None

    if open_event.query.filter_by(event_closed=False).first():
        event_details = open_event.query.filter_by(event_closed=False).first()

    if open_reg_form.validate_on_submit():

        open_event_ = open_event(start_date=open_reg_form.start_date.data,end_date=open_reg_form.end_date.data,event_title=open_reg_form.event_title.data,
                        event_abbr=open_reg_form.event_abbr.data,event_theme=open_reg_form.event_theme.data,event_venue=open_reg_form.event_venue.data,
                        registration_group1=open_reg_form.registration_group1.data,reg_fee_amnt1=open_reg_form.reg_fee_amnt1.data,registration_group2=open_reg_form.registration_group2.data,
                        reg_fee_amnt2=open_reg_form.reg_fee_amnt2.data,registration_group3=open_reg_form.registration_group3.data,reg_fee_amnt3=open_reg_form.reg_fee_amnt3.data,
                        event_other_info=open_reg_form.event_other_info.data,timestamp=datetime.now())
        
        db.session.add(open_event_)
        if not event_details:
            db.session.commit()
            flash("Event Opened Successfully!","success")
            return redirect(url_for("home"))
        else:
            flash("Event Already Opened","success")
            return redirect(url_for("home"))      
    else:
        for error in open_reg_form.errors:
            print("Reg Form Errors: ",error)

    return render_template('open_event.html',open_reg_form=open_reg_form)


#Admins Opening & Closing Registrations
@app.route("/opened_event_edit", methods=["POST", "GET"])
def opened_event_edit():

    open_reg_form = OpenEventForm()
    event_edit = open_event.query.filter_by(event_closed=False).first()

    if open_reg_form.validate_on_submit():

        event_edit.start_date=open_reg_form.start_date.data
        event_edit.end_date=open_reg_form.end_date.data
        event_edit.event_title=open_reg_form.event_title.data
        event_edit.event_abbr=open_reg_form.event_abbr.data
        event_edit.event_theme=open_reg_form.event_theme.data
        event_edit.event_venue=open_reg_form.event_venue.data
        event_edit.registration_group1=open_reg_form.registration_group1.data
        event_edit.reg_fee_amnt1=open_reg_form.reg_fee_amnt1.data
        event_edit.registration_group2=open_reg_form.registration_group2.data
        event_edit.reg_fee_amnt2=open_reg_form.reg_fee_amnt2.data
        event_edit.registration_group3=open_reg_form.registration_group3.data
        event_edit.reg_fee_amnt3=open_reg_form.reg_fee_amnt3.data
        
        db.session.commit()
        flash("Update Successful!","success")
        return redirect(url_for('home'))

    return render_template('opened_event_edit.html',open_reg_form=open_reg_form,event_details=event_edit)


def reg_confirmation():
    
    accommodation="No"
    event = open_event.query.filter_by(event_closed=False).first()
    print("CHECK EVENT: ",event)
    usr_ = church_user.query.get(current_user.id)
    reg_info = pop_transactions.query.filter_by(usr_id=current_user.id).first()

    if reg_info.accommodation_add_info == 1:
        accommodation = "Yes"

    def send_veri_mail():

        app.config["MAIL_SERVER"] = "smtp.googlemail.com"
        app.config["MAIL_PORT"] = 587
        app.config["MAIL_USE_TLS"] = True
        # Creditentials saved in environmental variables
        em = app.config["MAIL_USERNAME"] = creds.get('email')  # os.getenv("MAIL")
        app.config["MAIL_PASSWORD"] = creds.get('gpass') #os.getenv("PWD")
        app.config["MAIL_DEFAULT_SENDER"] = "noreply@gmail.com"

        mail = Mail(app)

        token = user_class().get_reset_token(current_user.id)
        usr_email = usr_.email

        msg = Message(subject="Registration Confirmation", sender="no-reply@gmail.com", recipients=[usr_email])

        msg.html = f"""<html>
<head>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f6f6f6;
            color: #333;
            padding: 20px;
        }}
        .container {{
            background-color: #ffffff;
            border-radius: 5px;
            padding: 20px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }}
        h2,h3 {{
            color: #4CAF50;
        }}
        p,li{{font-weight:500;color:#707070 }}
        .footer {{
            margin-top: 20px;
            font-size: 0.9em;
            color: #777;
        }}
        span{{ font-weight:600;color:coral}}
    </style>
</head>
<body>
    <div class="container">
        <img style="" src="https://yt3.googleusercontent.com/ytc/AIdro_kWhxLUK_wGrRkKhCAr_L_oGH2T1c-HMvF8VW0odpZ80g=s160-c-k-c0x00ffffff-no-rj" />
        <h2>Hi, {usr_.name}</h2>
        <p>This is to confirm that your registration for the African Evangelical Church's upcoming event was successful.</p>
        <p>Please see details below for your perusal:</p>
        <h3>Event Details:</h3>
        <ul>
            <li><span>Event Title:</span> {event.event_title}</li>
            <li><span>Date:</span> {event.start_date} - {event.end_date} </li>
            <li><span>Venue:</span> {event.event_venue}</li>
        </ul>
        <h3>Registration Information:</h3>
        <ul>
            <li><span>Name:</span> {church_user.query.get(reg_info.usr_id).name}</li>
            <li><span>Age Group:</span> {reg_info.age_group}</li>
            <li><span>Special Diet:</span> {reg_info.special_diet}</li>
            <li><span>Accommodation:</span> {accommodation}</li>
            <li><span>Denominational Structure:</span> {reg_info.registration}</li>
            <li><span>Reg. Date:</span> {reg_info.timestamp.strftime("%d %b %y")}</li>
            <li><span>Payment Mode:</span> {reg_info.payment_platform}</li>
            <li><span>Transaction Token:</span> {reg_info.transaction_token}</li>
        </ul>
        <p class="footer">Thank you for registering!</p>
    </div>
</body>
</html>
"""


        try:
            mail.send(msg)
            flash(f'We have sent you an email with Registration Details', 'success')
            return "Email Sent"
        except Exception as e:
            flash(f'Email not sent here', 'error')
            return "The mail was not sent"

    # try:
    send_veri_mail() 
    # except:


@app.route("/add_children_form", methods=["POST", "GET"])
@login_required
def add_children_form():

    add_child_form = AddChildrenForm()
    # sq_num=["child_name_2","child_name_3","child_name_4","child_name_5","child_name_6","child_name_7"]
    
    if request.method == "POST":
        if add_child_form.validate_on_submit():
            child = children(name=add_child_form.child_name_1.data,parent_id=current_user.id,denom_structure="Sunday School",age_group="Sunday School",timestamp=datetime.now())
            db.session.add(child)
            #Processing many fields
            for key in list(request.form.keys()):
                if key.startswith('child-') and request.form.get(key): 
                    child = children(name=request.form.get(key),parent_id=current_user.id,denom_structure="Sunday School",age_group="Sunday School",timestamp=datetime.now())
                    db.session.add(child)

        db.session.commit()
        flash("Children Registered Successfully!")

    return render_template('add_children_form.html', add_child_form=add_child_form)


#User Registrations Form Edit Confirm
@app.route("/registration_form_edit_confirm", methods=["POST", "GET"])
@login_required
def registration_form_edit_confirm():
    val_registration = None
    registration_form = RegistrationsForm()
    get_user = User.query.get(current_user.id)
    usr_reg_details = pop_transactions.query.filter_by(usr_id=current_user.id).first()
    event = open_event.query.filter_by(event_closed=False).first()

    if registration_form.validate_on_submit():
        db.session.commit()
        flash("Update Successful!", "success")
        print("Details: ",usr_reg_details.special_diet)


    return render_template('confirm_form_edit.html',usr_reg_details=usr_reg_details,registration_form=registration_form,user=get_user,
                           event_details=event,val_registration=val_registration)


def Get_Registration_Amount(val):
     
    event = open_event.query.filter_by(event_closed=False).first()

    event_dict = event.__dict__
    key_found = None

    # Get the key of the pop_transactions.registration
    for key,value in event_dict.items():
        if value == val:
            key_found = key
            break
    
    # Cook up the fee key using the last digit of val's key to the amount 
    amount = event_dict.get("reg_fee_amnt" + key[-1])

    return amount


@app.route("/view_member", methods=["POST", "GET"])
@login_required
def view_member():

    usr = None
    loc_pastor = None

    user_qrd=User.query.get(request.args.get('id'))
    if user_qrd.role == "church_user":
        usr = church_user.query.get(user_qrd.id)
    elif user_qrd.role == "admin_user":
        usr = admin_user.query.get(user_qrd.id)

    check_loc_pastor = admin_user.query.filter_by(church_local=current_user.church_local,senior_pastor=True).first()
    if check_loc_pastor:
        loc_pastor = check_loc_pastor.name


    return render_template("view_member.html",user=usr,reg_details=pop_transactions,loc_pastor=loc_pastor)


# User Information
@app.route("/reg_view_member", methods=["POST", "GET"])
@login_required
def reg_view_member():


    usr=User.query.get(request.args.get('id'))

    return render_template("reg_view_member.html",user=usr,reg_details=pop_transactions)


# User Information
@app.route('/loc_commitee_memberships')
@login_required
def loc_committee_members():

    committees = ["Deacons","Youth Committee","Fathers Committee","Mothers Committee","Brothers Committee","Sisters Committee"]

    admins = admin_user.query.filter_by(church_local=current_user.church_local).all()

    deacons = admin_user.query.filter_by(church_local=current_user.church_local,committee_local_group="Deacons").all()
    youth_com = admin_user.query.filter_by(church_local=current_user.church_local,committee_local_group="Youth Committee").all()
    fathers_com = admin_user.query.filter_by(church_local=current_user.church_local,committee_local_group="Fathers Committee").all()
    mothers_com = admin_user.query.filter_by(church_local=current_user.church_local,committee_local_group="Mothers Committee").all()
    brothers_com = admin_user.query.filter_by(church_local=current_user.church_local,committee_local_group="Brothers Committee").all()
    sisters_com = admin_user.query.filter_by(church_local=current_user.church_local,committee_local_group="Sisters Committee").all()

    return render_template("local_church_committees.html",admins=admins,deacons=deacons,youth_com=youth_com,fathers_com=fathers_com,
                           mothers_com=mothers_com,brothers_com=brothers_com,sisters_com=sisters_com,committees=committees,admin_obj=admin_user)


# User Information
@app.route('/mission_commitee_memberships')
@login_required
def mission_committee_members():

    
    committees = ["MSAC Committee","MYC Committee"]

    admins = admin_user.query.filter_by(church_local=current_user.church_local).all()

    return render_template("mission_committees.html",admins=admins,committees=committees,admin_obj=admin_user)




#User Registrations Form
@app.route("/user_registration_form", methods=["POST", "GET"])
@login_required
def user_registration_form():

    val_registration = None
    event=open_event.query.filter_by(event_closed=0).first()
    # selected_platform = request.form.get('platform')
    registration_form = RegistrationsForm()

    get_user = User.query.get(current_user.id)

   
    # Update validators based on selection
    # registration_form.update_validators(registration_form.payment_platform.data)

    if event:
        val_registration = pop_transactions.query.filter_by(usr_id=current_user.id).first()
    
    if val_registration:
        flash(f"You are already registered.", "success")
        return redirect(url_for("already_registered"))# redirect(url_for("home"))
    
    if not current_user.church_local and not current_user.church_zone:
        flash("Please Finish Up Your Account Setup, First. You're Almost Done!","success")
        if current_user.role == "church_user":
            return redirect(url_for("usr_finish_signup"))
        else:
            return redirect(url_for("admin_finish_signup"))
    
    if registration_form.validate_on_submit():

        reg =registration_form.registration.data + " " + str(Get_Registration_Amount(registration_form.registration.data))
        registration = pop_transactions(
            usr_id=current_user.id,transaction_id=secrets.token_hex(16),transaction_token=secrets.token_hex(16)+str(current_user.id),
            timestamp=datetime.now(),payment_platform=registration_form.payment_platform.data,registration=reg,reg_tag=registration_form.registration.data, #accomodation = registration_form.accomodation.data
            accommodation_bool=registration_form.accommodation_bool.data,church_mission=current_user.church_mission,church_zone=current_user.church_zone,church_local=current_user.church_local,
            special_diet=registration_form.special_diet.data
            )
        
        if registration_form.pop_image.data:
            file =  process_pop_file(registration_form.pop_image.data,current_user.id)
            registration.pop_image = file

        db.session.add(registration)

        db.session.commit()
        reg_confirmation()

        return redirect(url_for("registration_success"))

    return render_template('registrations_form.html',registration_form=registration_form,user=get_user,event_details=event,val_registration=val_registration)


#User Registrations Form Edit
@app.route("/user_registration_form_edit", methods=["POST", "GET"])
@login_required
def user_registration_form_edit():
    val_registration = None
    registration_form = RegistrationsForm()
    get_user = User.query.get(current_user.id)
    usr_reg_details = pop_transactions.query.filter_by(usr_id=current_user.id).first()
    event = open_event.query.filter_by(event_closed=False).first()

    if not usr_reg_details:
        flash("Registration Form","success")
        return redirect(url_for('user_registration_form'))

    if event:
        val_registration = pop_transactions.query.filter_by(usr_id=current_user.id).first()
    
    if not current_user.church_local and not current_user.church_zone:
        flash("Please Finish Up Your Account Setup, First. You're Almost Done!","success")
        return redirect(url_for("finish_signup"))

    if registration_form.validate_on_submit():

        usr_reg_details.payment_platform=registration_form.payment_platform.data
        usr_reg_details.registration=registration_form.registration.data
        usr_reg_details.transaction_id=registration_form.transaction_id.data
        # usr_reg_details.accomodation = registration_form.accomodation.data
        usr_reg_details.accommodation_bool=registration_form.accommodation_bool.data
        usr_reg_details.accommodation_add_info=bool(registration_form.accommodation_add_info.data)
        if registration_form.special_diet_bool:
            usr_reg_details.special_diet=registration_form.special_diet.data

        if registration_form.pop_image.data:
            file =  process_pop_file(registration_form.pop_image.data,current_user.id)
            usr_reg_details.pop_image = file

        db.session.commit()
        flash("Please, Confirm Your Update", "success")
        # return redirect(url_for("registration_form_edit_confirm",registration_form=registration_form))
        # print("Details: ",usr_reg_details.special_diet)

    elif registration_form.errors:
        for error in registration_form.errors:
            print("Update Error: ",error)


    return render_template('registrations_form_edit.html',usr_reg_details=usr_reg_details,registration_form=registration_form,user=get_user,
                           event_details=event,val_registration=val_registration)


#User Registrations Form
@app.route("/already_registered", methods=["POST", "GET"])
@login_required
def already_registered():

    registered_user = church_user.query.get(current_user.id)
    _children = children.query.filter_by(parent_id=current_user.id).all()
    print("Debug Children: ", _children)
    for child in _children:
        print("Debug Children: ", child)

    return render_template('already-registered.html',user=registered_user,reg_info=pop_transactions,children=_children)


# User Information
@app.route("/local_members", methods=["POST", "GET"])
@login_required
def local_members():

    local = None
    loc_pastor = None

    registered_children = children.query.all()
    
    if request.args.get('loc'):
        local = request.args.get('loc')
    else:
        local = current_user.church_local

    print('Final: ',request.args.get('loc'))

    local_users =User.query.filter_by(church_local=local).all()

    check_loc_pastor = admin_user.query.filter_by(church_local=current_user.church_local,senior_pastor=True).first()
    if check_loc_pastor:
        loc_pastor = check_loc_pastor.name
    


    return render_template('local_members.html',local_usrs=local_users,registered_children=registered_children,pop_transactions=pop_transactions,
                           local=local,needed=None,loc_pastor=loc_pastor)


# User Registrations
@app.route("/registered_local", methods=["POST", "GET"])
@login_required
def registered_local():

    local = None

    registered_children = children.query.all()
    
    if request.args.get('loc'):
        local = request.args.get('loc')
    else:
        local = current_user.church_local

    print('Final: ',request.args.get('loc'))

    registered_users =pop_transactions.query.filter_by(church_local=local).all()


    return render_template('registered_local.html',users=User,reg_details=registered_users,registered_children=registered_children,pop_transactions=pop_transactions,
                           local=local,needed=None)


# User Registrations
@app.route("/registered_users", methods=["POST", "GET"])
@login_required
def registered_users():

    registered_users =pop_transactions.query.all()
    registered_children = children.query.all()
    # registered_no = pop_transactions.query.all()

    missions = {entry.church_mission for entry in pop_transactions.query.all()}
    
    print("MISSIONs: ",missions)

    for mission in missions:
        print("MISSION: ",mission)

    return render_template('registered_users.html',users=User,reg_details=registered_users,registered_children=registered_children,pop_transactions=pop_transactions,
                           missions=missions,needed=None)


# User Registrations
@app.route("/my_mission_registrations", methods=["POST", "GET"])
@login_required
def my_mission_registrations():

    registered_users =pop_transactions.query.filter_by(church_mission=current_user.church_mission).all()
    registered_children = children.query.all()
    # registered_no = pop_transactions.query.all()

    missions = {entry.church_mission for entry in pop_transactions.query.all()}
    
    print("MISSIONs: ",missions)

    for mission in missions:
        print("MISSION: ",mission)

    return render_template('my_mission_registrations.html',users=User,reg_details=registered_users,registered_children=registered_children,pop_transactions=pop_transactions,
                           missions=missions,needed=None)


# User Registrations
@app.route("/my_zone_registrations", methods=["POST", "GET"])
@login_required
def my_zone_registrations():

    registered_users =pop_transactions.query.filter_by(church_zone=current_user.church_zone).all()
    registered_children = children.query.all()
    # registered_no = pop_transactions.query.all()

    missions = {entry.church_mission for entry in pop_transactions.query.all()}
    
    print("MISSIONs: ",missions)

    for mission in missions:
        print("MISSION: ",mission)

    return render_template('my_zone.html',users=User,reg_details=registered_users,registered_children=registered_children,pop_transactions=pop_transactions,
                           missions=missions,needed=None)

# User Registrations
@app.route("/registered_zones", methods=["POST", "GET"])
@login_required
def registered_zones():

    registered_users =pop_transactions.query.all()
    registered_children = children.query.all()
    mission=request.args.get("missn")
    # registered_no = pop_transactions.query.all()

    zones = {entry.church_zone for entry in pop_transactions.query.filter_by(church_mission=mission).all()}
    
    # print("MISSIONs: ",missions)

    # for mission in missions:
    #     print("MISSION: ",mission)

    return render_template('registered_zones.html',users=User,reg_details=registered_users,registered_children=registered_children,pop_transactions=pop_transactions,
                           zones=zones,mission=mission,needed=None)


# User Registrations
@app.route("/registrations", methods=["POST", "GET"])
@login_required
def registrations():

    registered_users = church_user.query.all()
    registered_no = pop_transactions.query.all()

    return render_template('registrations.html',users=registered_users,reg_details=pop_transactions,registered_no=registered_no)

@app.route("/registration_success", methods=["POST", "GET"])
@login_required
def registration_success():

    registered_user = church_user.query.get(current_user.id)
    

    return render_template('registration-success.html',user=registered_user,reg_info=pop_transactions)


@app.route("/contact_form", methods=["POST", "GET"])
def contact_form():

    contact_form = Contact_Form()
    
    if request.method == 'POST':
       
        if contact_form.validate_on_submit():
            
            
            # Get user details through their email
            

            def send_link():
                app.config["MAIL_SERVER"] = "smtp.googlemail.com"
                app.config["MAIL_PORT"] = 587
                app.config["MAIL_USE_TLS"] = True
                em = app.config["MAIL_USERNAME"] = creds.get('email') #os.getenv("EMAIL")
                app.config["MAIL_PASSWORD"] = creds.get('gpass') # os.getenv("PWD")

                mail = Mail(app)

                # token = user_class().get_reset_token(usr_email.id)
                msg = Message("Inquiry Message", sender="noreply@demo.com", recipients=[em, 'aeceswatini2024@gmail.com'])
                msg.html = f"""<html>
<head>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f6f6f6;
            color: #333;
            padding: 20px;
        }}
        .container {{
            background-color: #ffffff;
            border-radius: 5px;
            padding: 20px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }}
        h2,h3 {{
            color: #4CAF50;
        }}
        p,li{{font-weight:500;color:#505050 }}
        .footer {{
            margin-top: 20px;
            font-size: 0.9em;
            color: #777;
        }}
        span{{ font-weight:600;color:coral}}
    </style>
</head>
<body>
    <div class="container">
        <img style="" src="https://africec.org/images/webimages/logo/logo.png" />
        <h4>Name:       {contact_form.name.data}</h4>
        <h4>Email:      {contact_form.email.data}</h4>
        <h4>Contact:    {contact_form.contact.data}</h4>
        <h4>Message:</h4>
        <p> {contact_form.message.data}</p>

        
        <p class="footer">If you did not request the above message please ignore it, and your password will remain unchanged.</p>
    </div>
</body>
</html>
"""

                try:
                    mail.send(msg)
                    flash('Email Successful Sent!', 'success')
                    return "Email Sent"
                except Exception as e:

                    flash('Ooops, Something went wrong Please Retry!!', 'error')
                    return "The mail was not sent"
        


            # Send the pwd reset request to the above email
            send_link()

            return redirect(url_for('home'))
        elif contact_form.errors:
            for error in contact_form.errors:
                flash(f"Error! Please Check the {error} Field", 'error')

    return render_template("issues_contact_form.html", contact_form=contact_form,user=User)


@app.route("/signup", methods=["POST","GET"])
def sign_up():

    register = Register()

    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if register.validate_on_submit():

        #print(f"Account Successfully Created for {register.name.data}")
        if request.method == 'POST':
            # context
            hashd_pwd = encry_pw.generate_password_hash(register.password.data).decode('utf-8')
            user1 = church_user(name=register.name.data, email=register.email.data, password=hashd_pwd,
                         confirm_password=hashd_pwd, image="default.jpg",timestamp=datetime.now())

            try:
                Register().validate_email(register.email.data)
                db.session.add(user1)
                db.session.commit()
                # flash(f"Account Successfully Created for {register.name.data}", "success")
                flash(f"Please Enter Login Details", "success")
                return redirect(url_for('login'))
                # return jsonify({"message": "User registered successfully"}), 201
            except IntegrityError:
                db.session.rollback()  # Rollback the session on error
                return jsonify({"message": "Email already exists"}), 409
            except Exception as e:
                db.session.rollback()  # Rollback on any other error
                return jsonify({"message": "An error occurred"}), 500

            # #print(register.name.data,register.email.data)
    elif register.errors:
        flash(f"Account Creation Unsuccessful ", "error")
        #print(register.errors)

    # from myproject.models import user
    return render_template("manual_signup.html",register=register)


@app.route("/admin_signup", methods=["POST","GET"])
def admin_signup():

    register = Register()

    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if register.validate_on_submit():

        #print(f"Account Successfully Created for {register.name.data}")
        if request.method == 'POST':
            # context
            hashd_pwd = encry_pw.generate_password_hash(register.password.data).decode('utf-8')
            user1 = admin_user(name=register.name.data, email=register.email.data, password=hashd_pwd,
                         confirm_password=hashd_pwd, image="default.jpg", timestamp=datetime.now()
                         )

            try:
                email = Register().validate_email(register.email.data)
                if email:
                    return jsonify({"Error":"This email Already Exists"})
                db.session.add(user1)
                db.session.commit()
                flash(f"Account Successfully Created for {register.name.data}", "success")
                return redirect(url_for('login'))
            except IntegrityError:
                flash(f"Something went wrong, check for errors", "success")
                jsonify({"Error":"This Email Already Exists"})

            # #print(register.name.data,register.email.data)
    elif register.errors:
        flash(f"Account Creation Unsuccessful ", "error")
        #print(register.errors)

    # from myproject.models import user
    return render_template("manual_signup.html",register=register)


def update_zone(registration_form):
    zone = registration_form.church_zone.data
    
    # Check if 'zone' is part of the input data
    if 'zone' not in zone.split():
        zone += ' zone'  # Append "zone" with a space if it is not present

    return zone

@app.route("/usr_finish_signup", methods=["POST","GET"])
@login_required
def usr_finish_signup():

    user=None

    finish_register = UserAccountForm()

    user = church_user.query.get(current_user.id) 


    if finish_register.validate_on_submit():

        if request.method == 'POST':

            user.contacts=finish_register.contacts.data
            user.address=finish_register.address.data
            user.church_local=update_zone(finish_register)
            user.church_zone=finish_register.church_zone.data
            user.church_mission=finish_register.church_mission.data
            user.age_group=finish_register.age_group.data
            user.gender=finish_register.gender.data

            if finish_register.image.data:
                user.image = process_file(finish_register.image.data)

            db.session.commit()
            flash(f"Congratulations✨, You have just finished signing up for your FEA membership", "success")
            return redirect(url_for('home'))

    elif finish_register.errors:
        for error in finish_register.errors:
            print("Error: ", error)
        flash(f"Account Creation Unsuccessful", "error")

    # from myproject.models import user
    return render_template("usr_finish_signup.html",finish_register=finish_register,user=user)


@app.route("/admin_finish_signup", methods=["POST","GET"])
@login_required
def admin_finish_signup():

    user=None

    finish_register = AdminAccountForm()

    user = admin_user.query.get(current_user.id)

    if finish_register.validate_on_submit():

        if request.method == 'POST':

            user.contacts=finish_register.contacts.data
            user.address=finish_register.address.data
            user.church_local=finish_register.church_local.data
            user.church_zone=finish_register.church_zone.data
            user.church_mission=finish_register.church_mission.data
            user.pastor=finish_register.pastor.data
            user.committee_local_group=finish_register.committee_local_group.data
            user.committee_local_pos=finish_register.committee_local_pos.data
            user.committee_mission_grp=finish_register.committee_mission_grp.data
            user.committee_mission_pos=finish_register.committee_mission_pos.data
            user.age_group=finish_register.age_group.data
            user.gender=finish_register.gender.data
            user.senior_pastor=finish_register.senior_pastor.data

            if finish_register.image.data:
                user.image = process_file(finish_register.image.data)

            db.session.commit()
            flash(f"Update Successful.", "success")
            return redirect(url_for('home'))

    elif finish_register.errors:
        for error in finish_register.errors:
            print("Error: ",error)
        flash(f"Account Creation Unsuccessful ", "error")

    # from myproject.models import user
    return render_template("admin_finish_signup.html",finish_register=finish_register,user=user)


@app.route("/reset/<token>", methods=['POST', "GET"])
def reset(token):
    reset_form = Reset()

    if request.method == 'POST':

        # try:

        usr_obj = user_class().verify_reset_token(token)
        pass_reset_hash = encry_pw.generate_password_hash(reset_form.new_password.data)
        usr_obj = User.query.get(usr_obj)
        usr_obj.password = pass_reset_hash
        db.session.commit()

        flash(f"You have Successfully Changed your Password! You can now Login with your New Password", "success")

        return redirect(url_for("login"))
        # except:
        #     print("Password Reset Failed!!")
        #     flash(f"Password Reset Failed, Please try again later", "error")
        #     return f'Reset Failed, Try again later'

    return render_template("pass_reset.html", reset_form=reset_form)


@app.route("/forgot_password", methods=['POST', "GET"])
def reset_request():

    reset_request_form = Reset_Request()

    if current_user.is_authenticated:
        logout_user()

    if request.method == 'POST':
        if reset_request_form.validate_on_submit():
            # Get user details through their email
            usr_email = User.query.filter_by(email=reset_request_form.email.data).first()

            if usr_email is None:
                # print("The email you are request for is not register with T.H.T, please register first, Please Retry")
                flash("The email you are requesting a password reset for, is not registered, please register an account first",
                    'error')

                return redirect(url_for("reset_request"))

            def send_link(usr_email):
                app.config["MAIL_SERVER"] = "smtp.googlemail.com"
                app.config["MAIL_PORT"] = 587
                app.config["MAIL_USE_TLS"] = True
                em = app.config["MAIL_USERNAME"] = creds.get('email') #os.getenv("EMAIL")
                app.config["MAIL_PASSWORD"] = creds.get('gpass') # os.getenv("PWD")

                mail = Mail(app)

                token = user_class().get_reset_token(usr_email.id)
                msg = Message("Password Reset Request", sender="noreply@demo.com", recipients=[usr_email.email])
                msg.html = f"""<html>
<head>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f6f6f6;
            color: #333;
            padding: 20px;
        }}
        .container {{
            background-color: #ffffff;
            border-radius: 5px;
            padding: 20px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }}
        h2,h3 {{
            color: #4CAF50;
        }}
        p,li{{font-weight:500;color:#505050 }}
        .footer {{
            margin-top: 20px;
            font-size: 0.9em;
            color: #777;
        }}
        span{{ font-weight:600;color:coral}}
    </style>
</head>
<body>
    <div class="container">
        <img style="" src="https://africec.org/images/webimages/logo/logo.png" />
        <h2>Good day, {usr_email.name}</h2>

        <p>You have requested a password reset for your Church Registrations - A.E.C Account.</p>
        <p style="font-weight:600">To reset your password, visit the following link;</p>
        <a href="{url_for('reset', token=token, _external=True)}" 
            style="display: inline-block; padding: 10px 20px; font-size: 16px; color: #fff; background-color: #4CAF50; 
                    border: none; border-radius: 15px; text-decoration: none; text-align: center;">
            Reset
        </a>
        <p class="footer">If you did not request the above message please ignore it, and your password will remain unchanged.</p>
    </div>
</body>
</html>
"""

                try:
                    mail.send(msg)
                    flash('An email has been sent with instructions to reset your password', 'success')
                    return "Email Sent"
                except Exception as e:

                    flash('Ooops, Something went wrong Please Retry!!', 'error')
                    return "The mail was not sent"


            # Send the pwd reset request to the above email
            send_link(usr_email)

            return redirect(url_for('login'))

    return render_template("password_reset_req.html", reset_request_form=reset_request_form)


@app.route("/verification", methods=["POST", "GET"])
# User email verification @login
# @login the user will register & when the log in the code checks if the user is verified first...
def verification():

    usr_ = User.query.get(current_user.id)

    def send_veri_mail():

        app.config["MAIL_SERVER"] = "smtp.googlemail.com"
        app.config["MAIL_PORT"] = 587
        app.config["MAIL_USE_TLS"] = True
        # Creditentials saved in environmental variables
        em = app.config["MAIL_USERNAME"] = creds.get('email')  # os.getenv("MAIL")
        app.config["MAIL_PASSWORD"] =  creds.get('gpass') #os.getenv("PWD")
        app.config["MAIL_DEFAULT_SENDER"] = "noreply@gmail.com"

        mail = Mail(app)

        token = user_class().get_reset_token(current_user.id)
        usr_email = usr_.email

        msg = Message(subject="Email Verification", sender="no-reply@gmail.com", recipients=[usr_email])

        msg.html = f"""<html>
<head>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f6f6f6;
            color: #333;
            padding: 20px;
        }}
        .container {{
            background-color: #ffffff;
            border-radius: 5px;
            padding: 20px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }}
        h2,h3 {{
            color: #4CAF50;
        }}
        p,li{{font-weight:500;color:#505050 }}
        .footer {{
            margin-top: 20px;
            font-size: 0.9em;
            color: #777;
        }}
        span{{ font-weight:600;color:coral}}
    </style>
</head>
<body>
    <div class="container">
        <img style="" src="https://africec.org/images/webimages/logo/logo.png" />
        <h2>Hi, {usr_.name}</h2>

        <p>Please follow the link below to verify your email with Church Registrations - AEC:</p>
        <p style="font-weight:600">Verification link;</p>
        <a href="{ url_for('verified', token=token, _external=True) }" 
            style="display: inline-block; padding: 10px 20px; font-size: 16px; color: #fff; background-color: #4CAF50; 
                    border: none; border-radius: 15px; text-decoration: none; text-align: center;">
            Verify Email
        </a>
        <p class="footer">Thank you for registering an account!</p>
    </div>
</body>
</html>
"""


        # try:
        mail.send(msg)
        flash(f'An email has been sent with a verification link to your email account', 'success')
        log_out()
        return "Email Sent"
        # except Exception as e:
        #     flash(f'Email not sent here', 'error')
        #     return "The mail was not sent"

    # try:
    if not usr_.verified:
        send_veri_mail()
    else:
        log_out()
        return redirect(url_for("home"))
    # except:
    #     flash(f'Email Not Sent. Please try again', 'error')
    #     log_out()
    #     return redirect(url_for("login"))

    return render_template('verification.html')


@app.route("/verified/<token>", methods=["POST", "GET"])
# Email verification link verified with a token
def verified(token):
    # Check to verify the token received from the user email
    # process the user_id for the following script
    user_id = user_class.verify_reset_token(token)

    try:
        usr = User.query.get(user_id)
        usr.verified = True
        db.session.commit()
        if usr.verified:
            login_user(usr)
            # if not current_user.is_authenticated:
            #     if not current_user.church_local and not current_user.church_zone:
            print("Finish Setup")
            flash(f"Please Finish your Sign-up process", "success")
            return redirect(url_for('finish_signup'))
            # return redirect(url_for('account'))
    except Exception as e:
        flash(f"Something went wrong, Please try again ", "error")
        return redirect(url_for('home'))

    return render_template('verified.html')


@app.route('/logout')
def log_out():

    logout_user()

    return redirect(url_for('home'))


def add_column(cls,attr):
    with app.app_context():
        # Check if the 'age' column already exists
        if not hasattr(cls, attr):
            db.session.execute.text(f'ALTER TABLE {cls} ADD COLUMN {attr} INT;')
            db.session.commit()
            print(f"Column {attr} added successfully.")
        else:
            print(f"Column {attr}  already exists.")

def get_class_attributes(cls):
    # Use vars() to get instance attributes (for an instance of the class)
    # For the class itself, use cls.__dict__ to get class attributes
    class_attributes = vars(cls) if isinstance(cls, object) else cls.__dict__
    
    # Retrieve only the attribute names
    attribute_names = [name for name, value in class_attributes.items() if not callable(value) and not name.startswith('__') and not name.startswith('_')]
    
    return attribute_names

def get_table_columns():
    pass


# Function to get column names of a table
def get_table_columns(table):
    """Retrieve column names of a specified table."""
    inspector = inspect(db.engine)
    columns = [column['name'] for column in inspector.get_columns(table)]
    return columns

# User Account
@app.route("/user_account", methods=["POST", "GET"])
def user_account():

    # #Check Attributes for table update
    # cls_attributes = get_class_attributes(church_user) #It lists both inherited and local

    # # print("ATTRIBUTES: ", cls_attributes)

    # print("TABLE COLUMNS: ",church_user.__table_name__)

    # # Check if a class has parent classes and get their names
    # if __bases__ := church_user.__bases__:
    #     parent_names = [base.__name__ for base in __bases__]
    # else:
    #     parent_names = []

    # print("BASES: ",parent_names)

    # if parent_names:
    #     parent_attrs = get_table_columns(parent_names[0]) #returns only parent class attributes
    #     attrs_not_in_par = [attr for attr in cls_attributes if attr not in parent_attrs]
    #     clas = get_table_columns("church_user") 
    #     print("cls specific attributes: ",attrs_not_in_par)

    #     a = set(attrs_not_in_par)
    #     b = set(clas)
    #     add_attrs = a - b
    #     print("ATTRS TO BE ADDED: ",add_attrs)
    #     for attr in add_attrs:
    #         add_column(church_user.__table_name__,attr)


    account_form = UserAccountForm()

    usr_account=church_user.query.get(current_user.id)


    if account_form.validate_on_submit():

        if request.method == 'POST':

            usr_account.contacts=account_form.contacts.data
            usr_account.address=account_form.address.data
            usr_account.church_mission=account_form.church_mission.data
            usr_account.church_zone=account_form.church_zone.data
            usr_account.age_group=account_form.age_group.data
            usr_account.church_local=account_form.church_local.data
            usr_account.gender=account_form.gender.data
            usr_account.next_of_kin=account_form.next_of_kin.data
            usr_account.next_of_kin_no=account_form.next_of_kin_no.data
            usr_account.employ_status=account_form.employ_status.data
            usr_account.employer=account_form.employer.data
            usr_account.skills=account_form.skills.data
            usr_account.qualifications=account_form.qualifications.data
            usr_account.experience=account_form.experience.data

            if account_form.image.data:
                usr_account.image = process_file(account_form.image.data)

            # try:
            db.session.commit()
            flash(f"Update Successful!", "success")
            print("Update Successful!")


    return render_template('user_account.html',account_form =account_form, usr_account=usr_account)


# Admin Account
@app.route("/admin_account", methods=["POST", "GET"])
def admin_account():

    account_form = AdminAccountForm()
    usr_account=admin_user.query.get(current_user.id)

    if account_form.validate_on_submit():

        if request.method == 'POST':

            usr_account.contacts=account_form.contacts.data
            usr_account.church_mission=account_form.church_mission.data
            usr_account.church_zone=account_form.church_zone.data
            usr_account.age_group=account_form.age_group.data
            usr_account.church_local=account_form.church_local.data
            usr_account.gender=account_form.gender.data
            usr_account.next_of_kin=account_form.next_of_kin.data
            usr_account.next_of_kin_no=account_form.next_of_kin_no.data
            usr_account.employ_status=account_form.employ_status.data
            usr_account.employer=account_form.employer.data
            usr_account.skills=account_form.skills.data
            usr_account.qualifications=account_form.qualifications.data
            usr_account.experience=account_form.experience.data
            usr_account.pastor=account_form.pastor.data
            usr_account.committee_local_pos=account_form.committee_local_pos.data
            usr_account.committee_local_group=account_form.committee_local_group.data
            usr_account.committee_mission_grp=account_form.committee_mission_grp.data
            usr_account.committee_mission_pos=account_form.committee_mission_pos.data
            usr_account.senior_pastor=account_form.senior_pastor.data

            if account_form.image.data:
                usr_account.image = process_file(account_form.image.data)

            # try:
            db.session.commit()
            flash(f"Update Successful!", "success")
            print("Update Successful!")

    return render_template('admin_account.html',usr_account=usr_account,account_form=account_form)


@app.route("/fea_calender", methods=["POST","GET"])
def fea_calender():


    return render_template("fea_calender.html")


@app.route("/google_signup", methods=["POST","GET"])
def google_signup():

    return render_template('google_signup.html')

#google login
@app.route("/google_login", methods=["POST","GET"])
def google_login():

    # print("DEBUG CREDITENTAILS: ",appConfig.get("OAUTH2_CLIENT_ID"),' ',appConfig.get("OAUTH2_CLIENT_SECRET"))

    return oauth.fearegistra.authorize_redirect(redirect_uri=url_for("google_signin",_external=True))


#login redirect
@app.route("/google_signin", methods=["POST","GET"])
def google_signin():

    token = oauth.fearegistra.authorize_access_token()

    session['user'] = token

    pretty=session.get("user")

    usr_info = pretty.get('userinfo')
    verified = usr_info.get("email_verified")
    usr_email = usr_info.get("email")
    usr_name=usr_info.get("name")
    usr_athash=usr_info.get("at_hash")

    if not verified:
        print("VERIFIED CHECK: ", verified)
        flash("Access Denied!, Your Email is not verified with Google")
        flash("Please, Set up your account manually")
        return redirect(url_for('login'))
    
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    #Sign Up
    if not User.query.filter_by(email=usr_email).first():

        print("Email Not Found!, We will register")

        # context
        hashd_pwd = encry_pw.generate_password_hash(usr_athash).decode('utf-8')
        user1 = church_user(name=usr_name, email=usr_email, password=hashd_pwd,
                        confirm_password=hashd_pwd, image="default.jpg",timestamp=datetime.now(),verified=True)

        try:
            db.session.add(user1)
            db.session.commit()

            #Login user
            usr_obj = User.query.filter_by(email=usr_email).first()
            login_user(usr_obj)

            if not current_user.church_local and not current_user.church_zone:

                # flash(f"Welcome! {usr_obj.name.title()}, Please Finish Part II of your Sign-up Process", "success")
                return redirect(url_for('finish_signup'))
        
        except IntegrityError:
            db.session.rollback()  # Rollback the session on error
            return jsonify({"message": "Email already exists"}), 409
        
        except Exception as e:
                db.session.rollback()  # Rollback on any other error
                return jsonify({"message": "An error occurred", "error": str(e)}), 500
        
    else:
        usr_obj = User.query.filter_by(email=usr_email).first()
        login_user(usr_obj)
        req_page = request.args.get('next')
        flash(f"Hello! {usr_obj.name.title()} You're Logged In!", "success")

        if not current_user.church_local and not current_user.church_zone:
            print("Finish Setup")
            flash(f"Please Finish your Sign-up process", "success")
            return redirect(url_for('finish_signup'))
    
        return redirect(req_page) if req_page else redirect(url_for('home'))

    return redirect(url_for("home"))

#Verification Pending
@app.route("/login", methods=["POST","GET"])
def login():

    login = Login()

    if login.validate_on_submit():

        if request.method == 'POST':

            user_login = User.query.filter_by(email=login.email.data).first()
            if user_login and encry_pw.check_password_hash(user_login.password, login.password.data):

                # if not user_login.verified:
                #     login_user(user_login)
                #     return redirect(url_for('verification'))
                # else:
                    # After login required prompt, take me to the page I requested earlier
                    login_user(user_login)
                    print("No Verification Needed: ", user_login.verified)
                    req_page = request.args.get('next')
                    flash(f"Hey! {user_login.name.title()} You're Logged In!", "success")

                    if not current_user.church_local and not current_user.church_zone:
                        print("Finish Setup")
                        flash(f"Please Finish Up your Sign-up process", "success")
                        if current_user.role == "church_user":
                            return redirect(url_for('usr_finish_signup'))
                        else:
                            return redirect(url_for('admin_finish_signup'))
                
                    return redirect(req_page) if req_page else redirect(url_for('home'))
                
            else:
                flash(f"Login Unsuccessful, please use correct email or password", "error")
                # print(login.errors)
    else:
        print("No Validation")
        if login.errors:
            for error in login.errors:
                print("Errors: ", error)
        else:
            print("No Errors found", login.email.data, login.password.data)

    return render_template("login.html",login=login)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    with app.app_context():
       db.create_all()

    app.run(debug=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
