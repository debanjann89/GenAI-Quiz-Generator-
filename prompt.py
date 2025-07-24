def get_quiz_prompt(source_text, num_questions, difficulty):
    return f"""
    Act as an expert Quiz Generator AI.

    Your task is to create a quiz based *only* on the source text provided below the separator "---".

    Quiz Specifications:
    1. Total Questions: {num_questions}
    2. Question Mix: Generate a mix of Multiple Choice and True/False questions.
    3. Difficulty: {difficulty}
    4. Output Format: The entire response must be a single, valid JSON object.

    JSON Structure:
    The JSON object should contain a single key, "quiz", which holds an array of question objects. Each question object must have these keys:
    - `question_number` (number)
    - `question_type` (string: "Multiple Choice" or "True/False")
    - `question_text` (string)
    - `options` (array of strings for Multiple Choice, or an empty array for True/False)
    - `correct_answer` (string)
    - `explanation` (string: A brief explanation of why the answer is correct)

    Do not include any text, markdown formatting, or explanations outside of the final JSON object.

    ---
    {source_text}
    """
