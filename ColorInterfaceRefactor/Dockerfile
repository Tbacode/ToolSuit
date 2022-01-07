FROM python:3.9.6-slim

WORKDIR /src

COPY . /src/

RUN pip install -r /src/requirements.txt

CMD ["python3", "run_case_ddt.py"]