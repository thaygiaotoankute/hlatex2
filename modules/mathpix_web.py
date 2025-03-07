# Web-adapted version of mathpix.py
# This module extracts the core functionality without PyQt dependencies

import re

def mathpix_to_ex_web(text):
    """Convert text to ex format (Web version)"""
    try:
        if not text:
            return {
                "status": "error",
                "message": "Vui lòng nhập nội dung cần chuyển đổi"
            }
            
        # Apply all transformations from the original function
        text = text.replace('frac','dfrac')
        text = text.replace('right.','rightcham')
        text = text.replace('BON','Câu')
        text = text.replace('DPAD','Câu')
        text = text.replace('Bài','Câu')
        text = text.replace('Ví dụ','Câu')
        text = re.sub(r'(d+)',"d", text)
        text = re.sub(r'(\^\{\\prime\})','\'', text)
        text = re.sub(r'(\n+)',r'\n', text)
        text = re.sub(r'([\^\_])\{([\da-z])\}',r'\1\2', text)
        text = re.sub(r'([\^\_]\{)\\dfrac',r'\1\\tfrac', text)
        text = re.sub(r'(\\int)(\\lim)(\\min)(\\max)(\_.{1,})',r'\1\2\3\4\\limits\5', text)
        text = re.sub(r'\\mathrm\{(.*?)\}',r'\1', text)
        text = re.sub(r'([A-D]\.\s.{1,})[.,]',r'\1', text)
        text = re.sub(r'([A-D]\.\s.{1,})',r'\1.', text)
        text = re.sub(r'([A-D]\.\s)(-?[\d]{1,}[.,]?[\d]{1,})\s?\.?',r'\1$\2$.', text)
        text = re.sub(r'([A-Z\']{1,}\s)\\cdot(\s[A-Z\']{1,})',r'\1.\2', text)
        text = re.sub(r'!\[\]\(.*?\)','%Hình vẽ', text)
        text = re.sub(r'(Câu\s[\d]{1,})([.:]?)\s+\[.*?\]',r'\1.', text)
        text = re.sub(r'(Câu)(\s[\d]{1,})([.:]?)',r'\1\2.', text)
        text = re.sub(r'(Giải[.:])',r'Lời giải.', text)
        text = re.sub(r'(Lời giải[.:])',r'Lời giải.', text)
        text = re.sub(r'(Câu\s[\d]{1,}[.:]\s.{1,})',r'ketthuc\n\1', text)
        text = re.sub(r'(Câu\s[\d]{1,}[.:]\s.{1,})',r'\\begin{ex}\n\1', text)
        text = text.replace('ketthuc','\\end{ex}\n')
        text = re.sub(r'[A]\.\s(.{1,})[.,]',r'\\choice\n{\1}', text)
        text = re.sub(r'[B-D]\.\s(.{1,})[.,]',r'{\1}', text)
        text = re.sub(r'(Câu\s[\d]{1,}[.:]\s)',r'', text)
        text = text.replace('rightcham','right.')
        text +="\n\\end{ex}"
        lines = text.splitlines()
        if len(lines) > 2:
            text = '\n'.join(lines[2:])
        else:
            text = ''  
        text = re.sub(r'Lời giải\.(.*?)\\end{ex}', r'\\loigiai{\t\1}\n\\end{ex}', text, flags=re.DOTALL)
        
        # Process special patterns
        patterns = [
            (re.compile(r'\\left\\{\\begin\{array\}\{\w\}(.*?)\\end\{array\}\\right\.', re.DOTALL),
             r'\\heva{\&\1}'),
            (re.compile(r'\\left\[\\begin\{array\}\{\w\}(.*?)\\end\{array\}\\right\.', re.DOTALL),
             r'\\hoac{\&\1}')
        ]
        
        def replacement(match):
            content = match.group(1)
            content = content.replace('\\\\', '\\\\&')
            if match.re.pattern == patterns[0][0].pattern:
                return f'\\heva{{&{content}}}'
            else:
                return f'\\hoac{{&{content}}}'
        
        for pattern, _ in patterns:
            text = pattern.sub(replacement, text)
        
        return {
            "status": "success",
            "converted_text": text,
            "title": "Chuyển đổi sang định dạng ex"
        }
    except Exception as error:
        return {"status": "error", "message": str(error)}

