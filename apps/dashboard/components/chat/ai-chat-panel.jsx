"use client";

import { useState } from "react";
import { Bot, KeyRound, Send, User } from "lucide-react";
import { sendAIChatMessage } from "../../services/ai-api";

export function AIChatPanel() {
  const [token, setToken] = useState("");

  const [messages, setMessages] = useState([
    {
      role: "assistant",
      text: "F.R.I.D.A.Y online. Paste your JWT token, then send a command to the AI orchestrator.",
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
          text: "JWT token missing. Login through the API and paste your token above.",
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
          phase: "4.2",
        },
      });

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text:
            data?.result?.response ||
            "F.R.I.D.A.Y received the command, but no response was returned.",
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
            Connected to protected API AI gateway.
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
              F.R.I.D.A.Y is thinking...
            </div>
          </div>
        )}
      </div>

      <form onSubmit={sendMessage} className="mt-5 flex gap-3">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Send AI command to F.R.I.D.A.Y..."
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