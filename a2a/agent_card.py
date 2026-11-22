from a2a.types import AgentCard,AgentCapabilities,AgentSkill,AgentInterface

delivery_skill = AgentSkill(
    name='food delivery',
    description='pick up food from the restorent and delivery it to customers.',
    tags=['food','pickup','delivery'],
    examples=["Deliver order 101 to the customer"],
    input_modes=["text/plain"],
    output_modes=["text/plain"],
)

delivery_agent_card = AgentCard(
    name="delivery agent",
    description='handle the food pick up and customer delivery',
    version="1.0.0",
    default_input_modes=["text/plain"],
    default_output_modes=["text/plain"],
    capabilities=AgentCapabilities(streaming=True),
    supported_interfaces= [AgentInterface(
        protocol_binding="JSONRPC",
        protocol_version="1.0",
        url="http://localhost:8001/",
    )
    ],
    skills=[delivery_skill],
)
print(delivery_agent_card)