def mathpix_to_extf_web(text):
    """Convert text to extf format (Web version)"""
    try:
        if not text:
            return {
                "status": "error",
                "message": "Vui lòng nhập nội dung cần chuyển đổi"
            }
            
        # Apply all transformations from the original function
        text = text.replace('frac','dfrac')
        text = text.replace('right.','rightcham')
        text = text.replace('BON','Câu')
        text = text.replace('DPAD','Câu')
        text = text.replace('Bài','Câu')
        text = text.replace('Ví dụ','Câu')
        text = re.sub(r'(d+)',"d", text)
        text = re.sub(r'(\^\{\\prime\})','\'', text)
        text = re.sub(r'(\n+)',r'\n', text)
        text = re.sub(r'([\^\_])\{([\da-z])\}',r'\1\2', text)
        text = re.sub(r'(\\int)(\\lim)(\\min)(\\max)(\_.{1,})',r'\1\2\3\4\\limits\5', text)
        text = re.sub(r'\\mathrm\{(.*?)\}',r'\1', text)
        text = re.sub(r'([a-d]\)\s.{1,})[.,]',r'\1', text)
        text = re.sub(r'([a-d]\)\s.{1,})',r'\1.', text)
        text = re.sub(r'([a-d]\.\s)(-?[\d]{1,}[.,]?[\d]{1,})\s?\.?',r'\1$\2$.', text)
        text = re.sub(r'([A-Z\']{1,}\s)\\cdot(\s[A-Z\']{1,})',r'\1.\2', text)
        text = text.replace('Bài','Câu')
        text = text.replace('Ví dụ','Câu')
        text = re.sub(r'!\[\]\(.*?\)','%Hình vẽ', text)
        text = re.sub(r'(Câu\s[\d]{1,})([.:]?)\s+\[.*?\]',r'\1.', text)
        text = re.sub(r'(Câu)(\s[\d]{1,})([.:]?)',r'\1\2.', text)
        text = re.sub(r'(Giải[.:])',r'Lời giải.', text)
        text = re.sub(r'(Lời giải[.:])',r'Lời giải.', text)
        text = re.sub(r'(Câu\s[\d]{1,}[.:]\s.{1,})',r'ketthuc\n\1', text)
        text = re.sub(r'(Câu\s[\d]{1,}[.:]\s.{1,})',r'\\begin{ex}\n\1', text)
        text = text.replace('ketthuc','\\end{ex}\n')
        text = re.sub(r'[a]\)\s(.{1,})[.,]',r'\\choiceTF\n{\1}', text)
        text = re.sub(r'[b-d]\)\s(.{1,})[.,]',r'{\1}', text)
        text = re.sub(r'(Câu\s[\d]{1,}[.:]\s)',r'', text)
        text = text.replace('rightcham','right.')
        text +="\n\\end{ex}"
        lines = text.splitlines()
        if len(lines) > 2:
            text = '\n'.join(lines[2:])
        else:
            text = ''  
        text = re.sub(r'Lời giải\.(.*?)\\end{ex}', r'\\loigiai{\t\1}\n\\end{ex}', text, flags=re.DOTALL)
        
        # Process special patterns
        patterns = [
            (re.compile(r'\\left\\{\\begin\{array\}\{\w\}(.*?)\\end\{array\}\\right\.', re.DOTALL),
             r'\\heva{\&\1}'),
            (re.compile(r'\\left\[\\begin\{array\}\{\w\}(.*?)\\end\{array\}\\right\.', re.DOTALL),
             r'\\hoac{\&\1}')
        ]
        
        def replacement(match):
            content = match.group(1)
            content = content.replace('\\\\', '\\\\&')
            if match.re.pattern == patterns[0][0].pattern:
                return f'\\heva{{&{content}}}'
            else:
                return f'\\hoac{{&{content}}}'
        
        for pattern, _ in patterns:
            text = pattern.sub(replacement, text)
        
        return {
            "status": "success",
            "converted_text": text,
            "title": "Chuyển đổi sang định dạng exTF"
        }
    except Exception as error:
        return {"status": "error", "message": str(error)}

