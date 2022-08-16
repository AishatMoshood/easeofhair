import math
import random
import os
import requests
import json
import re
from flask import render_template, request, redirect, flash, session, url_for
from sqlalchemy import desc
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer
from easetestprojapp import app, db, Message, mail
from easetestprojapp.mymodels import Book_service, Customer, Payment, Salon, Booking, Service_type, Service, Book_pay


@app.route('/')
def home():
    loggedin = session.get('loggedin')
    cust_deets = Customer.query.get(loggedin)
    all_salons = Salon.query.filter(Salon.salon_status == '1').limit(3)
    service_type = Service_type.query.all()
    servs51 = Service_type.query.order_by(Service_type.servtype_name).limit(5)
    servs52 = Service_type.query.order_by(desc( Service_type.servtype_id),Service_type.servtype_name).limit(5)
    recent_sals = Salon.query.filter(Salon.salon_status == '1').order_by(desc(Salon.salon_id)).order_by(Salon.salon_name).limit(3)
    salon_loggedin = session.get('salon_loggedin')
    salondeets = Salon.query.get(salon_loggedin)
    sal_count = Salon.query.count()
    return render_template('user/home.html', cust_deets=cust_deets, all_salons=all_salons, service_type=service_type, recent_sals=recent_sals,salondeets=salondeets, servs51=servs51, servs52=servs52, sal_count=sal_count)


@app.route('/signup')
def signup():
  return render_template('user/signup.html')


@app.route('/signup/submit', methods=['POST'])
def signup_submit():
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    email = request.form.get('email')
    pwd = request.form.get('pwd')
    confpwd = request.form.get('confpwd')
    gender = request.form.get('gender')
    vals = request.form.values()

    chkEmail = Customer.query.filter(Customer.cust_email==email).first()

    namereg = "([0-9])"
    namereg2 = "([a-zA-Z])"
    pwdreg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,}$"

    if re.search(namereg,fname) or re.search(namereg,lname):
            flash("Please ensure First name and Last name don't contain digits.")
            return redirect('/signup')
        
    if re.search(namereg2,fname) == None or re.search(namereg2,lname) == None:
        flash("Please ensure First name and Last name are valid.")
        return redirect('/signup')

    if re.match(pwdreg,pwd) == None:
        flash("Password: at least, 1 uppercase, 1 lowercase, 1 special character, 1 digit and at least, 8 characters in length")
        return redirect('/signup')

    if '' in vals:
        flash('Please complete all fields')
        return redirect('/signup')
    elif pwd != confpwd:
        flash('Please make sure both passwords are the same')
        return redirect('/signup')
    elif chkEmail:
        flash('This Email is taken')
        return redirect('/signup')
    else:
        encryptedpwd = generate_password_hash(pwd)

        c = Customer(cust_fname=fname, cust_lname=lname,
                     cust_email=email, cust_pwd=encryptedpwd, cust_gender=gender)

        db.session.add(c)
        db.session.commit()

        id = c.cust_id
        session['loggedin'] = id

        flash('Registration Successful, you can login now')
        return redirect('/user/login')


@app.route('/userdashboard')
def userdash():
    loggedin = session.get('loggedin')
    if loggedin == None:
        return redirect('/')
    else:
        custdeets = Customer.query.get(loggedin)
        return render_template('user/userdashboard.html', custdeets=custdeets)


@app.route('/user/login', methods=['POST', 'GET'])
def user_login():
    loggedin = session.get('loggedin')
    salon_loggedin = session.get('salon_loggedin')

    custdeets = Customer.query.get(loggedin)

    if (loggedin != None) or (salon_loggedin != None):
        flash('Please log out of current account, to login to another one')
        return redirect('/all/salons')
    else:
        if request.method == 'GET':
            return render_template('user/login.html', custdeets=custdeets)
        else:
            username = request.form.get('username')
            pwd = request.form.get('pwd')
            if username != '' and pwd != '':
                deets = Customer.query.filter(Customer.cust_email == username).first()
                
                if deets:
                    chk = deets.cust_pwd
                    formatted = check_password_hash(chk,pwd)

                    if formatted:
                        id = deets.cust_id
                        session['loggedin'] = id
                        return redirect('/userdashboard')
                    else:
                        flash('Invalid Credentials')
                        return redirect('/user/login')
                else:
                    flash("Please reconfirm details")
                    return redirect('/user/login')
            else:
                flash('Please complete all fields')
                return redirect('/user/login')


