from app import app, db
from flask import render_template, url_for, request, flash, redirect, session, send_file
from app.models import User, Application, Application_Version, Macbook, System_Info
from app.sessions import is_logged
import xml.etree.ElementTree as ET
from app.exports import ExportToCsv
from time import strftime
from app.check_location import convert_ipv4, check_ipv4_in


@app.route('/', methods=['GET'])
def index():
    return render_template('base.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('user dont exist')
        elif user.username==username and not User.verify_password(user.password_hash, password):
            flash('wrong password')
        else:
            session['logged_in'] = True
            session['username'] = user.username
            return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('you were logged out')
    return redirect(url_for('login'))


@app.route('/admin', methods=['GET'])
@is_logged
def admin():
    return render_template('admin.html')


@app.route('/app_view', methods=['GET'])
@is_logged
def app_view():
    app_list = db.session.query(Application, Application_Version).join(Application_Version)
    return render_template('app_view.html', iter_list = app_list)


@app.route('/hardware_view', methods=['GET'])
@is_logged
def hardware_view():
    macbook_list = db.session.query(Macbook, System_Info).join(System_Info)
    return render_template('hardware_view.html', iter_list = macbook_list)


@app.route('/api/hardware', methods=['POST'])
def add_hardware():
    ip_addr = None
    if request.data:
        ip_addr = request.args.get('ip_addr')
        root = ET.fromstring(request.data)

        for dict in root.findall('.array/dict/array/dict'):
            try:
                cpu = dict.find('string[4]').text
            except AttributeError:
                cpu = None

            try:
                cpu_cores = dict.find('integer[1]').text
            except AttributeError:
                cpu_cores = None

            try:
                cpu_clock = dict.find('string[5]').text
            except AttributeError:
                cpu_clock = None

            try:
                ram = dict.find('string[10]').text
            except AttributeError:
                ram = None

            try:
                if dict.find('string[12]').text == 'htt_enabled':
                    serial_number = dict.find('string[13]').text
                else:
                    serial_number = dict.find('string[12]').text
            except AttributeError:
                serial_number = None


        if not Macbook.verify_duplicate_serial(serial_number):
            location = None
            if check_ipv4_in(ip_addr):
                location = 'minsk'
            else:
                location = 'kiev'

            query = Macbook(serial_number=serial_number, cpu=cpu, cpu_clock=cpu_clock, cpu_cores=cpu_cores, ram=ram, location=location)
            try:
                db.session.add(query)
                db.session.commit()
                return('hardware record added\n')
            except:
                return('db error\n')
        else:
            return('hardware record exists\n')

    else:
        return('invalid request\n')


@app.route('/export_hardware', methods=['POST'])
def export_hardware():
    try:
        results = db.session.query(Macbook, System_Info).join(System_Info).all()
        print(results)
        data = ExportToCsv.export_hw_csv(results)
        current_date = strftime("%Y-%m-%d")
        return send_file('../exporthw.csv', attachment_filename ='export_' + current_date +'.csv', as_attachment=True)
    except:
        return redirect(url_for('index'))


@app.route('/api/system', methods=['POST'])
def add_system():
    userlist = None
    serial_number = None
    serial_number = request.args.get('serialnumber')
    userlist = request.args.get('userlist')
    if userlist and serial_number:
        root = ET.fromstring(request.data)

        for dict in root.findall('.array/dict/array/dict'):
            try:
                kernel_version = dict.find('string[4]').text
            except AttributeError:
                kernel_version = None
            try:
                os_version = dict.find('string[6]').text
            except AttributeError:
                os_version = None
            try:
                hostname = dict.find('string[5]').text
            except AttributeError:
                hostname = None
        try:
            get_serial = Macbook.query.filter_by(serial_number=serial_number).first()
            query = System_Info(kernel_version=kernel_version, os_version=os_version, hostname=hostname, usernames=userlist, systems=get_serial)
            try:
                db.session.add(query)
                db.session.commit()
                return('system record added\n')
            except:
                return('db error\n')
        except:
            return('no appropriate serial\n')

    else:
        return('invalid request\n')



@app.route('/api/applications', methods=['POST'])
def add_applications():
    apps_info = []
    apps_info_list = {}
    serial_number = None
    serial_number = request.args.get('serialnumber')
    if serial_number:
        root = ET.fromstring(request.data)
        get_serial = Macbook.query.filter_by(serial_number=serial_number).first()

    for dict in root.findall('.array/dict/array/dict'):
        try:
            name = dict.find('string[1]').text
        except AttributeError:
            name = None

        try:
            if dict.find('key[3]').text == 'install_version':
                version = dict.find('string[2]').text
                pkg_source = dict.find('string[3]').text
            else:
                version = None
                pkg_source = dict.find('string[2]').text
        except AttributeError:
            pkg_source = None

        try:
            date = dict.find('date[1]').text
        except AttributeError:
            date = None

        apps_info_list.update([('name', name), ('version', version), ('pkg_source', pkg_source), ('version', version), ('date', date)])
        apps_info.append(apps_info_list.copy())

    for item in apps_info:
        if Application.verify_duplicate_app(serial=get_serial, app_name=item['name']) == None:
            try:
                query_apps = Application(application_name=item['name'], pkg_source=item['pkg_source'], last_modified=item['date'], applications=get_serial)
                get_app = get_serial.apps.filter_by(application_name=item['name']).order_by(Application.id.desc()).first()
                query_versions = Application_Version(version=item['version'], versions=get_app)
                db.session.add(query_apps)
                db.session.add(query_versions)
                db.session.commit()
            except:
                return ('db error\n')
        else:
            try:
                get_app = get_serial.apps.filter_by(application_name=item['name']).order_by(Application.id.desc()).first()
                query_versions = Application_Version(version=item['version'], versions=get_app)
                db.session.add(query_versions)
                db.session.commit()
            except:
                return ('db error\n')

    return('apps records added\n')


@app.route('/export_application', methods=['POST'])
def export_application():
    try:
        results = db.session.query(Application, Application_Version, Macbook, System_Info) \
                            .join(Application_Version, Macbook, System_Info) \
                            .filter(Application.pkg_source == 'package_source_other')
        data = ExportToCsv.export_app_csv(results)
        current_date = strftime("%Y-%m-%d")
        return send_file('../export_app.csv', attachment_filename ='export_' + current_date +'.csv', as_attachment=True)
    except:
        return redirect(url_for('index'))