def mathpix_to_bt_web(text):
    """Convert text to bt format (Web version)"""
    try:
        if not text:
            return {
                "status": "error",
                "message": "Vui lòng nhập nội dung cần chuyển đổi"
            }
            
        # Apply all transformations from the original function
        text = text.replace('frac','dfrac')
        text = text.replace('right.','rightcham')
        text = text.replace('BON','Bài')
        text = text.replace('DPAD','Bài')
        text = text.replace('Câu','Bài')
        text = text.replace('Ví dụ','Bài')
        text = re.sub(r'(d+)',"d", text)
        text = re.sub(r'(\^\{\\prime\})','\'', text)
        text = re.sub(r'(\n+)',r'\n', text)
        text = re.sub(r'([\^\_])\{([\da-z])\}',r'\1\2', text)
        text = re.sub(r'(\\int)(\\lim)(\\min)(\\max)(\_.{1,})',r'\1\2\3\4\\limits\5', text)
        text = re.sub(r'\\mathrm\{(.*?)\}',r'\1', text)
        text = re.sub(r'([A-D]\.\s.{1,})[.,]',r'\1', text)
        text = re.sub(r'([A-D]\.\s.{1,})',r'\1.', text)
        text = re.sub(r'([A-D]\.\s)(-?[\d]{1,}[.,]?[\d]{1,})\s?\.?',r'\1$\2$.', text)
        text = re.sub(r'([A-Z\']{1,}\s)\\cdot(\s[A-Z\']{1,})',r'\1.\2', text)
        text = re.sub(r'!\[\]\(.*?\)','%Hình vẽ', text)
        text = re.sub(r'(Bài)(\s[\d]{1,})([.:]?)',r'\1\2.', text)
        text = re.sub(r'(Giải[.:])',r'Lời giải.', text)
        text = re.sub(r'(Lời giải[.:])',r'Lời giải.', text)
        text = re.sub(r'(Bài\s[\d]{1,}[.:]\s.{1,})',r'ketthuc\n\1', text)
        text = re.sub(r'(Bài\s[\d]{1,}[.:]\s.{1,})',r'\\begin{bt}\n\1', text)
        text = text.replace('ketthuc','\\end{bt}\n')
        text = re.sub(r'[A]\.\s(.{1,})[.,]',r'\\choice\n{\1}', text)
        text = re.sub(r'[B-D]\.\s(.{1,})[.,]',r'{\1}', text)
        text = re.sub(r'(Bài\s[\d]{1,}[.:]\s)',r'', text)
        text = text.replace('rightcham','right.')
        text +="\n\\end{bt}"
        lines = text.splitlines()
        if len(lines) > 2:
            text = '\n'.join(lines[2:])
        else:
            text = ''  
        text = re.sub(r'Lời giải\.(.*?)\\end{bt}', r'\\loigiai{\t\1}\n\\end{bt}', text, flags=re.DOTALL)
        
        # Process special patterns
        patterns = [
            (re.compile(r'\\left\\{\\begin\{array\}\{\w\}(.*?)\\end\{array\}\\right\.', re.DOTALL),
             r'\\heva{\&\1}'),
            (re.compile(r'\\left\[\\begin\{array\}\{\w\}(.*?)\\end\{array\}\\right\.', re.DOTALL),
             r'\\hoac{\&\1}')
        ]
        
        def replacement(match):
            content = match.group(1)
            content = content.replace('\\\\', '\\\\&')
            if match.re.pattern == patterns[0][0].pattern:
                return f'\\heva{{&{content}}}'
            else:
                return f'\\hoac{{&{content}}}'
        
        for pattern, _ in patterns:
            text = pattern.sub(replacement, text)
        
        return {
            "status": "success",
            "converted_text": text,
            "title": "Chuyển đổi sang định dạng bt"
        }
    except Exception as error:
        return {"status": "error", "message": str(error)}

