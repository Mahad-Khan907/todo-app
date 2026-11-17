"use client";

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Bot, X } from 'lucide-react';
import ChatInterface from './chat/ChatInterface';
import { useQueryClient } from '@tanstack/react-query';

interface FloatingChatButtonProps {
  user?: any; 
}

export default function FloatingChatButton({ user }: FloatingChatButtonProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [hasMounted, setHasMounted] = useState(false);
  const queryClient = useQueryClient();

  useEffect(() => {
    setHasMounted(true);
  }, []);

  if (!hasMounted || !user) {
    return null;
  }

  return (
    <>
      {!isOpen && (
        <motion.button
          onClick={() => setIsOpen(true)}
          className="fixed bottom-6 right-6 z-50 bg-gradient-to-r from-indigo-600 via-indigo-500 to-cyan-500 hover:opacity-95 text-white rounded-full p-3.5 shadow-xl shadow-indigo-500/30 flex items-center gap-2 group ring-1 ring-white/20"
          aria-label="Open AI Copilot"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
        >
          <Bot className="h-5 w-5" />
          <span className="hidden sm:inline-block text-xs font-semibold pr-1">Ask Copilot</span>
        </motion.button>
      )}

      <AnimatePresence>
        {isOpen && (
          <motion.div
            className="fixed bottom-6 inset-x-4 sm:inset-x-auto sm:right-6 z-50 w-auto sm:w-[480px] h-[580px] max-h-[85vh] bg-slate-900 border border-slate-800 rounded-2xl shadow-2xl shadow-black/70 overflow-hidden flex flex-col ring-1 ring-white/10"
            initial={{ opacity: 0, y: 30, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 30, scale: 0.95 }}
            transition={{ duration: 0.2 }}
          >
            <ChatInterface 
              onClose={() => setIsOpen(false)}
              onTaskChange={() => {
                queryClient.invalidateQueries({ queryKey: ['tasks'] });
              }} 
            />
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}
