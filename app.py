import os
import uuid
import platform
import subprocess
import requests
import sys
from flask import Flask, request, render_template, jsonify, session, redirect, url_for
from werkzeug.utils import secure_filename
import json

# Import web-adapted modules
from modules.bbt_web import generate_bbt_bac_nhat, generate_bbt_bac_hai, generate_bbt_bac_ba, generate_bbt_trung_phuong, generate_bbt_mot_mot, generate_bbt_hai_mot
from modules.bbtv2_web import generate_bbt_manual
from modules.graph_web import generate_graph_bac_nhat, generate_graph_bac_hai, generate_graph_bac_ba, generate_graph_trung_phuong, generate_graph_mot_mot, generate_graph_hai_mot
from modules.dothi_web import generate_custom_graph
from modules.mathpix_web import mathpix_to_ex_web, mathpix_to_extf_web, mathpix_to_bt_web, mathpix_to_vd_web
from modules.addtrue_web import add_true_to_answers_web
from modules.hkg_web import generate_tudiencb_web, generate_chop_tam_giac, generate_lang_tru, generate_hinh_hop, generate_khoi_non, generate_khoi_tru, generate_khoi_cau

# Create Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Hardware identification functions
def get_mac_address():
    """Get the MAC address of the current machine."""
    mac = ':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) for i in range(0, 2*6, 8)][::-1])
    return mac

def get_cpu_info():
    """Get the CPU information of the current machine."""
    return platform.processor()

def get_disk_serial():
    """Get the disk serial number of the current machine."""
    try:
        if platform.system() == "Windows":
            output = subprocess.check_output("wmic diskdrive get serialnumber", shell=True).decode()
            serials = output.split()
            return serials[1] if len(serials) > 1 else None
        else:
            return None
    except Exception:
        return None

def get_motherboard_uuid():
    """Get the motherboard UUID of the current machine."""
    try:
        if platform.system() == "Windows":
            output = subprocess.check_output("wmic csproduct get uuid", shell=True).decode()
            uuids = output.split()
            return uuids[1] if len(uuids) > 1 else None
        else:
            return None
    except Exception:
        return None

def get_system_info():
    """
    Combine hardware identifiers into a system info string for licensing.
    
    Returns:
        str: A unique system identifier string
    """
    disk_serial = get_disk_serial() or "unknown-disk"
    motherboard_uuid = get_motherboard_uuid() or "unknown-motherboard"
    # For web app, we might want to use a more web-friendly identifier
    # This is just a placeholder that mimics the original app's behavior
    system_info = f"{disk_serial}-{motherboard_uuid}"
    print(f"System Info: {system_info}")
    return system_info

def check_license(license_code):
    """
    Check if the provided license code is valid.
    
    Args:
        license_code (str): The license code to validate
        
    Returns:
        bool: True if the license is valid, False otherwise
    """
    url = "https://raw.githubusercontent.com/PhucRua/HLatex/main/funny"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            licenses_text = response.text.strip()
            print(f"Fetched licenses:\n{licenses_text}")
            print(f"Checking for license code: {license_code}")
            return license_code in licenses_text
        else:
            print(f"Failed to fetch licenses, status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error checking license: {e}")
        return False

# Registration check middleware
@app.before_request
def check_registration():
    # Paths that don't require registration
    exempt_paths = ['/', '/register', '/static', '/check_registration', '/system_info']
    
    # Check if path is exempt
    for path in exempt_paths:
        if request.path.startswith(path):
            return None
    
    # Check if registered for other paths
    if not session.get('is_registered', False):
        if request.content_type == 'application/json':
            return jsonify({'status': 'error', 'message': 'Bạn cần đăng kí bản quyền để sử dụng chức năng này'}), 403
        else:
            return redirect(url_for('register'))

# Main routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if request.content_type == 'application/json':
            license_code = request.json.get('license_code')
        else:
            license_code = request.form.get('license_code')
            
        is_registered = check_license(license_code)
        if is_registered:
            session['is_registered'] = True
            if request.content_type == 'application/json':
                return jsonify({'status': 'success', 'message': 'Đã đăng kí thành công'})
            else:
                return redirect(url_for('index'))
        else:
            if request.content_type == 'application/json':
                return jsonify({'status': 'error', 'message': 'Mã bản quyền không hợp lệ'})
            else:
                return render_template('register.html', error='Mã bản quyền không hợp lệ')
    
    return render_template('register.html')

@app.route('/check_registration')
def check_registration_status():
    is_registered = session.get('is_registered', False)
    return jsonify({'is_registered': is_registered})

@app.route('/system_info')
def system_info_route():
    info = get_system_info()
    return jsonify({"system_info": info})

# BBT routes
@app.route('/bbt_auto', methods=['GET', 'POST'])
def bbt_auto():
    if request.method == 'POST':
        data = request.json
        func_type = data.get('type')
        
        if func_type == 'bac_nhat':
            a = float(data.get('a', 0))
            b = float(data.get('b', 0))
            result = generate_bbt_bac_nhat(a, b)
        elif func_type == 'bac_hai':
            a = float(data.get('a', 0))
            b = float(data.get('b', 0))
            c = float(data.get('c', 0))
            result = generate_bbt_bac_hai(a, b, c)
        elif func_type == 'bac_ba':
            a = float(data.get('a', 0))
            b = float(data.get('b', 0))
            c = float(data.get('c', 0))
            d = float(data.get('d', 0))
            result = generate_bbt_bac_ba(a, b, c, d)
        elif func_type == 'trung_phuong':
            a = float(data.get('a', 0))
            b = float(data.get('b', 0))
            c = float(data.get('c', 0))
            result = generate_bbt_trung_phuong(a, b, c)
        elif func_type == 'mot_mot':
            a = float(data.get('a', 0))
            b = float(data.get('b', 0))
            c = float(data.get('c', 0))
            d = float(data.get('d', 0))
            result = generate_bbt_mot_mot(a, b, c, d)
        elif func_type == 'hai_mot':
            a = float(data.get('a', 0))
            b = float(data.get('b', 0))
            c = float(data.get('c', 0))
            m = float(data.get('m', 0))
            n = float(data.get('n', 0))
            result = generate_bbt_hai_mot(a, b, c, m, n)
        else:
            result = {'status': 'error', 'message': 'Loại hàm không hợp lệ'}
        
        return jsonify(result)
    
    return render_template('bbt_auto.html')

