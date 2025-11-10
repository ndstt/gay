FROM apache/kafka:latest as build
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERRED=1
ENV UV_LINK_MODE=copy
ENV UV_NO_CACHE=1

USER root
RUN pip install --no-cache-dir --disable-pip-version-check "uv==0.7.*"
USER 185
COPY --chown=185:185 pyproject.toml  .
RUN uv sync
COPY --chown=185:185 . .
ENV PATH "/app/.venv/bin:$PATH"
CMD ["python", "main.py"]
