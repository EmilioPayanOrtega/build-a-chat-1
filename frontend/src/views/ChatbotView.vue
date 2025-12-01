<template>
  <div class="w-full h-[calc(100vh-5rem)] flex animate-fade-in" @mousemove="resize" @mouseup="stopResize" @mouseleave="stopResize">
    <!-- Left Panel: Tree Visualization -->
    <div class="flex-1 bg-white/80 backdrop-blur-xl rounded-2xl shadow-lg border border-white/20 overflow-hidden flex flex-col relative">
      <div class="p-4 border-b border-gray-100 flex justify-between items-center bg-white/50">
        <h2 class="font-bold text-gray-800 flex items-center gap-2">
          <svg class="w-5 h-5 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.384-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"></path></svg>
          Mapa de Conocimiento
        </h2>
        <div class="flex gap-2">
          <!-- Controls are now inside TreeVisualization -->
        </div>
      </div>
      
      <!-- Tree Visualization -->
      <div class="flex-1 bg-slate-50 relative overflow-hidden">
        <div v-if="loading" class="absolute inset-0 flex items-center justify-center">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
        </div>
        <div v-else-if="error" class="absolute inset-0 flex items-center justify-center text-red-500 p-4 text-center">
          {{ error }}
        </div>
        <TreeVisualization v-else :data="treeData" />
      </div>
    </div>

    <!-- Resizer Handle -->
    <div 
      class="w-4 cursor-col-resize flex items-center justify-center hover:bg-blue-50 transition-colors group select-none"
      @mousedown="startResize"
    >
      <div class="w-1 h-8 bg-gray-200 rounded-full group-hover:bg-blue-400 transition-colors"></div>
    </div>

    <!-- Right Panel: Chat Interface -->
    <div 
      class="bg-white/90 backdrop-blur-xl rounded-2xl shadow-lg border border-white/20 flex flex-col overflow-hidden shrink-0"
      :style="{ width: chatWidth + 'px' }"
    >
      <!-- Chat Header -->
      <div class="p-4 border-b border-gray-100 bg-white/50 transition-colors duration-300" :class="{'bg-amber-50': isHumanSupport}">
        <div class="flex items-center gap-3">
          <div 
            class="w-10 h-10 rounded-full flex items-center justify-center text-white font-bold shadow-md transition-colors duration-300"
            :class="isHumanSupport ? 'bg-gradient-to-br from-amber-500 to-orange-600' : 'bg-gradient-to-br from-purple-500 to-indigo-600'"
          >
            {{ isHumanSupport ? 'HS' : 'AI' }}
          </div>
          <div>
            <h3 class="font-bold text-gray-800">{{ isHumanSupport ? 'Soporte Humano' : (chatbotTitle || 'Asistente Virtual') }}</h3>
            <p class="text-xs flex items-center gap-1" :class="isHumanSupport ? 'text-amber-600' : 'text-green-500'">
              <span class="w-1.5 h-1.5 rounded-full" :class="isHumanSupport ? 'bg-amber-500' : 'bg-green-500'"></span>
              {{ isHumanSupport ? 'Esperando agente...' : 'En línea' }}
            </p>
          </div>
        </div>
      </div>

      <!-- Messages Area -->
      <div class="flex-1 overflow-y-auto p-4 space-y-4 bg-slate-50/50">
        <div v-for="(msg, index) in messages" :key="index" :class="['flex', msg.isUser ? 'justify-end' : 'justify-start']">
          <div :class="['max-w-[85%] p-3 rounded-2xl text-sm shadow-sm', msg.isUser ? 'bg-blue-600 text-white rounded-br-none' : 'bg-white text-gray-700 rounded-bl-none border border-gray-100']">
            {{ msg.text }}
          </div>
        </div>
      </div>

      <!-- Input Area -->
      <div class="p-4 bg-white border-t border-gray-100">
        <form @submit.prevent="sendMessage" class="flex gap-2">
          <input 
            v-model="newMessage" 
            type="text" 
            placeholder="Escribe tu pregunta..." 
            class="flex-1 px-4 py-2 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all bg-gray-50"
          >
          <button type="submit" class="p-2 rounded-xl bg-blue-600 text-white hover:bg-blue-700 transition-colors shadow-md disabled:opacity-50 disabled:cursor-not-allowed" :disabled="!newMessage.trim()">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path></svg>
          </button>
        </form>
        <div class="mt-2 text-center">
          <button 
            @click="requestHumanSupport"
            class="text-xs transition-colors underline"
            :class="isHumanSupport ? 'text-red-500 hover:text-red-700' : 'text-gray-400 hover:text-blue-500'"
          >
            {{ isHumanSupport ? 'Cancelar ayuda humana' : '¿Necesitas ayuda humana?' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick } from 'vue';
import { useRoute } from 'vue-router';
import TreeVisualization from '../components/TreeVisualization.vue';
import { io, Socket } from 'socket.io-client';
import { useAuth } from '../store/auth';

const route = useRoute();
const chatbotId = route.params.id;
const { state: authState } = useAuth();

interface Message {
  text: string;
  isUser: boolean;
}

const messages = ref<Message[]>([
  { text: '¡Hola! Soy tu asistente virtual. ¿En qué puedo ayudarte sobre este tema?', isUser: false },
]);

const newMessage = ref('');
const treeData = ref<any>(null);
const chatbotTitle = ref('');
const loading = ref(true);
const error = ref('');
const isHumanSupport = ref(false);
const sessionId = ref<number | null>(null);

let socket: Socket | null = null;

// Resizing Logic
const chatWidth = ref(400);
const isResizing = ref(false);

function startResize() {
  isResizing.value = true;
}

function resize(e: MouseEvent) {
  if (!isResizing.value) return;
  
  // Calculate new width from right edge
  const newWidth = window.innerWidth - e.clientX - 32; // 32px for padding/margins
  
  // Constraints
  if (newWidth > 300 && newWidth < 800) {
    chatWidth.value = newWidth;
  }
}

function stopResize() {
  isResizing.value = false;
}

// Initialize socket connection
function initSocket(sessId: number) {
  // Use relative path for socket.io to go through proxy
  socket = io({
    path: '/socket.io',
    transports: ['websocket', 'polling']
  });

  socket.on('connect', () => {
    console.log('Socket connected');
    socket?.emit('join', { 
      session_id: sessId, 
      user_id: authState.userId 
    });
  });

  socket.on('message', (data: { user_id: number, content: string }) => {
    // Only add if it's not from current user (to avoid duplication as we add optimistically)
    if (String(data.user_id) !== String(authState.userId)) {
      messages.value.push({ text: data.content, isUser: false });
      scrollToBottom();
    }
  });

  socket.on('status', (data: { msg: string }) => {
    messages.value.push({ text: `[SISTEMA]: ${data.msg}`, isUser: false });
    scrollToBottom();
  });

  socket.on('session_updated', (data: { type: string }) => {
    console.log('Session updated event received:', data);
    if (data.type === 'human_support') {
      isHumanSupport.value = true;
    } else if (data.type === 'ai_conversation') {
      isHumanSupport.value = false;
    }
  });

  socket.on('error', (data: { msg: string }) => {
    console.error('Socket error:', data.msg);
  });
}

async function createSession() {
  try {
    const response = await fetch('/api/chat-sessions', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ chatbot_id: chatbotId })
    });
    const data = await response.json();
    if (data.success) {
      sessionId.value = data.session_id;
      if (data.type === 'human_support') {
        isHumanSupport.value = true;
      }
      initSocket(data.session_id);
      await fetchHistory(data.session_id);
    }
  } catch (e) {
    console.error('Failed to create session', e);
  }
}

