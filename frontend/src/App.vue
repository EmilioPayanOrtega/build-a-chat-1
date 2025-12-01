<template>
  <div class="min-h-screen flex flex-col bg-slate-50 relative overflow-hidden">
    <!-- Background Elements -->
    <div class="absolute top-0 left-0 w-full h-full overflow-hidden z-0 pointer-events-none">
      <div class="absolute -top-[20%] -left-[10%] w-[50%] h-[50%] rounded-full bg-blue-400/20 blur-3xl animate-pulse"></div>
      <div class="absolute top-[20%] -right-[10%] w-[40%] h-[40%] rounded-full bg-purple-400/20 blur-3xl animate-pulse delay-1000"></div>
    </div>

    <header class="sticky top-0 z-50 w-full border-b border-white/20 bg-white/70 backdrop-blur-md shadow-sm" v-if="!isChatPage">
      <div class="container mx-auto px-4 h-16 flex items-center justify-between">
        <RouterLink :to="isAuthenticated ? '/dashboard' : '/'" class="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent hover:opacity-80 transition-opacity">
          Build a Chat
        </RouterLink>
        <nav class="flex items-center gap-6 font-medium text-sm text-slate-600">
          <template v-if="!isAuthenticated">
            <RouterLink to="/register" class="hover:text-blue-600 transition-colors">Registrarse</RouterLink>
            <RouterLink to="/login" class="hover:text-blue-600 transition-colors">Iniciar sesión</RouterLink>
          </template>
          <template v-else>
            <RouterLink v-if="canCreateChatbots" to="/creator/chats" class="text-gray-600 hover:text-blue-600 font-medium transition-colors">
              Soporte
            </RouterLink>
            <RouterLink v-if="canCreateChatbots" to="/create-chatbot" class="text-gray-600 hover:text-blue-600 font-medium transition-colors">
              Crear chatbot
            </RouterLink>
          </template>
          <a href="#" @click.prevent="showContactModal = true" class="text-blue-600 font-semibold hover:text-blue-700 transition-colors">Contactarnos</a>
          
          <span v-if="isAuthenticated" class="flex items-center gap-4">
            <span class="flex items-center gap-2 px-3 py-1.5 rounded-full bg-white/50 border border-slate-200">
              <div class="w-2 h-2 rounded-full bg-green-500"></div>
              {{ username }}
            </span>
            <button @click="logout" class="text-red-500 hover:text-red-600 transition-colors font-medium">
              Cerrar sesión
            </button>
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

    <ContactModal :is-open="showContactModal" @close="showContactModal = false" />
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useAuth } from './store/auth';
import ContactModal from './components/ContactModal.vue';

const route = useRoute();
const router = useRouter();
const { isAuthenticated, state, logout: authLogout, canCreateChatbots } = useAuth();

const isChatPage = computed(() => route.path === '/chat');
const username = computed(() => state.username || 'Usuario');
const showContactModal = ref(false);

async function logout() {
  try {
    await fetch('/api/auth/logout', { method: 'POST' });
  } catch (e) {
    console.error('Logout failed', e);
  } finally {
    authLogout();
    router.push('/login');
  }
}
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


