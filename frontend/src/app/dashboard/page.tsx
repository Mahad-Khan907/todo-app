'use client'

import { useState, useEffect, useMemo } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  Plus, Check, X, Calendar, Tag, LayoutGrid, LayoutList, Search, 
  Sparkles, Zap, Target, Clock, MessageSquare, PenLine, LogOut, 
  Home, CheckCircle2, Bell, AlertCircle
} from 'lucide-react'
import { useAuth } from '@/contexts/AuthContext';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import api from '@/lib/api';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import ChatInterface from '@/components/chat/ChatInterface';
import FloatingChatButton from '@/components/FloatingChatButton';
import { ConversationProvider } from '@/contexts/ConversationContext';

interface Task {
  id: number
  title: string
  description?: string
  completed: boolean
  priority: 'high' | 'medium' | 'low'
  due_date?: string
  tags?: string[]
  completed_at?: string
  is_recurring?: boolean
  recurring_pattern?: 'daily' | 'weekly' | 'monthly' | 'custom'
  reminder_at?: string
  last_notified?: string
}

const priorityConfig = {
  high: { bg: 'bg-rose-500/15', text: 'text-rose-400', border: 'border-rose-500/30' },
  medium: { bg: 'bg-amber-500/15', text: 'text-amber-400', border: 'border-amber-500/30' },
  low: { bg: 'bg-emerald-500/15', text: 'text-emerald-400', border: 'border-emerald-500/30' },
}

export default function Dashboard() {
  return (
    <ConversationProvider>
      <DashboardContent />
    </ConversationProvider>
  );
}

