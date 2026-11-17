"use client";
import { useState, useRef, useEffect, useCallback } from "react";
import { useAuth } from "@/contexts/AuthContext";
import { useConversation } from "@/contexts/ConversationContext";
import { ScrollArea } from "@/components/ui/scroll-area";
import { 
  Send, 
  Bot, 
  User, 
  Plus, 
  History, 
  Sparkles, 
  Loader2, 
  X, 
  Trash2, 
  ChevronLeft
} from "lucide-react";
import api from "@/lib/api";
import { cn } from "@/lib/utils";

export default function ChatInterface({ onTaskChange, onClose }: { onTaskChange?: () => void, onClose?: () => void }) {
  const [inputValue, setInputValue] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isMessagesLoading, setIsMessagesLoading] = useState(false);
  const [showHistory, setShowHistory] = useState(false);
  const { user } = useAuth();

  const {
    messages, setMessages,
    selectedConversation, setSelectedConversation,
    conversations, setConversations,
    resetToNewChat
  } = useConversation() as any;

  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      const scrollContainer = scrollRef.current.querySelector('[data-radix-scroll-area-viewport]');
      if (scrollContainer) {
        scrollContainer.scrollTo({
          top: scrollContainer.scrollHeight,
          behavior: "smooth"
        });
      }
    }
  }, [messages, isLoading]);

  const fetchMessages = useCallback(async (id: number) => {
    setIsMessagesLoading(true);
    try {
      const res = await api.get(`/chat/conversations/${id}`);
      setMessages(res.data.messages.map((m: any) => ({
        id: m.id, role: m.role, content: m.content
      })));
    } catch (e) {
      console.error("Failed to load chat history");
      resetToNewChat();
    } finally {
      setIsMessagesLoading(false);
    }
  }, [setMessages, resetToNewChat]);

  const loadHistory = useCallback(async (shouldFetchMessages = false) => {
    if (!user) return;
    try {
      const res = await api.get("/chat/conversations");
      const history = res.data || [];
      setConversations(history);

      if (selectedConversation) {
        const exists = history.some((c: any) => c.id === selectedConversation);
        if (exists && shouldFetchMessages) {
          fetchMessages(selectedConversation);
        } else if (!exists) {
          resetToNewChat();
        }
      }
    } catch (e) {
      setConversations([]);
      console.error("History fetch failed");
    }
  }, [user, setConversations, selectedConversation, fetchMessages, resetToNewChat]);

  useEffect(() => {
    loadHistory(true);
  }, []);

  const handleSelectChat = async (id: number) => {
    if (selectedConversation === id) {
      setShowHistory(false);
      return;
    }
    setSelectedConversation(id);
    setMessages([]);
    setShowHistory(false); // Close history drawer once a chat is selected
    await fetchMessages(id);
  };

  const handleSend = async () => {
    if (!inputValue.trim() || isLoading) return;
    const msg = inputValue;
    const tempId = Date.now();
    setMessages((prev: any[]) => [...prev, { id: tempId, role: 'user', content: msg }]);
    setInputValue("");
    setIsLoading(true);

    try {
      const res = await api.post("/chat/", {
        message: msg,
        conversation_id: selectedConversation
      });

      setMessages((prev: any[]) => [...prev, {
        id: res.data.assistant_message_id,
        role: 'assistant',
        content: res.data.message
      }]);

      if (!selectedConversation) {
        setSelectedConversation(res.data.conversation_id);
        loadHistory(false);
      }
      if (onTaskChange) onTaskChange();
    } catch (error) {
      console.error("Chat Error:", error);
      setMessages((prev: any[]) => [...prev, {
        id: Date.now(),
        role: 'assistant',
        content: "Sorry, I encountered an issue processing your request. Please try again."
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDeleteChat = async (e: React.MouseEvent, id: number, title: string) => {
    e.stopPropagation();
    if (window.confirm(`Delete thread "${title || 'Untitled'}"?`)) {
      try {
        await api.delete(`/chat/conversations/${id}`);
        setConversations((prev: any[]) => prev.filter(c => c.id !== id));
        if (selectedConversation === id) resetToNewChat();
      } catch (error) {
        console.error("Failed to delete conversation:", error);
      }
    }
  };

  return (
    <div className="relative flex h-full w-full bg-slate-950 text-slate-100 font-sans overflow-hidden">
      {/* Sliding Conversations Drawer */}
      <div 
        className={cn(
          "absolute inset-y-0 left-0 z-30 w-72 bg-slate-900 border-r border-slate-800 shadow-2xl flex flex-col transition-transform duration-300 ease-in-out",
          showHistory ? "translate-x-0" : "-translate-x-full"
        )}
      >
        <div className="p-3.5 border-b border-slate-800 flex items-center justify-between">
          <button
            onClick={() => {
              resetToNewChat();
              setShowHistory(false);
            }}
            className="flex-1 inline-flex items-center justify-center gap-2 py-2 px-3 text-xs font-semibold rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white transition shadow-sm"
          >
            <Plus className="w-3.5 h-3.5" />
            <span>New Chat</span>
          </button>
          <button
            onClick={() => setShowHistory(false)}
            className="ml-2 p-1.5 text-slate-400 hover:text-white rounded-lg hover:bg-slate-800 transition"
            title="Close Drawer"
          >
            <ChevronLeft className="w-4 h-4" />
          </button>
        </div>

        <ScrollArea className="flex-1 px-2 py-3">
          <div className="flex items-center gap-2 px-3 mb-2 text-slate-500">
            <History className="w-3 h-3" />
            <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400">Chat History</span>
          </div>

          <div className="space-y-1">
            {conversations.length === 0 ? (
              <p className="text-xs text-slate-500 px-3 py-4 italic">No conversation history</p>
            ) : (
              conversations.map((c: { id: number; title: string }) => (
                <div
                  key={c.id}
                  onClick={() => handleSelectChat(c.id)}
                  className={cn(
                    "group relative w-full flex items-center justify-between px-3 py-2 rounded-xl text-xs cursor-pointer transition",
                    selectedConversation === c.id
                      ? "bg-indigo-600/20 text-indigo-300 border border-indigo-500/30 font-medium"
                      : "text-slate-400 hover:bg-slate-800 hover:text-white"
                  )}
                >
                  <span className="truncate flex-1 pr-2">{c.title || "Task Conversation"}</span>
                  <button
                    onClick={(e) => handleDeleteChat(e, c.id, c.title)}
                    className="opacity-0 group-hover:opacity-100 text-slate-500 hover:text-rose-400 transition-opacity p-1"
                  >
                    <Trash2 className="w-3 h-3" />
                  </button>
                </div>
              ))
            )}
          </div>
        </ScrollArea>
      </div>

      {/* Main Chat Interface */}
      <div className="flex-1 flex flex-col h-full bg-slate-950">
        {/* Header with History Toggle Button */}
        <div className="h-14 border-b border-slate-800 px-4 flex items-center justify-between bg-slate-900/40">
          <div className="flex items-center gap-2.5">
            <button
              onClick={() => setShowHistory(!showHistory)}
              className={cn(
                "p-1.5 rounded-lg border transition text-xs font-semibold flex items-center gap-1.5",
                showHistory 
                  ? "bg-indigo-600 border-indigo-500 text-white" 
                  : "bg-slate-800/80 hover:bg-slate-800 border-slate-700 text-slate-300 hover:text-white"
              )}
              title="Toggle Chat History"
            >
              <History className="w-3.5 h-3.5" />
              <span className="text-[11px]">History</span>
            </button>

            <div className="w-7 h-7 rounded-lg bg-gradient-to-tr from-indigo-600 to-cyan-400 flex items-center justify-center">
              <Bot className="w-4 h-4 text-white" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-xs font-bold text-white">TaskFlow Copilot</span>
                <span className="text-[10px] px-1.5 py-0.2 rounded-full bg-indigo-500/15 text-indigo-300 border border-indigo-500/30">
                  Particle AI
                </span>
              </div>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={() => resetToNewChat()}
              className="p-1.5 text-xs text-slate-400 hover:text-white rounded-lg hover:bg-slate-800 transition flex items-center gap-1"
              title="Start New Chat"
            >
              <Plus className="w-3.5 h-3.5" />
              <span className="hidden sm:inline text-[11px]">New</span>
            </button>
            {onClose && (
              <button 
                onClick={onClose}
                className="p-1 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition"
              >
                <X className="w-4 h-4" />
              </button>
            )}
          </div>
        </div>

        {/* Message Stream */}
        <ScrollArea ref={scrollRef} className="flex-1 p-4">
          <div className="max-w-3xl mx-auto space-y-4">
            {messages.length === 0 ? (
              <div className="text-center py-16">
                <div className="w-12 h-12 rounded-2xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center mx-auto mb-3">
                  <Sparkles className="w-6 h-6 text-indigo-400" />
                </div>
                <h4 className="text-sm font-semibold text-white">How can I assist your tasks today?</h4>
                <p className="text-xs text-slate-400 mt-1 max-w-sm mx-auto">
                  Ask me to &ldquo;Add task prepare report for tomorrow&rdquo;, &ldquo;List pending tasks&rdquo;, or &ldquo;Mark task as completed&rdquo;.
                </p>
              </div>
            ) : (
              messages.map((m: any, idx: number) => {
                const isUser = m.role === 'user';
                return (
                  <div
                    key={m.id || idx}
                    className={cn(
                      "flex gap-3",
                      isUser ? "justify-end" : "justify-start"
                    )}
                  >
                    {!isUser && (
                      <div className="w-7 h-7 rounded-lg bg-indigo-600/30 border border-indigo-500/30 flex items-center justify-center shrink-0 mt-0.5">
                        <Bot className="w-4 h-4 text-indigo-400" />
                      </div>
                    )}
                    <div
                      className={cn(
                        "rounded-2xl px-4 py-2.5 text-xs max-w-[80%] leading-relaxed whitespace-pre-wrap",
                        isUser
                          ? "bg-indigo-600 text-white rounded-tr-none shadow-md"
                          : "bg-slate-900 border border-slate-800 text-slate-200 rounded-tl-none"
                      )}
                    >
                      {m.content}
                    </div>
                    {isUser && (
                      <div className="w-7 h-7 rounded-lg bg-slate-800 flex items-center justify-center shrink-0 mt-0.5">
                        <User className="w-4 h-4 text-slate-400" />
                      </div>
                    )}
                  </div>
                );
              })
            )}

            {isLoading && (
              <div className="flex gap-3 items-center text-xs text-slate-400">
                <div className="w-7 h-7 rounded-lg bg-indigo-600/30 border border-indigo-500/30 flex items-center justify-center">
                  <Bot className="w-4 h-4 text-indigo-400" />
                </div>
                <div className="flex items-center gap-2 bg-slate-900 border border-slate-800 px-3 py-2 rounded-xl">
                  <Loader2 className="w-3.5 h-3.5 animate-spin text-indigo-400" />
                  <span>AI Copilot is processing...</span>
                </div>
              </div>
            )}
          </div>
        </ScrollArea>

        {/* Input Bar */}
        <div className="p-3 border-t border-slate-800 bg-slate-900/40">
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleSend();
            }}
            className="max-w-3xl mx-auto flex items-center gap-2"
          >
            <input
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder="Type instruction (e.g., 'Add task review PR today')..."
              className="flex-1 bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 transition"
              disabled={isLoading}
            />
            <button
              type="submit"
              disabled={isLoading || !inputValue.trim()}
              className="p-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white disabled:opacity-40 transition shadow-sm"
            >
              <Send className="w-4 h-4" />
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
