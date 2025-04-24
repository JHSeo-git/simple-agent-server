import json

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sse_starlette import EventSourceResponse, ServerSentEvent

from app.graph.builder import create_graph
from app.log import get_logger

logger = get_logger(__name__)


app = FastAPI(
    title="Simple Agent Server",
    description="API for simple agent workflow",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


class AppRequest(BaseModel):
    message: str = Field(..., description="The message to send to the agent")


@app.post("/")
def app_endpoint(request: AppRequest):
    graph = create_graph()

    result = graph.invoke({"messages": [request.message]})

    return {"message": result["messages"][-1]}


@app.post("/sse")
def app_endpoint(request: AppRequest, req: Request):
    graph = create_graph()

    try:

        async def event_generator():
            async for event in graph.astream({"messages": [request.message]}):
                if await req.is_disconnected():
                    logger.info("Client disconnected")
                    break

                for key, value in event.items():
                    yield ServerSentEvent(
                        event="message",
                        data=json.dumps(
                            {
                                "role": key,
                                "content": value,
                            },
                            ensure_ascii=False,
                        ),
                    )

        return EventSourceResponse(
            event_generator(),
            media_type="text/event-stream",
            sep="\n",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
