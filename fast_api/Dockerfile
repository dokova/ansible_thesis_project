FROM python:3.9.12-slim

RUN pip install fastapi uvicorn poetry wheel virtualenv ansible-runner

EXPOSE 8000

COPY ./main.py /usr/src/
#COPY ./pyproject.toml /fastapi

WORKDIR /usr/src/
# RUN poetry config virtualenvs.create false \
#   && poetry install

CMD ["uvicorn", "main:app"]