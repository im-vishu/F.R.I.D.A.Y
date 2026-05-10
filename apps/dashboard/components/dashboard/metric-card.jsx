export function MetricCard({
  icon: Icon,
  label,
  value,
  description,
}) {
  return (
    <div className="rounded-2xl border border-cyan-500/10 bg-slate-950/80 p-5 shadow-xl shadow-black/20">
      <div className="flex items-center justify-between">
        <div className="rounded-xl bg-cyan-400/10 p-3 text-cyan-300">
          <Icon size={22} />
        </div>

        <span className="rounded-full bg-emerald-400/10 px-3 py-1 text-xs font-semibold text-emerald-300">
          Live
        </span>
      </div>

      <p className="mt-5 text-sm text-slate-400">
        {label}
      </p>

      <h3 className="mt-2 text-3xl font-bold text-white">
        {value}
      </h3>

      <p className="mt-2 text-sm text-slate-500">
        {description}
      </p>
    </div>
  );
}