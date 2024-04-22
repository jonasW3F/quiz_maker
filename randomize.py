import os
import random
import re

def randomize_answers(question_content, question_number):
    """Randomize the order of answers within a question, keeping the [correct] tag, and apply LaTeX command handling workaround."""
    # Temporarily replace backslashes with forward slashes to avoid escaping issues
    question_content_temp = question_content.replace('\\', '/')
    
    # Extract answers, capturing [correct] where present
    answers = re.findall(r'/answer(\[correct\])?\{(.+?)\}', question_content_temp)
    random.shuffle(answers)  # Shuffle the list of answers

    # Construct the randomized answers block, reapplying [correct] where necessary
    randomized_answers = '\n'.join([f'    /answer{correct}{{{answer}}}' for correct, answer in answers])
    
    # Extract the question part, using forward slashes
    question_text = re.findall(r'/question\{(.+?)\}', question_content_temp)
    if question_text:
        # Prepend 'Question X:' to the extracted question text
        modified_question_text = f"Question {question_number}: {question_text[0]}"
        # Replace the original question text with the modified one in the question content
        question_content_temp = re.sub(r'/question\{.+?\}', f'/question{{{modified_question_text}}}', question_content_temp, count=1)
    
    # Replace the answers block with a placeholder, then replace that placeholder with the randomized answers
    question_content_with_placeholder = re.sub(r'/begin\{answers\}.*?/end\{answers\}', 'PLACEHOLDER', question_content_temp, flags=re.DOTALL)
    randomized_question_content = question_content_with_placeholder.replace('PLACEHOLDER', f'/begin{{answers}}\n{randomized_answers}\n/end{{answers}}')
    
    # Revert forward slashes back to backslashes for proper LaTeX syntax
    final_question_content = randomized_question_content.replace('/', '\\')
    
    return final_question_content

def create_exam(folder_path, file_name, version):
    question_number = 1

    """Create an exam file with randomized questions and answers."""
    question_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.startswith('q') and f.endswith('.tex')]
    random.shuffle(question_files)  # Randomize the order of questions
    
    exam_questions = ""
    for q_file in question_files:
        with open(q_file, 'r') as file:
            question_content = file.read()
            randomized_content = randomize_answers(question_content, question_number)
            question_number += 1
            exam_questions += randomized_content + '\n\n'
    
    exam_instructions = r"""
    {\Large
    \begin{center}
    \textbf{Welcome!} Please follow these instructions closely:
    \end{center}

    \begin{enumerate}
        \item \textbf{Exam Materials}: You should have received two sets of papers. The first set contains the exam questions (this one), and the second set is your answer sheet. If something is missing, let us know.
        \item \textbf{Answering Questions}: Each question has three possible answers, but only one is correct. Record your selected answer on the answer sheet. Ensure that your markings are clear and legible to avoid any scoring errors.
        \item \textbf{Filling Out the Answer Sheet}: Clearly fill in your name and the exam version (either A or B, as indicated on this sheet) at the top of the answer sheet.
        \item \textbf{Scoring}:
        \begin{itemize}
            \item \textbf{Correct Answers}: Each correct answer earns you one point.
            \item \textbf{Incorrect Answers}: Each incorrect answer results in a deduction of one point.
            \item \textbf{Multiple Answers}: If you mark more than one answer per question, you will receive a deduction of one point.
            \item \textbf{Unanswered Questions}: Leaving a question unanswered neither adds nor deducts points.
        \end{itemize}
    \end{enumerate}

    \textbf{Important}: Avoid guessing! Given the deduction of points for incorrect answers, it's advisable to answer only if you are reasonably confident in your response.
    \vfill
    \textbf{NAME:} \underline{\hspace{10cm}} % Provides a space for the student to write their name
    }
    """

    exam_content = f"""\\documentclass{{article}}
\\usepackage[margin=1in]{{geometry}}  % Adjust margin here
\\usepackage{{enumitem}}
\\usepackage{{xifthen}}
\\usepackage{{xcolor}}
\\usepackage{{titlesec}}
\\titleformat*{{\\section}}{{\\normalfont\\large\\bfseries}}  % Customize section titles

\\newlist{{answers}}{{enumerate}}{{1}}
\\setlist[answers]{{label=\\arabic*.}}  % Change from \\alph*.) to \\arabic*.)

\\newcommand{{\\answer}}[2][]{{%
    \\ifthenelse{{\\equal{{#1}}{{correct}}}}
        {{\\item \\textbf{{#2}} \\textcolor{{red}}{{(Correct)}}}} % Uncomment for instructor version
        {{\\item #2}}%
}}

\\newcommand{{\\question}}[1]{{\\section*{{#1}}}}

\\title{{Module 2: Exam ({version})}}
\\date{{}}

\\begin{{document}}

\\maketitle

{exam_instructions}

\\newpage
{{\\large
{exam_questions}
\\end{{document}}
}}
"""

    # Save the exam file
    with open(os.path.join(folder_path, file_name), 'w') as file:
        file.write(exam_content)

def remove_correct_tags(file_path, new_file_path):
    """Remove all occurrences of '[correct]' from a LaTeX file."""
    with open(file_path, 'r') as file:
        content = file.read()

    # Remove the '[correct]' tag
    modified_content = content.replace('[correct]', '')

    # Save the modified content to a new file
    with open(new_file_path, 'w') as file:
        file.write(modified_content)

# Example usage
folder_path = './'  # Adjust this path to where your question files are stored
create_exam(folder_path, 'exam_A_solution.tex', "A")
create_exam(folder_path, 'exam_B_solution.tex', "B")
remove_correct_tags(os.path.join(folder_path, 'exam_A_solution.tex'), os.path.join(folder_path, 'exam_A.tex'))
remove_correct_tags(os.path.join(folder_path, 'exam_B_solution.tex'), os.path.join(folder_path, 'exam_B.tex'))