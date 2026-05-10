import { Sidebar } from "./sidebar";

export function AppShell({ children }) {
  return (
    <main className="min-h-screen bg-slate-950/30 text-slate-100">
      <div className="flex min-h-screen">
        <Sidebar />

        <section className="flex-1 p-4 md:p-6 lg:p-8">
          <div className="mx-auto max-w-7xl">
            {children}
          </div>
        </section>
      </div>
    </main>
  );
}