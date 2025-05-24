
import streamlit as st
import streamlit.components.v1 as components
import requests
import json

st.set_page_config(page_title="塔羅牌 AI 占卜", layout="centered")

st.title("🔮 AI 塔羅占卜小助手")

st.markdown("請在下方輸入你想問的問題，例如：**我最近的感情如何？**")

user_question = st.text_input("📝 請輸入你的提問：")

# 讀取嵌入的 HTML 卡牌頁面
st.markdown("### 🃏 請在下方抽牌")
with open("tarot_cards.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# 嵌入 HTML 占卜卡片
components.html(html_content, height=800, scrolling=True)

# 模擬使用者抽到的牌（未連接 JS 傳值，示範用）
drawn_cards = ["The Fool（正位）：新開始，自由，冒險", "The Magician（逆位）：欺騙，浪費潛能"]

if st.button("✨ 開始解牌"):
    if not user_question:
        st.warning("請先輸入你的提問內容。")
    else:
        prompt = f"我問：「{user_question}」\n\n我抽到了以下塔羅牌：\n"
        for card in drawn_cards:
            prompt += f"- {card}\n"
        prompt += "\n請你用專業的塔羅解牌師身份，告訴我這些牌的含義和對我提問的建議，請以親切口吻給出具體建議。"

        st.markdown("#### 🧠 解牌結果：")
        with st.spinner("AI 解讀中..."):
            try:
                response = requests.post(
                    "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct",
                    headers={"Authorization": "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"},  # ⚠️ 請填入你的 Hugging Face Token
                    json={"inputs": prompt}
                )
                if response.status_code == 200:
                    result = response.json()
                    output = result[0]["generated_text"] if isinstance(result, list) else result.get("generated_text", "")
                    st.success(output.replace(prompt, "").strip())
                else:
                    st.error("模型呼叫失敗，請檢查 Token 或稍後再試。")
            except Exception as e:
                st.error(f"發生錯誤：{e}")
