from app.agents.registry import AGENT_REGISTRY, list_agents


class AgentService:
    def list_available_agents(self):
        return {
            "success": True,
            "count": len(list_agents()),
            "agents": list_agents(),
        }

    def select_agent(self, message: str):
        lower_message = message.lower()

        best_agent = AGENT_REGISTRY["coordinator-agent"]
        best_score = 0

        for agent in AGENT_REGISTRY.values():
            score = 0

            for keyword in agent.get("keywords", []):
                if keyword in lower_message:
                    score += 1

            if score > best_score:
                best_score = score
                best_agent = agent

        return {
            "agent": best_agent,
            "score": best_score,
        }


agent_service = AgentService()