import os
from pathlib import Path
import asyncio
import time
import yaml
import textwrap
from openai import OpenAI
from google.generativeai import GenerativeModel
from dotenv import load_dotenv
from gemini_config import gemini
from utils import clean_cypher_code

load_dotenv()

def load_prompts():
    with open("./prompts/prompts_cypher.yaml", 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def chunk_text(text, max_chunk_size=3000):
    """Chia văn bản thành các phần nhỏ hơn"""
    return textwrap.wrap(text, max_chunk_size, break_long_words=False, replace_whitespace=False)

class ModelConfig:
    def __init__(self, name, output_dir):
        self.name = name
        self.output_dir = output_dir
        self.conversation_messages = []
        os.makedirs(output_dir, exist_ok=True)

class DeepSeekModel(ModelConfig):
    def __init__(self):
        super().__init__("DeepSeek", "./cypher_deepseek_sguv1")
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY"),
        )

    def generate_cypher(self, user_message):
        self.conversation_messages.append({"role": "user", "content": user_message})
        response = self.client.chat.completions.create(
            messages=self.conversation_messages,
            model="deepseek/deepseek-chat-v3-0324:free",
            temperature=0.1,
        )
        generated_cypher = response.choices[0].message.content
        for keyword in ["```cypher", "```"]:
            generated_cypher = generated_cypher.replace(keyword, "")
        self.conversation_messages.append({
            "role": "assistant", 
            "content": generated_cypher
        })
        return generated_cypher.strip()

class GeminiModel(ModelConfig):
    def __init__(self):
        super().__init__("Gemini", "./cypher_gemini_sguv2")
        self.model = gemini.model

    def generate_cypher(self, user_message):
        # Chia user message thành các phần nhỏ hơn nếu cần
        message_chunks = chunk_text(user_message)
        
        # Xử lý từng phần và tích lũy kết quả
        full_response = []
        for chunk in message_chunks:
            try:
                # Format messages cho phần hiện tại
                current_messages = self.conversation_messages + [{"role": "user", "parts": [chunk]}]
                formatted_messages = "\n".join([
                    f"{msg['role']}: {msg.get('parts', msg.get('content', ''))[0]}" 
                    for msg in current_messages
                ])
                
                # Thêm delay giữa các chunks để tránh rate limit
                time.sleep(2)
                
                # Get response từ Gemini
                generated_chunk = clean_cypher_code(self.model.generate_content(formatted_messages))
                full_response.append(generated_chunk)
            
            except Exception as e:
                print(f"Warning: Error processing chunk: {str(e)}")
                continue

        # Kết hợp tất cả phản hồi
        final_response = "\n".join(full_response)
        
        # Cập nhật conversation history
        self.conversation_messages.append({
            "role": "user",
            "parts": [user_message]
        })
        self.conversation_messages.append({
            "role": "assistant",
            "parts": [final_response]
        })
        
        return final_response.strip()

class OpenAIModel(ModelConfig):
    def __init__(self):
        super().__init__("OpenAI", "./cypher_openai_sguv3")
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def generate_cypher(self, user_message):
        self.conversation_messages.append({"role": "user", "content": user_message})
        response = self.client.chat.completions.create(
            messages=self.conversation_messages,
            model="gpt-4o-mini",
            temperature=0.1,
        )
        generated_cypher = response.choices[0].message.content
        for keyword in ["```cypher", "```"]:
            generated_cypher = generated_cypher.replace(keyword, "")
        self.conversation_messages.append({
            "role": "assistant",
            "content": generated_cypher
        })
        return generated_cypher.strip()

async def process_file_with_model(model, filename, data_text, ontology, prompts):
    try:
        print(f"\n[+] Đang xử lý file {filename} với {model.name}")

        # Nếu conversation_messages trống, thêm system prompt
        if not model.conversation_messages:
            if isinstance(model, GeminiModel):
                model.conversation_messages.append({
                    "role": "system",
                    "parts": [prompts["system_prompt"]]
                })
            else:
                model.conversation_messages.append({
                    "role": "system",
                    "content": prompts["system_prompt"]
                })

        # Format user message
        user_message = prompts["user_prompt_template"].format(
            filename=filename,
            data_text=data_text,
            ontology=ontology
        )
        
        # Generate cypher và giữ lại context
        generated_cypher = model.generate_cypher(user_message)
        
        # Lưu kết quả
        cypher_file = os.path.join(model.output_dir, f"{filename}.cypher")
        with open(cypher_file, "w", encoding="utf-8") as f:
            f.write(generated_cypher)
        print(f"✅ Đã lưu Cypher vào file: {cypher_file}")
        
        return cypher_file
    except Exception as e:
        print(f"❌ Lỗi khi xử lý file {filename} với {model.name}: {str(e)}")
        return None

async def main():
    # Load prompts
    prompts = load_prompts()
    
    # Khởi tạo models
    models = [ GeminiModel()]
    
    # Đọc ontology
    ontology_file = "./ontology/skeleton_ontology.ttl"
    print("Bắt đầu đọc ontology từ:", ontology_file)
    with open(ontology_file, "r", encoding="utf-8") as f:
        ontology = f.read()
    print("Đã đọc ontology, độ dài:", len(ontology), "ký tự")

    # Lấy danh sách file từ dataset
    dataset_dir = "./dataset"
    txt_files = [f for f in os.listdir(dataset_dir) if f.endswith(".txt") and "PHẦN 1" in f]
    txt_files.sort()

    # Xử lý từng model riêng biệt để duy trì conversation history
    for model in models:
        print(f"\n=== Bắt đầu xử lý với model {model.name} ===")
        for filename in txt_files:
            with open(os.path.join(dataset_dir, filename), "r", encoding="utf-8") as f:
                data_text = f.read()
            
            await process_file_with_model(model, filename, data_text, ontology, prompts)

    print("\nĐã xử lý xong tất cả các model và file!")

if __name__ == "__main__":
    asyncio.run(main())
