"use client";

import { useEffect } from "react";
import { Brain, Shield } from "lucide-react";
import { checkApiHealth, checkGatewayHealth } from "../../services/api";
import { useSystemStore } from "../../store/system-store";

export function SystemStatus({ title, type, items }) {
  const {
    apiStatus,
    gatewayStatus,
    socketStatus,
    setApiStatus,
    setGatewayStatus,
  } = useSystemStore();

  const Icon = type === "security" ? Shield : Brain;

  useEffect(() => {
    async function checkServices() {
      try {
        await checkApiHealth();
        setApiStatus("online");
      } catch {
        setApiStatus("offline");
      }

      try {
        await checkGatewayHealth();
        setGatewayStatus("online");
      } catch {
        setGatewayStatus("offline");
      }
    }

    checkServices();
  }, [setApiStatus, setGatewayStatus]);

  const liveItems = [
    ...items,
    ["API Service", apiStatus],
    ["Realtime Gateway", gatewayStatus],
    ["Socket Client", socketStatus],
  ];

  return (
    <div className="rounded-2xl border border-cyan-500/10 bg-slate-950/80 p-6">
      <div className="flex items-center gap-3">
        <div className="rounded-xl bg-purple-400/10 p-3 text-purple-300">
          <Icon size={22} />
        </div>

        <h3 className="text-lg font-bold text-white">{title}</h3>
      </div>

      <div className="mt-6 space-y-4">
        {liveItems.map(([label, status]) => (
          <div
            key={label}
            className="flex items-center justify-between border-b border-slate-800 pb-3 last:border-0"
          >
            <span className="text-sm text-slate-400">{label}</span>

            <span className="rounded-full bg-cyan-400/10 px-3 py-1 text-xs font-semibold text-cyan-300">
              {status}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}