import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# 페이지 설정
st.set_page_config(page_title="사진 기반 음악 추천 앱", page_icon="🎵", layout="centered")

st.title("📸 사진 기반 음악 추천 앱 🎵")
st.write("사진의 분위기에 딱 맞는 음악 3곡을 추천해 드립니다!")

# 사이드바에서 API 키 입력받기 (보안 및 편의성)
with st.sidebar:
    st.header("설정")
    api_key = st.text_input("Google Gemini API 키를 입력하세요:", type="password")
    st.markdown("[API 키 발급받기 (무료)](https://aistudio.google.com/)")
    st.markdown("---")
    st.write("이 앱은 Google의 Gemini AI 모델을 사용하여 이미지를 분석하고 어울리는 음악을 추천합니다.")

# 메인 화면: 이미지 업로드
uploaded_file = st.file_uploader("이미지를 업로드하세요 (JPG, JPEG, PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 이미지 표시
    image = Image.open(uploaded_file)
    st.image(image, caption="업로드된 사진", use_column_width=True)
    
    # 추천 버튼
    if st.button("이 사진에 어울리는 음악 추천받기"):
        if not api_key:
            st.error("왼쪽 사이드바에서 Gemini API 키를 먼저 입력해주세요!")
        else:
            with st.spinner("AI가 사진을 분석하고 음악을 고르는 중입니다... 🤔"):
                try:
                    # Gemini API 설정
                    genai.configure(api_key=api_key)
                    # 사용할 모델 선택 (이미지 분석이 가능한 gemini-1.5-flash 모델 권장)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    # AI에게 내릴 프롬프트(명령어) 작성
                    prompt = """
                    이 사진의 전반적인 분위기, 상황, 색감, 감정을 분석해주세요.
                    그리고 이 사진과 가장 잘 어울리는 음악 3곡을 추천해주세요. 
                    각 음악에 대해 '곡 제목 - 아티스트' 형식으로 적고, 왜 이 사진과 어울리는지 1~2문장으로 이유를 설명해주세요.
                    답변은 반드시 한국어로 작성해주세요.
                    """
                    
                    # API 호출
                    response = model.generate_content([prompt, image])
                    
                    st.success("추천이 완료되었습니다!")
                    st.markdown("### 🎶 추천 음악 리스트")
                    st.write(response.text)
                    
                except Exception as e:
                    st.error(f"오류가 발생했습니다: {e}")
                    st.info("API 키가 정확한지, 또는 네트워크 연결이 원활한지 확인해주세요.")
