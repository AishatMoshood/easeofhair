import os, math, random, re
from flask import make_response, render_template, request, abort, redirect, flash, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer
from easetestprojapp import app, db, Message, mail
from easetestprojapp.mymodels import Booking, Customer, Salon, Service, Service_type, Salon_servicetype


@app.route('/salon/signup')
def salon_signup():
    loggedin = session.get('loggedin')
    salon_loggedin = session.get('salon_loggedin')

    if (loggedin != None) or (salon_loggedin != None):
        flash('Please log out of current account to sign up')
        return redirect('/')
    else:
        return render_template('user/signup.html')


@app.route('/salon/signup/submit', methods=['POST'])
def salon_signup_submit():
    sfname = request.form.get('sfname')
    slname = request.form.get('slname')
    salonname = request.form.get('salonname')
    semail = request.form.get('semail')
    spwd = request.form.get('spwd')
    sconfpwd = request.form.get('sconfpwd')
    saddress = request.form.get('address')
    sphone = request.form.get('salonphn')
    vals = request.form.values()

    sal = Salon.query.filter(Salon.salon_email==semail).first()
    chkSalName = Salon.query.filter(Salon.salon_name==salonname).first()

    namereg = "([0-9])"
    namereg2 = "([a-zA-Z])"
    pwdreg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,}$"

    if re.search(namereg, sfname) or re.search(namereg, slname):
            flash("Please ensure First name and Last name doesn't contain digits.")
            return redirect('/salon/signup')
        
    if re.search(namereg2, sfname) == None or re.search(namereg2, slname) == None:
        flash("Please ensure First name and Last name are valid.")
        return redirect('/salon/signup')

    if re.match(pwdreg, spwd) == None:
        flash("Please entered password should contain at least; one capital Letter, one special character, one digit and length should be at least 8.")
        return redirect('/salon/signup')

    if '' in vals:
        flash('Please complete all fields')
        return redirect('/salon/signup')
    elif spwd != sconfpwd:
        flash('The two passwords must match')
        return redirect('/salon/signup')
    elif sal:
        flash('This Email is taken')
        return redirect('/salon/signup')
    elif chkSalName:
        flash('This salon name has already been used')
        return redirect('/salon/signup')
    else:
        encryptedpwd = generate_password_hash(spwd)

        s = Salon(salon_ownerfname=sfname, salon_ownerlname=slname, salon_name=salonname, salon_email=semail, salon_pwd=encryptedpwd, salon_address=saddress, salon_phone=sphone)

        db.session.add(s)
        db.session.commit()

        id = s.salon_id
        session['salon_loggedin'] = id

        flash('Registration Successful') 
        return redirect('/salon/login')



@app.route('/salon/login', methods=['POST','GET'])
def salon_login():
    loggedin = session.get('loggedin')
    salon_loggedin = session.get('salon_loggedin')

    if (loggedin != None) or (salon_loggedin != None):
        flash('Please log out of current account, to login to another one')
        return redirect('/')
    else:
        if request.method == 'GET':
            return render_template('salon/login.html')
        else:
            username = request.form.get('username')
            pwd = request.form.get('pwd')

            if username == '' or pwd == '':
                flash('Please Complete all fields')
                return redirect('/salon/login')
            else:
                salondeets = Salon.query.filter(Salon.salon_email==username).first()
                
                if salondeets:
                    chk = salondeets.salon_pwd
                    formatted = check_password_hash(chk,pwd)

                    if formatted:
                        id = salondeets.salon_id
                        session['salon_loggedin'] = id
                        return redirect('/salon/dashboard')
                    else:
                        flash('Invalid Credentials')
                        return redirect('/salon/login')
                else:
                    flash("Please reconfirm details")
                    return redirect('/salon/login')


@app.route('/salon/dashboard')
def salon_dashboard():
    salon_loggedin = session.get('salon_loggedin')
    if salon_loggedin == None:
        return redirect('/')
    else:
        salondeets = Salon.query.get(salon_loggedin)
        return render_template('salon/salondashboard.html', salondeets=salondeets)


@app.route('/salon/settings', methods=['POST','GET'])
def salon_settings():
    salon_loggedin = session.get('salon_loggedin')
    if salon_loggedin == None:
        return redirect('/')
    else:
        service_type = Service_type.query.all()
        salondeets = Salon.query.get(salon_loggedin)
        service = Service.query.get(salon_loggedin)
        all_services = Service.query.filter(Service.serv_salonid==salon_loggedin).all()
        return render_template('salon/salonsettings.html', service_type=service_type, salondeets=salondeets, service=service, all_services=all_services)


@app.route('/salon/update/<id>', methods=['POST'])
def salon_update(id):
    salon_loggedin = session.get('salon_loggedin')
    
    if salon_loggedin == None:
        return redirect('/')
    else:
        fname = request.form.get('sfname')
        lname = request.form.get('slname')
        salonname = request.form.get('salonname')
        address = request.form.get('address')
        email = request.form.get('semail')
        salonphn = request.form.get('salonphn')
        pref = request.form.getlist('preference')
        salonimg =request.files.get('salonimg')

        if int(salon_loggedin) == int(id):
            s = Salon.query.get(id)
            servs = Service.query.get(id)
            serv_type = Service_type.query.get(id)

            for p in pref:
                servs_filter = Service.query.filter(Service.serv_salonid == id, Service.serv_servtypeid == p).all() 
                if not servs_filter:
                    servadd = Service(serv_salonid=id, serv_servtypeid=p)
                    db.session.add(servadd) 
                db.session.commit()


            all_servs = Service.query.filter(Service.serv_salonid==s.salon_id).all()   

            for a in all_servs:
                sal_servtype = Salon_servicetype(salonserv_salonid=s.salon_id, salonserv_servtypeid=serv_type.servtype_id)
                db.session.add(sal_servtype)
            db.session.commit()

            if all_servs:
                s.salon_status = '1'
            db.session.commit()

            org_file = salonimg.filename
            extension = os.path.splitext(org_file)
            fn = math.ceil(random.random() * 10000000)
            img_save = str(fn) + extension[1]
            salonimg.save(f'easetestprojapp/static/salon_images/{img_save}')
            
            s.salon_ownerfname = fname
            s.salon_ownerlname = lname
            s.salon_name = salonname
            s.salon_address = address
            s.salon_email = email
            s.salon_phone = salonphn
            s.salon_image = img_save
            
            db.session.add(s)
            db.session.commit()

            flash('Changes Made Successfully')
            return redirect('/salon/dashboard')