@app.route('/bbt_manual', methods=['GET', 'POST'])
def bbt_manual():
    if request.method == 'POST':
        data = request.json
        result = generate_bbt_manual(data)
        return jsonify(result)
    
    return render_template('bbt_manual.html')

# Graph routes
@app.route('/graph_standard', methods=['GET', 'POST'])
def graph_standard():
    if request.method == 'POST':
        data = request.json
        func_type = data.get('type')
        
        if func_type == 'bac_nhat':
            a = float(data.get('a', 0))
            b = float(data.get('b', 0))
            result = generate_graph_bac_nhat(a, b)
        elif func_type == 'bac_hai':
            a = float(data.get('a', 0))
            b = float(data.get('b', 0))
            c = float(data.get('c', 0))
            result = generate_graph_bac_hai(a, b, c)
        elif func_type == 'bac_ba':
            a = float(data.get('a', 0))
            b = float(data.get('b', 0))
            c = float(data.get('c', 0))
            d = float(data.get('d', 0))
            result = generate_graph_bac_ba(a, b, c, d)
        elif func_type == 'trung_phuong':
            a = float(data.get('a', 0))
            b = float(data.get('b', 0))
            c = float(data.get('c', 0))
            result = generate_graph_trung_phuong(a, b, c)
        elif func_type == 'mot_mot':
            a = float(data.get('a', 0))
            b = float(data.get('b', 0))
            c = float(data.get('c', 0))
            d = float(data.get('d', 0))
            result = generate_graph_mot_mot(a, b, c, d)
        elif func_type == 'hai_mot':
            a = float(data.get('a', 0))
            b = float(data.get('b', 0))
            c = float(data.get('c', 0))
            m = float(data.get('m', 0))
            n = float(data.get('n', 0))
            result = generate_graph_hai_mot(a, b, c, m, n)
        else:
            result = {'status': 'error', 'message': 'Loại hàm không hợp lệ'}
        
        return jsonify(result)
    
    return render_template('graph_standard.html')

@app.route('/graph_custom', methods=['GET', 'POST'])
def graph_custom():
    if request.method == 'POST':
        data = request.json
        result = generate_custom_graph(data)
        return jsonify(result)
    
    return render_template('graph_custom.html')

# Conversion routes
@app.route('/convert_ex', methods=['GET', 'POST'])
def convert_ex():
    if request.method == 'POST':
        text = request.json.get('text', '')
        result = mathpix_to_ex_web(text)
        return jsonify(result)
    
    return render_template('convert_ex.html')

@app.route('/convert_extf', methods=['GET', 'POST'])
def convert_extf():
    if request.method == 'POST':
        text = request.json.get('text', '')
        result = mathpix_to_extf_web(text)
        return jsonify(result)
    
    return render_template('convert_extf.html')

@app.route('/convert_bt', methods=['GET', 'POST'])
def convert_bt():
    if request.method == 'POST':
        text = request.json.get('text', '')
        result = mathpix_to_bt_web(text)
        return jsonify(result)
    
    return render_template('convert_bt.html')

@app.route('/convert_vd', methods=['GET', 'POST'])
def convert_vd():
    if request.method == 'POST':
        text = request.json.get('text', '')
        result = mathpix_to_vd_web(text)
        return jsonify(result)
    
    return render_template('convert_vd.html')

@app.route('/add_true', methods=['GET', 'POST'])
def add_true():
    if request.method == 'POST':
        data = request.json
        result = add_true_to_answers_web(data)
        return jsonify(result)
    
    return render_template('add_true.html')

# HKG routes
@app.route('/hkg', methods=['GET', 'POST'])
def hkg():
    if request.method == 'POST':
        data = request.json
        hkg_type = data.get('type')
        
        if hkg_type == 'tu_dien_co_ban':
            result = generate_tudiencb_web(data)
        elif hkg_type == 'chop_tam_giac':
            result = generate_chop_tam_giac(data)
        elif hkg_type == 'lang_tru':
            result = generate_lang_tru(data)
        elif hkg_type == 'hinh_hop':
            result = generate_hinh_hop(data)
        elif hkg_type == 'khoi_non':
            result = generate_khoi_non(data)
        elif hkg_type == 'khoi_tru':
            result = generate_khoi_tru(data)
        elif hkg_type == 'khoi_cau':
            result = generate_khoi_cau(data)
        else:
            result = {'status': 'error', 'message': 'Loại mẫu hình không hợp lệ'}
        
        return jsonify(result)
    
    return render_template('hkg.html')

if __name__ == '__main__':
    # Check if running on render.com
    is_production = os.environ.get('RENDER', False)
    if is_production:
        # Running in production on render.com
        port = int(os.environ.get('PORT', 10000))
        app.run(host='0.0.0.0', port=port)
    else:
        # Running locally for development
        app.run(debug=True)
