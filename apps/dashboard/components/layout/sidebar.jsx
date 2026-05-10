import {
  Bot,
  Brain,
  Database,
  Gauge,
  Home,
  Mic,
  Radio,
  Shield,
  Terminal,
  Wrench,
} from "lucide-react";

const navItems = [
  { label: "Command", icon: Home },
  { label: "AI Chat", icon: Bot },
  { label: "Voice", icon: Mic },
  { label: "Agents", icon: Brain },
  { label: "Memory", icon: Database },
  { label: "Tools", icon: Wrench },
  { label: "Gateway", icon: Radio },
  { label: "Analytics", icon: Gauge },
  { label: "Security", icon: Shield },
  { label: "Logs", icon: Terminal },
];

export function Sidebar() {
  return (
    <aside className="hidden min-h-screen w-72 border-r border-cyan-500/10 bg-slate-950/80 p-5 backdrop-blur-xl lg:block">
      <div className="rounded-2xl border border-cyan-400/20 bg-cyan-400/10 p-5">
        <p className="text-xs font-bold uppercase tracking-[0.35em] text-cyan-300">
          F.R.I.D.A.Y
        </p>

        <h2 className="mt-3 text-xl font-bold text-white">
          AI OS Core
        </h2>

        <p className="mt-2 text-sm text-slate-400">
          Fully Responsive Intelligent Digital Assistant for You.
        </p>
      </div>

      <nav className="mt-8 space-y-2">
        {navItems.map((item) => {
          const Icon = item.icon;

          return (
            <button
              key={item.label}
              className="flex w-full items-center gap-3 rounded-xl px-4 py-3 text-left text-sm font-medium text-slate-400 transition hover:bg-cyan-400/10 hover:text-cyan-300"
            >
              <Icon size={18} />
              {item.label}
            </button>
          );
        })}
      </nav>
    </aside>
  );
}