FROM python:3.10-slim as python
ENV PYTHONUNBUFFERED=true
WORKDIR /app

FROM python as builder
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV PATH="$POETRY_HOME/bin:$PATH"

RUN python -c 'from urllib.request import urlopen; print(urlopen("https://install.python-poetry.org").read().decode())' | python -
COPY . /app
RUN ls -al
RUN poetry install --no-interaction --no-ansi -vvv

FROM python as runtime
ENV PATH="/app/.venv/bin:$PATH"
COPY --from=builder /app /app
EXPOSE 8000
ENTRYPOINT ["uvicorn", "--host=0.0.0.0", "--port=8000", "--workers=1" ]
CMD ["todo_api:app"]