@app.route('/user/settings')
def user_settings():
    loggedin = session.get('loggedin')
    if loggedin == None:
        return redirect('/')
    else:
        custdeets = Customer.query.get(loggedin)
        return render_template('user/usersettings.html', custdeets=custdeets)


@app.route('/user/update/<id>', methods=['POST'])
def user_update(id):
    loggedin = session.get('loggedin')
    if loggedin == None:
        return redirect('/')
    else:
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        email = request.form.get('email')
        phone = request.form.get('phone')
        img = request.files.get('img')

        original_file = img.filename
        extension = os.path.splitext(original_file)
        fn = math.ceil(random.random() * 100000000)
        save_as = str(fn) + extension[1]

        if extension[1].lower() in ['.jpg', '.png', '.jpeg', '.webp', '.svg']:
            img.save(f'easetestprojapp/static/user_images/{save_as}')
    
        if int(loggedin) == int(id):
            c = Customer.query.get(id)
            
            c.cust_fname = fname
            c.cust_lname = lname
            c.cust_email = email
            c.cust_phone = phone
            c.cust_img = save_as
            db.session.add(c)
            db.session.commit()

        flash('Changes Made Successfully')
        return redirect('/userdashboard')


@app.route('/logout')
def logout():
    loggedin = session.get('loggedin')
    if loggedin == None:
        return redirect('/')
    else:
        session.pop('loggedin')
        return redirect('/user/login')


@app.route('/about')
def about():
    loggedin = session.get('loggedin')
    custdeets = Customer.query.get(loggedin)
    return render_template('user/about.html', custdeets=custdeets)


@app.route('/layout')
def layout():
    loggedin = session.get('loggedin')
    cust_deets = Customer.query.get(loggedin)
    return render_template('user/layout.html', cust_deets=cust_deets)


@app.route('/book/salon/<id>', methods=['POST', 'GET'])
def book_salon(id):
    loggedin = session.get('loggedin')
    salon_loggedin = session.get('salon_loggedin')

    if salon_loggedin != None:
        flash('You can only book a salon with a customer account, please login to your customer account.', 'error')
        return redirect('/all/salons')
    else:
        if loggedin == None:
            return redirect('/user/login')
        else:    
            if request.method == 'GET':
                all_salons = Salon.query.get(id)
                servs = Service.query.filter(Service.serv_salonid == id).all()
                cust_deets = Customer.query.get(loggedin)
                return render_template('user/booksalon.html', all_salons=all_salons, servs=servs, cust_deets=cust_deets)
            else:
                s = Salon.query.get(id)
                cust = Customer.query.get(loggedin)

                date = request.form.get('date')
                time = request.form.get('time')
                servs = request.form.getlist('services')

                b = Booking(book_salonid=s.salon_id, book_custid=loggedin,
                            book_date=date, book_time=time)
                db.session.add(b)
                db.session.commit()

                for v in servs:
                    bserv = Book_service(bserv_bookid=b.book_id, bserv_servid=v)
                    db.session.add(bserv)
                db.session.commit()

                bookid = b.book_id
                session['booked'] = bookid

                return redirect('/booking/summary')


