<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm" @click.self="close">
    <div class="bg-white rounded-2xl shadow-xl w-full max-w-md overflow-hidden animate-fade-in-up">
      <div class="p-6">
        <div class="flex justify-between items-center mb-6">
          <h2 class="text-2xl font-bold text-slate-800">Contáctanos</h2>
          <button @click="close" class="text-slate-400 hover:text-slate-600 transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <form @submit.prevent="submitForm" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-1">Nombre</label>
            <input 
              v-model="form.name" 
              type="text" 
              required
              class="w-full px-4 py-2 rounded-lg border border-slate-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all outline-none"
              placeholder="Tu nombre"
            >
          </div>

          <div>
            <label class="block text-sm font-medium text-slate-700 mb-1">Email</label>
            <input 
              v-model="form.email" 
              type="email" 
              required
              class="w-full px-4 py-2 rounded-lg border border-slate-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all outline-none"
              placeholder="tu@email.com"
            >
          </div>

          <div>
            <label class="block text-sm font-medium text-slate-700 mb-1">Asunto</label>
            <input 
              v-model="form.subject" 
              type="text" 
              required
              class="w-full px-4 py-2 rounded-lg border border-slate-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all outline-none"
              placeholder="¿En qué podemos ayudarte?"
            >
          </div>

          <div>
            <label class="block text-sm font-medium text-slate-700 mb-1">Mensaje</label>
            <textarea 
              v-model="form.message" 
              required
              rows="4"
              class="w-full px-4 py-2 rounded-lg border border-slate-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all outline-none resize-none"
              placeholder="Escribe tu mensaje aquí..."
            ></textarea>
          </div>

          <div v-if="status.message" :class="{'text-green-600': status.success, 'text-red-600': !status.success}" class="text-sm text-center font-medium">
            {{ status.message }}
          </div>

          <button 
            type="submit" 
            :disabled="loading"
            class="w-full py-3 px-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white font-bold rounded-lg shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="loading">Enviando...</span>
            <span v-else>Enviar Mensaje</span>
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';

const props = defineProps<{
  isOpen: boolean
}>();

const emit = defineEmits(['close']);

const loading = ref(false);
const status = reactive({
  success: false,
  message: ''
});

const form = reactive({
  name: '',
  email: '',
  subject: '',
  message: ''
});

function close() {
  emit('close');
  // Reset form after closing if needed, or keep state
  if (status.success) {
    status.message = '';
    status.success = false;
    form.name = '';
    form.email = '';
    form.subject = '';
    form.message = '';
  }
}

async function submitForm() {
  loading.value = true;
  status.message = '';
  
  try {
    const response = await fetch('http://127.0.0.1:5000/api/contact', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(form)
    });

    const data = await response.json();

    if (response.ok) {
      status.success = true;
      status.message = '¡Mensaje enviado con éxito!';
      setTimeout(() => {
        close();
      }, 2000);
    } else {
      status.success = false;
      status.message = data.error || 'Error al enviar el mensaje';
    }
  } catch (e) {
    status.success = false;
    status.message = 'Error de conexión';
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.animate-fade-in-up {
  animation: fadeInUp 0.3s ease-out;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
