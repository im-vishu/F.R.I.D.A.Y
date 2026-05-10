import { AppShell } from "../components/layout/app-shell";
import { MetricCard } from "../components/dashboard/metric-card";
import { SystemStatus } from "../components/dashboard/system-status";
import { AIChatPanel } from "../components/chat/ai-chat-panel";
import { metrics } from "../lib/data";

import {
  Activity,
  Brain,
  Database,
  Radio,
  Zap,
} from "lucide-react";

export default function Home() {
  const icons = [Brain, Radio, Database, Zap];

  return (
    <AppShell>
      <section className="space-y-8">
        <div className="rounded-3xl border border-cyan-500/20 bg-slate-950/80 p-8 shadow-2xl shadow-cyan-500/10">
          <div className="flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">
            <div>
              <p className="text-sm font-semibold uppercase tracking-[0.4em] text-cyan-400">
                AI Operating System
              </p>

              <h1 className="mt-4 text-4xl font-bold tracking-tight text-white md:text-6xl">
                F.R.I.D.A.Y Command Center
              </h1>

              <p className="mt-4 max-w-2xl text-slate-400">
                Realtime AI orchestration dashboard for agents, memory, tools,
                voice intelligence, and system analytics.
              </p>
            </div>

            <div className="rounded-2xl border border-cyan-400/20 bg-cyan-400/10 px-6 py-4">
              <div className="flex items-center gap-3 text-cyan-300">
                <Activity size={22} />
                <span className="font-semibold">System Online</span>
              </div>

              <p className="mt-2 text-sm text-slate-400">
                Gateway, API, Memory, and AI runtime ready.
              </p>
            </div>
          </div>
        </div>

        <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-4">
          {metrics.map((metric, index) => {
            const Icon = icons[index];

            return <MetricCard key={metric.label} icon={Icon} {...metric} />;
          })}
        </div>

        <div className="grid gap-6 xl:grid-cols-[1.1fr_0.9fr]">
          <AIChatPanel />

          <div className="space-y-6">
            <SystemStatus
              title="AI Runtime"
              type="runtime"
              items={[
                ["Coordinator Agent", "Active"],
                ["Memory Engine", "Ready"],
                ["Tool Engine", "Standby"],
                ["Voice Pipeline", "Queued"],
              ]}
            />

            <SystemStatus
              title="Security Layer"
              type="security"
              items={[
                ["JWT Auth", "Planned"],
                ["RBAC", "Planned"],
                ["Audit Logs", "Pending"],
                ["Tool Sandbox", "Pending"],
              ]}
            />
          </div>
        </div>
      </section>
    </AppShell>
  );
}