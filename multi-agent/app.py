# import streamlit as st
# import os
# import time
# import json
# from typing import List, Dict, Optional
# from dataclasses import dataclass
# from collections import defaultdict, deque
# from datetime import datetime

# import pandas as pd
# from dotenv import load_dotenv
# from neo4jconnector import Neo4jConnection, Neo4jVectorSearchError

# # Load environment variables
# load_dotenv()

# # Configure page
# st.set_page_config("SGU Vector Chatbot", page_icon="🎓", layout="centered")


# @dataclass
# class SearchResult:
#     name: str
#     node_type: str
#     similarity: float
#     description: Optional[str] = None

# # 1) Cache Neo4j clients -------------------------------------------------------
# @st.cache_resource(show_spinner=False)
# def init_neo4j_clients() -> Dict[str, Dict]:
#     cfg = {
#         "uri": os.getenv("NEO4J_URI", "bolt://localhost:7687"),
#         "user": os.getenv("NEO4J_USER", "neo4j"),
#         "password": os.getenv("NEO4J_PASSWORD"),
#     }
#     return {
#         "deepseek": {
#             "conn": Neo4jConnection(**cfg, dbname="deepseek"),
#             "label_file": "labels/neo4j_labels_deepseek.txt",
#         },
#         "gemini": {
#             "conn": Neo4jConnection(**cfg, dbname="gemini"),
#             "label_file": "labels/neo4j_labels_gemini.txt",
#         },
#         "openai": {
#             "conn": Neo4jConnection(**cfg, dbname="openai"),
#             "label_file": "labels/neo4j_labels_openai.txt",
#         },
#     }
# def extract_labels_from_file(file_path: str) -> List[str]:
#     """Extract labels from a file and return as a list"""
#     try:
#         with open(file_path, "r", encoding="utf-8") as f:
#             labels = [label.strip() for label in f.read().splitlines() if label.strip()]
#         return labels
#     except Exception as e:
#         st.error(f"Error reading labels from file: {str(e)}")
#         return []
# def perform_search(neo4j: Neo4jConnection, query: str, node_types: List[str],
#                    min_similarity: float = 0.5, limit: int = 15) -> List[Dict]:
#     all_results = []
#     try:
#         for node_type in node_types:
#             results = neo4j.similarity_search(
#                 query_text=query,
#                 node_label=node_type,
#                 limit=limit,
#                 min_similarity=min_similarity
#             )
#             for r in results:
#                 r['node_type'] = node_type
#             all_results.extend(results)
#     except Exception as e:
#         st.error(f"Error performing search: {str(e)}")
#     return sorted(all_results, key=lambda x: x['similarity'], reverse=True)
# def get_answer_from_search_results(neo4j: Neo4jConnection, userQuery: str, labels: List[str]) -> Optional[str]:
#     """Get answer from search results using OpenAI API"""
#     try:
#         # Perform search
#         search_results = perform_search(neo4j, userQuery, labels, min_similarity=0.6, limit=30)
        
#         if search_results:
#             # Generate answer
#             answer = neo4j.generate_answer(neo4j, userQuery, search_results)
#             return answer
#         else:
#             st.info("Không tìm thấy kết quả phù hợp với tiêu chí của bạn")
#             return None
#     except Exception as e:
#         st.error(f"Error getting answer: {str(e)}")
#         return None
# # 2) Cache Graph & Direct Map --------------------------------------------------
# @st.cache_resource(show_spinner=False)
# def get_relation_graph(client_name: str) -> Dict[str, List[tuple]]:
#     path_map = {
#         "deepseek": "ontology_relations_deepseek.csv",
#         "gemini":   "ontology_relations_gemini.csv",
#         "openai":   "ontology_relations_openai.csv"
#     }
#     path = path_map.get(client_name)
#     if not path or not os.path.exists(path):
#         return {}
#     df = pd.read_csv(path)
#     graph = defaultdict(list)
#     for rel in df.to_dict(orient="records"):
#         subj = rel["subject"].split("#")[-1].replace("_", " ").strip()
#         obj  = rel["object"].split("#")[-1].replace("_", " ").strip()
#         pred = rel["predicate"].split("#")[-1].strip()
#         graph[subj].append((obj, pred))
#     return graph

# @st.cache_resource(show_spinner=False)
# def load_direct_map(client_name: str) -> Dict[str, List[Dict]]:
#     path = f"./precomputed_relations/{client_name}_direct_map.json"
#     if not os.path.exists(path):
#         return {}
#     with open(path, "r", encoding="utf-8") as fp:
#         return json.load(fp)

