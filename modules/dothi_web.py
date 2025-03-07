# Web-adapted version of dothi.py
# This module extracts the core functionality without PyQt dependencies

import re

def generate_custom_graph(data):
    """Generate a custom graph based on user input"""
    try:
        # Extract parameters from the request
        xmin = data.get('xmin', '')
        xmax = data.get('xmax', '')
        ymin = data.get('ymin', '')
        ymax = data.get('ymax', '')
        gtx = data.get('gtx', '')
        gty = data.get('gty', '')
        hsf = data.get('hsf', '')
        fa = data.get('fa', '')
        fb = data.get('fb', '')
        hsg = data.get('hsg', '')
        ga = data.get('ga', '')
        gb = data.get('gb', '')
        
        # Process input
        if hsf:
            hsf = re.sub(r'(x)', r'(\\\1)', hsf)
            hsf = re.sub(r'(\d)(\(\\x\))', r'\1*\2', hsf)
        
        if hsg:
            hsg = re.sub(r'(x)', r'(\\\1)', hsg)
            hsg = re.sub(r'(\d)(\(\\x\))', r'\1*\2', hsg)
        
        # Generate the LaTeX code
        block = dothi_course(xmin, xmax, ymin, ymax, gtx, gty, hsf, fa, fb, hsg, ga, gb)
        
        # Format functions for title
        f_display = hsf.replace(r'(\x)', 'x').replace(r'\x', 'x')
        g_display = hsg.replace(r'(\x)', 'x').replace(r'\x', 'x') if hsg else ''
        
        # Return a structured response
        return {
            "status": "success",
            "latex": block,
            "title": "Đồ thị hàm tuỳ ý",
            "functions": [
                f"f(x) = {f_display}" if hsf else "",
                f"g(x) = {g_display}" if hsg else ""
            ]
        }
    except ValueError as error:
        return {"status": "error", "message": str(error)}

def dothi_course(xmin, xmax, ymin, ymax, gtx, gty, hsf, fa, fb, hsg, ga, gb):
    """Generate LaTeX code for custom graph"""
    try:
        # Validate inputs
        if xmin and not is_numeric(xmin):
            raise ValueError("xmin phải là số")
        if xmax and not is_numeric(xmax):
            raise ValueError("xmax phải là số")
        if ymin and not is_numeric(ymin):
            raise ValueError("ymin phải là số")
        if ymax and not is_numeric(ymax):
            raise ValueError("ymax phải là số")
        
        # Set default values if not provided
        xmin = xmin or "-5"
        xmax = xmax or "5"
        ymin = ymin or "-5"
        ymax = ymax or "5"
        
        # Build the LaTeX code
        block = "\\begin{tikzpicture}[scale=1,>=stealth, line join=round, line cap=round, line width=1pt]"\
            + f"\n\t\\tikzset{{declare function={{xmin={xmin};xmax={xmax};ymin={ymin};ymax={ymax};}},smooth,samples=450}}"\
            + "\n\t\\path (0,0) node[below left]{$ O $};"

        if gtx:
            block += f"\n\t\\foreach \\x in {{{gtx}}}{{\\draw (\\x,-.05)--(\\x,.05);\\path (\\x,0)node[below]{{$\\x$}};}}"
            
        if gty:
            block += f"\n\t\\foreach \\y in {{{gty}}}{{\\draw (-.05,\\y)--(.05,\\y);\\path (0,\\y)node[left]{{$\\y$}};}}"
            
        block += "\n\t\\draw[->] (xmin,0)--(xmax,0) node[below]{$ x $};"\
            + "\n\t\\draw[->] (0,ymin)--(0,ymax) node[right]{$ y $};"\
            + "\n\t\\clip (xmin+.2,ymin+.2) rectangle (xmax-.2,ymax-.2);"

        if hsf:
            if fa and fb:
                block += f"\n\t\\draw  plot[domain={fa}:{fb}] (\\x, {{{hsf}}});"
            else:
                block += f"\n\t\\draw  plot[domain=xmin+.2:xmax-.2] (\\x, {{{hsf}}});"
                
        if hsg:
            if ga and gb:
                block += f"\n\t\\draw  plot[domain={ga}:{gb}] (\\x, {{{hsg}}});"
            else:
                block += f"\n\t\\draw  plot[domain=xmin+.2:xmax-.2] (\\x, {{{hsg}}});"
                
        block += "\n\\end{tikzpicture}"
        
        return block
    except Exception as error:
        raise ValueError(f"Lỗi khi tạo đồ thị: {str(error)}")

def is_numeric(value):
    """Check if a value is numeric"""
    try:
        float(value)
        return True
    except ValueError:
        return False
