<template>
  <div class="w-full h-[calc(100vh-5rem)] flex gap-4 animate-fade-in">
    <!-- Left Panel: Tree Visualization -->
    <div class="flex-1 bg-white/80 backdrop-blur-xl rounded-2xl shadow-lg border border-white/20 overflow-hidden flex flex-col relative">
      <div class="p-4 border-b border-gray-100 flex justify-between items-center bg-white/50">
        <h2 class="font-bold text-gray-800 flex items-center gap-2">
          <svg class="w-5 h-5 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.384-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"></path></svg>
          Mapa de Conocimiento
        </h2>
        <div class="flex gap-2">
          <button class="p-1.5 rounded-lg hover:bg-gray-100 text-gray-500" title="Zoom In">+</button>
          <button class="p-1.5 rounded-lg hover:bg-gray-100 text-gray-500" title="Zoom Out">-</button>
        </div>
      </div>
      
      <!-- Placeholder for D3/VueFlow -->
      <div class="flex-1 bg-slate-50 relative overflow-hidden flex items-center justify-center">
        <div class="absolute inset-0 opacity-10" style="background-image: radial-gradient(#cbd5e1 1px, transparent 1px); background-size: 20px 20px;"></div>
        <div class="text-center p-8">
          <div class="w-24 h-24 bg-blue-100 rounded-full mx-auto mb-4 flex items-center justify-center animate-pulse">
            <svg class="w-12 h-12 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
          </div>
          <p class="text-gray-500 font-medium">Visualización del Árbol</p>
          <p class="text-sm text-gray-400 mt-1">(Próximamente: Integración con D3.js/VueFlow)</p>
        </div>
      </div>
    </div>

    <!-- Right Panel: Chat Interface -->
    <div class="w-96 bg-white/90 backdrop-blur-xl rounded-2xl shadow-lg border border-white/20 flex flex-col overflow-hidden">
      <!-- Chat Header -->
      <div class="p-4 border-b border-gray-100 bg-white/50">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-full bg-gradient-to-br from-purple-500 to-indigo-600 flex items-center justify-center text-white font-bold shadow-md">
            AI
          </div>
          <div>
            <h3 class="font-bold text-gray-800">Asistente Virtual</h3>
            <p class="text-xs text-green-500 flex items-center gap-1">
              <span class="w-1.5 h-1.5 rounded-full bg-green-500"></span>
              En línea
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
          <button class="text-xs text-gray-400 hover:text-blue-500 transition-colors underline">
            ¿Necesitas ayuda humana?
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const chatbotId = route.params.id;

const messages = ref([
  { text: '¡Hola! Soy tu asistente virtual. ¿En qué puedo ayudarte sobre este tema?', isUser: false },
]);

const newMessage = ref('');

function sendMessage() {
  if (!newMessage.value.trim()) return;
  
  // Add user message
  messages.value.push({ text: newMessage.value, isUser: true });
  
  const userText = newMessage.value;
  newMessage.value = '';

  // Mock AI response
  setTimeout(() => {
    messages.value.push({ 
      text: `Entiendo que preguntas sobre "${userText}". Como soy una demo, aún no puedo analizar el árbol de conocimiento real, pero pronto podré hacerlo.`, 
      isUser: false 
    });
  }, 1000);
}
</script>
