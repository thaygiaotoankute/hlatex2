# Web-adapted version of bbt.py
# This module extracts the core functionality without PyQt dependencies

from modules.def_cal import *
from modules.def_bbt import *

def generate_bbt_bac_nhat(a, b):
    """Generate BBT for first-degree functions"""
    try:
        a = float(a)
        b = float(b)
        
        if a == 0:
            return {
                "status": "error", 
                "message": "Hàm số không đổi trên $\\mathbb{R}$."
            }
        
        # Get the original LaTeX code from the function
        block = 'Bảng biến thiên của hàm số $y=' + view_dt_bac_nhat(a, b, x='x') + '$.\n\n'
        block += bbt_bac_nhat_source(a, b)
        
        # Return a structured response
        return {
            "status": "success",
            "latex": block,
            "title": f"Bảng biến thiên hàm bậc nhất",
            "function": f"y = {view_dt_bac_nhat(a, b, x='x')}"
        }
    except ValueError as error:
        return {"status": "error", "message": str(error)}

def generate_bbt_bac_hai(a, b, c):
    """Generate BBT for quadratic functions"""
    try:
        a = float(a)
        b = float(b)
        c = float(c)
        
        block = 'Bảng biến thiên của hàm số $y=' + view_dt_bac_hai(a, b, c, x='x') + '$.\n\n'
        if float(a) == 0:
            block += bbt_bac_nhat_source(b, c)
        else:
            block += bbt_bac_hai_source(a, b, c)
        
        # Return a structured response
        return {
            "status": "success",
            "latex": block,
            "title": f"Bảng biến thiên hàm bậc hai",
            "function": f"y = {view_dt_bac_hai(a, b, c, x='x')}"
        }
    except ValueError as error:
        return {"status": "error", "message": str(error)}

def generate_bbt_bac_ba(a, b, c, d):
    """Generate BBT for cubic functions"""
    try:
        a = float(a)
        b = float(b)
        c = float(c)
        d = float(d)
        
        block = 'Bảng biến thiên của hàm số $y=' + view_dt_bac_ba(a, b, c, d, x='x') + '$.\n\n'
        if float(a) == 0:
            block += bbt_bac_hai_source(b, c, d)
        else:
            block += bbt_bac_ba_source(a, b, c, d)
        
        # Return a structured response
        return {
            "status": "success",
            "latex": block,
            "title": f"Bảng biến thiên hàm bậc ba",
            "function": f"y = {view_dt_bac_ba(a, b, c, d, x='x')}"
        }
    except ValueError as error:
        return {"status": "error", "message": str(error)}

def generate_bbt_trung_phuong(a, b, c):
    """Generate BBT for biquadratic functions"""
    try:
        a = float(a)
        b = float(b)
        c = float(c)
        
        block = 'Bảng biến thiên của hàm số $y=' + view_dt_bac_bon(a, 0, b, 0, c, x='x') + '$.\n\n'
        block += bbt_trung_phuong_source(a, b, c)
        
        # Return a structured response
        return {
            "status": "success",
            "latex": block,
            "title": f"Bảng biến thiên hàm trùng phương",
            "function": f"y = {view_dt_bac_bon(a, 0, b, 0, c, x='x')}"
        }
    except ValueError as error:
        return {"status": "error", "message": str(error)}

def generate_bbt_mot_mot(a, b, c, d):
    """Generate BBT for rational functions (form 1/1)"""
    try:
        a = float(a)
        b = float(b)
        c = float(c)
        d = float(d)
        
        if c == 0:
            return {
                "status": "error", 
                "message": "Mẫu không thể bằng 0. Vui lòng kiểm tra lại giá trị c."
            }
            
        block = 'Bảng biến thiên của hàm số $y=\\dfrac{' + view_dt_bac_nhat(a, b, x='x') + '}{' + view_dt_bac_nhat(c, d, x='x') + '}$.\n\n'
        block += bbt_mot_mot_source(a, b, c, d)
        
        # Return a structured response
        return {
            "status": "success",
            "latex": block,
            "title": f"Bảng biến thiên hàm phân thức",
            "function": f"y = \\dfrac{{{view_dt_bac_nhat(a, b, x='x')}}}{{{view_dt_bac_nhat(c, d, x='x')}}}"
        }
    except ValueError as error:
        return {"status": "error", "message": str(error)}

def generate_bbt_hai_mot(a, b, c, m, n):
    """Generate BBT for rational functions (form 2/1)"""
    try:
        a = float(a)
        b = float(b)
        c = float(c)
        m = float(m)
        n = float(n)
        
        if m == 0:
            return {
                "status": "error", 
                "message": "Mẫu không thể bằng 0. Vui lòng kiểm tra lại giá trị m."
            }
            
        block = 'Bảng biến thiên của hàm số $y=\\dfrac{' + view_dt_bac_hai(a, b, c, x='x') + '}{' + view_dt_bac_nhat(m, n, x='x') + '}$.\n\n'
        block += bbt_hai_mot_source(a, b, c, m, n)
        
        # Return a structured response
        return {
            "status": "success",
            "latex": block,
            "title": f"Bảng biến thiên hàm phân thức",
            "function": f"y = \\dfrac{{{view_dt_bac_hai(a, b, c, x='x')}}}{{{view_dt_bac_nhat(m, n, x='x')}}}"
        }
    except ValueError as error:
        return {"status": "error", "message": str(error)}
