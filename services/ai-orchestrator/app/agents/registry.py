AGENT_REGISTRY = {
    "coordinator-agent": {
        "name": "coordinator-agent",
        "role": "Coordinates requests and routes tasks to specialist agents.",
        "keywords": [],
    },
    "research-agent": {
        "name": "research-agent",
        "role": "Handles research, summaries, comparisons, and information gathering.",
        "keywords": ["research", "compare", "summarize", "explain", "find"],
    },
    "coding-agent": {
        "name": "coding-agent",
        "role": "Handles coding, architecture, APIs, debugging, and implementation.",
        "keywords": ["code", "api", "backend", "frontend", "function", "component", "build"],
    },
    "planning-agent": {
        "name": "planning-agent",
        "role": "Handles roadmaps, phases, project planning, and execution strategy.",
        "keywords": ["plan", "phase", "roadmap", "steps", "strategy"],
    },
    "debugging-agent": {
        "name": "debugging-agent",
        "role": "Diagnoses errors, logs, bugs, crashes, and broken workflows.",
        "keywords": ["error", "bug", "fix", "issue", "traceback", "failed", "not working"],
    },
    "security-agent": {
        "name": "security-agent",
        "role": "Reviews auth, RBAC, secrets, threat models, and secure architecture.",
        "keywords": ["security", "jwt", "auth", "rbac", "token", "secret", "vulnerability"],
    },
    "automation-agent": {
        "name": "automation-agent",
        "role": "Handles workflows, task automation, scheduled jobs, and tool execution.",
        "keywords": ["automate", "workflow", "schedule", "tool", "execute"],
    },
}


def list_agents():
    return list(AGENT_REGISTRY.values())


def get_agent(agent_name: str):
    return AGENT_REGISTRY.get(agent_name)