# # 3) Các hàm hỗ trợ (vector search, load labels, load ontology triples) ----------


# def load_labels(path: str) -> List[str]:
#     with open(path, encoding="utf-8") as f:
#         return [l.strip() for l in f if l.strip()]

# def find_indirect_paths(graph: Dict, start: str, targets: set, max_depth: int = 3):
#     """Nếu vẫn cần hàm này cho BFS riêng lẻ."""
#     paths = []
#     queue = deque([(start, [], {start})])
#     while queue:
#         node, path, visited = queue.popleft()
#         if len(path) > max_depth:
#             continue
#         for neighbor, rel in graph.get(node, []):
#             if neighbor in visited:
#                 continue
#             new_path = path + [(node, rel, neighbor)]
#             if neighbor in targets:
#                 paths.append(new_path)
#             else:
#                 queue.append((neighbor, new_path, visited | {neighbor}))
#     return paths

# # def format_time_info(start_time: float, end_time: float) -> str:
# #     """Format thời gian thực hiện với màu sắc"""
# #     total_time = end_time - start_time
# #     start_str = datetime.fromtimestamp(start_time).strftime("%H:%M:%S")
    
# #     if total_time < 1:
# #         time_str = f"{total_time*1000:.0f}ms"
# #         color = "green"
# #     elif total_time < 3:
# #         time_str = f"{total_time:.2f}s"
# #         color = "orange"
# #     else:
# #         time_str = f"{total_time:.2f}s"
# #         color = "red"
    
# #     return f"""
# #     <div style="background-color: #f0f2f6; padding: 8px; border-radius: 5px; margin: 5px 0;">
# #         <small>
# #             ⏰ <strong>Thời gian:</strong> {start_str} | 
# #             ⚡ <strong>Thời gian xử lý:</strong> 
# #             <span style="color: {color}; font-weight: bold;">{time_str}</span>
# #         </small>
# #     </div>
# #     """

# # 4) Hàm xử lý query từng lần user submit -------------------------------------
# def handle_query(
#     prompt: str,
#     neo4j: Neo4jConnection,
#     labels: List[str],
#     graph: Dict[str, List[tuple]],
#     direct_map: Dict[str, List[Dict]],
#     min_sim: float = 0.5,
#     limit: int = 15
# ):
#     # Bắt đầu đo thời gian
#     start_time = time.time()
    
#     # 4.1) Lưu lịch sử và hiển thị user message
#     st.session_state.chat_history.append({
#         "role": "user", 
#         "content": prompt,
#         "timestamp": start_time
#     })
#     with st.chat_message("user"):
#         st.markdown(prompt)
#         # # Hiển thị thời gian đặt câu hỏi
#         # st.markdown(f"<small>📅 {datetime.fromtimestamp(start_time).strftime('%H:%M:%S, %d/%m/%Y')}</small>", 
#         #            unsafe_allow_html=True)

#     # 4.2) Vector search
#     search_start = time.time()
#     with st.spinner("🔎 Đang tìm kiếm..."):
#         results = perform_search(neo4j, prompt, labels, min_similarity=min_sim, limit=limit)
#         st.session_state.last_results = results
#     search_end = time.time()

#     if not results:
#         end_time = time.time()
#         response_text = "Không tìm thấy kết quả phù hợp."
#         with st.chat_message("assistant"):
#             st.markdown(response_text)
#             # Hiển thị thông tin thời gian
#             # st.markdown(format_time_info(start_time, end_time), unsafe_allow_html=True)
        
#         st.session_state.chat_history.append({
#             "role": "assistant", 
#             "content": response_text,
#             "timestamp": end_time,
#             "processing_time": end_time - start_time,
#             "search_time": search_end - search_start
#         })
#         return

#     # 4.3) Chuẩn bị related_relations
#     relation_start = time.time()
#     names = set(r["name"] for r in results)
#     related_relations = []

#     # 4.3a) Direct lookup từ direct_map (precomputed)
#     for name in names:
#         for pair in direct_map.get(name, []):
#             subj = name
#             pred = pair["predicate"]
#             obj  = pair["neighbor"]
#             related_relations.append(f"{subj} → {pred} → {obj}")
#     relation_end = time.time()

