
from sqlalchemy import Column, String, Integer, Date, ForeignKey, Boolean
from flask_sqlalchemy import SQLAlchemy

# database_name = "trivia"
# database_path = "postgres://postgres:1@{}/{}".format(
#     'localhost:5432', database_name)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=None):
    if database_path is None:
        app.config.from_object("config")
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = database_path
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db.create_all()
    db.app = app
    db.init_app(app)


class Base(db.Model):
    __abstract__ = True

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


class User(Base):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    username = Column(String(200), unique=True)
    email = Column(String(200), nullable=False, unique=True)
    phone_number = Column(Integer, nullable=False)
    password = Column(String(200), nullable=False)
    date_of_joining = Column(Date)
    role = Column(Integer, nullable=False)
    histories_of_user_activity = db.relationship(
        'History_of_user_activity', backref=db.backref('user', uselist=False), lazy='dynamic')
    orders = db.relationship('Order', backref=db.backref(
        'user', uselist=False), lazy='dynamic')
    histories_of_company = db.relationship(
        'History_of_company', backref=db.backref('user', uselist=False), lazy='dynamic')
    histories_of_marketing = db.relationship(
        'History_of_marketing', backref=db.backref('user', uselist=False), lazy='dynamic')
    reports = db.relationship('Report', backref=db.backref(
        'user', uselist=False), lazy='dynamic')

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'username': self.username,
            'email': self.email,
            'date_of_joining': self.date_of_joining,
            'role': self.role
        }


class History_of_user_activity(Base):
    __tablename__ = 'History_of_user_activity'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('User.id'), nullable=False)
    zone_id = Column(Integer, ForeignKey('Zone.id'), nullable=False)
    pharmacy_id = Column(Integer, ForeignKey('Pharmacy.id'), nullable=False)
    doctor_id = Column(Integer, ForeignKey('Doctor.id'))
    date = Column(Date)
    histories_of_doctor = db.relationship('History_of_doctor', backref=db.backref(
        'History_of_user_activity', uselist=False), lazy='dynamic')
    histories_of_pharmacy = db.relationship('History_of_pharmacy', backref=db.backref(
        'History_of_user_activity', uselist=False), lazy='dynamic')

    def format(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'zone_id': self.zone_id,
            'pharmacy_id': self.pharmacy_id,
            'doctor_id': self.doctor_id,
            'date': self.date,
        }


class Zone(Base):
    __tablename__ = 'Zone'
    id = Column(Integer, primary_key=True)
    zone = Column(String(100), nullable=False)
    histories_of_user_activity = db.relationship(
        'History_of_user_activity', backref=db.backref('zone', uselist=False), lazy='dynamic')
    pharmacies = db.relationship('Pharmacy', backref=db.backref(
        'zone', uselist=False), lazy='dynamic')
    orders = db.relationship('Order', backref=db.backref(
        'zone', uselist=False), lazy='dynamic')
    doctors = db.relationship('Doctor', backref=db.backref(
        'zone', uselist=False), lazy='dynamic')
    reports = db.relationship('Report', backref=db.backref(
        'zone', uselist=False), lazy='dynamic')

    def format(self):
        return {
            'id': self.id,
            'Zone': self.Zone,
        }


class Pharmacy(Base):
    __tablename__ = 'Pharmacy'

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    phone_number = Column(Integer, nullable=False)
    address = Column(String(200), nullable=False)
    zone_id = Column(Integer, ForeignKey('Zone.id'), nullable=False)
    support = Column(String(200))
    date_of_joining = Column(Date)
    histories_of_user_activity = db.relationship(
        'History_of_user_activity', backref=db.backref('pharmacy', uselist=False), lazy='dynamic')
    orders = db.relationship('Order', backref=db.backref(
        'pharmacy', uselist=False), lazy='dynamic')
    acceptance_of_items = db.relationship('Acceptance_of_item', backref=db.backref(
        'pharmacy', uselist=False), lazy='dynamic')
    availabilty_of_items = db.relationship('Availabilty_of_item', backref=db.backref(
        'pharmacy', uselist=False), lazy='dynamic')
    histories_Of_marketing = db.relationship(
        'History_of_marketing', backref=db.backref('pharmacy', uselist=False), lazy='dynamic')
    doctors = db.relationship('Doctor', backref=db.backref(
        'pharmacy', uselist=False), lazy='dynamic')
    histories_of_pharmacy = db.relationship('History_of_pharmacy', backref=db.backref(
        'pharmacy', uselist=False), lazy='dynamic')
    reports = db.relationship('Report', backref=db.backref(
        'pharmacy', uselist=False), lazy='dynamic')

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone_number': self.phone_number,
            'address': self.address,
            'zone_id': self.zone_id,
            'doctor_id': self.doctor_id,
            'support': self.support,
            'date_of_joining': self.date_of_joining
        }


