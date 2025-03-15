import os
import uuid
import platform
import subprocess
import requests
import sys
import time
import hashlib
import json
from flask import Flask, request, render_template, jsonify, session, redirect, url_for
from werkzeug.utils import secure_filename
from functools import wraps

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

# URL của file users.json và check-convert trên GitHub
USERS_FILE_URL = "https://raw.githubusercontent.com/thayphuctoan/pconvert/refs/heads/main/latex.json"
ACTIVATION_FILE_URL = "https://raw.githubusercontent.com/thayphuctoan/pconvert/main/check-convert"

# Cache các dữ liệu từ GitHub
users_cache = {"data": None, "timestamp": 0}
activation_cache = {"data": None, "timestamp": 0}

# ------------------------------ Authentication Functions ------------------------------
def get_users():
    """Lấy danh sách người dùng từ GitHub với cache 5 phút"""
    current_time = time.time()
    if users_cache["data"] is None or current_time - users_cache["timestamp"] > 300:
        try:
            response = requests.get(USERS_FILE_URL)
            if response.status_code == 200:
                users_cache["data"] = json.loads(response.text)
                users_cache["timestamp"] = current_time
                return users_cache["data"]
            else:
                return {}
        except Exception as e:
            print(f"Lỗi khi lấy danh sách người dùng: {str(e)}")
            return {}
    return users_cache["data"]

def get_activated_ids():
    """Lấy danh sách ID đã kích hoạt từ GitHub với cache 5 phút"""
    current_time = time.time()
    if activation_cache["data"] is None or current_time - activation_cache["timestamp"] > 300:
        try:
            response = requests.get(ACTIVATION_FILE_URL)
            if response.status_code == 200:
                activation_cache["data"] = response.text.strip().split('\n')
                activation_cache["timestamp"] = current_time
                return activation_cache["data"]
            else:
                return []
        except Exception as e:
            print(f"Lỗi khi lấy danh sách ID kích hoạt: {str(e)}")
            return []
    return activation_cache["data"]

def authenticate_user(username, password):
    """Xác thực người dùng"""
    users = get_users()
    if username in users and users[username] == password:
        return True
    return False

def generate_hardware_id(username):
    """Tạo hardware ID cố định từ username"""
    hardware_id = hashlib.md5(username.encode()).hexdigest().upper()
    formatted_id = '-'.join([hardware_id[i:i+8] for i in range(0, len(hardware_id), 8)])
    return formatted_id + "-Premium"

def check_activation(hardware_id):
    """Kiểm tra kích hoạt"""
    activated_ids = get_activated_ids()
    return hardware_id in activated_ids

def login_required(f):
    """Decorator yêu cầu đăng nhập"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session or not session['logged_in']:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def activation_required(f):
    """Decorator yêu cầu kích hoạt"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session or not session['logged_in']:
            return redirect(url_for('login'))
        
        if 'activation_status' not in session or session['activation_status'] != "ĐÃ KÍCH HOẠT":
            return redirect(url_for('activation_status'))
            
        return f(*args, **kwargs)
    return decorated_function

# ------------------------------ Hardware identification functions ------------------------------
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

# ------------------------------ Authentication/Authorization Middleware ------------------------------
@app.before_request
def check_auth():
    # Paths that don't require authentication
    auth_exempt_paths = ['/login', '/register', '/api/login', '/api/register', 
                         '/static', '/check_activation', '/system_info']
    
    # Check if path is exempt from authentication
    for path in auth_exempt_paths:
        if request.path.startswith(path):
            return None
    
    # Check if logged in for other paths
    if 'logged_in' not in session or not session['logged_in']:
        if request.content_type == 'application/json':
            return jsonify({'status': 'error', 'message': 'Bạn cần đăng nhập để sử dụng chức năng này'}), 401
        else:
            return redirect(url_for('login'))
    
    # Check activation for paths that require it
    activation_exempt_paths = ['/activation_status', '/api/activation-status', '/api/check-activation']
    if not any(request.path.startswith(path) for path in activation_exempt_paths):
        if 'activation_status' not in session or session['activation_status'] != "ĐÃ KÍCH HOẠT":
            if request.content_type == 'application/json':
                return jsonify({'status': 'error', 'message': 'Bạn cần kích hoạt phần mềm để sử dụng chức năng này'}), 403
            else:
                return redirect(url_for('activation_status'))