#     # 4.4) Generate answer với GPT/Gemini
#     with st.chat_message("assistant"):
#         with st.spinner("🤖 Trợ lý đang trả lời..."):
#             generate_start = time.time()
#             chat_history_copy = st.session_state.chat_history.copy()
#             response_text = neo4j.generate_answer(
#                 prompt,
#                 results
#                 # ontology_relations=related_relations,
#                 # chat_history=chat_history_copy
#             )
#             generate_end = time.time()
#             end_time = time.time()
            
#             st.markdown(response_text)
            
#             # Hiển thị thông tin thời gian chi tiết
#             # st.markdown(format_time_info(start_time, end_time), unsafe_allow_html=True)
            
#             # Hiển thị breakdown thời gian trong expander
#             with st.expander("⏱️ Chi tiết thời gian xử lý"):
#                 st.markdown(f"""
#                 - **🔍 Tìm kiếm vector:** {(search_end - search_start)*1000:.0f}ms
#                 - **🔗 Xử lý quan hệ:** {(relation_end - relation_start)*1000:.0f}ms  
#                 - **🤖 Sinh câu trả lời:** {(generate_end - generate_start)*1000:.0f}ms
#                 - **📊 Tổng thời gian:** {(end_time - start_time)*1000:.0f}ms
#                 """)
    
#     # Lưu thông tin chi tiết vào lịch sử
#     st.session_state.chat_history.append({
#         "role": "assistant", 
#         "content": response_text,
#         "timestamp": end_time,
#         "processing_time": end_time - start_time,
#         "search_time": search_end - search_start,
#         "relation_time": relation_end - relation_start,
#         "generate_time": generate_end - generate_start
#     })

#     # 4.5) Hiển thị chi tiết kết quả
#     with st.expander("🔎 Chi tiết kết quả"):
#         for r in results:
#             st.markdown(
#                 f"**{r['name']}** ({r['node_type']}) — Similarity: `{r['similarity']:.4f}`"
#             )
#             if desc := r.get("description"):
#                 st.write(desc)
#             st.divider()

# # 5) Hàm main ---------------------------------------------------------------
# def main():
#     st.title("🎓 Trợ lý Chatbot SGU")

#     # Khởi tạo state lần đầu
#     if "chat_history" not in st.session_state:
#         st.session_state.chat_history = []
#     if "last_results" not in st.session_state:
#         st.session_state.last_results = []

#     # 5.1) Load/cached resources (chỉ chạy 1 lần mỗi khi client_name thay đổi)
#     clients = init_neo4j_clients()
#     client_name = st.sidebar.selectbox("🔧 Chọn mô hình", list(clients))
#     neo4j = clients[client_name]["conn"]
#     labels = load_labels(clients[client_name]["label_file"])
#     graph = get_relation_graph(client_name)
#     direct_map = load_direct_map(client_name)

#     # 5.2) Sidebar thống kê
#     if st.session_state.chat_history:
#         with st.sidebar:
#             st.markdown("### 📊 Thống kê phiên làm việc")
#             assistant_messages = [msg for msg in st.session_state.chat_history if msg["role"] == "assistant"]
#             if assistant_messages:
#                 times = [msg.get("processing_time", 0) for msg in assistant_messages if msg.get("processing_time")]
#                 if times:
#                     avg_time = sum(times) / len(times)
#                     max_time = max(times)
#                     min_time = min(times)
#                     st.markdown(f"""
#                     - **Số câu hỏi:** {len(times)}
#                     - **Thời gian TB:** {avg_time:.2f}s
#                     - **Nhanh nhất:** {min_time:.2f}s  
#                     - **Chậm nhất:** {max_time:.2f}s
#                     """)

#     # 5.3) Hiển thị lịch sử chat
#     for msg in st.session_state.chat_history:
#         with st.chat_message(msg["role"]):
#             st.markdown(msg["content"])
            
#             # Hiển thị thời gian cho tin nhắn cũ
#             if "timestamp" in msg:
#                 timestamp_str = datetime.fromtimestamp(msg["timestamp"]).strftime('%H:%M:%S')
#                 if msg["role"] == "assistant" and "processing_time" in msg:
#                     processing_time = msg["processing_time"]
#                     if processing_time < 1:
#                         time_str = f"{processing_time*1000:.0f}ms"
#                     else:
#                         time_str = f"{processing_time:.2f}s"
#                     st.markdown(f"<small>⏰ {timestamp_str} | ⚡ {time_str}</small>", 
#                                unsafe_allow_html=True)
#                 else:
#                     st.markdown(f"<small>📅 {timestamp_str}</small>", 
#                                unsafe_allow_html=True)

