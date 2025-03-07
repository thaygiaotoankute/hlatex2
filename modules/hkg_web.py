# Web-adapted version of hkg.py
# This module extracts the core functionality without PyQt dependencies

from modules.def_hkg import *

def generate_tudiencb_web(data):
    """Generate Tu Dien Co Ban (Web version)"""
    try:
        # Extract parameters from the request
        A = data.get('tda', 'A')
        B = data.get('tdb', 'B')
        C = data.get('tdc', 'C')
        D = data.get('tdd', 'D')
        
        # Generate the LaTeX code
        block = tu_dien_co_ban_course(A, B, C, D)
        
        # Return a structured response
        return {
            "status": "success",
            "latex": block,
            "title": f"Tứ diện {A}{B}{C}{D}"
        }
    except ValueError as error:
        return {"status": "error", "message": str(error)}

def generate_chop_tam_giac(data):
    """Generate different types of triangular-based pyramids"""
    try:
        chop_type = data.get('chop_type', '')
        
        if chop_type == 'loai_mot':
            # S.ABC có h=SA
            S = data.get('tg1s', 'S')
            A = data.get('tg1a', 'A')
            B = data.get('tg1b', 'B')
            C = data.get('tg1c', 'C')
            block = chop_tam_giac_loai_mot_source(S, A, B, C)
            title = f"Chóp tam giác {S}.{A}{B}{C} có h={S}{A}"
        elif chop_type == 'loai_hai':
            # S.ABC đều
            S = data.get('tg2s', 'S')
            A = data.get('tg2a', 'A')
            B = data.get('tg2b', 'B')
            C = data.get('tg2c', 'C')
            G = data.get('tg2g', 'G')
            M = data.get('tg2m', 'M')
            block = chop_tam_giac_loai_hai_source(S, A, B, C, G, M)
            title = f"Chóp tam giác đều {S}.{A}{B}{C}"
        elif chop_type == 'loai_ba':
            # S.ABC có SBC đứng
            S = data.get('tg3s', 'S')
            A = data.get('tg3a', 'A')
            B = data.get('tg3b', 'B')
            C = data.get('tg3c', 'C')
            H = data.get('tg3h', 'H')
            block = chop_tam_giac_loai_ba_source(S, A, B, C, H)
            title = f"Chóp tam giác {S}.{A}{B}{C} có {S}{B}{C} đứng"
        else:
            return {"status": "error", "message": "Loại chóp tam giác không hợp lệ"}
        
        # Return a structured response
        return {
            "status": "success",
            "latex": block,
            "title": title
        }
    except ValueError as error:
        return {"status": "error", "message": str(error)}

def generate_chop_tu_giac(data):
    """Generate different types of quadrilateral-based pyramids"""
    try:
        chop_type = data.get('chop_type', '')
        
        if chop_type == 'loai_mot':
            # S.ABCD có h=SA
            S = data.get('tug1s', 'S')
            A = data.get('tug1a', 'A')
            B = data.get('tug1b', 'B')
            C = data.get('tug1c', 'C')
            D = data.get('tug1d', 'D')
            block = chop_tu_giac_loai_mot_source(S, A, B, C, D)
            title = f"Chóp tứ giác {S}.{A}{B}{C}{D} có h={S}{A}"
        elif chop_type == 'loai_hai':
            # S.ABCD đều
            S = data.get('tug2s', 'S')
            A = data.get('tug2a', 'A')
            B = data.get('tug2b', 'B')
            C = data.get('tug2c', 'C')
            D = data.get('tug2d', 'D')
            G = data.get('tug2g', 'G')
            block = chop_tu_giac_loai_hai_source(S, A, B, C, D, G)
            title = f"Chóp tứ giác đều {S}.{A}{B}{C}{D}"
        elif chop_type == 'loai_ba':
            # S.ABCD có SAB đứng
            S = data.get('tug3s', 'S')
            A = data.get('tug3a', 'A')
            B = data.get('tug3b', 'B')
            C = data.get('tug3c', 'C')
            D = data.get('tug3d', 'D')
            H = data.get('tug3h', 'H')
            block = chop_tu_giac_loai_ba_source(S, A, B, C, D, H)
            title = f"Chóp tứ giác {S}.{A}{B}{C}{D} có {S}{A}{B} đứng"
        else:
            return {"status": "error", "message": "Loại chóp tứ giác không hợp lệ"}
        
        # Return a structured response
        return {
            "status": "success",
            "latex": block,
            "title": title
        }
    except ValueError as error:
        return {"status": "error", "message": str(error)}

