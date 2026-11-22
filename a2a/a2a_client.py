import asyncio
from a2a.client import create_client
from a2a.helpers import new_text_message
from a2a.types import Role, SendMessageRequest

async def main():
    # connection 
    client = await create_client('http://localhost:8001/')
    print('connected to the delivery agent..')
    #  send the request through message
    message = new_text_message( "Deliver order 101. Pickup: ABC Restaurant. Customer address: Davanagere.",role=Role.ROLE_USER)
    request = SendMessageRequest(message)
    await client.close()

if __name__ == "__main__":
    asyncio.run(main())