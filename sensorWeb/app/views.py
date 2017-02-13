from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from forms import LoginForm
from model import *
import hashlib

@app.route ( '/' )
@app.route ( '/index' )
@login_required
def index ():
    user = g.user
    sensors = []
    devices = Devices.query.all ()
    for d in devices:
        for s in d.sensors:
            if s.sensor_type == 1 or s.sensor_type == 65537 or s.sensor_type == 65538:
                sensors.append ( { 'descr': s.description, 'value': s.value - s.fix_value } )
            if s.sensor_type == 8 and s.value == 0:
                sensors.append ( { 'descr': s.description, 'value': 'ON' } )
            if s.sensor_type == 8 and s.value == 1:
                sensors.append ( { 'descr': s.description, 'value': 'OFF' } )
    w = Weather.query.get ( 0 )
    weather = w.weather
    return render_template("index.html",
        title = 'Home',
        user = user,
        weather = weather,
        sensors = sensors )

@app.before_request
def before_request():
    g.user = current_user

@lm.user_loader
def load_user(username):
    return Users.query.filter_by ( user_id = username ).first ()

@app.route ( '/login', methods = [ 'GET', 'POST' ] )
def login ():
    if g.user is not None and g.user.is_authenticated ():
        return redirect ( url_for ( 'index' ) )
    form = LoginForm ()
    if form.validate_on_submit ():
        user = Users.query.filter_by ( user_id = form.userid.data ).first ()
#        try:
        passwd = hashlib.md5 ( form.passwd.data ).hexdigest ()
        if user.passwd == passwd:
            login_user ( user )
            print "login successful"
            flash ( 'Login ' + form.userid.data )
            return redirect ( '/index' )
        else:
            print "unseccessful"
#        except AttributeError as ERR:
#            print ERR
    return render_template ( 'login.html', title = 'Sign in', form = form )

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route ( '/schedulers' )
@login_required
def schedulers ():
    return redirect ( url_for ( 'index' ) )

@app.route ( '/devices' )
@login_required
def devices ():
    user = g.user
    devs = []
    devices = Devices.query.all ()
    for d in devices:
        devs.append ( { 'address': d.address, 'descr': d.description, 'last_seen': d.last_seen } )
    return render_template ( 'devices.html', title = 'Devices', user = user, devs = devs )

@app.route ( '/sensors' )
@login_required
def sensors ():
    user = g.user
    sensors = []
    sensor_types = []
    devices = Devices.query.all ()
    sensorTypes = SensorType.query.all ()
    for d in devices:
        for s in d.sensors:
            sensors.append ( { 'address': d.address, 'type': s.sensor_type, 'fix': s.fix_value,  'descr': s.description } )
    for st in sensorTypes:
        sensor_types.append ( { 'id': st.sensor_type_id, 'name': st.sensor_name } )
    return render_template ( 'sensors.html', title = 'Sensors', user = user, sensors = sensors, st = sensor_types )