def generate_lang_tru(data):
    """Generate different types of prisms"""
    try:
        lang_tru_type = data.get('lang_tru_type', '')
        
        if lang_tru_type == 'dung':
            # Lăng trụ đứng tam giác
            M = data.get('lt1m', 'M')
            N = data.get('lt1n', 'N')
            P = data.get('lt1p', 'P')
            A = data.get('lt1a', 'A')
            B = data.get('lt1b', 'B')
            C = data.get('lt1c', 'C')
            block = lang_tru_dung_source(A, B, C, M, N, P)
            title = f"Lăng trụ đứng tam giác {A}{B}{C}.{M}{N}{P}"
        elif lang_tru_type == 'xien':
            # Lăng trụ xiên tam giác
            M = data.get('lt2m', 'M')
            N = data.get('lt2n', 'N')
            P = data.get('lt2p', 'P')
            A = data.get('lt2a', 'A')
            B = data.get('lt2b', 'B')
            C = data.get('lt2c', 'C')
            block = lang_tru_xien_source(A, B, C, M, N, P)
            title = f"Lăng trụ xiên tam giác {A}{B}{C}.{M}{N}{P}"
        else:
            return {"status": "error", "message": "Loại lăng trụ không hợp lệ"}
        
        # Return a structured response
        return {
            "status": "success",
            "latex": block,
            "title": title
        }
    except ValueError as error:
        return {"status": "error", "message": str(error)}

def generate_hinh_hop(data):
    """Generate different types of rectangular prisms"""
    try:
        hinh_hop_type = data.get('hinh_hop_type', '')
        
        if hinh_hop_type == 'chu_nhat':
            # Hình hộp chữ nhật
            M = data.get('hh1m', 'M')
            N = data.get('hh1n', 'N')
            P = data.get('hh1p', 'P')
            Q = data.get('hh1q', 'Q')
            A = data.get('hh1a', 'A')
            B = data.get('hh1b', 'B')
            C = data.get('hh1c', 'C')
            D = data.get('hh1d', 'D')
            block = hinh_hop_chu_nhat_source(A, B, C, D, M, N, P, Q)
            title = f"Hình hộp chữ nhật {A}{B}{C}{D}.{M}{N}{P}{Q}"
        elif hinh_hop_type == 'thuong':
            # Hình hộp thường
            M = data.get('hh2m', 'M')
            N = data.get('hh2n', 'N')
            P = data.get('hh2p', 'P')
            Q = data.get('hh2q', 'Q')
            A = data.get('hh2a', 'A')
            B = data.get('hh2b', 'B')
            C = data.get('hh2c', 'C')
            D = data.get('hh2d', 'D')
            block = hinh_hop_thuong_source(A, B, C, D, M, N, P, Q)
            title = f"Hình hộp thường {A}{B}{C}{D}.{M}{N}{P}{Q}"
        elif hinh_hop_type == 'lap_phuong':
            # Hình lập phương
            M = data.get('hh3m', 'M')
            N = data.get('hh3n', 'N')
            P = data.get('hh3p', 'P')
            Q = data.get('hh3q', 'Q')
            A = data.get('hh3a', 'A')
            B = data.get('hh3b', 'B')
            C = data.get('hh3c', 'C')
            D = data.get('hh3d', 'D')
            block = hinh_lap_phuong_source(A, B, C, D, M, N, P, Q)
            title = f"Hình lập phương {A}{B}{C}{D}.{M}{N}{P}{Q}"
        else:
            return {"status": "error", "message": "Loại hình hộp không hợp lệ"}
        
        # Return a structured response
        return {
            "status": "success",
            "latex": block,
            "title": title
        }
    except ValueError as error:
        return {"status": "error", "message": str(error)}

def generate_khoi_non(data):
    """Generate cone shape"""
    try:
        R = data.get('hnr', '2')
        h = data.get('hnh', '3')
        
        # Generate the LaTeX code
        block = khoi_non_course(R, h)
        
        # Return a structured response
        return {
            "status": "success",
            "latex": block,
            "title": f"Khối nón"
        }
    except ValueError as error:
        return {"status": "error", "message": str(error)}

def generate_khoi_tru(data):
    """Generate cylinder shape"""
    try:
        R = data.get('htr', '2')
        h = data.get('hth', '3')
        
        # Generate the LaTeX code
        block = khoi_tru_course(R, h)
        
        # Return a structured response
        return {
            "status": "success",
            "latex": block,
            "title": f"Khối trụ"
        }
    except ValueError as error:
        return {"status": "error", "message": str(error)}

def generate_khoi_cau(data):
    """Generate sphere shape"""
    try:
        R = data.get('hcr', '2')
        
        # Generate the LaTeX code
        block = khoi_cau_course(R)
        
        # Return a structured response
        return {
            "status": "success",
            "latex": block,
            "title": f"Khối cầu"
        }
    except ValueError as error:
        return {"status": "error", "message": str(error)}
