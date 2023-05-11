requirements:
	pip-compile requirements.in --resolver=backtracking -o requirements.txt --verbose

install:
	pip install -r requirements.txt

run:
	streamlit run src/app.py
