import os
import time
from openai import OpenAI
import base64
from dotenv import load_dotenv
import mimetypes

load_dotenv()

def encode_image(image_path):
    mime_type = mimetypes.guess_type(image_path)[0] or 'image/png'
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8'), mime_type

def analyze_images(image_paths, existing_ttl=None):
    if not os.getenv('OPENAI_API_KEY'):
        raise ValueError("OPENAI_API_KEY not found in environment variables")
        
    client = OpenAI()
    
    initial_prompt = "Phân tích nội dung trong tất cả các ảnh sau và tạo ontology dưới dạng TTL."
    if existing_ttl:
        initial_prompt += " Sử dụng và mở rộng ontology đã có sau đây làm ngữ cảnh:\n" + existing_ttl
    
    content = [
        {
            "type": "text",
            "text": initial_prompt
        }
    ]
    
    MAX_RETRY = 3
    RETRY_DELAY = 5
    
    for image_path in image_paths:
        if os.path.getsize(image_path) > 20 * 1024 * 1024:
            raise ValueError(f"Image size too large: {image_path}")
        
        base64_image, mime_type = encode_image(image_path)
        content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:{mime_type};base64,{base64_image}",
                "detail": "low"
            }
        })
    
    for attempt in range(MAX_RETRY):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "Bạn là một chuyên gia trong việc phân tích hình ảnh và tạo ontology theo định dạng TTL (Turtle). Hãy phân tích nội dung trong tất cả các hình ảnh được cung cấp và chỉ trả về TTL hoàn chỉnh, không kèm theo ghi chú hay comment. Hãy kết hợp thông tin từ tất cả các ảnh để tạo một ontology nhất quán."
                    },
                    {
                        "role": "user",
                        "content": content
                    }
                ],
                max_tokens=8192
            )
            time.sleep(2)
            return response.choices[0].message.content
            
        except Exception as e:
            if attempt == MAX_RETRY - 1:
                raise
            print(f"Attempt {attempt + 1} failed: {str(e)}. Retrying in {RETRY_DELAY} seconds...")
            time.sleep(RETRY_DELAY)

def process_images(image_dir="images"):
    if not os.path.exists(image_dir):
        raise FileNotFoundError(f"Directory not found: {image_dir}")
    
    images = [f for f in os.listdir(image_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    if not images:
        raise ValueError(f"No valid image files found in {image_dir}")
    
    try:
        images.sort(key=lambda x: int(x.split('_')[1].split('.')[0]))
    except (IndexError, ValueError):
        images.sort()
    
    os.makedirs('ontology', exist_ok=True)
    output_path = os.path.join('ontology', 'ontology_generated.ttl')
    
    image_paths = [os.path.join(image_dir, image) for image in images]
    total_images = len(images)
    
    # Process first half of images
    mid_point = len(image_paths) // 2
    first_half = image_paths[:mid_point]
    second_half = image_paths[mid_point:]
    
    print(f"\nXử lý {len(first_half)} hình ảnh đầu tiên...")
    try:
        # Process first half
        first_ttl = analyze_images(first_half)
        if not first_ttl:
            raise ValueError("No content generated from first half analysis")
            
        print(f"\nXử lý {len(second_half)} hình ảnh còn lại...")
        # Process second half with context from first half
        final_ttl = analyze_images(second_half, existing_ttl=first_ttl)
        if not final_ttl:
            raise ValueError("No content generated from second half analysis")
        
        # Remove any ``` markers that might be in the response
        final_ttl = final_ttl.replace('```', '').strip()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(final_ttl)
        
        print(f"\n✅ Đã xử lý thành công {total_images} hình ảnh")
        print(f"✅ Đã lưu kết quả vào {output_path}")
        
    except Exception as e:
        print(f"❌ Lỗi khi xử lý hình ảnh: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        process_images()
    except Exception as e:
        print(f"❌ Lỗi: {str(e)}")