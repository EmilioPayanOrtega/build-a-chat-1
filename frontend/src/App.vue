<template>
  <div class="app-container">
    <header class="app-header">
      <h1 class="brand">Build a Chat</h1>
      <nav class="nav">
        <RouterLink to="/login">Iniciar sesión</RouterLink>
        <span class="divider">•</span>
        <RouterLink to="/register">Registrarse</RouterLink>
      </nav>
    </header>

    <main class="app-main">
      <RouterView />
    </main>
  </div>
  
</template>

<script setup lang="ts">
// No script logic needed here for now
</script>

<style scoped>
.app-container { display: flex; flex-direction: column; min-height: 100vh; }
.app-header { display: flex; justify-content: space-between; align-items: center; padding: 1rem 1.25rem; border-bottom: 1px solid #e5e7eb; }
.brand { font-weight: 700; font-size: 1.1rem; }
.nav { display: flex; gap: .5rem; align-items: center; }
.divider { color: #9ca3af; }
.app-main { flex: 1; display: flex; align-items: center; justify-content: center; padding: 2rem 1rem; }
a { color: #2563eb; text-decoration: none; }
a:hover { text-decoration: underline; }
</style>