# ------------------------------ Authentication Routes ------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.content_type == 'application/json':
            data = request.json
            username = data.get('username')
            password = data.get('password')
        else:
            username = request.form.get('username')
            password = request.form.get('password')
        
        if authenticate_user(username, password):
            session['logged_in'] = True
            session['username'] = username
            
            # Kiểm tra kích hoạt
            hardware_id = generate_hardware_id(username)
            session['hardware_id'] = hardware_id
            
            if check_activation(hardware_id):
                session['activation_status'] = "ĐÃ KÍCH HOẠT"
                if request.content_type == 'application/json':
                    return jsonify({"success": True, "activated": True})
                else:
                    return redirect(url_for('index'))
            else:
                session['activation_status'] = "CHƯA KÍCH HOẠT"
                if request.content_type == 'application/json':
                    return jsonify({"success": True, "activated": False})
                else:
                    return redirect(url_for('activation_status'))
        else:
            if request.content_type == 'application/json':
                return jsonify({"success": False, "message": "Tên đăng nhập hoặc mật khẩu không đúng"})
            else:
                return render_template('login.html', error="Tên đăng nhập hoặc mật khẩu không đúng")
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if request.content_type == 'application/json':
            data = request.json
            username = data.get('username')
            password = data.get('password')
            email = data.get('email')
        else:
            username = request.form.get('username')
            password = request.form.get('password')
            email = request.form.get('email')
        
        users = get_users()
        if username in users:
            if request.content_type == 'application/json':
                return jsonify({"success": False, "message": "Tên đăng nhập đã tồn tại"})
            else:
                return render_template('register.html', error="Tên đăng nhập đã tồn tại")
        
        # Trong môi trường thực tế, bạn sẽ cần một cơ chế để cập nhật file users.json
        # Ở đây chúng ta giả định là đã đăng ký thành công
        
        hardware_id = generate_hardware_id(username)
        
        if request.content_type == 'application/json':
            return jsonify({
                "success": True,
                "message": "Đăng ký thành công! Vui lòng liên hệ với nhà cung cấp để kích hoạt.",
                "hardwareId": hardware_id
            })
        else:
            return render_template('register.html', 
                                success="Đăng ký thành công! Vui lòng liên hệ với nhà cung cấp để kích hoạt.",
                                hardware_id=hardware_id)
    
    return render_template('register.html')

@app.route('/activation_status')
@login_required
def activation_status():
    username = session.get('username')
    hardware_id = session.get('hardware_id')
    activation_status = session.get('activation_status')
    
    # Kiểm tra lại trạng thái kích hoạt mỗi khi vào trang này
    if hardware_id and check_activation(hardware_id):
        session['activation_status'] = "ĐÃ KÍCH HOẠT"
        activation_status = "ĐÃ KÍCH HOẠT"
    
    return render_template('activation.html', 
                          username=username,
                          hardware_id=hardware_id,
                          activation_status=activation_status)

@app.route('/check_activation')
@login_required
def check_activation_route():
    hardware_id = session.get('hardware_id')
    
    if hardware_id and check_activation(hardware_id):
        session['activation_status'] = "ĐÃ KÍCH HOẠT"
        return redirect(url_for('index'))
    else:
        session['activation_status'] = "CHƯA KÍCH HOẠT"
        return redirect(url_for('activation_status'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ------------------------------ API Authentication Routes ------------------------------
@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if authenticate_user(username, password):
        session['logged_in'] = True
        session['username'] = username
        
        # Kiểm tra kích hoạt
        hardware_id = generate_hardware_id(username)
        session['hardware_id'] = hardware_id
        
        if check_activation(hardware_id):
            session['activation_status'] = "ĐÃ KÍCH HOẠT"
            activated = True
        else:
            session['activation_status'] = "CHƯA KÍCH HOẠT"
            activated = False
        
        return jsonify({"success": True, "activated": activated})
    else:
        return jsonify({"success": False, "message": "Tên đăng nhập hoặc mật khẩu không đúng"})

@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    
    users = get_users()
    if username in users:
        return jsonify({"success": False, "message": "Tên đăng nhập đã tồn tại"})
    
    # Trong môi trường thực tế, bạn sẽ cần một cơ chế để cập nhật file users.json
    # Ở đây chúng ta giả định là đã đăng ký thành công
    
    hardware_id = generate_hardware_id(username)
    
    return jsonify({
        "success": True,
        "message": "Đăng ký thành công! Vui lòng liên hệ với nhà cung cấp để kích hoạt.",
        "hardwareId": hardware_id
    })

@app.route('/api/activation-status')
def api_activation_status():
    if 'logged_in' not in session or not session['logged_in']:
        return jsonify({"error": "Unauthorized", "message": "Bạn cần đăng nhập trước"}), 401
    
    username = session.get('username')
    hardware_id = session.get('hardware_id')
    
    # Kiểm tra lại trạng thái kích hoạt
    activated = False
    if hardware_id and check_activation(hardware_id):
        session['activation_status'] = "ĐÃ KÍCH HOẠT"
        activated = True
    else:
        session['activation_status'] = "CHƯA KÍCH HOẠT"
    
    return jsonify({
        "username": username,
        "hardwareId": hardware_id,
        "activated": activated
    })

@app.route('/api/check-activation')
def api_check_activation():
    if 'logged_in' not in session or not session['logged_in']:
        return jsonify({"error": "Unauthorized", "message": "Bạn cần đăng nhập trước"}), 401
    
    hardware_id = session.get('hardware_id')
    
    activated = False
    if hardware_id and check_activation(hardware_id):
        session['activation_status'] = "ĐÃ KÍCH HOẠT"
        activated = True
    else:
        session['activation_status'] = "CHƯA KÍCH HOẠT"
    
    return jsonify({"activated": activated})

# ------------------------------ Main routes ------------------------------
@app.route('/')
def index():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))
        
    if 'activation_status' not in session or session['activation_status'] != "ĐÃ KÍCH HOẠT":
        return redirect(url_for('activation_status'))
        
    return render_template('index.html')

