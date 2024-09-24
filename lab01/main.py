import requests
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

rapidapi_key = os.getenv('RAPID_API_TOKEN')
imgbbapi_key = os.getenv('IMGBB_API_TOKEN')

headers_api1 = {
    "x-rapidapi-key": rapidapi_key,
    "x-rapidapi-host": "faceswap-image-transformation-api.p.rapidapi.com",
    "Content-Type": "application/json"
}
headers_api2 = {
    "x-rapidapi-key": rapidapi_key,
    "x-rapidapi-host": "face-swap-video-image-multiface.p.rapidapi.com",
    "Content-Type": "application/json"
}

def upload_image(image):
    url = "https://api.imgbb.com/1/upload"
    payload = {"key": imgbbapi_key}
    files = {'image': image}

    response = requests.post(url, data=payload, files=files)
    if response.status_code == 200:
        return response.json()['data']['url']
    else:
        st.error(f"Ошибка загрузки изображения: {response.text}")
        return None

def face_swap_api_1(source_url, target_url):
    url = "https://faceswap-image-transformation-api.p.rapidapi.com/faceswap"
    payload = {
        "SourceImageUrl": source_url,
        "TargetImageUrl": target_url
    }

    response = requests.post(url, json=payload, headers=headers_api1)
    if response.status_code == 200:
        result = response.json()
        if result.get("Success"):
            return result.get("ResultImageUrl")
        else:
            st.error(f"Ошибка API 1: {result.get('Message')}")
            return None
    else:
        st.error(f"Ошибка API 1: {response.text}")
        return None

def face_swap_api_2(source_url, target_url):
    url = "https://face-swap-video-image-multiface.p.rapidapi.com/runsync"
    payload = {
        "input": {
            "enhanceState": True,
            "mode": "swap-face",
            "url": source_url,
            "targetUrl": target_url
        }
    }

    response = requests.post(url, json=payload, headers=headers_api2)
    if response.status_code == 200:
        return response.json().get("output").get("uploadedUrl")
    else:
        st.error(f"Ошибка API 2: {response.text}")
        return None

st.title("FaceSwap API Tester")

col1, col2 = st.columns(2)

with col1:
    source_file = st.file_uploader("Загрузите Source изображение", type=["jpg", "png", "jpeg"], key="source")
with col2:
    target_file = st.file_uploader("Загрузите Target изображение", type=["jpg", "png", "jpeg"], key="target")

if source_file and target_file:
    col1, col2 = st.columns(2)
    with col1:
        st.image(source_file, caption="Source Image", use_column_width=True)
    with col2:
        st.image(target_file, caption="Target Image", use_column_width=True)

    if st.button("Отправить запрос"):
        with st.spinner("Загрузка изображений..."):
            source_url = upload_image(source_file)
            target_url = upload_image(target_file)

        if source_url and target_url:
            st.success(f"Изображения загружены:\n Source URL: {source_url}, Target URL: {target_url}")
            
            result_col1, result_col2 = st.columns(2)
            
            with st.spinner("Выполняем FaceSwap для API 1..."):
                result_url_api_1 = face_swap_api_1(source_url, target_url)
            
            with st.spinner("Выполняем FaceSwap для API 2..."):
                result_url_api_2 = face_swap_api_2(source_url, target_url)
            
            if result_url_api_1:
                with result_col1:
                    st.image(result_url_api_1, caption="Результат FaceSwap API 1", use_column_width=True)
            if result_url_api_2:
                with result_col2:
                    st.image(result_url_api_2, caption="Результат FaceSwap API 2", use_column_width=True)