class Item(Base):
    __tablename__ = 'Item'

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    company_id = Column(Integer, ForeignKey('Company.id'), nullable=False)
    expire_date = Column(Date, nullable=False)
    price = Column(Integer)
    acceptance_of_items = db.relationship(
        'Acceptance_of_item', backref=db.backref('item', uselist=False), lazy='dynamic')
    availabilty_of_items = db.relationship(
        'Availabilty_of_item', backref=db.backref('item', uselist=False), lazy='dynamic')
    item_orders = db.relationship('item_order', backref=db.backref(
        'item', uselist=False), lazy='dynamic')
    reports = db.relationship('Report', backref=db.backref(
        'item', uselist=False), lazy='dynamic')

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'company_id': self.company_id,
            'expire_date': self.expire_date,
            'price': self.price,
        }


class Report(Base):
    __tablename__ = 'Report'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('User.id'), nullable=False)
    zone_id = Column(Integer, ForeignKey('Zone.id'), nullable=False)
    doctor_id = Column(Integer, ForeignKey('Doctor.id'), nullable=False)
    pharmacy_id = Column(Integer, ForeignKey('Pharmacy.id'), nullable=False)
    company_id = Column(Integer, ForeignKey('Company.id'), nullable=False)
    item_id = Column(Integer, ForeignKey("Item.id"), nullable=False)
    acceptance_of_item_id = Column(Integer, ForeignKey(
        "Acceptance_of_item.id"), nullable=False)
    availabilty_of_item_id = Column(Integer, ForeignKey(
        "Availabilty_of_item.id"), nullable=False)
    history_of_pharmacy_id = Column(Integer, ForeignKey(
        "History_of_pharmacy.id"), nullable=False)

    def format(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'zone_id': self.zone_id,
            'doctor_id': self.doctor_id,
            'pharmacy_id': self.pharmacy_id,
            'company_id': self.company_id,
            'item_id': self.item_id,
            'acceptance_of_item_id': self.acceptance_of_item_id,
            'availabilty_of_item_id': self.availabilty_of_item_id,
            'history_of_pharmacy_id': self.history_of_pharmacy_id
        }

    def short(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'zone_id': self.zone_id,
            'doctor_id': self.doctor_id,
            'pharmacy_id': self.pharmacy_id,
            'company_id': self.company_id,
            'item_id': self.item_id,
            'acceptance_of_item_id': self.acceptance_of_item_id,
            'availabilty_of_item_id': self.availabilty_of_item_id,
            'history_of_pharmacy_id': self.history_of_pharmacy_id
        }


class Order(Base):
    __tablename__ = 'Order'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('User.id'), nullable=False)
    zone_id = Column(Integer, ForeignKey('Zone.id'), nullable=False)
    pharmacy_id = Column(Integer, ForeignKey('Pharmacy.id'), nullable=False)
    doctor_id = Column(Integer, ForeignKey('Doctor.id'))
    comment = Column(String(200))
    date_of_order = Column(Date, nullable=False)
    approved = Column(Boolean)
    histories_of_doctor = db.relationship(
        'History_of_doctor', backref=db.backref('order', uselist=False), lazy='dynamic')
    histories_of_pharmacy = db.relationship(
        'History_of_pharmacy', backref=db.backref('order', uselist=False), lazy='dynamic')
    item_orders = db.relationship('item_order', backref=db.backref(
        'order', uselist=False), lazy='dynamic')

    def format(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'zone_id': self.zone_id,
            'pharmacy_id': self.pharmacy_id,
            'doctor_id': self.doctor_id,
            'comment': self.comment,
            'date_of_order': self.date_of_order,
        }


class item_order(Base):
    __tablename__ = 'item_order'

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("Order.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("Item.id"), nullable=False)
    quantity = Column(Integer, default=1)
    price = Column(Integer, nullable=False)

    def format(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'item_id': self.item_id,
            'quantity': self.quantity,
            'price': self.price
        }


class Acceptance_of_item(Base):
    __tablename__ = 'Acceptance_of_item'

    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey('Item.id'), nullable=False)
    acceptance = Column(String(200), nullable=False)
    pharmacy_id = Column(Integer, ForeignKey('Pharmacy.id'), nullable=False)
    doctor_id = Column(Integer, ForeignKey('Doctor.id'), nullable=False)
    comment = Column(String(500))
    reports = db.relationship('Report', backref=db.backref(
        'acceptance_of_item', uselist=False), lazy='dynamic')

    def format(self):
        return {
            'id': self.id,
            'item_id': self.item_id,
            'acceptance': self.acceptance,
            'pharmacy_id': self.pharmacy_id,
            'doctor_id': self.doctor_id,
            'comment': self.comment,
        }


