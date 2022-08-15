import datetime
from easetestprojapp import db


class Customer(db.Model): 
    cust_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    cust_fname = db.Column(db.String(255), nullable=False)
    cust_lname = db.Column(db.String(255), nullable=False)
    cust_email = db.Column(db.String(255), nullable=False)
    cust_pwd = db.Column(db.String(255), nullable=False)
    cust_gender = db.Column(db.Enum('male','female'), nullable=True)
    cust_phone = db.Column(db.String(255), nullable=True)
    cust_img = db.Column(db.String(255), nullable=True)
    cust_reg = db.Column(db.DateTime(), default=datetime.datetime.utcnow())

    #setup the relationships         
    myrevobj = db.relationship('Review', back_populates ='custrev')
    mycustbookobj = db.relationship('Booking', back_populates='custbook')
    mypayobj = db.relationship('Payment', back_populates='custpay')
    pay_custpayobj = db.relationship('Book_pay', back_populates='bookingpay_cust')


class Review(db.Model): 
    rev_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    rev_reg = db.Column(db.DateTime(), default=datetime.datetime.utcnow())

    #create the foreign key
    rev_salonid = db.Column(db.Integer(), db.ForeignKey("salon.salon_id"))
    rev_custid = db.Column(db.Integer(), db.ForeignKey("customer.cust_id"))
    
    #set up the relationship
    mysalonobj = db.relationship('Salon', back_populates ='revsalon')
    custrev = db.relationship('Customer', back_populates ='myrevobj')


class Salon(db.Model):
    salon_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    salon_email = db.Column(db.String(255), nullable=False)
    salon_image = db.Column(db.String(255), nullable=True)
    salon_ownerfname = db.Column(db.String(255), nullable=False)
    salon_ownerlname  = db.Column(db.String(255), nullable=False)
    salon_name = db.Column(db.String(255), nullable=False)
    salon_pwd  = db.Column(db.String(255), nullable=False)
    salon_address  = db.Column(db.String(255), nullable=False)
    salon_phone = db.Column(db.String(255), nullable=False)
    salon_status = db.Column(db.Enum('1','0'), nullable=False, default='0')
    salon_reg = db.Column(db.DateTime(), default=datetime.datetime.utcnow())

    #foreign Keys
    salon_subtypeid = db.Column(db.Integer(), db.ForeignKey('subscription_type.subtype_id'))
    salon_servicetypeid = db.Column(db.Integer(), db.ForeignKey('service_type.servtype_id'))

    #Relationships
    salon_servtypeobj = db.relationship('Service_type', back_populates ='servtype_salon')
    revsalon = db.relationship('Review', back_populates ='mysalonobj')
    mysubsalonobj = db.relationship('Salon_subscription', back_populates='salonsub')
    mybookobj = db.relationship('Booking', back_populates='salonbook')
    myimgobj = db.relationship('Catalogue', back_populates='salonimg')
    mypaysalonobj = db.relationship('Payment', back_populates='salonpay')
    salon_salonservobj = db.relationship('Salon_servicetype', back_populates ='salonserv_salon')
    salonobj_serv = db.relationship('Service', back_populates ='serv_salonobj')
    pay_salonpayobj = db.relationship('Book_pay', back_populates='bookingpay_salon')


class Salon_servicetype(db.Model):
    salonserv_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    salonserv_salonid = db.Column(db.Integer(), db.ForeignKey("salon.salon_id"))
    salonserv_servtypeid = db.Column(db.Integer(), db.ForeignKey("service_type.servtype_id"))
   
    #set up relationships
    salonserv_salon = db.relationship('Salon', back_populates ='salon_salonservobj')
    salonserv_servicetype = db.relationship('Service_type', back_populates ='servicetype_salonservobj')


class Catalogue(db.Model): 
    img_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    img_url = db.Column(db.String(255), nullable=False)
    img_desc = db.Column(db.String(255), nullable=False)
    img_reg = db.Column(db.DateTime(), default=datetime.datetime.utcnow())

    #Foreign Keys
    img_salonid =  db.Column(db.Integer(), db.ForeignKey('salon.salon_id'))

    #set up the relationship
    salonimg = db.relationship('Salon', back_populates='myimgobj')   


class Subscription_type(db.Model): 
    subtype_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    subtype_name = db.Column(db.String(255), nullable=False)

    #set up the relationship
    mysubobj = db.relationship('Salon_subscription', back_populates='subtypesub')      


class Salon_subscription(db.Model):
    sub_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    sub_amt =  db.Column(db.Float(), nullable=False)
    sub_stat =  db.Column(db.Enum('paid','not paid', 'incomplete'), nullable=False)
    sub_reg =  db.Column(db.DateTime(), default=datetime.datetime.utcnow())

    #Foreign Keys
    sub_salonid =  db.Column(db.Integer(), db.ForeignKey('salon.salon_id'))
    sub_subtypeid = db.Column(db.Integer(), db.ForeignKey('subscription_type.subtype_id'))

    #relationships
    salonsub = db.relationship('Salon', back_populates='mysubsalonobj')
    subtypesub = db.relationship('Subscription_type', back_populates='mysubobj') 