#     # 5.4) Nhận input user
#     prompt = st.chat_input("Nhập câu hỏi...")

#     if prompt:
#         handle_query(
#             prompt=prompt,
#             neo4j=neo4j,
#             labels=labels,
#             graph=graph,
#             direct_map=direct_map,
#         )

#     # 5.5) Nút xóa lịch sử
#     if st.sidebar.button("🧹 Xóa hội thoại"):
#         st.session_state.chat_history = []
#         st.session_state.last_results = []
#         st.rerun()

# if __name__ == "__main__":
#     main()



import streamlit as st
import os
import time
import json
import threading
from typing import List, Dict, Optional
from dataclasses import dataclass
from collections import defaultdict, deque
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

import pandas as pd
from dotenv import load_dotenv
from neo4jconnector import Neo4jConnection, Neo4jVectorSearchError

# Load environment variables
load_dotenv()

# Configure page
st.set_page_config("SGU Multi-Model Chatbot", page_icon="🎓", layout="wide")

@dataclass
class ModelResult:
    model_name: str
    response: str
    search_results: List[Dict]
    error: Optional[str] = None

@dataclass
class SearchResult:
    name: str
    node_type: str
    similarity: float
    description: Optional[str] = None

# 1) Cache Neo4j clients -------------------------------------------------------
@st.cache_resource(show_spinner=False)
def init_neo4j_clients() -> Dict[str, Dict]:
    cfg = {
        "uri": os.getenv("NEO4J_URI", "bolt://localhost:7687"),
        "user": os.getenv("NEO4J_USER", "neo4j"),
        "password": os.getenv("NEO4J_PASSWORD"),
    }
    return {
        "deepseek": {
            "conn": Neo4jConnection(**cfg, dbname="deepseek"),
            "label_file": "labels/neo4j_labels_deepseek.txt",
        },
        "gemini": {
            "conn": Neo4jConnection(**cfg, dbname="gemini"),
            "label_file": "labels/neo4j_labels_gemini.txt",
        },
        "openai": {
            "conn": Neo4jConnection(**cfg, dbname="openai"),
            "label_file": "labels/neo4j_labels_openai.txt",
        },
    }

def load_labels(path: str) -> List[str]:
    try:
        with open(path, encoding="utf-8") as f:
            return [l.strip() for l in f if l.strip()]
    except:
        return []

def perform_search(neo4j: Neo4jConnection, query: str, node_types: List[str],
                   min_similarity: float = 0.5, limit: int = 15) -> List[Dict]:
    all_results = []
    try:
        for node_type in node_types:
            results = neo4j.similarity_search(
                query_text=query,
                node_label=node_type,
                limit=limit,
                min_similarity=min_similarity
            )
            for r in results:
                r['node_type'] = node_type
            all_results.extend(results)
    except Exception as e:
        st.error(f"Error performing search: {str(e)}")
    return sorted(all_results, key=lambda x: x['similarity'], reverse=True)[:limit]

# 2) Xử lý query cho từng model riêng lẻ
def process_single_model(model_name: str, prompt: str, clients: Dict) -> ModelResult:
    """Xử lý query cho một model duy nhất"""
    try:
        # Get model resources
        neo4j = clients[model_name]["conn"]
        labels = load_labels(clients[model_name]["label_file"])
        
        # Search
        results = perform_search(neo4j, prompt, labels, min_similarity=0.8, limit=15)
        
        if not results:
            return ModelResult(
                model_name=model_name,
                response="Không tìm thấy kết quả phù hợp.",
                search_results=[]
            )
        
        # Generate answer
        response_text = neo4j.generate_answer(prompt, results)
        
        return ModelResult(
            model_name=model_name,
            response=response_text,
            search_results=results
        )
        
    except Exception as e:
        return ModelResult(
            model_name=model_name,
            response="",
            search_results=[],
            error=str(e)
        )

# 3) Xử lý đồng thời cho tất cả models
def process_all_models(prompt: str, clients: Dict) -> Dict[str, ModelResult]:
    """Chạy đồng thời query trên tất cả 3 models"""
    results = {}
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        # Submit tasks cho tất cả models
        futures = {
            executor.submit(process_single_model, model_name, prompt, clients): model_name
            for model_name in clients.keys()
        }
        
        # Collect results
        for future in as_completed(futures):
            model_result = future.result()
            results[model_result.model_name] = model_result
    
    return results

