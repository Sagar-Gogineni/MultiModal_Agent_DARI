# Use a slim base image
FROM python:3.10-slim-bullseye

#ENV PATH="/home/user/.local/bin:$PATH"
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/home/user/.local/bin:$PATH" \
    POETRY_VERSION=1.4.2 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

RUN useradd -m -u 1000 user
#USER user

WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && ln -s /opt/poetry/bin/poetry /usr/local/bin/poetry

COPY  ./dataAnalyst-agent .

CMD [ "cd /app/dataAnalyst-agent/" ]

RUN poetry config installer.max-workers 10
RUN  poetry install --no-interaction --no-ansi -vvv && rm -rf ~/.cache/pypoetry

EXPOSE  8501
ENTRYPOINT [ "poetry", "run" ,"streamlit","run" ,"dataanalyst_agent/main.py","--server.port=8501" ]