@app.route('/system_info')
def system_info_route():
    # Trả về ID phần cứng từ session nếu đã đăng nhập
    if 'logged_in' in session and session['logged_in'] and 'hardware_id' in session:
        return jsonify({"system_info": session['hardware_id']})
    
    # Nếu chưa đăng nhập, trả về thông tin hệ thống thông thường
    info = get_system_info()
    return jsonify({"system_info": info})

# ------------------------------ BBT routes ------------------------------
@app.route('/bbt_auto', methods=['GET', 'POST'])
@activation_required
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
@activation_required
def bbt_manual():
    if request.method == 'POST':
        data = request.json
        result = generate_bbt_manual(data)
        return jsonify(result)
    
    return render_template('bbt_manual.html')

# ------------------------------ Graph routes ------------------------------
@app.route('/graph_standard', methods=['GET', 'POST'])
@activation_required
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
@activation_required
def graph_custom():
    if request.method == 'POST':
        data = request.json
        result = generate_custom_graph(data)
        return jsonify(result)
    
    return render_template('graph_custom.html')

# ------------------------------ Conversion routes ------------------------------
@app.route('/convert_ex', methods=['GET', 'POST'])
@activation_required
def convert_ex():
    if request.method == 'POST':
        text = request.json.get('text', '')
        result = mathpix_to_ex_web(text)
        return jsonify(result)
    
    return render_template('convert_ex.html')

@app.route('/convert_extf', methods=['GET', 'POST'])
@activation_required
def convert_extf():
    if request.method == 'POST':
        text = request.json.get('text', '')
        result = mathpix_to_extf_web(text)
        return jsonify(result)
    
    return render_template('convert_extf.html')

@app.route('/convert_bt', methods=['GET', 'POST'])
@activation_required
def convert_bt():
    if request.method == 'POST':
        text = request.json.get('text', '')
        result = mathpix_to_bt_web(text)
        return jsonify(result)
    
    return render_template('convert_bt.html')

@app.route('/convert_vd', methods=['GET', 'POST'])
@activation_required
def convert_vd():
    if request.method == 'POST':
        text = request.json.get('text', '')
        result = mathpix_to_vd_web(text)
        return jsonify(result)
    
    return render_template('convert_vd.html')

@app.route('/add_true', methods=['GET', 'POST'])
@activation_required
def add_true():
    if request.method == 'POST':
        data = request.json
        result = add_true_to_answers_web(data)
        return jsonify(result)
    
    return render_template('add_true.html')

# ------------------------------ HKG routes ------------------------------
@app.route('/hkg', methods=['GET', 'POST'])
@activation_required
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
    # Kiểm tra nếu đang chạy trong môi trường phát triển
    if not os.environ.get('RENDER') and not os.environ.get('FLY_APP_NAME'):
        app.run(debug=True)
    else:
        # Khi sử dụng gunicorn, không cần gọi app.run()
        port = int(os.environ.get('PORT', 8080))
        app.run(host='0.0.0.0', port=port)
