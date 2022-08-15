from flask import make_response, render_template, request, abort, redirect, flash, session
from sqlalchemy import desc
from easetestprojapp import app, db
from easetestprojapp.mymodels import Customer, Admin, Salon, Service_type
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/admin/signup', methods=['GET','POST'])
def admin_signup():
    loggedin = session.get('loggedin')
    salon_loggedin = session.get('salon_loggedin')
    admin_loggedin = session.get('admin_loggedin')

    if (loggedin != None) or (salon_loggedin != None):
        return redirect('/')
    elif admin_loggedin != None:
        flash("You can't sign up again")
        return redirect('/')
    else:
        if request.method == 'GET':
            return render_template('admin/signup.html')
        else:
            username = request.form.get('username')
            pwd = request.form.get('pwd')
            confpwd = request.form.get('confpwd')

            if username == '' or pwd == '':
                flash('Complete all fields')
                return redirect('/admin/signup')
            elif pwd != confpwd:
                flash('The two passwords must match')
                return redirect('/admin/signup')
            else:
                format = generate_password_hash(pwd)
                a = Admin(admin_username=username, admin_password=format)

                db.session.add(a)
                db.session.commit()

                flash('Registration Successful')
                return redirect('/admin/home')


@app.route('/admin/home', methods=['POST','GET'])
def admin_home():
    loggedin = session.get('loggedin')
    salon_loggedin = session.get('salon_loggedin')

    if (loggedin != None) or (salon_loggedin != None):
        return redirect('/')
    else:
        if request.method == 'GET':
            return render_template('admin/login.html')
        else:
            username = request.form.get('username')
            pwd = request.form.get('pwd')

            if username == '' or pwd == '':
                flash('Complete all fields')
                return redirect('/admin/home')    
            else:
                admindeets = Admin.query.filter(Admin.admin_username==username).first()
                chk = admindeets.admin_password
                formatted = check_password_hash(chk,pwd)

                if admindeets and formatted:
                    id = admindeets.admin_id
                    session['admin_loggedin'] = id
                    return redirect('/admin/dashboard')
                else:
                    flash('Invalid Credentials')
                    return redirect('/admin/home')


@app.route('/admin/dashboard')
def admin_dashboard():
    admin_loggedin = session.get('admin_loggedin')
    if admin_loggedin == None:
        return redirect('/')
    else:
        tot_sals = Salon.query.all()
        tot_cust = Customer.query.all()
        admindeets = Admin.query.get(admin_loggedin)
        act_sals = Salon.query.filter(Salon.salon_status=='1').all()
        return render_template('admin/admin_layout.html', admindeets=admindeets, tot_sals=tot_sals, tot_cust=tot_cust, act_sals=act_sals)


@app.route('/admin/salons')
def admin_salons():
    admin_loggedin = session.get('admin_loggedin')
    if  admin_loggedin== None:
        return redirect('/')
    else:
        admindeets = Admin.query.get(admin_loggedin)
        all_salons = Salon.query.all()
        return render_template('admin/salons.html', admindeets=admindeets,  all_salons=all_salons)


@app.route('/admin/deletesalon/<id>')
def admin_delsal(id):
    admin_loggedin = session.get('admin_loggedin')
    if admin_loggedin == None:
        return redirect('/')
    else:
        s = Salon.query.get(id)
        db.session.delete(s)
        db.session.commit()
        return redirect('/admin/salons')


@app.route('/admin/logout')
def admin_logout():
    admin_loggedin = session.get('admin_loggedin')
    if admin_loggedin == None:
        return redirect('/')
    else:
        session.pop('admin_loggedin')
        return redirect('/admin/home')


@app.route('/admin/services')
def services():
    admin_loggedin = session.get('admin_loggedin')
    if admin_loggedin == None:
        return redirect('/')
    else:
        admindeets = Admin.query.get(admin_loggedin)
        servs = Service_type.query.all()
        return render_template('admin/services.html', servs=servs,  admindeets=admindeets)

@app.route('/admin/delete/service/<id>')
def del_service(id):
    admin_loggedin = session.get('admin_loggedin')
    if admin_loggedin == None:
        return redirect('/')
    else:
        delserv = Service_type.query.get(id)

        db.session.delete(delserv)
        db.session.commit()

        flash(f'Deleted successfully')
        return redirect('/admin/services')


@app.route('/admin/addservice', methods=['POST','GET'])
def add_service():
    admin_loggedin = session.get('admin_loggedin')
    if admin_loggedin == None:
        return redirect('/')
    else:
        admindeets = Admin.query.get(admin_loggedin)

        if request.method == 'GET':
            return render_template('admin/addservices.html', admindeets=admindeets)
        else:
            servname = request.form.get('servname')
            servprice = request.form.get('servprice')

            addserv = Service_type(servtype_name=servname, servtype_price=servprice)

            db.session.add(addserv)
            db.session.commit()

            flash(f'{servname} successfully added')
            return redirect('/admin/services')
            

@app.route('/admin/active/salon')
def active_salon():
    admin_loggedin = session.get('admin_loggedin')
    admindeets = Admin.query.get(admin_loggedin)

    if admin_loggedin == None:
        return redirect('/admin/home')
    else:
        act_sals = Salon.query.filter(Salon.salon_status=='1')
        return render_template('admin/active_salons.html',act_sals=act_sals, admindeets=admindeets)


@app.route('/admin/users')
def all_users():
    admin_loggedin = session.get('admin_loggedin')
    admindeets = Admin.query.get(admin_loggedin)

    if admin_loggedin == None:
        return redirect('/admin/home')
    else:
        users = Customer.query.all()
        return render_template('admin/customers.html',users=users, admindeets=admindeets)




