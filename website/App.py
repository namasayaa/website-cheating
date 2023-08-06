from flask import Blueprint, render_template, request, flash, redirect, url_for, Response, jsonify, current_app
from ._init_ import db, bcrypt
from .model import Using, History, Screenshot
from .form import  pengaturan, formulir
from flask_login import login_user, login_required, logout_user, current_user
from website.form import formulir, pengaturan
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
import os


App = Blueprint('views', __name__,template_folder='templete')
stop_detection = False
form_data = {}
screenshot_db = []

# Define the allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Function to check if the file has an allowed extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@App.route('/formulir',methods=['GET', 'POST'])
@login_required
def dashboard():
    form = formulir()
       
    if form.validate_on_submit():        
        form_data['nama_pengawas'] = form.nama_pengawas.data
        form_data['subject'] = form.matkul.data
        form_data['classes'] = form.kelas.data
        form_data['room'] = form.ruangan.data
        form_data['date'] = form.tanggal.data
        form_data['time'] = form.jam.data

        history = History(name=form.nama_pengawas.data,subject=form.matkul.data,
                               classes=form.kelas.data,
                               room=form.ruangan.data, date=form.tanggal.data, time=form.jam.data)
        if current_user.name != form.nama_pengawas.data:
            flash('Nama Pengawas harus sama dengan Nama Lengkap User!', 'error')
            return redirect(url_for('app.dashboard'))
        
        db.session.add(history)
        db.session.commit()
        return redirect(url_for('app.detection'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'terjadi error dalam mengisi formulir: {err_msg}', category='error')
    return render_template("dashboard.html", user=current_user, form=form, fill_formulir=current_user)

@App.route('/pengawasan')
@login_required
def pengawasan():
    return render_template("Pengawasan.html", user=current_user)

@App.route('/histori')
@login_required
def histori():
    user_id = current_user.id
    #formulir = History.query.filter_by(user_id=current_user.id).all()
    formulir = History.query.all()
    #print(formulir)
    return render_template("histori.html", formulir=formulir, user=current_user)

@App.route('/history/<string:id>', methods= ["GET", "POST"])
@login_required
def delete(id):
    user_to_delete = History.query.get_or_404(id)
    screenshots = Screenshot.query.filter_by(history_id=id).all()
    for screenshot in screenshots:
        db.session.delete(screenshot)
    
    try :
        db.session.delete(user_to_delete)
        db.session.commit()
    except:
         error_msg = "error dalam menghapus history"
         flash(error_msg, category="error")

    return redirect(url_for("app.histori"))

@App.route('/histori-view/<int:history_id>')
@login_required
def histori2(history_id):
    db_screenshots = Screenshot.query.filter_by(history_id=history_id).all()
    user = Using.query.get_or_404(current_user.id)
    nama_pengawas = user.name
    screenshot_dir = f"detect/{nama_pengawas}/"
    screenshots = [url_for('static', filename = screenshot_dir + screenshot.path) for screenshot in db_screenshots]
    return render_template("histori2.html", user=current_user, screenshots=screenshots)

@App.route('/setting', methods= ['GET','POST'])
@login_required
def setting():
    form = pengaturan()
    id = current_user.id
    user_to_update = Using.query.get_or_404(id)
    if request.method == "POST":
        setting_type = request.form['setting_type']
        
        if setting_type == 'account-tab':
            if form.name.data.strip():
                user_to_update.name = form.name.data

            if form.email_address.data.strip():
                user_to_update.email = form.email_address.data

            if form.phone.data and form.phone.data.strip():
                user_to_update.handphone = form.phone.data.strip()
            else:
                form.phone.data = user_to_update.handphone

            if form.bio.data.strip():
                user_to_update.bio = form.bio.data

        elif setting_type == 'password-tab':
            # Password Update
            old_password = request.form['old_password']
            new_password = request.form['new_password']
            confirm_password = request.form['confirm_password'] 

            if old_password and new_password and confirm_password:
                if not bcrypt.check_password_hash(user_to_update.password_hash, old_password):
                    flash('password lama invalid.', 'error')
                    return redirect(url_for('setting'))
                if new_password != confirm_password:
                    flash('Password baru dan konfirmasi Password tidak cocok!', 'error')
                    return redirect(url_for('setting'))
                
                hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
                user_to_update.password_hash = hashed_password

        try :
            db.session.commit()
            flash("user berhasil Diperbarui!.", category="success")
        except :
            flash("error! mohon coba kembali", category="error")

        return redirect(url_for('app.setting', form=form, name_to_update=user_to_update ))
 
    return render_template("setting.html", user=current_user, form=form, name_to_update=user_to_update, id=id)

@App.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logout. Thank You!', category='success')
    return redirect(url_for('view.home'))


def start_detection(nama_pengawas, kelas, matkul):
    global stop_detection, screenshot_db

    import cv2
    import torch
    import torch.backends.cudnn as cudnn
    import numpy as np
    import time
    import datetime

    from numpy import random
    from pathlib import Path

    from models.experimental import attempt_load
    from utils.datasets import LoadStreams, LoadImages
    from utils.general import check_img_size, check_requirements, check_imshow, non_max_suppression, apply_classifier, \
        scale_coords, xyxy2xywh, strip_optimizer, set_logging, increment_path
    from utils.plots import plot_one_box
    from utils.torch_utils import select_device, load_classifier, time_synchronized, TracedModel
    
    video_source = 'rtsp://Adiageng:uhuy123@192.168.1.2:554/stream1'
    # video_source = '0'
    weights = 'yolov7-custom.pt'
    img_size = 640
    conf_thresh = 0.5
    iou_thresh = 0.45
    parent = None
    webcam = video_source.isnumeric() or video_source.endswith('.txt') or video_source.lower().startswith(('rtsp://',
                                                                                                            'rtmp://',
                                                                                                            'http://',
                                                                                                            'https://'))

    save_dir = Path(f'website/static/detect/{nama_pengawas}').resolve() # increment run
    (save_dir).mkdir(parents=True, exist_ok=True)  # make dir

    #Initialize
    set_logging()
    device = select_device('')
    half = device.type != 'cpu'

    ##### RUN YOLO DETECTION
    model = attempt_load(weights, map_location = device)
    stride = int(model.stride.max())
    imgsz = check_img_size(img_size, s=stride)

    if half:
        model.half()
    
    vid_path, vid_writer = None, None
    view_img = check_imshow()
    cudnn.benchmark = True
    dataset = LoadStreams(video_source, img_size = imgsz, stride = stride)

    names = model.module.names if hasattr(model, 'module') else model.names
    colors = [[random.randint(0, 255) for _ in range(3)] for _ in names]

    # Run inference
    if device.type != 'cpu':
        model(torch.zeros(1, 3, imgsz, imgsz).to(device).type_as(next(model.parameters())))
    old_img_w = old_img_h = imgsz
    old_img_b = 1

    t0 = time.time()
    for path, img, im0s, vid_cap in dataset:
        img = torch.from_numpy(img).to(device)
        img = img.half() if half else img.float()
        img /= 255.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)
        if device.type != 'cpu' and (old_img_b != img.shape[0] or old_img_h != img.shape[2] or old_img_w != img.shape[3]):
            old_img_b = img.shape[0]
            old_img_h = img.shape[2]
            old_img_w = img.shape[3]
            for i in range(3):
                model(img, augment = False)[0]
        
        #Inference
        t1 = time_synchronized()
        with torch.no_grad():
            pred = model(img, augment = False)[0]
        t2 = time_synchronized()

        pred = non_max_suppression(pred, conf_thresh, iou_thresh, classes = None, agnostic=False)
        t3 = time_synchronized()

        for i, det in enumerate(pred):
            if stop_detection:
                dataset.cap.release()
                stop_detection = False
                break
            if webcam:
                p, s, im0, frame = path[i], '%g: ' % i, im0s[i].copy(), dataset.count
            
            

            gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]

            if len(det):
                det[:, :4] = scale_coords(img.shape[2:], det[:,:4], im0.shape).round()
                for c in det[:, -1].unique():
                    n = (det[:, -1] == c).sum()
                    s += f"{n} {names[int(c)]}{'s' * (n>1)}, "
                
                for *xyxy, conf, cls in reversed(det):
                    if view_img:
                        label = f'{names[int(cls)]} {conf:.2f}'
                        plot_one_box(xyxy, im0, label = label, color = colors[int(cls)], line_thickness=1)
                    
            
                #Saving screenshot with detection
           
            
                #screenshot_path = save_dir / screenshot_name
                now = datetime.datetime.now()
                timestamp = now.strftime("%H-%M-%S")
                screenshot_name = f"{nama_pengawas}_{kelas}_{matkul}_{timestamp}.jpg"
                save_path = save_dir / screenshot_name
                if str(screenshot_name) not in screenshot_db:
                    screenshot_db.append(str(screenshot_name))


                cv2.imwrite(str(save_path), im0)
                

            ref, buffer = cv2.imencode('.jpg', im0)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + frame +b'\r\n')

