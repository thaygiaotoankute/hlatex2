# Web-adapted version of addtrue.py
# This module extracts the core functionality without PyQt dependencies

import re

def add_true_to_answers_web(data):
    """Add \True to answers in LaTeX content (Web version)"""
    try:
        # Extract input from the request
        clipboard_content = data.get('content', '')
        correct_answers = data.get('answers', [])  # List of correct answers (A, B, C, D) for each question
        
        if not clipboard_content:
            return {
                "status": "error",
                "message": "Vui lòng nhập nội dung cần xử lý"
            }
            
        if not correct_answers:
            return {
                "status": "error",
                "message": "Vui lòng chọn các phương án đúng"
            }
        
        # Process the content as in the original function
        clipboard_content = clipboard_content.replace('\t', '')
        num_questions = clipboard_content.count('\\begin{ex}')
        
        # Check if number of questions matches number of answers
        if num_questions != len(correct_answers):
            return {
                "status": "warning",
                "message": f"Số câu hỏi ({num_questions}) không khớp với số phương án đã chọn ({len(correct_answers)})",
                "content": clipboard_content
            }
        
        clipboard_content = re.sub(r'\\dfrac\s\{([^}]*)\}\s\{([^}]*)\}', r'\\dfrac{\1}{\2}', clipboard_content)
        
        # Find all \choice blocks
        pattern = re.compile(r"\\choice\s\{(.*?)\}\s\{(.*?)\}\s\{(.*?)\}\s\{(.*?)\}", re.DOTALL)
        matches = list(pattern.finditer(clipboard_content))
        
        if matches:
            for i, match in enumerate(matches):
                if i < len(correct_answers):
                    correct_answer = correct_answers[i]
                    if correct_answer:
                        answer_map = {"A": 0, "B": 1, "C": 2, "D": 3}
                        if correct_answer in answer_map:
                            correct_answer_index = answer_map[correct_answer]
                            choices = list(match.groups())
                            
                            # Remove existing \True if present
                            choices = [re.sub(r'\\True\s*', '', choice) for choice in choices]
                            
                            # Add \True to the correct answer
                            correct_answer_text = f"\\True {choices[correct_answer_index].strip()}"
                            choices[correct_answer_index] = correct_answer_text
                            
                            # Build the new choice block
                            new_choice_block = f"\\choice\n{{{choices[0]}}}\n{{{choices[1]}}}\n{{{choices[2]}}}\n{{{choices[3]}}}"
                            clipboard_content = clipboard_content.replace(match.group(0), new_choice_block, 1)
            
            # Clean up any formatting issues
            clipboard_content = re.sub(r'\\dfrac\s\{([^}]*)\}\s\{([^}]*)\}', r'\\dfrac{\1}{\2}', clipboard_content)
            
            return {
                "status": "success",
                "content": clipboard_content,
                "message": "Đã thêm \\True vào phương án đúng",
                "title": "Thêm \\True vào phương án đúng"
            }
        else:
            return {"status": "error", "message": "Không tìm thấy cấu trúc \\choice trong nội dung!"}
    except Exception as error:
        return {"status": "error", "message": str(error)}

def count_questions(text):
    """Count the number of questions in the text"""
    return text.count('\\begin{ex}')