@app.route('/salon/logout')
def salon_logout():
    salon_loggedin = session.get('salon_loggedin')
    if salon_loggedin == None:
        return redirect('/')
    else:
        session.pop('salon_loggedin')
        return redirect('/salon/login')


@app.route('/salon/bookings/<id>')
def salon_bookings(id):
    salon_loggedin = session.get('salon_loggedin')
    if salon_loggedin == None:
        return redirect('/')
    else:
        salondeets = Salon.query.get(salon_loggedin)
        s = Salon.query.get(id)
        b = Booking.query.filter(Booking.book_salonid == salon_loggedin).all()
        msg = print('You do not have any bookings at this moment, you will get an email once a user books your service(s). In the meantime you can explore some of our other services.')
        return render_template('salon/salonbookings.html', b=b, salondeets=salondeets, msg=msg)


@app.route('/salon/delete/booking/<id>')
def salon_del_book(id):
    salon_loggedin = session.get('salon_loggedin')
    if salon_loggedin == None:
        return redirect('/')
    else:
        delbook = Booking.query.get(id)

        db.session.delete(delbook)
        db.session.commit()
        return redirect('/salon/bookings/salon_loggedin')


@app.route('/salon/delete/service/<id>')
def salon_del_service(id):
    salon_loggedin = session.get('salon_loggedin')
    if salon_loggedin == None:
        return redirect('/')
    else:
        delserv = Service.query.get(id)

        db.session.delete(delserv)
        db.session.commit()
        return redirect('/salon/services')


@app.route('/salon/check/mail', methods=["POST","GET"])
def salon_check_mail():
    salon_loggedin = session.get('salon_loggedin')
    salondeets = Salon.query.get(salon_loggedin)
    return render_template('salon/checkmail.html', salondeets=salondeets)


@app.route('/salon/reset/password', methods=["POST","GET"])
def salon_reset_pwd():
    if request.method == "GET":
        return render_template('salon/resetpassword.html')
    else:
        email = request.form.get("forgotpwdemail")

        if email != '':
            try:
                salon = Salon.query.filter(Salon.salon_email==email).first()
            except:
                flash('Invalid email address!', 'error')
                return render_template('salon/resetpassword.html', 'error')

            if salon:
                def salon_send_password_reset_link(salon_email):
                    password_reset_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

                    password_reset_url = url_for(
                        'salon_token_reset',
                        token = password_reset_serializer.dumps(salon_email, salt='password-reset-salt'),
                        _external=True)
                    
                    msg = Message('Password Reset Requested', sender = 'aishatmoshood1@gmail.com', recipients = [salon_email])
                    msg.body = f'Find below the requested link for your password reset {password_reset_url}'
                    mail.send(msg)
                    
                salon_send_password_reset_link(email)
                flash('Please check your email for a password reset link.', 'success')
            else:
                flash('No record of email.', 'error')
                return redirect('/salon/reset/password')
        else:
            flash('Please input your email address', 'error')
            return redirect('/salon/reset/password')

        return redirect('/salon/check/mail')


@app.route('/salon/reset/<token>', methods=["GET", "POST"])
def salon_token_reset(token):
    if request.method == 'GET':
        return render_template('salon/inputpassword.html',token=token)
    else:
        try:
            password_reset_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
            email = password_reset_serializer.loads(token, salt='password-reset-salt', max_age=3600)
        except:
            flash('The password reset link is invalid or has expired.', 'error')
            return redirect(url_for('salon_login'))

        pwd = request.form.get('resetpwd')
        pwdreg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,}$"

        if pwd != '':
            if re.match(pwdreg, pwd) == None:
                flash("Please entered password should contain at least; one capital Letter, one special character, one digit and length should be at least 8.")
                redirect('/salon/reset/<token>')
            else:     
                salon = Salon.query.filter(Salon.salon_email==email).first()
                
                salon.salon_pwd = generate_password_hash(pwd).decode('utf-8')
                db.session.add(salon)
                db.session.commit()
                flash('Your password has been updated!', 'success')
                return redirect(url_for('salon_login'))
        else:
            flash('Please input a new password', 'error')
            return redirect('/salon/reset/<token>')
    
    return redirect('/salon/login')


@app.route('/salon/services/')
def salon_services():
    salon_loggedin = session.get('salon_loggedin')
    if salon_loggedin == None:
        return redirect('/')
    else:
        salondeets = Salon.query.get(salon_loggedin)
        sal_servs = Service.query.filter(Service.serv_salonid==salon_loggedin).all()
        return render_template('salon/salonservices.html', salondeets=salondeets, sal_servs=sal_servs)


      