class Service_type(db.Model): 
    servtype_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    servtype_name = db.Column(db.String(255), nullable=False)
    servtype_price = db.Column(db.Float(), nullable=False)

    #set up the relationship
    servtype_salon = db.relationship('Salon', back_populates ='salon_servtypeobj')
    myservtypeobj = db.relationship('Service', back_populates ='servtypeserv')
    servicetype_salonservobj = db.relationship('Salon_servicetype', back_populates ='salonserv_servicetype')


class Service(db.Model): 
    serv_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    
    # create the foreign keys
    serv_salonid = db.Column(db.Integer(), db.ForeignKey("salon.salon_id")) 
    serv_servtypeid = db.Column(db.Integer(), db.ForeignKey("service_type.servtype_id")) 

    #set up the relationships
    servtypeserv = db.relationship('Service_type', back_populates ='myservtypeobj')
    mybookservobj = db.relationship('Booking', back_populates ='servbook')
    servicebserv = db.relationship('Book_service', back_populates ='bservservice')
    serv_salonobj = db.relationship('Salon', back_populates ='salonobj_serv')


class Booking(db.Model): 
    book_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    book_date = db.Column(db.Date(), nullable=False)
    book_time = db.Column(db.String(255), nullable=False)

    #create the foreign keys
    book_salonid = db.Column(db.Integer(), db.ForeignKey("salon.salon_id"))
    book_custid = db.Column(db.Integer(), db.ForeignKey("customer.cust_id"))
    book_servid = db.Column(db.Integer(), db.ForeignKey("service.serv_id"))
    
    #set up the relationships
    salonbook = db.relationship('Salon', back_populates='mybookobj')
    custbook = db.relationship('Customer', back_populates='mycustbookobj')
    servbook = db.relationship('Service', back_populates ='mybookservobj')
    mypaybookobj = db.relationship('Payment', back_populates ='bookpay')
    bookbserv = db.relationship('Book_service', back_populates ='bservbook')


class Book_service(db.Model):
    bserv_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    bserv_bookid = db.Column(db.Integer(), db.ForeignKey("booking.book_id"))
    bserv_servid = db.Column(db.Integer(), db.ForeignKey("service.serv_id"))
    bserv_date = db.Column(db.DateTime(), default=datetime.datetime.utcnow())
   
    #set up relationships
    bservbook = db.relationship('Booking', back_populates ='bookbserv')
    bservservice = db.relationship('Service', back_populates ='servicebserv')
    bookserv_bookingpayobj = db.relationship('Book_pay', back_populates='bookingpay_bookserv')
    

class Payment(db.Model): 
    pay_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    pay_amt =  db.Column(db.Float(), nullable=False)
    pay_stat =  db.Column(db.Enum('completed','incomplete','in progress'), nullable=False)
    pay_reg = db.Column(db.DateTime(), default=datetime.datetime.utcnow())
    pay_refno = db.Column(db.String(255), nullable=False)

    #create the foreign key
    pay_salonid = db.Column(db.Integer(), db.ForeignKey("salon.salon_id"))
    pay_custid = db.Column(db.Integer(), db.ForeignKey("customer.cust_id"))
    pay_bookid = db.Column(db.Integer(), db.ForeignKey("booking.book_id"))
    pay_bookpayid = db.Column(db.Integer(), db.ForeignKey('book_pay.bookpay_id'))
    
    #set up the relationships
    salonpay = db.relationship('Salon', back_populates='mypaysalonobj')
    custpay = db.relationship('Customer', back_populates='mypayobj')
    bookpay = db.relationship('Booking', back_populates ='mypaybookobj')
    pay_bookingpayobj = db.relationship('Book_pay', back_populates='bookingpay_pay')


class Book_pay(db.Model):
    bookpay_id = db.Column(db.Integer(),primary_key=True, autoincrement=True)
    bookpay_amt = db.Column(db.Float(),nullable=False)
    bookpay_ref = db.Column(db.String(255), nullable=False)
    bookpay_reg = db.Column(db.DateTime(), default=datetime.datetime.utcnow())

    #foreign keys
    bookpay_bookservid = db.Column(db.Integer(), db.ForeignKey('book_service.bserv_id'))
    bookpay_bookcustid = db.Column(db.Integer(), db.ForeignKey('customer.cust_id'))
    bookpay_booksalonid = db.Column(db.Integer(), db.ForeignKey('salon.salon_id'))

    #relationships
    bookingpay_bookserv = db.relationship('Book_service', back_populates='bookserv_bookingpayobj')
    bookingpay_pay = db.relationship('Payment', back_populates='pay_bookingpayobj')
    bookingpay_cust = db.relationship('Customer', back_populates='pay_custpayobj')
    bookingpay_salon = db.relationship('Salon', back_populates='pay_salonpayobj')


class Admin(db.Model): 
    admin_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    admin_username = db.Column(db.String(255), nullable=False)
    admin_password = db.Column(db.String(255), nullable=False)
    admin_lastlogin = db.Column(db.DateTime(), onupdate=datetime.datetime.utcnow())



