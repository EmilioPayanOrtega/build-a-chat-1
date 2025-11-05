<template>
  <div class="app-container">
    <header class="app-header" v-if="!isChatPage">
      <h1 class="brand">Build a Chat</h1>
      <nav class="nav">
        <RouterLink v-if="!isAuthenticated" to="/login">Iniciar sesión</RouterLink>
        <span v-if="!isAuthenticated" class="divider">•</span>
        <RouterLink v-if="!isAuthenticated" to="/register">Registrarse</RouterLink>
        <span v-if="isAuthenticated" class="user-info">Usuario: {{ username }}</span>
      </nav>
    </header>

    <main class="app-main">
      <RouterView />
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

<style scoped>
.app-container { display: flex; flex-direction: column; min-height: 100vh; }
.app-header { display: flex; justify-content: space-between; align-items: center; padding: 1rem 1.25rem; border-bottom: 1px solid #e5e7eb; }
.brand { font-weight: 700; font-size: 1.1rem; }
.nav { display: flex; gap: .5rem; align-items: center; }
.divider { color: #9ca3af; }
.user-info { color: #374151; font-weight: 500; }
.app-main { flex: 1; display: flex; align-items: center; justify-content: center; padding: 2rem 1rem; }
a { color: #2563eb; text-decoration: none; }
a:hover { text-decoration: underline; }
</style>


