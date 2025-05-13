# Simple Agent Server

A simple agent server using langchain + langgraph + fastapi

```bash
uv init --app --python 3.11
```

## docker

```bash
docker build -t simple-agent-server .
# docker build --platform linux/amd64 -t simple-agent-server .
# docker buildx build --platform linux/amd64,linux/arm64 -t aoaiaiplayground.azurecr.io/agent/simple-agent-server --push .
```
