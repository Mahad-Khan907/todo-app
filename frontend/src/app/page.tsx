'use client';

import { useRouter } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';
import { motion } from 'framer-motion';
import { 
  CheckCircle2, 
  Sparkles, 
  Bot, 
  Bell, 
  Calendar, 
  ArrowRight, 
  Layers,
  Zap,
  ShieldCheck,
  Check,
  Clock,
  ChevronRight
} from 'lucide-react';
import Link from 'next/link';

export default function HomePage() {
  const { user, loading } = useAuth();
  const router = useRouter();

  const handleGetStarted = () => {
    if (user) {
      router.push('/dashboard');
    } else {
      router.push('/register');
    }
  };

  const handleLogin = () => {
    if (user) {
      router.push('/dashboard');
    } else {
      router.push('/login');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-[#07090e] flex items-center justify-center">
        <div className="w-9 h-9 border-3 border-indigo-500 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#07090e] text-slate-100 font-sans selection:bg-indigo-500/25 selection:text-indigo-200 overflow-x-hidden">
      {/* Dynamic Background Ambient Gradients */}
      <div className="fixed top-0 left-1/2 -translate-x-1/2 w-[1200px] h-[550px] bg-gradient-to-b from-indigo-600/15 via-violet-600/5 to-transparent blur-[140px] pointer-events-none -z-10" />
      <div className="fixed top-1/4 -right-40 w-96 h-96 bg-cyan-500/10 blur-[130px] pointer-events-none -z-10" />
      <div className="fixed bottom-10 -left-40 w-96 h-96 bg-purple-600/10 blur-[130px] pointer-events-none -z-10" />

      {/* Grid pattern overlay */}
      <div className="fixed inset-0 bg-[linear-gradient(to_right,#ffffff05_1px,transparent_1px),linear-gradient(to_bottom,#ffffff05_1px,transparent_1px)] bg-[size:3.5rem_3.5rem] [mask-image:radial-gradient(ellipse_75%_50%_at_50%_0%,#000_70%,transparent_100%)] pointer-events-none -z-10" />

      {/* Navbar */}
      <header className="sticky top-0 z-50 backdrop-blur-xl bg-[#07090e]/80 border-b border-white/[0.06]">
        <div className="max-w-7xl mx-auto px-6 h-18 flex items-center justify-between">
          <div 
            onClick={() => router.push('/')}
            className="flex items-center gap-3 cursor-pointer"
          >
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 via-indigo-500 to-cyan-400 flex items-center justify-center shadow-lg shadow-indigo-500/25 ring-1 ring-white/20">
              <CheckCircle2 className="w-5 h-5 text-white" />
            </div>
            <div className="flex items-center gap-2">
              <span className="text-lg font-bold text-white tracking-tight">TaskFlow AI</span>
              <span className="hidden sm:inline-block px-2 py-0.5 text-[10px] font-semibold tracking-wide uppercase bg-indigo-500/10 text-indigo-300 border border-indigo-500/20 rounded-full">
                Particle Agent
              </span>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={handleLogin}
              className="px-4 py-2 text-xs font-semibold text-slate-300 hover:text-white rounded-xl hover:bg-white/[0.04] transition-colors"
            >
              Sign In
            </button>
            <button
              onClick={handleGetStarted}
              className="inline-flex items-center gap-1.5 px-4 py-2 text-xs font-semibold text-white bg-indigo-600 hover:bg-indigo-500 rounded-xl shadow-md shadow-indigo-600/25 transition-all hover:scale-[1.02] active:scale-[0.98]"
            >
              <span>Get Started</span>
              <ChevronRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <main className="max-w-7xl mx-auto px-6 pt-16 pb-24">
        <div className="flex flex-col items-center text-center max-w-4xl mx-auto">
          {/* Top Pill */}
          <motion.div
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-white/[0.03] border border-white/[0.08] shadow-inner mb-6 text-xs text-slate-300 backdrop-blur-md"
          >
            <span className="flex h-2 w-2 rounded-full bg-emerald-400 animate-pulse" />
            <span className="font-medium text-slate-300">OpenRouter Particle AI &bull; Intelligent Reminders</span>
          </motion.div>

          {/* Headline */}
          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="text-4xl sm:text-6xl md:text-7xl font-extrabold tracking-tight text-white leading-[1.12] mb-6"
          >
            Manage tasks effortlessly with{' '}
            <span className="bg-gradient-to-r from-indigo-400 via-violet-300 to-cyan-300 bg-clip-text text-transparent">
              conversational AI
            </span>
          </motion.h1>

          {/* Description */}
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="text-base sm:text-lg text-slate-400 max-w-2xl mb-10 leading-relaxed font-normal"
          >
            A high-performance workspace designed for focus. Automate routines with recurring schedules, stay on track with smart email reminders, and let Particle AI execute bulk task actions with natural language.
          </motion.p>

          {/* Call to Actions */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="flex flex-col sm:flex-row items-center justify-center gap-3 w-full max-w-md mb-16"
          >
            <button
              onClick={handleGetStarted}
              className="w-full sm:w-auto px-6 py-3.5 rounded-xl text-sm font-semibold text-white bg-gradient-to-r from-indigo-600 via-indigo-500 to-cyan-500 shadow-xl shadow-indigo-600/30 hover:shadow-indigo-600/40 hover:scale-[1.02] active:scale-[0.98] transition-all flex items-center justify-center gap-2"
            >
              <span>Start Free Workspace</span>
              <ArrowRight className="w-4 h-4" />
            </button>
            <button
              onClick={handleLogin}
              className="w-full sm:w-auto px-6 py-3.5 rounded-xl text-sm font-semibold text-slate-300 bg-white/[0.04] hover:bg-white/[0.08] border border-white/[0.08] hover:border-white/[0.15] transition-all"
            >
              Open Dashboard
            </button>
          </motion.div>

          {/* Interactive UI Mockup Preview */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="w-full max-w-5xl rounded-2xl border border-white/[0.08] bg-[#0c1017]/90 p-4 sm:p-6 shadow-2xl shadow-black/80 backdrop-blur-xl mb-20 text-left"
          >
            <div className="flex items-center justify-between pb-4 mb-5 border-b border-white/[0.06]">
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-rose-500/80" />
                <div className="w-3 h-3 rounded-full bg-amber-500/80" />
                <div className="w-3 h-3 rounded-full bg-emerald-500/80" />
                <span className="text-xs text-slate-500 ml-2 font-mono">workspace.taskflow.app</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-[11px] px-2.5 py-0.5 rounded-full bg-indigo-500/15 text-indigo-300 border border-indigo-500/30 font-medium">
                  AI Agent Ready
                </span>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="p-4 rounded-xl bg-white/[0.02] border border-white/[0.05]">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-[10px] font-bold uppercase tracking-wider text-rose-400 bg-rose-500/10 px-2 py-0.5 rounded">High Priority</span>
                  <span className="text-xs text-slate-500">Today</span>
                </div>
                <h4 className="text-sm font-semibold text-white mb-1">Finalize project deployment</h4>
                <p className="text-xs text-slate-400">Deploy Next.js &amp; FastAPI unified build to Vercel production server.</p>
              </div>

              <div className="p-4 rounded-xl bg-white/[0.02] border border-white/[0.05]">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-[10px] font-bold uppercase tracking-wider text-amber-400 bg-amber-500/10 px-2 py-0.5 rounded">Medium</span>
                  <span className="text-xs text-cyan-400 flex items-center gap-1">
                    <Zap className="w-3 h-3" /> Daily
                  </span>
                </div>
                <h4 className="text-sm font-semibold text-white mb-1">Team Standup Sync</h4>
                <p className="text-xs text-slate-400">Review blockers, task backlog, and schedule notifications.</p>
              </div>

              <div className="p-4 rounded-xl bg-indigo-600/[0.08] border border-indigo-500/20">
                <div className="flex items-center gap-2 mb-2 text-indigo-400">
                  <Bot className="w-4 h-4" />
                  <span className="text-xs font-semibold">Particle AI Copilot</span>
                </div>
                <p className="text-xs text-slate-300 italic">
                  &ldquo;I have scheduled your recurring tasks and set an email reminder for 5:00 PM.&rdquo;
                </p>
              </div>
            </div>
          </motion.div>

          {/* Core Feature Pillars */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full text-left">
            <div className="p-6 rounded-2xl bg-white/[0.02] border border-white/[0.06] hover:border-indigo-500/30 transition-all">
              <div className="w-10 h-10 rounded-xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center mb-4">
                <Bot className="w-5 h-5 text-indigo-400" />
              </div>
              <h3 className="text-base font-bold text-white mb-2">Natural Language Agent</h3>
              <p className="text-xs text-slate-400 leading-relaxed">
                Connects directly to your database with MCP tools to add, filter, update, or clear tasks through natural chat commands.
              </p>
            </div>

            <div className="p-6 rounded-2xl bg-white/[0.02] border border-white/[0.06] hover:border-cyan-500/30 transition-all">
              <div className="w-10 h-10 rounded-xl bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center mb-4">
                <Bell className="w-5 h-5 text-cyan-400" />
              </div>
              <h3 className="text-base font-bold text-white mb-2">Smart Email Reminders</h3>
              <p className="text-xs text-slate-400 leading-relaxed">
                Never lose track of critical deadlines. Set date and time alarms and receive instant notification alerts.
              </p>
            </div>

            <div className="p-6 rounded-2xl bg-white/[0.02] border border-white/[0.06] hover:border-purple-500/30 transition-all">
              <div className="w-10 h-10 rounded-xl bg-purple-500/10 border border-purple-500/20 flex items-center justify-center mb-4">
                <Calendar className="w-5 h-5 text-purple-400" />
              </div>
              <h3 className="text-base font-bold text-white mb-2">Recurring Schedules</h3>
              <p className="text-xs text-slate-400 leading-relaxed">
                Configure daily, weekly, or monthly repeating tasks that automatically regenerate on exact schedule intervals.
              </p>
            </div>
          </div>
        </div>
      </main>

      {/* Modern Footer */}
      <footer className="border-t border-white/[0.06] py-10 bg-[#07090e]">
        <div className="max-w-7xl mx-auto px-6 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-slate-500">
          <div className="flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-indigo-400" />
            <span className="font-semibold text-slate-300">TaskFlow AI</span>
            <span>&bull; &copy; {new Date().getFullYear()} All rights reserved.</span>
          </div>
          <div className="flex items-center gap-6">
            <span>FastAPI Server</span>
            <span>Neon PostgreSQL</span>
            <span>Particle AI 1</span>
          </div>
        </div>
      </footer>
    </div>
  );
}