# 4) Display functions
def display_model_result(model_name: str, result: ModelResult, col):
    """Hiển thị kết quả của một model trong column"""
    
    # Model header với icon
    model_icons = {
        "deepseek": "🔍",
        "gemini": "✨", 
        "openai": "🤖"
    }
    
    with col:
        st.markdown(f"### {model_icons.get(model_name, '🔧')} {model_name.upper()}")
        
        if result.error:
            st.error(f"❌ Lỗi: {result.error}")
            return
        
        # Display response
        with st.container():
            st.markdown("#### 💬 Câu trả lời:")
            st.markdown(result.response)
        
        # Search results details
        if result.search_results:
            with st.expander(f"🔎 Chi tiết kết quả ({len(result.search_results)} items)"):
                for i, r in enumerate(result.search_results[:5]):  # Show top 5
                    st.markdown(
                        f"**{r['name']}** ({r['node_type']}) — Similarity: `{r['similarity']:.4f}`"
                    )
                    if desc := r.get("description"):
                        st.write(f"📝 {desc[:200]}...")
                    if i < len(result.search_results) - 1:
                        st.divider()

# 5) Main function
def main():
    st.title("🎓 SGU Multi-Model Chatbot")
    st.markdown("### Hỏi cùng lúc 3 AI models: DeepSeek, Gemini & OpenAI")
    
    # Initialize session state
    if "multi_chat_history" not in st.session_state:
        st.session_state.multi_chat_history = []
    
    # Load clients
    clients = init_neo4j_clients()
    
    # Sidebar - Statistics
    with st.sidebar:
        st.markdown("### 📊 Thống kê")
        
        if st.session_state.multi_chat_history:
            total_queries = len(st.session_state.multi_chat_history)
            st.markdown(f"**Tổng số câu hỏi:** {total_queries}")
        
        st.divider()
        
        # Model status
        st.markdown("### 🔧 Trạng thái Models")
        for model_name in clients.keys():
            try:
                # Quick health check
                neo4j = clients[model_name]["conn"]
                st.markdown(f"✅ {model_name.upper()}")
            except:
                st.markdown(f"❌ {model_name.upper()}")
        
        st.divider()
        
        # Clear history button
        if st.button("🧹 Xóa lịch sử", use_container_width=True):
            st.session_state.multi_chat_history = []
            st.rerun()
    
    # Display chat history
    for i, chat in enumerate(st.session_state.multi_chat_history):
        with st.container():
            # User message
            st.markdown(f"### 👤 Câu hỏi {i+1}")
            st.markdown(f"**{chat['prompt']}**")
            st.markdown(f"<small>📅 {chat['timestamp']}</small>", unsafe_allow_html=True)
            st.markdown(f"<small>📅 {chat['endtime']}</small>", unsafe_allow_html=True)
            # Model responses in 3 columns
            if "results" in chat:
                st.markdown("#### 💬 Câu trả lời từ các Models")
                col1, col2, col3 = st.columns(3)
                
                cols = [col1, col2, col3]
                model_names = ["deepseek", "gemini", "openai"]
                
                for j, model_name in enumerate(model_names):
                    if model_name in chat["results"]:
                        display_model_result(model_name, chat["results"][model_name], cols[j])
            
            st.divider()
  
    
    # Input area
    st.markdown("### 💭 Đặt câu hỏi mới")
    prompt = st.text_area(
        "Nhập câu hỏi của bạn:",
        placeholder="Ví dụ: Khoa Công nghệ thông tin có những chuyên ngành gì?",
        height=100
    )
    
    col1, col2 = st.columns([1, 4])
    
    with col1:
        submit_button = st.button("🚀 Hỏi tất cả Models", type="primary", use_container_width=True)
    
    with col2:
        if submit_button and prompt.strip():
            st.markdown("*Đang xử lý trên 3 models...*")
    
    # Process query when submitted
    if submit_button and prompt.strip():
        with st.spinner("🔄 Đang xử lý trên tất cả models..."):
            # Add user message to history first
            timestamp = datetime.now().strftime('%H:%M:%S, %d/%m/%Y')
            starttime = time.time()
            # Process all models simultaneously
            results = process_all_models(prompt.strip(), clients)
            endtime = time.time()
            # Add to chat history
            st.session_state.multi_chat_history.append({
                "prompt": prompt.strip(),
                "timestamp": timestamp,
                "results": results,
                "endtime": endtime - starttime
            })
            
            # Show success message
            st.success(f"✅ Hoàn thành!")
            st.rerun()

if __name__ == "__main__":
    main()