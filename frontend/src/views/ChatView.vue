<template>
  <div class="chat-container">
    <header class="chat-header">
      <h2>Chat con Cientibot</h2>
      <button @click="handleLogout" class="logout-btn">Cerrar sesión</button>
    </header>
    
    <div class="chat-messages" ref="messagesContainer">
      <div
        v-for="(msg, index) in messages"
        :key="index"
        :class="['message', msg.sender === username ? 'message-sent' : 'message-received']"
      >
        <div class="message-sender">{{ msg.sender }}</div>
        <div class="message-text" v-html="formatMessage(msg.text)"></div>
        <div class="message-time">{{ formatTime(msg.timestamp) }}</div>
      </div>
      
      <div v-if="showMenu && menuOptions.length > 0" class="menu-container">
        <div class="menu-title">Menú:</div>
        <button
          v-for="option in menuOptions"
          :key="option.id"
          @click="selectMenuOption(option.id)"
          class="menu-button"
        >
          {{ option.label }}
        </button>
        <button @click="showMenu = false" class="menu-button close-menu">Cerrar menú</button>
      </div>
    </div>

    <div class="chat-input-container">
      <input
        v-model="messageInput"
        @keyup.enter="sendMessage"
        class="chat-input"
        placeholder="Escribe tu mensaje aquí... (Escribe 'Menu' para ver el menú)"
        :disabled="loading"
      />
      <button @click="sendMessage" class="send-button" :disabled="loading || !messageInput.trim()">
        Enviar
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick } from 'vue';
import { useRouter } from 'vue-router';
import { getSocket, disconnectSocket } from '../services/socket';

interface Message {
  text: string;
  timestamp: string;
  sender: string;
}

interface MenuOption {
  id: string;
  label: string;
}

const router = useRouter();
const socket = getSocket();
const username = ref(localStorage.getItem('username') || 'Usuario');
const messages = ref<Message[]>([]);
const messageInput = ref('');
const loading = ref(false);
const showMenu = ref(false);
const menuOptions = ref<MenuOption[]>([]);
const messagesContainer = ref<HTMLElement | null>(null);

function formatTime(timestamp: string): string {
  if (!timestamp) return '';
  const date = new Date(timestamp);
  return date.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' });
}

function formatMessage(text: string): string {
  // Convert URLs to clickable links
  const urlRegex = /(https?:\/\/[^\s]+)/g;
  return text.replace(urlRegex, '<a href="$1" target="_blank" rel="noopener noreferrer">$1</a>');
}

function scrollToBottom() {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
    }
  });
}

function sendMessage() {
  if (!messageInput.value.trim() || loading.value) return;
  
  const timestamp = new Date().toISOString();
  const message: Message = {
    text: messageInput.value,
    timestamp,
    sender: username.value
  };
  
  socket.emit('message', {
    text: messageInput.value,
    timestamp
  });
  
  messageInput.value = '';
}

function selectMenuOption(optionId: string) {
  socket.emit('menu_option_selected', { id: optionId });
  showMenu.value = false;
}

function handleLogout() {
  disconnectSocket();
  localStorage.removeItem('user_id');
  localStorage.removeItem('username');
  router.push('/login');
}

onMounted(() => {
  // Register user name
  socket.emit('register_name', {
    name: username.value,
    timestamp: new Date().toISOString()
  });

  // Join chat
  socket.emit('join');

  // Socket event listeners
  socket.on('connected', (data) => {
    console.log('Connected:', data);
  });

  socket.on('message', (msg: Message) => {
    messages.value.push(msg);
    scrollToBottom();
  });

  socket.on('chat_history', (history: Message[]) => {
    messages.value = history;
    scrollToBottom();
  });

  socket.on('show_menu', (data: { menu?: MenuOption[] }) => {
    if (data.menu) {
      menuOptions.value = data.menu;
      showMenu.value = true;
    }
  });

  socket.on('show_submenu', (data: { submenu: MenuOption[] }) => {
    menuOptions.value = data.submenu;
    showMenu.value = true;
  });

  socket.on('show_info', (data: { label: string; text: string }) => {
    const infoMessage: Message = {
      text: `${data.label}: ${data.text}`,
      timestamp: new Date().toISOString(),
      sender: 'Cientibot'
    };
    messages.value.push(infoMessage);
    scrollToBottom();
  });

  socket.on('show_link', (data: { label: string; link: string }) => {
    const linkMessage: Message = {
      text: `${data.label}: ${data.link}`,
      timestamp: new Date().toISOString(),
      sender: 'Cientibot'
    };
    messages.value.push(linkMessage);
    scrollToBottom();
  });

  socket.on('show_map', (data: { image: string; label: string }) => {
    const mapMessage: Message = {
      text: `${data.label}: [Imagen: ${data.image}]`,
      timestamp: new Date().toISOString(),
      sender: 'Cientibot'
    };
    messages.value.push(mapMessage);
    scrollToBottom();
  });
});

onUnmounted(() => {
  socket.off('connected');
  socket.off('message');
  socket.off('chat_history');
  socket.off('show_menu');
  socket.off('show_submenu');
  socket.off('show_info');
  socket.off('show_link');
  socket.off('show_map');
});
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  max-width: 800px;
  margin: 0 auto;
  background: #fff;
}

.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid #e5e7eb;
  background: #f9fafb;
}

.chat-header h2 {
  margin: 0;
  font-size: 1.25rem;
}

.logout-btn {
  padding: 0.5rem 1rem;
  background: #ef4444;
  color: white;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
  font-size: 0.875rem;
}

.logout-btn:hover {
  background: #dc2626;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.message {
  display: flex;
  flex-direction: column;
  max-width: 70%;
  padding: 0.75rem;
  border-radius: 0.5rem;
}

.message-sent {
  align-self: flex-end;
  background: #3b82f6;
  color: white;
}

.message-received {
  align-self: flex-start;
  background: #f3f4f6;
  color: #111827;
}

.message-sender {
  font-weight: 600;
  font-size: 0.875rem;
  margin-bottom: 0.25rem;
}

.message-text {
  word-wrap: break-word;
}

.message-text a {
  color: #3b82f6;
  text-decoration: underline;
}

.message-sent .message-text a {
  color: #bfdbfe;
}

.message-time {
  font-size: 0.75rem;
  opacity: 0.7;
  margin-top: 0.25rem;
}

.menu-container {
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  padding: 1rem;
  margin-top: 0.5rem;
}

.menu-title {
  font-weight: 600;
  margin-bottom: 0.75rem;
}

.menu-button {
  display: block;
  width: 100%;
  padding: 0.75rem;
  margin-bottom: 0.5rem;
  background: white;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  cursor: pointer;
  text-align: left;
  transition: background 0.2s;
}

.menu-button:hover {
  background: #f3f4f6;
}

.menu-button:last-child {
  margin-bottom: 0;
}

.menu-button.close-menu {
  background: #ef4444;
  color: white;
  border-color: #ef4444;
}

.menu-button.close-menu:hover {
  background: #dc2626;
}

.chat-input-container {
  display: flex;
  gap: 0.5rem;
  padding: 1rem;
  border-top: 1px solid #e5e7eb;
  background: #f9fafb;
}

.chat-input {
  flex: 1;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  font-size: 1rem;
}

.chat-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.send-button {
  padding: 0.75rem 1.5rem;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
}

.send-button:hover:not(:disabled) {
  background: #2563eb;
}

.send-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>

