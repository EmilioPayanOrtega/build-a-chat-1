<template>
  <div class="w-full max-w-6xl mx-auto animate-fade-in p-6">
    <h2 class="text-3xl font-bold text-gray-800 mb-8">Solicitudes de Soporte</h2>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 h-[600px]">
      <!-- Sessions List -->
      <div class="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden flex flex-col">
        <div class="p-4 border-b border-gray-100 bg-gray-50">
          <h3 class="font-bold text-gray-700">Chats Activos</h3>
        </div>
        <div class="flex-1 overflow-y-auto p-2 space-y-2">
          <div v-if="sessions.length === 0" class="text-center py-8 text-gray-500 text-sm">
            No hay solicitudes pendientes
          </div>
          <button
            v-for="session in sessions"
            :key="session.id"
            @click="selectSession(session)"
            :class="['w-full text-left p-4 rounded-xl transition-all', selectedSession?.id === session.id ? 'bg-blue-50 border-blue-200 shadow-sm' : 'hover:bg-gray-50 border border-transparent']"
          >
            <div class="font-bold text-gray-800">{{ session.chatbot_title }}</div>
            <div class="text-xs text-gray-500 mt-1">Usuario #{{ session.user_id }}</div>
            <div class="text-xs text-gray-400 mt-1">{{ formatDate(session.created_at) }}</div>
          </button>
        </div>
      </div>

      <!-- Chat Area -->
      <div class="lg:col-span-2 bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden flex flex-col">
        <div v-if="!selectedSession" class="flex-1 flex items-center justify-center text-gray-400 flex-col gap-4">
          <svg class="w-16 h-16 opacity-20" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path></svg>
          <p>Selecciona un chat para comenzar</p>
        </div>
        
        <template v-else>
          <!-- Header -->
          <div class="p-4 border-b border-gray-100 flex justify-between items-center bg-gray-50">
            <div>
              <h3 class="font-bold text-gray-800">{{ selectedSession.chatbot_title }}</h3>
              <p class="text-xs text-green-600 flex items-center gap-1">
                <span class="w-1.5 h-1.5 rounded-full bg-green-500"></span>
                Conectado con Usuario #{{ selectedSession.user_id }}
              </p>
            </div>
          </div>

          <!-- Messages -->
          <div class="flex-1 overflow-y-auto p-4 space-y-4 bg-slate-50" ref="messagesContainer">
            <div v-for="(msg, index) in messages" :key="index" :class="['flex', msg.isMe ? 'justify-end' : 'justify-start']">
              <div :class="['max-w-[80%] p-3 rounded-2xl text-sm shadow-sm', msg.isMe ? 'bg-blue-600 text-white rounded-br-none' : 'bg-white text-gray-700 rounded-bl-none border border-gray-100']">
                {{ msg.text }}
              </div>
            </div>
          </div>

          <!-- Input -->
          <div class="p-4 bg-white border-t border-gray-100">
            <form @submit.prevent="sendMessage" class="flex gap-2">
              <input 
                v-model="newMessage" 
                type="text" 
                placeholder="Escribe una respuesta..." 
                class="flex-1 px-4 py-2 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 outline-none bg-gray-50"
              >
              <button type="submit" class="p-2 rounded-xl bg-blue-600 text-white hover:bg-blue-700 transition-colors shadow-md" :disabled="!newMessage.trim()">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path></svg>
              </button>
            </form>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick } from 'vue';
import { io, Socket } from 'socket.io-client';
import { useAuth } from '../store/auth';

interface Session {
  id: number;
  chatbot_title: string;
  user_id: number;
  created_at: string;
}

interface Message {
  text: string;
  isMe: boolean;
}

const sessions = ref<Session[]>([]);
const selectedSession = ref<Session | null>(null);
const messages = ref<Message[]>([]);
const newMessage = ref('');
const { state: authState } = useAuth();
let socket: Socket | null = null;
const messagesContainer = ref<HTMLElement | null>(null);

async function fetchSessions() {
  try {
    const response = await fetch('/api/creator/sessions');
    const data = await response.json();
    if (data.success) {
      sessions.value = data.sessions;
    }
  } catch (e) {
    console.error('Error fetching sessions', e);
  }
}

function selectSession(session: Session) {
  if (selectedSession.value?.id === session.id) return;
  
  // Leave previous room if any
  if (socket) {
    socket.disconnect();
  }

  selectedSession.value = session;
  messages.value = []; // Clear messages
  
  // Connect to new room
  initSocket(session.id);
}

function initSocket(sessionId: number) {
  socket = io({
    path: '/socket.io',
    transports: ['websocket', 'polling']
  });

  socket.on('connect', () => {
    console.log('Creator connected to socket');
    socket?.emit('join', { 
      session_id: sessionId, 
      user_id: authState.userId 
    });
  });

  socket.on('message', (data: { user_id: number, content: string }) => {
    const isMe = String(data.user_id) === String(authState.userId);
    if (!isMe) {
      messages.value.push({ text: data.content, isMe });
      scrollToBottom();
    }
  });
  
  socket.on('status', (data: { msg: string }) => {
     messages.value.push({ text: `[SISTEMA]: ${data.msg}`, isMe: false });
     scrollToBottom();
  });
}

function sendMessage() {
  if (!newMessage.value.trim() || !selectedSession.value) return;
  
  const content = newMessage.value;
  newMessage.value = '';
  
  // Optimistic update
  messages.value.push({ text: content, isMe: true });
  scrollToBottom();

  socket?.emit('message', {
    session_id: selectedSession.value.id,
    user_id: authState.userId,
    content: content
  });
}

function scrollToBottom() {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
    }
  });
}

function formatDate(dateStr: string) {
  return new Date(dateStr).toLocaleString();
}

onMounted(() => {
  fetchSessions();
  // Poll for new sessions every 30s
  const interval = setInterval(fetchSessions, 30000);
  onUnmounted(() => clearInterval(interval));
});

onUnmounted(() => {
  if (socket) socket.disconnect();
});
</script>
