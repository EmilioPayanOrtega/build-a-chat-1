<template>
  <div class="min-h-screen flex items-center justify-center p-4 animate-fade-in">
    <div class="w-full max-w-md bg-white/80 backdrop-blur-xl rounded-3xl shadow-2xl border border-white/20 p-8 relative overflow-hidden">
      <!-- Decorative Elements -->
      <div class="absolute top-0 right-0 w-32 h-32 bg-gradient-to-br from-blue-400/20 to-purple-400/20 rounded-bl-full -mr-8 -mt-8 pointer-events-none"></div>
      
      <div class="relative z-10">
        <h2 class="text-3xl font-bold text-gray-800 mb-2 text-center">Crear Chatbot</h2>
        <p class="text-gray-500 text-center mb-8">Define los detalles de tu nuevo asistente</p>

        <form @submit.prevent="createChatbot" class="space-y-6">
          <!-- Title Input -->
          <div class="space-y-2">
            <label class="text-sm font-medium text-gray-700 ml-1">Título</label>
            <input 
              v-model="form.title"
              type="text" 
              required
              class="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all bg-white/50"
              placeholder="Ej: Guía de Python"
            >
          </div>

          <!-- Description Input -->
          <div class="space-y-2">
            <label class="text-sm font-medium text-gray-700 ml-1">Descripción</label>
            <textarea 
              v-model="form.description"
              rows="3"
              class="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all bg-white/50 resize-none"
              placeholder="Describe brevemente el propósito de tu chatbot..."
            ></textarea>
          </div>

          <!-- Visibility Select -->
          <div class="space-y-2">
            <label class="text-sm font-medium text-gray-700 ml-1">Visibilidad</label>
            <select 
              v-model="form.visibility"
              class="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all bg-white/50"
            >
              <option value="private">Privado (Solo tú)</option>
              <option value="public">Público (Todos)</option>
              <option value="link_only">Solo con enlace</option>
            </select>
          </div>

          <!-- Error Message -->
          <div v-if="error" class="p-3 rounded-xl bg-red-50 text-red-600 text-sm text-center border border-red-100 animate-shake">
            {{ error }}
          </div>

          <!-- Submit Button -->
          <button 
            type="submit" 
            :disabled="loading"
            class="w-full py-3.5 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-bold shadow-lg hover:shadow-xl hover:scale-[1.02] active:scale-[0.98] transition-all disabled:opacity-70 disabled:cursor-not-allowed flex items-center justify-center gap-2"
          >
            <span v-if="loading" class="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
            <span>{{ loading ? 'Creando...' : 'Crear Chatbot' }}</span>
          </button>

          <div class="text-center">
            <RouterLink to="/dashboard" class="text-sm text-gray-500 hover:text-blue-600 transition-colors">
              Cancelar
            </RouterLink>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const form = ref({
  title: '',
  description: '',
  visibility: 'private',
  tree_json: { label: 'Root', children: [] } // Initialize with a basic root node
});

const loading = ref(false);
const error = ref('');

async function createChatbot() {
  loading.value = true;
  error.value = '';

  try {
    const response = await fetch('/api/chatbots', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(form.value),
    });

    const data = await response.json();

    if (data.success) {
      router.push(`/chatbot/${data.id}`);
    } else {
      error.value = data.error || 'Error al crear el chatbot';
    }
  } catch (e) {
    error.value = 'Error de conexión';
    console.error(e);
  } finally {
    loading.value = false;
  }
}
</script>
