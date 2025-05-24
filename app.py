
import streamlit as st
import json
import random
import requests

st.set_page_config(page_title="AI 塔羅牌占卜小助手", layout="centered")
st.title("🔮 AI 塔羅牌占卜小助手")

# 讀取塔羅牌資料
@st.cache_data
def load_cards():
    with open("tarot_cards.json", "r", encoding="utf-8") as f:
        return json.load(f)
cards = load_cards()

# 用戶輸入
num_cards = st.selectbox("請選擇要抽幾張牌", [1, 2, 3], index=2)
user_question = st.text_input("請輸入你想占卜的問題（例如：近期感情運？）")

if st.button("開始占卜 🔮"):
    selected_cards = random.sample(cards, num_cards)
    st.subheader("你抽到的牌：")

    prompt = f"我問：「{user_question}」\n\n請根據以下塔羅牌進行占卜解釋：\n"
    for card in selected_cards:
        is_reversed = random.choice([True, False])
        pos = "逆位" if is_reversed else "正位"
        meaning = card["meaning_rev"] if is_reversed else card["meaning_up"]
        st.markdown(f"🃏 **{card['name']}**（{pos}）：{meaning}")
        prompt += f"- {card['name']}（{pos}）：{meaning}\n"

    prompt += "\n請用簡潔直白的方式告訴我這些牌對我提問的解答，以及你的總結與建議。"

    st.subheader("AI 占卜解釋：")
    with st.spinner("神秘塔羅正在解讀中..."):
        response = requests.post(
            "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct",
            headers={"Authorization": "Bearer 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"},  # 用戶需自行填寫 Token
            json={"inputs": prompt}
        )
        if response.status_code == 200:
            result = response.json()
            output = result[0]["generated_text"] if isinstance(result, list) else result.get("generated_text", "")
            st.write(output.replace(prompt, "").strip())
        else:
            st.error("呼叫 Hugging Face 模型失敗，請稍後再試。")