class Availabilty_of_item(Base):
    __tablename__ = 'Availabilty_of_item'

    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey('Item.id'), nullable=False)
    available = Column(Boolean, nullable=False)
    pharmacy_id = Column(Integer, ForeignKey('Pharmacy.id'), nullable=False)
    doctor_id = Column(Integer, ForeignKey('Doctor.id'))
    comment = Column(String(500))
    reports = db.relationship('Report', backref=db.backref(
        'availabilty_of_item', uselist=False), lazy='dynamic')

    def format(self):
        return {
            'id': self.id,
            'item_id': self.item_id,
            'acceptance': self.acceptance,
            'pharmacy_id': self.pharmacy_id,
            'doctor_id': self.doctor_id,
            'comment': self.comment,
        }


class Company(Base):
    __tablename__ = "Company"
    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String(200), nullable=False)
    items = db.relationship('Item', backref=db.backref(
        'company', uselist=False), lazy='dynamic')
    histories_of_company = db.relationship('History_of_company', backref=db.backref(
        'company', uselist=False), lazy='dynamic')
    reports = db.relationship('Report', backref=db.backref(
        'company', uselist=False), lazy='dynamic')

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
        }


class History_of_company(Base):
    __tablename__ = "History_of_company"
    id = Column(Integer, nullable=False, primary_key=True)
    company_id = Column(Integer, ForeignKey('Company.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('User.id'), nullable=False)
    date = Column(Date)

    def format(self):
        return {
            'id': self.id,
            'company_id': self.company_id,
            'user_id': self.user_id,
            'date': self.date
        }


class History_of_marketing(Base):
    __tablename__ = "History_of_marketing"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('User.id'), nullable=False)
    doctor_id = Column(Integer, ForeignKey('Doctor.id'))
    pharmacy_id = Column(Integer, ForeignKey('Pharmacy.id'), nullable=False)
    date = Column(Date)

    def format(self):
        return {
            'id': self.id,
            'doctor_id': self.doctor_id,
            'user_id': self.user_id,
            'pharmacy_id': self.pharmacy_id,
            'date': self.date,
        }


class Doctor(Base):
    __tablename__ = "Doctor"
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    phone = Column(Integer, nullable=True)
    zone_id = Column(Integer, ForeignKey('Zone.id'))
    speciality = Column(String(200), nullable=False)
    d_class = Column(String(2), nullable=True)
    pharmacy_id = Column(Integer, ForeignKey('Pharmacy.id'), nullable=False)
    support = Column(String(200), nullable=False)
    loyality = Column(String(200), nullable=False)
    date_of_joining = Column(Date)
    histories_of_user_activity = db.relationship(
        'History_of_user_activity', backref=db.backref('doctor', uselist=False), lazy='dynamic')
    orders = db.relationship('Order', backref=db.backref(
        'doctor', uselist=False), lazy='dynamic')
    acceptance_of_items = db.relationship('Acceptance_of_item', backref=db.backref(
        'doctor', uselist=False), lazy='dynamic')
    availabilty_of_items = db.relationship(
        'Availabilty_of_item', backref=db.backref('doctor', uselist=False), lazy='dynamic')
    histories_of_marketing = db.relationship(
        'History_of_marketing', backref=db.backref('doctor', uselist=False), lazy='dynamic')
    histories_of_doctor = db.relationship('History_of_doctor', backref=db.backref(
        'doctor', uselist=False), lazy='dynamic')
    reports = db.relationship('Report', backref=db.backref(
        'doctor', uselist=False), lazy='dynamic')

    def format(self):
        return {
            'id': self.id,
            'Name': self.Name,
            'phone': self.phone,
            'pharmacy_id': self.pharmacy_id,
            'zone_id': self.zone_id,
            'speciality': self.speciality,
            'd_class': self.d_class,
            'support': self.support,
            'loyality': self.loyality,
            'date_of_joining': self.date_of_joining,
        }


class History_of_doctor(Base):
    __tablename__ = 'History_of_doctor'
    id = Column(Integer, primary_key=True)
    doctor_id = Column(Integer, ForeignKey('Doctor.id'), nullable=False)
    visit_id = Column(Integer, ForeignKey(
        'History_of_user_activity.id'), nullable=False)
    order_id = Column(Integer, ForeignKey('Order.id'), nullable=False)

    def format(self):
        return {
            'id': self.id,
            'doctor_id': self.doctor_id,
            'visit': self.visit_id,
            'order': self.order_id
        }


class History_of_pharmacy(Base):
    __tablename__ = 'History_of_pharmacy'
    id = Column(Integer, primary_key=True)
    pharmacy_id = Column(Integer, ForeignKey('Pharmacy.id'), nullable=False)
    visit_id = Column(Integer, ForeignKey(
        'History_of_user_activity.id'), nullable=False)
    order_id = Column(Integer, ForeignKey('Order.id'), nullable=False)
    reports = db.relationship('Report', backref=db.backref(
        'history_of_pharmacy', uselist=False), lazy='dynamic')

    def format(self):
        return {
            'id': self.id,
            'pharmacy_id': self.pharmacy_id,
            'visit': self.visit_id,
            'order': self.order_id
        }