@App.route('/webapp')
def webapp():
    nama_pengawas = form_data['nama_pengawas']
    kelas = form_data['classes']
    matkul = form_data['subject']

    return Response(start_detection(nama_pengawas, kelas, matkul), mimetype='multipart/x-mixed-replace; boundary=frame; boundary=frame')


""" @App.route('/start_detection')
def start_detection():
    return redirect(url_for('detection')) """

@App.route('/detection')
def detection():
    return render_template('detection.html')

@App.route('/stop')
def stop():
    global stop_detection, screenshot_db
    stop_detection = True
    
    nama_pengawas = form_data['nama_pengawas']
    tanggal = form_data['date']
    jam = form_data['time']
    ruangan = form_data['room']
    kelas = form_data['classes']
    matkul = form_data['subject']

    history = History.query.filter_by(
        name = nama_pengawas,
        subject = matkul,
        date = tanggal,
        time = jam,
        room = ruangan,
        classes = kelas        
    ).first()


    #print(screenshot_db)
    history.screenshots.clear()
    for path in screenshot_db:
    #    print(path)
        screenshot = Screenshot(path=path)
        db.session.add(screenshot)
        history.screenshots.append(screenshot)
    
    db.session.commit()
    screenshot_db = []

    return render_template('histori.html')

    
@App.route('/upload_profile_picture', methods=['POST'])
@login_required  # Decorator to ensure the user is logged in
def upload_profile_picture():
    file = request.files['file']
    if file:
        filename = save_profile_picture(file)
        if filename:
            current_user.profile_picture = filename
            db.session.commit()
            profile_picture_url = url_for('static', filename= '/uploads/'+ filename)
            return jsonify({'success': True, 'profile_picture_url': profile_picture_url})
        else:
            return jsonify({'success': False, 'error': 'Failed to save profile picture.'})
    else:
        return jsonify({'success': False, 'error': 'No file uploaded.'})

def save_profile_picture(file):
    app = current_app._get_current_object()
    if file and allowed_file(file.filename):
        filename = 'user_profile_picture.png'  # Set the desired filename for the profile picture
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return filename
    else:
        return 'static/default/default_user.png'