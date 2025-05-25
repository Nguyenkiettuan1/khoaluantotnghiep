import os
from openai import OpenAI
from pathlib import Path
import dotenv
# Load environment variables
dotenv.load_dotenv()
# Initialize OpenAI client
client = OpenAI(
    api_key="YOUR_API_KEY_HERE"
)

def read_dataset_files(folder_path):
    """Read all txt files in dataset folder"""
    content = ""
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                content += file.read() + "\n\n"
    return content

def generate_questions(content, num_questions=40):
    """Generate questions using OpenAI API"""
    prompt = f"""
    Dựa vào nội dung sau đây, hãy tạo {num_questions} câu hỏi năng lực bằng tiếng Việt.
    Mỗi câu hỏi nên kiểm tra khả năng hiểu và phân tích thông tin của người đọc.
    
    Format câu hỏi như sau:
    1. [Câu hỏi]
    2. [Câu hỏi]
    ...

    Nội dung: {content}
    
    Yêu cầu:
    - Các câu hỏi được đánh số từ 1 đến {num_questions}
    - Câu hỏi phải bằng tiếng Việt
    - Câu hỏi cần rõ ràng và súc tích
    - Tập trung vào kiểm tra khả năng hiểu và phân tích
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Bạn là chuyên gia tạo câu hỏi năng lực từ nội dung cho trước."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    
    return response.choices[0].message.content

def save_questions(questions, output_file):
    """Save questions to text file"""
    os.makedirs("CQs", exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(questions)

def main(num_questions=40):
    # Read data from dataset
    content = read_dataset_files("./dataset")
    
    # Generate questions
    questions = generate_questions(content, num_questions)
    
    # Save results
    output_file = os.path.join("CQs", "competency_questions.txt")
    save_questions(questions, output_file)
    print(f"Đã tạo {num_questions} câu hỏi và lưu vào {output_file}")

if __name__ == "__main__":
    main()