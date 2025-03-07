# Web-adapted version of bbtv2.py
# This module extracts the core functionality without PyQt dependencies

import re

def generate_bbt_manual(data):
    """Generate a custom BBT based on user input"""
    try:
        # Extract data from the request
        row_headers = data.get('rowHeaders', [])
        values = data.get('values', {})
        
        # Determine which type of BBT to generate
        if "Biến" in row_headers and "Xét dấu" in row_headers and "Giá trị" in row_headers:
            block = generate_bbt_loai_1(values)
        elif "Biến" in row_headers and "Xét dấu" in row_headers and "Giá trị" not in row_headers:
            block = generate_bxd(values)
        elif "Biến" in row_headers and "Giá trị" in row_headers and "Xét dấu" not in row_headers:
            block = generate_bbt_loai_2(values)
        else:
            return {"status": "error", "message": "Không đáp ứng bất kỳ điều kiện định dạng nào."}
        
        # Return a structured response
        return {
            "status": "success",
            "latex": block,
            "title": "Bảng biến thiên thủ công"
        }
    except Exception as error:
        return {"status": "error", "message": str(error)}

def generate_bbt_loai_1(values):
    """Generate BBT type 1 - with variable, sign test, and value"""
    try:
        # Extract values from the data
        dong1 = values.get('dong1', '')
        dong2 = values.get('dong2', '')
        dong3 = values.get('dong3', '')
        valueh = values.get('valueh', ["", "", ""])
        
        # Build the LaTeX code
        block = "\\begin{tikzpicture}"\
            + "\n\t\\tkzTabInit[nocadre,lgt=1.2,espcl=2.5]"\
            + f"\n\t{{{valueh[0]}/0.7, {valueh[1]}/0.7, {valueh[2]}/2}}"\
            + f"\n\t{{{dong1}}}"\
            + f"\n\t\\tkzTabLine{{,{dong2},}}"\
            + f"\n\t\\tkzTabVar{{{dong3}}}"\
            + "\n\\end{tikzpicture}"
        
        return block
    except Exception as error:
        raise ValueError(f"Lỗi khi tạo bảng biến thiên loại 1: {str(error)}")

def generate_bxd(values):
    """Generate sign table only - with variable and sign test"""
    try:
        # Extract values from the data
        dong1 = values.get('dong1', '')
        dong2 = values.get('dong2', '')
        valueh = values.get('valueh', ["", ""])
        
        # Build the LaTeX code
        block = "\\begin{tikzpicture}"\
            + "\n\t\\tkzTabInit[nocadre,lgt=1.2,espcl=2.5]"\
            + f"\n\t{{{valueh[0]}/0.7, {valueh[1]}/0.7}}"\
            + f"\n\t{{{dong1}}}"\
            + f"\n\t\\tkzTabLine{{,{dong2},}}"\
            + "\n\\end{tikzpicture}"
        
        return block
    except Exception as error:
        raise ValueError(f"Lỗi khi tạo bảng xét dấu: {str(error)}")

def generate_bbt_loai_2(values):
    """Generate BBT type 2 - with variable and value only"""
    try:
        # Extract values from the data
        dong1 = values.get('dong1', '')
        dong3 = values.get('dong3', '')
        valueh = values.get('valueh', ["", ""])
        
        # Build the LaTeX code
        block = "\\begin{tikzpicture}"\
            + "\n\t\\tkzTabInit[nocadre,lgt=1.2,espcl=2.5]"\
            + f"\n\t{{{valueh[0]}/0.7, {valueh[1]}/2}}"\
            + f"\n\t{{{dong1}}}"\
            + f"\n\t\\tkzTabVar{{{dong3}}}"\
            + "\n\\end{tikzpicture}"
        
        # If dong3 contains fractional values, format them properly
        block = re.sub(r"/([^/\,]*)",r"/$\1$", block)
        
        return block
    except Exception as error:
        raise ValueError(f"Lỗi khi tạo bảng biến thiên loại 2: {str(error)}")
