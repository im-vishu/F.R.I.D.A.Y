"use client";

import { useEffect, useState } from "react";
import { Bot, Send, User, Wifi } from "lucide-react";
import { socket } from "../../services/socket";
import { useSystemStore } from "../../store/system-store";

export function AIChatPanel() {
  const { socketStatus, setSocketStatus } = useSystemStore();

  const [messages, setMessages] = useState([
    {
      role: "assistant",
      text: "F.R.I.D.A.Y online. Realtime gateway connection initializing.",
    },
  ]);

  const [input, setInput] = useState("");

  useEffect(() => {
    socket.connect();

    socket.on("connect", () => {
      setSocketStatus("connected");
    });

    socket.on("disconnect", () => {
      setSocketStatus("disconnected");
    });

    socket.on("gateway:connected", (payload) => {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text: payload.message,
        },
      ]);
    });

    socket.on("chat:response", (payload) => {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text: payload.message,
        },
      ]);
    });

    return () => {
      socket.off("connect");
      socket.off("disconnect");
      socket.off("gateway:connected");
      socket.off("chat:response");
      socket.disconnect();
    };
  }, [setSocketStatus]);

  function sendMessage(e) {
    e.preventDefault();

    if (!input.trim()) return;

    const userMessage = {
      role: "user",
      text: input,
    };

    setMessages((prev) => [...prev, userMessage]);

    socket.emit("chat:message", {
      message: input,
      timestamp: new Date().toISOString(),
    });

    setInput("");
  }

  return (
    <div className="rounded-2xl border border-cyan-500/10 bg-slate-950/80 p-6">
      <div className="flex items-center justify-between gap-3">
        <div className="flex items-center gap-3">
          <div className="rounded-xl bg-cyan-400/10 p-3 text-cyan-300">
            <Bot size={22} />
          </div>

          <div>
            <h3 className="text-lg font-bold text-white">AI Chat Interface</h3>
            <p className="text-sm text-slate-400">
              Realtime Socket.IO command interface.
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2 rounded-full bg-cyan-400/10 px-3 py-1 text-xs font-semibold text-cyan-300">
          <Wifi size={14} />
          {socketStatus}
        </div>
      </div>

      <div className="mt-6 h-[360px] space-y-4 overflow-y-auto rounded-2xl border border-slate-800 bg-slate-900/60 p-4">
        {messages.map((message, index) => {
          const isUser = message.role === "user";
          const Icon = isUser ? User : Bot;

          return (
            <div
              key={index}
              className={`flex gap-3 ${isUser ? "justify-end" : "justify-start"}`}
            >
              {!isUser && (
                <div className="mt-1 rounded-full bg-cyan-400/10 p-2 text-cyan-300">
                  <Icon size={16} />
                </div>
              )}

              <div
                className={`max-w-[80%] rounded-2xl px-4 py-3 text-sm ${
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
      </div>

      <form onSubmit={sendMessage} className="mt-5 flex gap-3">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Send realtime command to F.R.I.D.A.Y..."
          className="flex-1 rounded-xl border border-slate-800 bg-slate-900 px-4 py-3 text-sm text-white outline-none transition placeholder:text-slate-500 focus:border-cyan-400"
        />

        <button
          type="submit"
          className="rounded-xl bg-cyan-400 px-5 py-3 font-semibold text-slate-950 transition hover:bg-cyan-300"
        >
          <Send size={18} />
        </button>
      </form>
    </div>
  );
}