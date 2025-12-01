<template>
  <div class="w-full max-w-6xl mx-auto animate-fade-in">
    <!-- Header Section -->
    <div class="mb-8 text-center">
      <h2 class="text-4xl font-bold text-gray-800 mb-4">Explora Chatbots</h2>
      <p class="text-gray-600 max-w-2xl mx-auto">
        Descubre asistentes inteligentes creados por la comunidad o crea el tuyo propio para compartir conocimiento.
      </p>
    </div>

    <!-- Search Bar -->
    <div class="mb-10 relative max-w-2xl mx-auto">
      <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
        <svg class="h-6 w-6 text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
      </div>
      <input
        v-model="searchQuery"
        type="text"
        class="w-full pl-12 pr-4 py-4 rounded-2xl border-0 shadow-lg bg-white/80 backdrop-blur-xl focus:ring-2 focus:ring-blue-500 transition-all text-lg"
        placeholder="Buscar chatbots por título..."
      />
    </div>

    <!-- Chatbots Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="bot in filteredChatbots" :key="bot.id" class="group relative bg-white rounded-2xl shadow-md hover:shadow-xl transition-all duration-300 overflow-hidden border border-gray-100 hover:-translate-y-1">
        <div class="h-32 bg-gradient-to-r from-blue-500 to-purple-600 p-6 flex items-end">
          <h3 class="text-white text-xl font-bold truncate">{{ bot.title }}</h3>
        </div>
        <div class="p-6">
          <p class="text-gray-600 mb-4 line-clamp-2">{{ bot.description }}</p>
          <div class="flex justify-between items-center">
            <span class="text-sm text-gray-500 flex items-center gap-1">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path></svg>
              {{ bot.creator }}
            </span>
            <RouterLink :to="`/chatbot/${bot.id}`" class="px-4 py-2 rounded-lg bg-blue-50 text-blue-600 font-medium hover:bg-blue-100 transition-colors">
              Explorar
            </RouterLink>
          </div>
        </div>
      </div>
      
      <!-- Empty State -->
      <div v-if="filteredChatbots.length === 0" class="col-span-full text-center py-12">
        <div class="inline-flex items-center justify-center w-16 h-16 rounded-full bg-gray-100 mb-4">
          <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
        </div>
        <h3 class="text-lg font-medium text-gray-900">No se encontraron resultados</h3>
        <p class="text-gray-500">Intenta con otros términos de búsqueda.</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';

// Mock data - replace with API call later
const chatbots = ref([
  { id: 1, title: 'Guía de Python', description: 'Aprende Python desde cero con este mapa interactivo de conceptos.', creator: 'PythonMaster' },
  { id: 2, title: 'Historia del Arte', description: 'Explora los movimientos artísticos más importantes de la historia.', creator: 'ArtLover' },
  { id: 3, title: 'Recetas Veganas', description: 'Un árbol de decisiones para encontrar tu próxima comida favorita.', creator: 'ChefGreen' },
  { id: 4, title: 'Manual de React', description: 'Documentación interactiva para desarrolladores frontend.', creator: 'DevGuru' },
  { id: 5, title: 'Astronomía Básica', description: 'Descubre el sistema solar y más allá.', creator: 'StarGazer' },
]);

const searchQuery = ref('');

const filteredChatbots = computed(() => {
  return chatbots.value.filter(bot => 
    bot.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    bot.description.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
});
</script>
