FROM python:3.8.2-buster
COPY *.py ./
COPY requirements.txt ./
RUN pip install -r requirements.txt
CMD streamlit run ui.py