@app.route('/booking/summary', methods=['POST', 'GET'])
def booking_sum():
    loggedin = session.get('loggedin')
    cust_deets = Customer.query.get(loggedin)

    booked = session.get('booked')
    bookdeets = Booking.query.get(booked)

    bservdeets = Book_service.query.filter(Book_service.bserv_bookid == bookdeets.book_id).all()
    
    refno = math.ceil(random.random() * 1000000000)

    if loggedin == None:
        return redirect('/user/login')
    else:
        if request.method == 'GET':
            return render_template('user/booksummary.html', cust_deets=cust_deets, bookdeets=bookdeets, bservdeets=bservdeets)
        else:
            tot = request.form.get('tot')

            for bs in bservdeets:
                bkpay = Book_pay(bookpay_amt=tot, bookpay_ref=refno,
                                 bookpay_bookservid=bs.bserv_id,bookpay_bookcustid=loggedin,bookpay_booksalonid=bookdeets.book_salonid)
                db.session.add(bkpay)
            db.session.commit()

            p = Payment(pay_amt=tot, pay_refno=refno, pay_stat='completed',pay_salonid=bookdeets.book_salonid,pay_custid=loggedin, pay_bookid=bookdeets.book_id)

            db.session.add(p)
            db.session.commit()

            session['total'] = tot
            session['ref'] = refno
            return redirect('/user/payment')


@app.route('/user/payment')
def user_payment():
    loggedin = session.get('loggedin')
    custdeets = Customer.query.get(loggedin)

    booked = session.get('booked')
    bookdeets = Booking.query.get(booked)

    refnum = session.get('ref')

    bservdeets = Book_service.query.filter(
        Book_service.bserv_bookid == bookdeets.book_id).all()
    bservdeets2 = Book_service.query.filter(
        Book_service.bserv_bookid == bookdeets.book_id).first()

    bpaydeets = Book_pay.query.filter(
        Book_pay.bookpay_bookservid == Book_service.bserv_id).first()

    amtdeets = Book_pay.query.filter(Book_pay.bookpay_ref == refnum).first()

    if loggedin == None or refnum == None or amtdeets == None:
        return redirect('/')
    else:
        if request.method == 'GET':
            return render_template('user/payment.html', custdeets=custdeets, bservdeets=bservdeets, bservdeets2=bservdeets2, bpaydeets=bpaydeets, refnum=refnum, amtdeets=amtdeets)
        else:   

            url = "https://api.paystack.co/transaction/initialize"

            data = {'email': custdeets.cust_email,
                    'amount': amtdeets.bookpay_amt, 'ref': amtdeets.bookpay_ref, 'status':'Transaction Completed'}

            headers = {'Content-Type': 'application/json',
                       'Authorization': 'Bearer sk_test_cd05140387131fa0a4b595e1a7d8a2b1b9ae6b76'}

            response = requests.post(
                'https://api.paystack.co/transaction/initialize', headers=headers, data=json.dumps(data))

            rspjson = json.loads(response.text)

            if rspjson.get('status') == True:
               
                authurl = rspjson['data']['authorization_url']

                return redirect(authurl)   
            else:
                return 'Please try again'



@app.route('/user/confirmpay')
def confirm_pay():
    loggedin = session.get('loggedin')
    if loggedin == None:
        return redirect('/')
    else:
        cust_deets = Customer.query.get(loggedin)
        return render_template('user/confirmpay.html', cust_deets=cust_deets)


@app.route('/user/dashboard/payment')
def dashboard_payment():
    loggedin = session.get('loggedin')
    custdeets = Customer.query.get(loggedin)
    if loggedin == None:
        return redirect('/')
    else:
        paydeets = Payment.query.filter(Payment.pay_custid==loggedin).all()
        return render_template('user/userpayment_dashboard.html', paydeets=paydeets, custdeets=custdeets)



@app.route('/user/bookings')
def user_bookings():
    loggedin = session.get('loggedin')
    if loggedin == None:
        return redirect('/')
    else:
        custdeets = Customer.query.get(loggedin)
        b = Booking.query.filter(Booking.book_custid == loggedin).all()
        msg = 'You have not booked for a salon yet. Book now to enjoy the best service you can get, while also qualifying for bonuses and other benefits.'
        return render_template('user/userbookings.html', b=b, custdeets=custdeets, msg=msg)


@app.route('/user/services')
def user_services():
    loggedin = session.get('loggedin')
    cust_deets = Customer.query.get(loggedin)
    return render_template('user/services.html', cust_deets=cust_deets)


