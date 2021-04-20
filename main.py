from flask import *
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import smtplib


g_txt = 1
application = Flask(__name__, static_url_path="/static")
app = application
app.config['SECRET_KEY'] = 'batrpo21'
# UPLOAD_FOLDER = r'/home/batyrrpo/mysite/static/img/upload'
UPLOAD_FOLDER = r'/home/batyrrpo/mysite/static/img/upload'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4'}
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mass = db.Column(db.Integer, nullable=False)
    class_product = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    all_title = db.Column(db.Text, nullable=False)
    made_of = db.Column(db.Text, nullable=False)
    nutritional_value = db.Column(db.Text, nullable=False)
    energy_value = db.Column(db.Text, nullable=False)
    photo = db.Column(db.Text, nullable=False)
    about = db.Column(db.Text, nullable=False)
    gost = db.Column(db.Text, nullable=False)
    articl = db.Column(db.Text, nullable=False)
    time_out = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id

class Count(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<count %r>' % self.id

db.create_all()
def send_email(addr_to, msg_subj, msg_text, files):
    addr_from = "server.souz@gmail.com"                           # Отправитель
    password  = 'Klopik21'                    # Пароль

    msg = MIMEMultipart()                                   # Создаем сообщение
    msg['From']    = addr_from                              # Адресат
    msg['To']      = addr_to                                # Получатель
    msg['Subject'] = msg_subj                               # Тема сообщения

    body = msg_text                                         # Текст сообщения
    msg.attach(MIMEText(body, 'plain'))                     # Добавляем в сообщение текст

    process_attachement(msg, files)

    #======== Этот блок настраивается для каждого почтового провайдера отдельно ===============================================
    server = smtplib.SMTP_SSL('smtp.gmail.com:465')        # Создаем объект SMTP
    #server.starttls()                                      # Начинаем шифрованный обмен по TLS
    #server.set_debuglevel(True)                            # Включаем режим отладки, если не нужен - можно закомментировать
    server.login(addr_from, password)                       # Получаем доступ
    server.send_message(msg)                                # Отправляем сообщение
    server.quit()                                           # Выходим
    #==========================================================================================================================

def process_attachement(msg, files):                        # Функция по обработке списка, добавляемых к сообщению файлов
    for f in files:
        if os.path.isfile(f):                               # Если файл существует
            attach_file(msg,f)                              # Добавляем файл к сообщению
        elif os.path.exists(f):                             # Если путь не файл и существует, значит - папка
            dir = os.listdir(f)                             # Получаем список файлов в папке
            for file1 in dir:                                # Перебираем все файлы и...
                attach_file(msg,f+"/"+file1)

def attach_file(msg, filepath):                             # Функция по добавлению конкретного файла к сообщению
    filename = os.path.basename(filepath)                   # Получаем только имя файла
    ctype, encoding = mimetypes.guess_type(filepath)        # Определяем тип файла на основе его расширения
    if ctype is None or encoding is not None:               # Если тип файла не определяется
        ctype = 'application/octet-stream'                  # Будем использовать общий тип
    maintype, subtype = ctype.split('/', 1)
    print('MAINtype:', maintype)                 # Получаем тип и подтип
    if maintype == 'text':                                  # Если текстовый файл
        with open(filepath) as fp:                          # Открываем файл для чтения
            file = MIMEText(fp.read(), _subtype=subtype)    # Используем тип MIMEText
            fp.close()                                      # После использования файл обязательно нужно закрыть
    elif maintype == 'image':                               # Если изображение
        with open(filepath, 'rb') as fp:
            file = MIMEImage(fp.read(), _subtype=subtype)
            fp.close()
    elif maintype == 'audio':                               # Если аудио
        with open(filepath, 'rb') as fp:
            file = MIMEAudio(fp.read(), _subtype=subtype)
            fp.close()
    else:                                                   # Неизвестный тип файла
        with open(filepath, 'rb') as fp:
            file = MIMEBase(maintype, subtype)              # Используем общий MIME-тип
            file.set_payload(fp.read())                     # Добавляем содержимое общего типа (полезную нагрузку)
            fp.close()
            encoders.encode_base64(file)                    # Содержимое должно кодироваться как Base64
    file.add_header('Content-Disposition', 'attachment', filename=filename) # Добавляем заголовки
    msg.attach(file)                                        # Присоединяем файл к сообщению


@app.route('/', methods=['POST', 'GET'])
@app.route('/all', methods=['POST', 'GET'])
def index():
    session['user'] = 0
    global g_txt
    if request.method != 'POST':
        all_catalog = Article.query.order_by(-Article.id).all()
        print(all_catalog)
        all_count, bread, cake1, pie, cake, cookie = 0, 0, 0, 0, 0, 0
        for elem in all_catalog:
            all_count += 1
            if int(elem.class_product) == 1:
                bread += 1
            elif int(elem.class_product) == 3:
                cake1 += 1
            elif int(elem.class_product) == 4:
                pie += 1
            elif int(elem.class_product) == 5:
                cake += 1
            elif int(elem.class_product) == 2:
                cookie += 1
            else:
                pass
        counts = [all_count, bread, cake1, pie, cake, cookie]
        print(counts)
        return render_template('index.html', title='Каталог', text=g_txt, session=session, catalog=all_catalog, counts=counts)
    else:
        rq = request.form
        print(rq)
        session['user'] = 0
        return redirect('/')


@app.route('/call', methods=['POST', 'GET'])
def call():
    global g_txt
    session['user'] = 0
    if request.method != 'POST':
        return render_template('contacts.html', title='Контактные данные', text=g_txt, session=session)
    else:
        rq = request.form
        print(rq)
        session['user'] = 0
        return redirect('/')

@app.route('/about', methods=['POST', 'GET'])
def about():
    session['user'] = 0
    global g_txt
    if request.method != 'POST':
        return render_template('about.html', title='О Нас', text=g_txt, session=session, catalog=[])
    else:
        rq = request.form
        print(rq)
        session['admin'] = 0
        return redirect('/')

@app.route('/docs', methods=['POST', 'GET'])
def docs():
    global g_txt
    if request.method != 'POST':
        return render_template('index.html', title='Документы', text=g_txt, session=session)
    else:
        rq = request.form
        print(rq)
        session['admin'] = 0
        return redirect('/')




@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method != 'POST':
        return render_template('login.html')
    else:
        login = request.form.get('login')
        password = request.form.get('password')
        req = [login, password]
        print(req)
        check = [['btr21', 'batyr_rpo_5547!'], ['m170rd', 'Svoloch21+-'], ['padenev', 'Svoloch21+-!'], ['padenev2005', 'Klopik21+-'], ['admin', 'admin19921']]
        if req in check:
            session['admin'] = 1
        else:
            flash('Неверный логин или пароль')
            return redirect(url_for('login'))
        return redirect(url_for('index'))

@app.route('/unlogin', methods=['POST', 'GET'])
def unlogin():
    del session['admin']
    return redirect(url_for('index'))


@app.route('/add', methods=['POST', 'GET'])
def add_product():
    if request.method != 'POST':
        if 'admin' in session and session['admin'] == 1:
            return render_template('add.html', title='Добавление продукта')
        else:
            return redirect(url_for('index'))
    else:
        if 'admin' in session and session['admin'] == 1:
            title = request.form.get('title')
            all_title = request.form.get('all_title')
            type_product = request.form.get('type_product')
            mass = request.form.get('mass')
            made_of = request.form.get('made_of')
            pv_b = request.form.get('PV-B')
            pv_z = request.form.get('PV-Z')
            pv_y = request.form.get('PV-Y')
            ev = request.form.get('EV')
            time_out = request.form.get('time_out')
            gost = request.form.get('GOST')
            about = request.form.get('about')
            art = request.form.get('arcticle')
            time_out = request.form.get('time_out')
            file = request.files['file']
            new_id_file = Count.query.filter_by(id=1).one().count
            check = Article.query.filter_by(articl=art).first()
            coount = Count.query.filter_by(id=1).one()
            print(check)
            if check != None:
                flash('Уже есть продукт с таким артикулом')
                return redirect(url_for('add_product'))
            else:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    filename = str(new_id_file) + "-arcticle." + filename.split('.')[1]
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    print(file, filename)
                print (title, all_title, mass, made_of, pv_b, pv_y, pv_z, ev, time_out, gost, about, type_product)
                new_product = Article(class_product=type_product, title=title, mass=mass, all_title=all_title, made_of=made_of, time_out=time_out, nutritional_value=f'БЕЛКИ: {pv_b} Г; ЖИРЫ: {pv_z} Г; УГЛЕВОДЫ: {pv_y} Г', energy_value=f'{float(ev)} кКал', photo=filename, about=about, gost=gost, articl=art)
                db.session.add(new_product)
                coount.count += 1
                db.session.commit()
        return redirect(url_for('index'))

@app.route('/info/<ids>', methods=['POST', 'GET'])
def info_product(ids):
    elem = Article.query.filter_by(id=ids).first()
    print(elem)
    elem.class_product = ['Хлеб','', 'Пирожное', 'Пирог', 'Торт'][int(elem.class_product)-1]
    elem.made_of = elem.made_of.upper()
    return render_template('info.html', el=elem, title=elem.title)


@app.route('/del/<ids>', methods=['POST', 'GET'])
def delete_product(ids):
    if 'admin' in session and session['admin'] == 1:
        elem = Article.query.filter_by(id=ids).first()
        if elem != None:
            Article.query.filter_by(id=ids).delete()
            db.session.commit()
    return redirect(url_for('index'))


@app.route('/form' , methods=['POST','GET'])
def form_get_price():
    if request.method != 'POST':
        return render_template('price_list.html', title="Обратная связь")
    else:
        name = request.form.get('name')
        email = request.form.get('email')
        text = request.form.get('text')
        tel = request.form.get('tel')
        send_email('padenev21@gmail.com', '❗Новая форма обратной связи', f"▶Адресат: {email} ({name}) \n▶Номер телефона: {tel} \n\n➖➖➖➖➖➖➖➖\n\n▶Текст сообщения: \n\n{text}\n➖➖➖➖➖➖➖➖\n~ Server feedback ~", ['none'])
        flash('Форма отправлена')
        return redirect(url_for('form_get_price'))


@app.route('/edit/<ids>', methods=['POST', 'GET'])
def edit_product(ids):
    if request.method != 'POST':
        if 'admin' in session and session['admin'] == 1:
            elem = Article.query.filter_by(id=ids).first()
            if elem != None:
                answ = elem.nutritional_value.replace('БЕЛКИ:', '')
                answ = answ.replace('ЖИРЫ:', '')
                answ = answ.replace('УГЛЕВОДЫ:', '')
                answ = answ.replace('Г', '')
                pv_b, pv_z, pv_y = answ.split(';')[0], answ.split(';')[1], answ.split(';')[2]
                return render_template('edit.html', title='Изменение продукта', el=elem, pv=[int(pv_b), int(pv_z), int(pv_y), float(elem.energy_value.replace(' кКал', ''))])
            return redirect(url_for('index'))
        else:
            return redirect(url_for('index'))
    else:
        print('EDITED')
        if 'admin' in session and session['admin'] == 1:
            elem = Article.query.filter_by(id=ids).first()
            title = request.form.get('title')
            all_title = request.form.get('all_title')
            type_product = request.form.get('type_product')
            mass = request.form.get('mass')
            made_of = request.form.get('made_of')
            pv_b = request.form.get('PV-B')
            pv_z = request.form.get('PV-Z')
            pv_y = request.form.get('PV-Y')
            ev = request.form.get('EV')
            time_out = request.form.get('time_out')
            gost = request.form.get('GOST')
            about = request.form.get('about')
            art = request.form.get('arcticle')
            time_out = request.form.get('time_out')
            file = request.files['file']
            new_id_file = Count.query.filter_by(id=1).one().count
            check = Article.query.filter_by(articl=art).first()
            coount = Count.query.filter_by(id=1).one()
            print(check)
            if check != None and check.articl != elem.articl:
                flash('Уже есть продукт с таким артикулом')
                return redirect(url_for('add_product'))
            else:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    filename = str(new_id_file) + "-arcticle." + filename.split('.')[1]
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    print(file, filename)
                    new_product = Article(class_product=type_product, title=title, mass=mass, all_title=all_title, made_of=made_of, time_out=time_out, nutritional_value=f'БЕЛКИ: {pv_b} Г; ЖИРЫ: {pv_z} Г; УГЛЕВОДЫ: {pv_y} Г', energy_value=f'{float(ev)} кКал', photo=filename, about=about, gost=gost, articl=art)
                else:
                    new_product = Article(class_product=type_product, title=title, mass=mass, all_title=all_title, made_of=made_of, time_out=time_out, nutritional_value=f'БЕЛКИ: {pv_b} Г; ЖИРЫ: {pv_z} Г; УГЛЕВОДЫ: {pv_y} Г', energy_value=f'{float(ev)} кКал', photo=(str(elem.photo)), about=about, gost=gost, articl=art)
                Article.query.filter_by(id=ids).delete()
                db.session.add(new_product)
                db.session.commit()
        return redirect(url_for('index'))



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

if __name__ == '__main__':
    application.run(port=8080, host='127.0.0.1', debug=True)