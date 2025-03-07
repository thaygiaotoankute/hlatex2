# Web-adapted version of graph.py
# This module extracts the core functionality without PyQt dependencies

from modules.def_cal import *
from modules.def_bbt import *

def generate_graph_bac_nhat(a, b):
    """Generate graph for first-degree functions"""
    try:
        a = float(a)
        b = float(b)
        
        block = 'Đồ thị của hàm số $y=' + view_dt_bac_nhat(a, b, x='x') + '$.\n\n'
        block += dothi_bac_nhat_source(a, b, '', '', '')
        
        # Return a structured response
        return {
            "status": "success",
            "latex": block,
            "title": f"Đồ thị hàm bậc nhất",
            "function": f"y = {view_dt_bac_nhat(a, b, x='x')}"
        }
    except ValueError as error:
        return {"status": "error", "message": str(error)}

def generate_graph_bac_hai(a, b, c):
    """Generate graph for quadratic functions"""
    try:
        a = float(a)
        b = float(b)
        c = float(c)
        
        block = 'Đồ thị của hàm số $y=' + view_dt_bac_hai(a, b, c, x='x') + '$.\n\n'
        block += dothi_bac_hai_source(a, b, c, '', '', '')
        
        # Return a structured response
        return {
            "status": "success",
            "latex": block,
            "title": f"Đồ thị hàm bậc hai",
            "function": f"y = {view_dt_bac_hai(a, b, c, x='x')}"
        }
    except ValueError as error:
        return {"status": "error", "message": str(error)}

def generate_graph_bac_ba(a, b, c, d):
    """Generate graph for cubic functions"""
    try:
        a = float(a)
        b = float(b)
        c = float(c)
        d = float(d)
        
        block = 'Đồ thị của hàm số $y=' + view_dt_bac_ba(a, b, c, d, x='x') + '$.\n\n'
        block += dothi_bac_ba_source(a, b, c, d, '', '', '')
        
        # Return a structured response
        return {
            "status": "success",
            "latex": block,
            "title": f"Đồ thị hàm bậc ba",
            "function": f"y = {view_dt_bac_ba(a, b, c, d, x='x')}"
        }
    except ValueError as error:
        return {"status": "error", "message": str(error)}

def generate_graph_trung_phuong(a, b, c):
    """Generate graph for biquadratic functions"""
    try:
        a = float(a)
        b = float(b)
        c = float(c)
        
        block = 'Đồ thị của hàm số $y=' + view_dt_bac_bon(a, 0, b, 0, c, x='x') + '$.\n\n'
        block += dothi_trung_phuong_source(a, b, c, '', '', '')
        
        # Return a structured response
        return {
            "status": "success",
            "latex": block,
            "title": f"Đồ thị hàm trùng phương",
            "function": f"y = {view_dt_bac_bon(a, 0, b, 0, c, x='x')}"
        }
    except ValueError as error:
        return {"status": "error", "message": str(error)}

def generate_graph_mot_mot(a, b, c, d):
    """Generate graph for rational functions (form 1/1)"""
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
            
        block = 'Đồ thị của hàm số $y=\\dfrac{' + view_dt_bac_nhat(a, b, x='x') + '}{' + view_dt_bac_nhat(c, d, x='x') + '}$.\n\n'
        block += dothi_bac_mot_mot_source(a, b, c, d, '', '', '')
        
        # Return a structured response
        return {
            "status": "success",
            "latex": block,
            "title": f"Đồ thị hàm phân thức",
            "function": f"y = \\dfrac{{{view_dt_bac_nhat(a, b, x='x')}}}{{{view_dt_bac_nhat(c, d, x='x')}}}"
        }
    except ValueError as error:
        return {"status": "error", "message": str(error)}

def generate_graph_hai_mot(a, b, c, m, n):
    """Generate graph for rational functions (form 2/1)"""
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
            
        block = 'Đồ thị của hàm số $y=\\dfrac{' + view_dt_bac_hai(a, b, c, x='x') + '}{' + view_dt_bac_nhat(m, n, x='x') + '}$.\n\n'
        block += dothi_bac_hai_mot_source(a, b, c, m, n, '', '', '')
        
        # Return a structured response
        return {
            "status": "success",
            "latex": block,
            "title": f"Đồ thị hàm phân thức",
            "function": f"y = \\dfrac{{{view_dt_bac_hai(a, b, c, x='x')}}}{{{view_dt_bac_nhat(m, n, x='x')}}}"
        }
    except ValueError as error:
        return {"status": "error", "message": str(error)}