async function fetchHistory(sessId: number) {
  try {
    const response = await fetch(`/api/chat-sessions/${sessId}/messages`);
    const data = await response.json();
    if (data.success) {
      messages.value = [
        { text: '¡Hola! Soy tu asistente virtual. ¿En qué puedo ayudarte sobre este tema?', isUser: false },
        ...data.messages.map((m: any) => ({
          text: m.content,
          isUser: m.sender_type === 'user'
        }))
      ];
      scrollToBottom();
    }
  } catch (e) {
    console.error('Failed to fetch history', e);
  }
}

async function fetchChatbotData() {
  try {
    loading.value = true;
    const response = await fetch(`/api/chatbots/${chatbotId}`);
    const data = await response.json();
    
    if (data.success) {
      treeData.value = data.tree;
      chatbotTitle.value = data.chatbot.title;
    } else {
      error.value = data.error || 'Error al cargar los datos del chatbot';
    }
  } catch (e) {
    error.value = 'Error al conectar con el servidor';
    console.error(e);
  } finally {
    loading.value = false;
  }
}

async function sendMessage() {
  if (!newMessage.value.trim() || !sessionId.value) return;
  
  const content = newMessage.value;
  newMessage.value = '';
  
  // Optimistic update
  messages.value.push({ text: content, isUser: true });
  scrollToBottom();

  if (isHumanSupport.value) {
    // Send via socket for human chat
    socket?.emit('message', {
      session_id: sessionId.value,
      user_id: authState.userId,
      content: content
    });
  } else {
    // AI Chat flow
    // 1. Save user message via socket (or API, but socket is easier if connected)
    socket?.emit('message', {
      session_id: sessionId.value,
      user_id: authState.userId,
      content: content
    });

    // 2. Request AI response
    try {
      const response = await fetch(`/api/chat-sessions/${sessionId.value}/ask`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({
          current_node_id: treeData.value?.id || 1, 
          query: content
        })
      });
      const data = await response.json();
      if (!data.success) {
        console.error('AI Error:', data.error);
        messages.value.push({ text: '[Error de AI]: ' + data.error, isUser: false });
      }
      // AI response will be received via socket
    } catch (e) {
      console.error('AI Error', e);
    }
  }
}

function requestHumanSupport() {
  if (!sessionId.value) return;

  if (isHumanSupport.value) {
    // Cancel request
    socket?.emit('cancel_human', {
      session_id: sessionId.value,
      user_id: authState.userId
    });
  } else {
    // Request support
    socket?.emit('request_human', {
      session_id: sessionId.value,
      user_id: authState.userId
    });
  }
}

function scrollToBottom() {
  nextTick(() => {
    const container = document.querySelector('.overflow-y-auto');
    if (container) container.scrollTop = container.scrollHeight;
  });
}

onMounted(async () => {
  await fetchChatbotData();
  await createSession();
});

onUnmounted(() => {
  if (socket) socket.disconnect();
});
</script>