@app.route('/all/salons')
def all_salons():
    loggedin = session.get('loggedin')
    cust_deets = Customer.query.get(loggedin)
    all_salons = Salon.query.order_by(Salon.salon_name)
    return render_template('user/allsalons.html', cust_deets=cust_deets, all_salons=all_salons)


@app.route('/user/search', methods=['GET','POST'])
def user_search():
    loggedin = session.get('loggedin')
    cust_deets = Customer.query.get(loggedin)

    if request.method == 'GET':
        return redirect('/')
    else:
        locationdrop = request.form.get('locationdrop')
        servicedrop = request.form.get('servicedrop')
        searchkey = request.form.get('searchkey')

        locationsearch = '%{}%'.format(locationdrop)
        searchkey = '%{}%'.format(searchkey)
    
        filterstr = ''
        loc_res = ''
        serv_res = ''
        input_res = ''
        both_res = ''

        if locationdrop != '':
            filterstr = filterstr + (Salon.salon_address.like(locationsearch))
            loc_res = db.session.query(Salon).filter(filterstr).all()
        if servicedrop != '':
            serv_res = Service.query.filter(Service.serv_servtypeid == servicedrop).all()
        if searchkey != '':
            filterstr = filterstr + (Salon.salon_name.like(searchkey))
            input_res = db.session.query(Salon).filter(filterstr).all()
            
        return render_template('user/search.html', cust_deets=cust_deets, serv_res=serv_res, loc_res=loc_res, both_res=both_res, input_res=input_res)


@app.route('/user/check/mail', methods=["POST","GET"])
def check_mail():
    loggedin = session.get('loggedin')
    cust_deets = Customer.query.get(loggedin)
    return render_template('user/checkmail.html', cust_deets=cust_deets)


@app.route('/user/reset/password', methods=["POST","GET"])
def reset_pwd():
    if request.method == "GET":
        return render_template('user/resetpassword.html')
    else:
        email = request.form.get("forgotpwdemail")

        if email != '':
            try:
                user = Customer.query.filter(Customer.cust_email==email).first()
            except:
                flash('Invalid email address!', 'error')
                return render_template('user/resetpassword.html', 'error')

            if user:
                def send_password_reset_link(user_email):
                    password_reset_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

                    password_reset_url = url_for(
                        'token_reset',
                        token = password_reset_serializer.dumps(user_email, salt='password-reset-salt'),
                        _external=True)

                    
                    msg = Message('Password Reset Requested', sender = 'aishatmoshood1@gmail.com', recipients = [user_email])
                    msg.body = f'Find below the requested link for your password reset {password_reset_url}'
                    mail.send(msg)
                    
                send_password_reset_link(email)
                flash('Please check your email for a password reset link.', 'success')
            else:
                flash('No record of email.', 'error')
                return redirect('/user/reset/password')
        else:
            flash('Please input your email address', 'error')
            return redirect('/user/reset/password')

        return redirect('/user/check/mail')


@app.route('/reset/<token>', methods=["GET", "POST"])
def token_reset(token):
    if request.method == 'GET':
        return render_template('user/inputpassword.html',token=token)
    else:
        try:
            password_reset_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
            email = password_reset_serializer.loads(token, salt='password-reset-salt', max_age=3600)
        except:
            flash('The password reset link is invalid or has expired.', 'error')
            return redirect(url_for('user_login'))

        pwd = request.form.get('resetpwd')
        pwdreg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,}$"

        if pwd != '':
            if re.match(pwdreg, pwd) == None:
                flash("Please entered password should contain at least; one capital Letter, one special character, one digit and length should be at least 8.")
                return redirect('/reset/<token>')
            else:
                user = Customer.query.filter(Customer.cust_email==email).first()
                user.cust_pwd = generate_password_hash(pwd).decode('utf-8')
                db.session.add(user)
                db.session.commit()
                flash('Your password has been updated!', 'success')
                return redirect(url_for('user_login'))
        else:
            flash('Please input a new password', 'error')
            return redirect('/reset/<token>')
    
    return redirect('/user/login')


@app.errorhandler(404)
def errorpage(Error):
    return render_template("user/error.html"),404