def mathpix_to_vd_web(text):
    """Convert text to vd format (Web version)"""
    try:
        if not text:
            return {
                "status": "error",
                "message": "Vui lòng nhập nội dung cần chuyển đổi"
            }
            
        # Apply all transformations from the original function
        text = text.replace('frac','dfrac')
        text = text.replace('right.','rightcham')
        text = text.replace('BON','Ví dụ')
        text = text.replace('DPAD','Ví dụ')
        text = text.replace('Câu','Ví dụ')
        text = text.replace('Bài','Ví dụ')
        text = re.sub(r'(d+)',"d", text)
        text = re.sub(r'(\^\{\\prime\})','\'', text)
        text = re.sub(r'(\n+)',r'\n', text)
        text = re.sub(r'([\^\_])\{([\da-z])\}',r'\1\2', text)
        text = re.sub(r'(\\int)(\\lim)(\\min)(\\max)(\_.{1,})',r'\1\2\3\4\\limits\5', text)
        text = re.sub(r'\\mathrm\{(.*?)\}',r'\1', text)
        text = re.sub(r'([A-D]\.\s.{1,})[.,]',r'\1', text)
        text = re.sub(r'([A-D]\.\s.{1,})',r'\1.', text)
        text = re.sub(r'([A-D]\.\s)(-?[\d]{1,}[.,]?[\d]{1,})\s?\.?',r'\1$\2$.', text)
        text = re.sub(r'([A-Z\']{1,}\s)\\cdot(\s[A-Z\']{1,})',r'\1.\2', text)
        text = re.sub(r'!\[\]\(.*?\)','%Hình vẽ', text)
        text = re.sub(r'(Ví dụ)(\s[\d]{1,})([.:]?)',r'\1\2.', text)
        text = re.sub(r'(Giải[.:])',r'Lời giải.', text)
        text = re.sub(r'(Lời giải[.:])',r'Lời giải.', text)
        text = re.sub(r'(Ví dụ\s[\d]{1,}[.:]\s.{1,})',r'ketthuc\n\1', text)
        text = re.sub(r'(Ví dụ\s[\d]{1,}[.:]\s.{1,})',r'\\begin{vd}\n\1', text)
        text = text.replace('ketthuc','\\end{vd}\n')
        text = re.sub(r'[A]\.\s(.{1,})[.,]',r'\\choice\n{\1}', text)
        text = re.sub(r'[B-D]\.\s(.{1,})[.,]',r'{\1}', text)
        text = re.sub(r'(Ví dụ\s[\d]{1,}[.:]\s)',r'', text)
        text = text.replace('rightcham','right.')
        text +="\n\\end{vd}"
        lines = text.splitlines()
        if len(lines) > 2:
            text = '\n'.join(lines[2:])
        else:
            text = ''  
        text = re.sub(r'Lời giải\.(.*?)\\end{vd}', r'\\loigiai{\t\1}\n\\end{vd}', text, flags=re.DOTALL)
        
        # Process special patterns
        patterns = [
            (re.compile(r'\\left\\{\\begin\{array\}\{\w\}(.*?)\\end\{array\}\\right\.', re.DOTALL),
             r'\\heva{\&\1}'),
            (re.compile(r'\\left\[\\begin\{array\}\{\w\}(.*?)\\end\{array\}\\right\.', re.DOTALL),
             r'\\hoac{\&\1}')
        ]
        
        def replacement(match):
            content = match.group(1)
            content = content.replace('\\\\', '\\\\&')
            if match.re.pattern == patterns[0][0].pattern:
                return f'\\heva{{&{content}}}'
            else:
                return f'\\hoac{{&{content}}}'
        
        for pattern, _ in patterns:
            text = pattern.sub(replacement, text)
        
        return {
            "status": "success",
            "converted_text": text,
            "title": "Chuyển đổi sang định dạng vd"
        }
    except Exception as error:
        return {"status": "error", "message": str(error)}
