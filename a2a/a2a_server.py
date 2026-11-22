import uvicorn
from fastapi import FastAPI
from agent_card import delivery_agent_card
from delivery_executor import DeliveryAgentExecutor
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.server.routes import create_jsonrpc_routes,create_agent_card_routes

request_handler =  DefaultRequestHandler(
    agent_executor=DeliveryAgentExecutor(),
    task_store=InMemoryTaskStore(),
    agent_card=delivery_agent_card,
)

routes = [
    *create_agent_card_routes(delivery_agent_card),
    *create_jsonrpc_routes(request_handler, "/"),
]

app = FastAPI(routes=routes)

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8001
    )