function DashboardContent() {
  const formatToLocalDateTime = (date: Date): string => {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    return `${year}-${month}-${day}T${hours}:${minutes}`;
  };

  const queryClient = useQueryClient();
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [priority, setPriority] = useState<Task['priority']>('medium')
  const [dueDate, setDueDate] = useState('')
  const [tags, setTags] = useState('')
  const [isRecurring, setIsRecurring] = useState<boolean>(false)
  const [recurringPattern, setRecurringPattern] = useState<'daily' | 'weekly' | 'monthly' | 'custom'>('weekly')
  const [reminderAt, setReminderAt] = useState<string>('')
  const [editingTask, setEditingTask] = useState<Task | null>(null)
  const [showModal, setShowModal] = useState(false)
  const [viewMode, setViewMode] = useState<'grid' | 'list' | 'chat'>('grid')
  const [searchQuery, setSearchQuery] = useState('')
  const [filterType, setFilterType] = useState<'all' | 'pending' | 'completed' | 'high' | 'medium' | 'low' | 'date'>('all')

  const { user, logout, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && !user) {
      router.push('/login');
    }
  }, [user, loading, router]);

  const { data: tasks = [] } = useQuery<Task[]>({
    queryKey: ['tasks'],
    queryFn: async () => {
      const response = await api.get('/tasks/'); 
      return response.data;
    },
    enabled: !!user && !loading,
  });

  const createTaskMutation = useMutation({
    mutationFn: async (taskData: Omit<Task, 'id'>) => {
      const response = await api.post('/tasks/', taskData);
      return response.data;
    },
    onMutate: async (newTask) => {
      await queryClient.cancelQueries({ queryKey: ['tasks'] });
      const previousTasks = queryClient.getQueryData<Task[]>(['tasks']);
      const optimisticTask: Task = {
        id: Date.now(),
        title: newTask.title,
        description: newTask.description,
        completed: newTask.completed ?? false,
        priority: newTask.priority,
        due_date: newTask.due_date,
        tags: newTask.tags,
        is_recurring: newTask.is_recurring,
        recurring_pattern: newTask.recurring_pattern,
        reminder_at: newTask.reminder_at,
      };
      queryClient.setQueryData<Task[]>(['tasks'], (old = []) => [optimisticTask, ...old]);
      return { previousTasks };
    },
    onError: (err, newTask, context) => {
      if (context?.previousTasks) {
        queryClient.setQueryData(['tasks'], context.previousTasks);
      }
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] });
    },
  });

  const updateTaskMutation = useMutation({
    mutationFn: async ({ id, taskData }: { id: number; taskData: Partial<Task> }) => {
      const response = await api.patch(`/tasks/${id}`, taskData);
      return response.data;
    },
    onMutate: async ({ id, taskData }) => {
      await queryClient.cancelQueries({ queryKey: ['tasks'] });
      const previousTasks = queryClient.getQueryData<Task[]>(['tasks']);
      queryClient.setQueryData<Task[]>(['tasks'], (old = []) =>
        old.map(task => (task.id === id ? { ...task, ...taskData } : task))
      );
      return { previousTasks };
    },
    onError: (err, variables, context) => {
      if (context?.previousTasks) {
        queryClient.setQueryData(['tasks'], context.previousTasks);
      }
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] });
    },
  });

  const deleteTaskMutation = useMutation({
    mutationFn: async (id: number) => {
      const response = await api.delete(`/tasks/${id}`);
      return id;
    },
    onMutate: async (id) => {
      await queryClient.cancelQueries({ queryKey: ['tasks'] });
      const previousTasks = queryClient.getQueryData<Task[]>(['tasks']);
      queryClient.setQueryData<Task[]>(['tasks'], (old = []) =>
        old.filter(task => task.id !== id)
      );
      return { previousTasks };
    },
    onError: (err, id, context) => {
      if (context?.previousTasks) {
        queryClient.setQueryData(['tasks'], context.previousTasks);
      }
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] });
    },
  });

  const stats = useMemo(() => {
    const total = tasks.length
    const today = new Date();
    const completed = tasks.filter(t => t.completed).length
    const todayCompleted = tasks.filter(t =>
      t.completed && t.completed_at && new Date(t.completed_at).toDateString() === today.toDateString()
    ).length
    const dueSoon = tasks.filter(t => {
      if (!t.due_date || t.completed) return false
      const due = new Date(t.due_date)
      const diff = (due.getTime() - today.getTime()) / (1000*60*60*24)
      return diff >= 0 && diff <= 3
    }).length
    const score = total ? Math.round((completed / total) * 100) : 0
    return { total, completed, todayCompleted, dueSoon, score }
  }, [tasks])

  const filteredTasks = useMemo(() => {
    let filtered = tasks.filter(task => {
      const matchesSearch =
        task.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        task.description?.toLowerCase().includes(searchQuery.toLowerCase()) ||
        task.tags?.some(tag => tag.toLowerCase().includes(searchQuery.toLowerCase()))

      if (filterType === 'pending') return matchesSearch && !task.completed
      if (filterType === 'completed') return matchesSearch && task.completed
      if (['high', 'medium', 'low'].includes(filterType)) return matchesSearch && task.priority === filterType
      return matchesSearch
    });

    if (filterType === 'date') {
      const today = new Date();
      filtered = filtered.sort((a, b) => {
        const aDue = a.due_date ? new Date(a.due_date).getTime() : Infinity;
        const bDue = b.due_date ? new Date(b.due_date).getTime() : Infinity;
        return Math.abs(aDue - today.getTime()) - Math.abs(bDue - today.getTime());
      });
    }

    return filtered;
  }, [tasks, searchQuery, filterType]);

  const openModal = (task?: Task) => {
    if (task) {
      setEditingTask(task)
      setTitle(task.title)
      setDescription(task.description || '')
      setPriority(task.priority)
      setDueDate(task.due_date ? formatToLocalDateTime(new Date(task.due_date)) : '')
      setTags(task.tags?.join(', ') || '')
      setIsRecurring(task.is_recurring || false)
      setRecurringPattern(task.recurring_pattern || 'weekly')
      setReminderAt(task.reminder_at ? formatToLocalDateTime(new Date(task.reminder_at)) : '')
    } else {
      setEditingTask(null)
      setTitle('')
      setDescription('')
      setPriority('medium')
      setDueDate('')
      setTags('')
      setIsRecurring(false)
      setRecurringPattern('weekly')
      setReminderAt('')
    }
    setShowModal(true)
  }

  const saveTask = async () => {
    if (!title.trim()) return;

    const parsedTags = tags
      ? tags.split(',').map(t => t.trim()).filter(Boolean)
      : [];

    const taskData: any = {
      title,
      description: description || undefined,
      priority,
      due_date: dueDate ? new Date(dueDate).toISOString() : undefined,
      tags: parsedTags,
      is_recurring: isRecurring,
      recurring_pattern: isRecurring ? recurringPattern : undefined,
      reminder_at: reminderAt ? new Date(reminderAt).toISOString() : undefined,
    }

    if (editingTask) {
      updateTaskMutation.mutate({ id: editingTask.id, taskData });
    } else {
      createTaskMutation.mutate(taskData);
    }
    setShowModal(false);
  }

  const toggleComplete = async (id: number) => {
    const task = tasks.find(t => t.id === id);
    if (!task) return;
    const updatedTaskData = { 
      completed: !task.completed, 
      completed_at: !task.completed ? new Date().toISOString() : undefined 
    };
    updateTaskMutation.mutate({ id, taskData: updatedTaskData });
  }

  const deleteTask = async (id: number) => {
    deleteTaskMutation.mutate(id);
  }

  const handleLogout = () => {
    logout();
    router.push('/login');
  };

  if (loading || !user) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="w-10 h-10 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans selection:bg-indigo-500/30 selection:text-indigo-200">
      {/* Decorative ambient background */}
      <div className="fixed top-0 left-1/2 -translate-x-1/2 w-[1100px] h-[400px] bg-gradient-to-b from-indigo-600/15 via-purple-600/10 to-transparent blur-3xl pointer-events-none -z-10" />

      {/* Top Navbar */}
      <header className="sticky top-0 z-40 backdrop-blur-xl bg-slate-950/75 border-b border-slate-800/80">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 h-18 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Link href="/" className="flex items-center gap-2.5 group">
              <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-indigo-600 to-cyan-400 flex items-center justify-center shadow-md shadow-indigo-500/20 group-hover:scale-105 transition-transform">
                <CheckCircle2 className="w-5 h-5 text-white" />
              </div>
              <span className="font-bold text-lg tracking-tight bg-gradient-to-r from-white via-slate-200 to-slate-400 bg-clip-text text-transparent">
                TaskFlow AI
              </span>
            </Link>
          </div>

          <div className="flex items-center gap-3">
            <div className="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-full bg-slate-900 border border-slate-800 text-xs text-slate-300">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
              <span className="font-medium">{user.email}</span>
            </div>
            <button
              onClick={handleLogout}
              className="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-xl text-xs font-semibold text-slate-300 hover:text-white bg-slate-900 hover:bg-slate-800 border border-slate-800 hover:border-slate-700 transition-colors"
            >
              <LogOut className="w-3.5 h-3.5" />
              <span>Log out</span>
            </button>
          </div>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 py-8">
        {/* Header & Quick Action */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-8">
          <div>
            <h1 className="text-3xl font-extrabold tracking-tight text-white">Workspace Overview</h1>
            <p className="text-sm text-slate-400 mt-1">Organize priorities, manage recurring schedules, and collaborate with AI.</p>
          </div>

          <button
            onClick={() => openModal()}
            className="inline-flex items-center justify-center gap-2 px-5 py-2.5 rounded-xl font-semibold text-sm text-white bg-gradient-to-r from-indigo-600 via-indigo-500 to-cyan-500 shadow-lg shadow-indigo-500/25 hover:shadow-indigo-500/40 hover:scale-[1.02] active:scale-[0.98] transition-all"
          >
            <Plus className="w-4 h-4" />
            <span>Create Task</span>
          </button>
        </div>

        {/* Stats Row */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          {[
            { icon: Sparkles, label: "Completion Rate", value: `${stats.score}%`, color: "text-indigo-400", bg: "bg-indigo-500/10" },
            { icon: Zap, label: "Completed Today", value: stats.todayCompleted, color: "text-cyan-400", bg: "bg-cyan-500/10" },
            { icon: Target, label: "Active Tasks", value: tasks.length - tasks.filter(t => t.completed).length, color: "text-purple-400", bg: "bg-purple-500/10" },
            { icon: Clock, label: "Due Next 3 Days", value: stats.dueSoon, color: "text-amber-400", bg: "bg-amber-500/10" },
          ].map((stat, i) => (
            <div
              key={i}
              className="p-5 rounded-2xl bg-slate-900/70 border border-slate-800/80 backdrop-blur-sm"
            >
              <div className="flex items-center justify-between mb-3">
                <span className="text-xs font-medium text-slate-400">{stat.label}</span>
                <div className={`p-2 rounded-xl ${stat.bg} ${stat.color}`}>
                  <stat.icon className="w-4 h-4" />
                </div>
              </div>
              <p className="text-2xl font-bold text-white tracking-tight">{stat.value}</p>
            </div>
          ))}
        </div>

        {/* Search, Filter & View Controls */}
        <div className="flex flex-col lg:flex-row items-stretch lg:items-center justify-between gap-4 mb-6">
          <div className="relative flex-1 max-w-md">
            <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
            <input
              value={searchQuery}
              onChange={e => setSearchQuery(e.target.value)}
              placeholder="Search by title, description, or tags..."
              className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-slate-900/80 border border-slate-800 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 transition-all"
            />
          </div>

          <div className="flex flex-wrap items-center gap-2">
            {/* View Switcher */}
            <div className="flex items-center p-1 rounded-xl bg-slate-900 border border-slate-800">
              <button 
                onClick={() => setViewMode('grid')} 
                className={`p-1.5 rounded-lg text-xs font-medium transition ${viewMode === 'grid' ? 'bg-indigo-600 text-white shadow' : 'text-slate-400 hover:text-white'}`}
                title="Grid View"
              >
                <LayoutGrid className="w-4 h-4" />
              </button>
              <button 
                onClick={() => setViewMode('list')} 
                className={`p-1.5 rounded-lg text-xs font-medium transition ${viewMode === 'list' ? 'bg-indigo-600 text-white shadow' : 'text-slate-400 hover:text-white'}`}
                title="List View"
              >
                <LayoutList className="w-4 h-4" />
              </button>
              <button 
                onClick={() => setViewMode('chat')} 
                className={`p-1.5 rounded-lg text-xs font-medium transition ${viewMode === 'chat' ? 'bg-indigo-600 text-white shadow' : 'text-slate-400 hover:text-white'}`}
                title="AI Copilot View"
              >
                <MessageSquare className="w-4 h-4" />
              </button>
            </div>

            {/* Filter Pills */}
            {viewMode !== 'chat' && (
              <div className="flex flex-wrap items-center gap-1.5">
                {(['all', 'pending', 'completed', 'high', 'medium', 'low'] as const).map(f => (
                  <button
                    key={f}
                    onClick={() => setFilterType(f as any)}
                    className={`px-3 py-1.5 rounded-xl text-xs font-medium capitalize transition ${
                      filterType === f
                        ? 'bg-slate-800 text-white border border-slate-700 shadow-sm'
                        : 'text-slate-400 hover:text-slate-200 bg-slate-900/50 hover:bg-slate-900 border border-slate-800/60'
                    }`}
                  >
                    {f}
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Views Container */}
        {viewMode === 'chat' ? (
          <div className="h-[650px] rounded-2xl overflow-hidden border border-slate-800 bg-slate-900/60 backdrop-blur-md shadow-2xl">
            <ChatInterface onTaskChange={() => queryClient.invalidateQueries({ queryKey: ['tasks'] })} />
          </div>
        ) : (
          <div>
            {filteredTasks.length === 0 ? (
              <div className="text-center py-20 bg-slate-900/30 rounded-2xl border border-slate-800/80">
                <CheckCircle2 className="w-12 h-12 text-slate-600 mx-auto mb-3" />
                <h3 className="text-lg font-semibold text-slate-300">No tasks found</h3>
                <p className="text-xs text-slate-500 mt-1 max-w-sm mx-auto">
                  {searchQuery ? "No matches for your current search term." : "Your workspace is empty. Create a task or use the AI Copilot to get started!"}
                </p>
                <button
                  onClick={() => openModal()}
                  className="mt-5 px-4 py-2 text-xs font-semibold text-indigo-300 bg-indigo-500/10 hover:bg-indigo-500/20 border border-indigo-500/30 rounded-xl transition"
                >
                  Add Your First Task
                </button>
              </div>
            ) : (
              <div className={viewMode === 'grid' ? "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4" : "space-y-3"}>
                <AnimatePresence>
                  {filteredTasks.map(task => {
                    const priorityStyle = priorityConfig[task.priority] || priorityConfig.medium;
                    return (
                      <motion.div
                        key={task.id}
                        layout
                        initial={{ opacity: 0, scale: 0.98 }}
                        animate={{ opacity: 1, scale: 1 }}
                        exit={{ opacity: 0, scale: 0.98 }}
                        className={`group relative p-5 rounded-2xl bg-slate-900/70 border border-slate-800 hover:border-slate-700 transition-all shadow-lg ${
                          task.completed ? 'opacity-65' : ''
                        }`}
                      >
                        <div className="flex items-start justify-between gap-3 mb-3">
                          <button
                            onClick={() => toggleComplete(task.id)}
                            className={`w-6 h-6 rounded-lg border flex items-center justify-center transition-colors ${
                              task.completed
                                ? 'bg-indigo-600 border-indigo-600 text-white'
                                : 'border-slate-700 hover:border-indigo-400 bg-slate-950/50'
                            }`}
                          >
                            {task.completed && <Check className="w-3.5 h-3.5" />}
                          </button>

                          <div className="flex items-center gap-1 opacity-80 group-hover:opacity-100 transition-opacity">
                            <button
                              onClick={() => openModal(task)}
                              className="p-1.5 text-slate-400 hover:text-white rounded-lg hover:bg-slate-800 transition"
                              title="Edit"
                            >
                              <PenLine className="w-3.5 h-3.5" />
                            </button>
                            <button
                              onClick={() => {
                                if (confirm("Delete this task?")) {
                                  deleteTask(task.id);
                                }
                              }}
                              className="p-1.5 text-slate-400 hover:text-rose-400 rounded-lg hover:bg-slate-800 transition"
                              title="Delete"
                            >
                              <X className="w-3.5 h-3.5" />
                            </button>
                          </div>
                        </div>

                        <h3 className={`text-base font-semibold text-white mb-1.5 ${task.completed ? 'line-through text-slate-400' : ''}`}>
                          {task.title}
                        </h3>

                        {task.description && (
                          <p className="text-xs text-slate-400 leading-relaxed line-clamp-3 mb-3">
                            {task.description}
                          </p>
                        )}

                        {task.tags && task.tags.length > 0 && (
                          <div className="flex flex-wrap gap-1.5 mb-3">
                            {task.tags.map((tag, idx) => (
                              <span key={idx} className="px-2 py-0.5 rounded-md text-[10px] font-medium bg-slate-800 text-slate-300 border border-slate-700">
                                #{tag}
                              </span>
                            ))}
                          </div>
                        )}

                        <div className="pt-3 border-t border-slate-800/80 flex items-center justify-between text-[11px] text-slate-400">
                          <span className={`px-2 py-0.5 rounded-full font-semibold uppercase tracking-wider text-[10px] ${priorityStyle.bg} ${priorityStyle.text} border ${priorityStyle.border}`}>
                            {task.priority}
                          </span>

                          <div className="flex items-center gap-3">
                            {task.due_date && (
                              <span className="flex items-center gap-1">
                                <Calendar className="w-3 h-3 text-slate-500" />
                                {new Date(task.due_date).toLocaleDateString()}
                              </span>
                            )}
                          </div>
                        </div>

                        {(task.is_recurring || task.reminder_at) && (
                          <div className="mt-2.5 pt-2 border-t border-slate-800/50 flex flex-wrap gap-2 text-[10px] text-slate-400">
                            {task.is_recurring && (
                              <span className="inline-flex items-center gap-1 text-cyan-300">
                                <Zap className="w-3 h-3 text-cyan-400" />
                                <span>Recurring: {task.recurring_pattern}</span>
                              </span>
                            )}
                            {task.reminder_at && (
                              <span className="inline-flex items-center gap-1 text-indigo-300">
                                <Bell className="w-3 h-3 text-indigo-400" />
                                <span>Reminder: {new Date(task.reminder_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
                              </span>
                            )}
                          </div>
                        )}
                      </motion.div>
                    );
                  })}
                </AnimatePresence>
              </div>
            )}
          </div>
        )}
      </main>

      {/* Task Creation & Edit Modal */}
      <AnimatePresence>
        {showModal && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md"
            onClick={() => setShowModal(false)}
          >
            <motion.div
              initial={{ scale: 0.95, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.95, opacity: 0 }}
              onClick={e => e.stopPropagation()}
              className="w-full max-w-lg bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-2xl overflow-y-auto max-h-[90vh]"
            >
              <div className="flex items-center justify-between mb-5">
                <h2 className="text-xl font-bold text-white">
                  {editingTask ? 'Edit Task' : 'Create New Task'}
                </h2>
                <button 
                  onClick={() => setShowModal(false)}
                  className="p-1 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>

              <div className="space-y-4">
                <div>
                  <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
                    Task Title *
                  </label>
                  <input
                    value={title}
                    onChange={e => setTitle(e.target.value)}
                    placeholder="e.g., Deploy production updates"
                    className="w-full px-4 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-sm text-white focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 transition"
                  />
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
                    Description
                  </label>
                  <textarea
                    value={description}
                    onChange={e => setDescription(e.target.value)}
                    placeholder="Details or steps required..."
                    rows={3}
                    className="w-full px-4 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-sm text-white focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 transition resize-none"
                  />
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  <div>
                    <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
                      Priority
                    </label>
                    <div className="grid grid-cols-3 gap-2">
                      {(['low', 'medium', 'high'] as const).map(p => (
                        <button
                          key={p}
                          type="button"
                          onClick={() => setPriority(p)}
                          className={`py-2 rounded-xl text-xs font-semibold capitalize border transition ${
                            priority === p
                              ? 'bg-indigo-600 border-indigo-500 text-white shadow-md'
                              : 'bg-slate-950 border-slate-800 text-slate-400 hover:text-white'
                          }`}
                        >
                          {p}
                        </button>
                      ))}
                    </div>
                  </div>

                  <div>
                    <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
                      Due Date
                    </label>
                    <input
                      type="date"
                      value={dueDate ? dueDate.split('T')[0] : ''}
                      onChange={e => setDueDate(e.target.value)}
                      className="w-full px-4 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white focus:outline-none focus:border-indigo-500 transition [color-scheme:dark]"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
                    Tags (Comma separated)
                  </label>
                  <input
                    value={tags}
                    onChange={e => setTags(e.target.value)}
                    placeholder="work, urgent, frontend"
                    className="w-full px-4 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white focus:outline-none focus:border-indigo-500 transition"
                  />
                </div>

                {/* Recurring Task toggle */}
                <div className="p-3.5 rounded-xl bg-slate-950 border border-slate-800 flex items-center justify-between">
                  <div>
                    <p className="text-xs font-semibold text-slate-200">Recurring Schedule</p>
                    <p className="text-[11px] text-slate-500">Auto-create task when cycle completes</p>
                  </div>
                  <input
                    type="checkbox"
                    checked={isRecurring}
                    onChange={e => setIsRecurring(e.target.checked)}
                    className="w-4 h-4 accent-indigo-600 rounded cursor-pointer"
                  />
                </div>

                {isRecurring && (
                  <div>
                    <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
                      Recurrence Frequency
                    </label>
                    <select
                      value={recurringPattern}
                      onChange={e => setRecurringPattern(e.target.value as any)}
                      className="w-full px-4 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white focus:outline-none focus:border-indigo-500"
                    >
                      <option value="daily">Daily</option>
                      <option value="weekly">Weekly</option>
                      <option value="monthly">Monthly</option>
                    </select>
                  </div>
                )}

                {/* Reminder DateTime Picker */}
                <div>
                  <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
                    Email Reminder Date & Time
                  </label>
                  <input
                    type="datetime-local"
                    value={reminderAt}
                    onChange={e => setReminderAt(e.target.value)}
                    className="w-full px-4 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white focus:outline-none focus:border-indigo-500 transition [color-scheme:dark]"
                  />
                </div>
              </div>

              <div className="flex items-center justify-end gap-3 mt-6 pt-4 border-t border-slate-800">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="px-4 py-2 rounded-xl text-xs font-semibold text-slate-400 hover:text-white bg-slate-800/50 hover:bg-slate-800 transition"
                >
                  Cancel
                </button>
                <button
                  type="button"
                  onClick={saveTask}
                  className="px-5 py-2 rounded-xl text-xs font-semibold text-white bg-gradient-to-r from-indigo-600 to-cyan-500 hover:opacity-95 shadow-lg shadow-indigo-500/25 transition"
                >
                  {editingTask ? 'Save Changes' : 'Create Task'}
                </button>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      <FloatingChatButton user={user} />
    </div>
  );
}
