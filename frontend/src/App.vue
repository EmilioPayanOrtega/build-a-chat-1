<template>
  <div class="min-h-screen flex flex-col bg-slate-50 relative overflow-hidden">
    <!-- Background Elements -->
    <div class="absolute top-0 left-0 w-full h-full overflow-hidden z-0 pointer-events-none">
      <div class="absolute -top-[20%] -left-[10%] w-[50%] h-[50%] rounded-full bg-blue-400/20 blur-3xl animate-pulse"></div>
      <div class="absolute top-[20%] -right-[10%] w-[40%] h-[40%] rounded-full bg-purple-400/20 blur-3xl animate-pulse delay-1000"></div>
    </div>

    <header class="sticky top-0 z-50 w-full border-b border-white/20 bg-white/70 backdrop-blur-md shadow-sm" v-if="!isChatPage">
      <div class="container mx-auto px-4 h-16 flex items-center justify-between">
        <h1 class="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
          Build a Chat
        </h1>
        <nav class="flex items-center gap-6 font-medium text-sm text-slate-600">
          <template v-if="!isAuthenticated">
            <RouterLink to="/login" class="hover:text-blue-600 transition-colors">Iniciar sesión</RouterLink>
            <span class="text-slate-300">•</span>
            <RouterLink to="/register" class="px-4 py-2 rounded-full bg-slate-900 text-white hover:bg-slate-800 transition-all hover:shadow-lg hover:-translate-y-0.5">
              Registrarse
            </RouterLink>
          </template>
          <span v-else class="flex items-center gap-2 px-3 py-1.5 rounded-full bg-white/50 border border-slate-200">
            <div class="w-2 h-2 rounded-full bg-green-500"></div>
            {{ username }}
          </span>
        </nav>
      </div>
    </header>

    <main class="flex-1 flex items-center justify-center p-4 relative z-10">
      <RouterView v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </RouterView>
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();

const isChatPage = computed(() => route.path === '/chat');
const isAuthenticated = computed(() => localStorage.getItem('user_id') !== null);
const username = computed(() => localStorage.getItem('username') || 'Usuario');
</script>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>


