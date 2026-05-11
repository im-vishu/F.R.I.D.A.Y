"use client";

import { useState } from "react";
import { Bot, Brain, KeyRound, Send, User, Wrench, Database } from "lucide-react";
import { sendAIChatMessage } from "../../services/ai-api";

export function AIChatPanel() {
  const [token, setToken] = useState("");

  const [messages, setMessages] = useState([
    {
      role: "assistant",
      text: "F.R.I.D.A.Y online. Paste JWT token, then send a command.",
    },
  ]);

  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  async function sendMessage(e) {
    e.preventDefault();

    if (!input.trim()) return;

    if (!token.trim()) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text: "JWT token missing. Paste your token first.",
        },
      ]);
      return;
    }

    const userText = input;

    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        text: userText,
      },
    ]);

    setInput("");
    setLoading(true);

    try {
      const data = await sendAIChatMessage({
        token,
        message: userText,
        sessionId: "dashboard-chat-session",
        context: {
          source: "dashboard",
          phase: "7.1",
        },
      });

      const result = data?.result;
      const metadata = result?.metadata;

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text:
            result?.response ||
            "F.R.I.D.A.Y received the command, but no response was returned.",
          selectedAgent: metadata?.selected_agent || result?.agent,
          agentRole: result?.agent_role,
          toolUsed: metadata?.tool_executed,
          memoryCount: metadata?.memory_count,
        },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text:
            error?.response?.data?.message ||
            "AI request failed. Check API, token, and orchestrator services.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="rounded-2xl border border-cyan-500/10 bg-slate-950/80 p-6">
      <div className="flex items-center gap-3">
        <div className="rounded-xl bg-cyan-400/10 p-3 text-cyan-300">
          <Bot size={22} />
        </div>

        <div>
          <h3 className="text-lg font-bold text-white">AI Chat Interface</h3>
          <p className="text-sm text-slate-400">
            Memory-aware, tool-aware, and agent-aware AI gateway.
          </p>
        </div>
      </div>

      <div className="mt-5 flex items-center gap-3 rounded-xl border border-slate-800 bg-slate-900 px-4 py-3">
        <KeyRound size={18} className="text-cyan-300" />

        <input
          value={token}
          onChange={(e) => setToken(e.target.value)}
          placeholder="Paste JWT token here..."
          className="flex-1 bg-transparent text-xs text-white outline-none placeholder:text-slate-500"
        />
      </div>

      <div className="mt-6 h-[360px] space-y-4 overflow-y-auto rounded-2xl border border-slate-800 bg-slate-900/60 p-4">
        {messages.map((message, index) => {
          const isUser = message.role === "user";
          const Icon = isUser ? User : Bot;

          return (
            <div
              key={index}
              className={`flex gap-3 ${
                isUser ? "justify-end" : "justify-start"
              }`}
            >
              {!isUser && (
                <div className="mt-1 rounded-full bg-cyan-400/10 p-2 text-cyan-300">
                  <Icon size={16} />
                </div>
              )}

              <div
                className={`max-w-[80%] whitespace-pre-wrap rounded-2xl px-4 py-3 text-sm ${
                  isUser
                    ? "bg-cyan-400 text-slate-950"
                    : "bg-slate-800 text-slate-200"
                }`}
              >
                {message.text}

                {!isUser &&
                  (message.selectedAgent ||
                    message.toolUsed ||
                    message.memoryCount !== undefined) && (
                    <div className="mt-3 flex flex-wrap gap-2 border-t border-slate-700 pt-3 text-xs">
                      {message.selectedAgent && (
                        <span className="inline-flex items-center gap-1 rounded-full bg-purple-400/10 px-3 py-1 text-purple-300">
                          <Brain size={12} />
                          Agent: {message.selectedAgent}
                        </span>
                      )}

                      {message.toolUsed && (
                        <span className="inline-flex items-center gap-1 rounded-full bg-amber-400/10 px-3 py-1 text-amber-300">
                          <Wrench size={12} />
                          Tool: {message.toolUsed}
                        </span>
                      )}

                      {message.memoryCount !== undefined && (
                        <span className="inline-flex items-center gap-1 rounded-full bg-cyan-400/10 px-3 py-1 text-cyan-300">
                          <Database size={12} />
                          Memories: {message.memoryCount}
                        </span>
                      )}

                      {message.agentRole && (
                        <span className="w-full rounded-xl bg-slate-900 px-3 py-2 text-slate-400">
                          {message.agentRole}
                        </span>
                      )}
                    </div>
                  )}
              </div>

              {isUser && (
                <div className="mt-1 rounded-full bg-slate-800 p-2 text-slate-300">
                  <Icon size={16} />
                </div>
              )}
            </div>
          );
        })}

        {loading && (
          <div className="flex gap-3">
            <div className="mt-1 rounded-full bg-cyan-400/10 p-2 text-cyan-300">
              <Bot size={16} />
            </div>

            <div className="rounded-2xl bg-slate-800 px-4 py-3 text-sm text-slate-300">
              F.R.I.D.A.Y is routing through agents...
            </div>
          </div>
        )}
      </div>

      <form onSubmit={sendMessage} className="mt-5 flex gap-3">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder='Try: "Review JWT security" or "Plan next phase"'
          className="flex-1 rounded-xl border border-slate-800 bg-slate-900 px-4 py-3 text-sm text-white outline-none transition placeholder:text-slate-500 focus:border-cyan-400"
        />

        <button
          type="submit"
          disabled={loading}
          className="rounded-xl bg-cyan-400 px-5 py-3 font-semibold text-slate-950 transition hover:bg-cyan-300 disabled:cursor-not-allowed disabled:opacity-60"
        >
          <Send size={18} />
        </button>
      </form>
    </div>
  );
}