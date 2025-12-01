<template>
  <div class="w-full min-h-[calc(100vh-4rem)] flex items-center justify-center animate-fade-in px-4">
    <div class="container mx-auto grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
      <!-- Left Content -->
      <div class="space-y-6 text-center lg:text-left">
        <h1 class="text-5xl lg:text-6xl font-bold text-gray-900 leading-tight">
          Desbloquee todo el <br class="hidden lg:block" />
          potencial de su <br class="hidden lg:block" />
          negocio
        </h1>
        <p class="text-xl text-gray-500 font-medium max-w-lg mx-auto lg:mx-0">
          Construya un Chatbot con nosotros y <span class="font-bold text-gray-700">aumente su agilidad</span>
        </p>
        <div class="pt-4 flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
          <RouterLink to="/register" class="btn primary text-lg px-8 py-3 rounded-full shadow-xl hover:shadow-2xl hover:-translate-y-1 transition-all">
            Comenzar ahora
          </RouterLink>
          <button class="px-8 py-3 rounded-full border-2 border-gray-200 text-gray-600 font-medium hover:border-gray-400 hover:text-gray-800 transition-all">
            Ver demo
          </button>
        </div>
      </div>

      <!-- Right Image Placeholder -->
      <div class="relative w-full aspect-square max-w-md mx-auto lg:max-w-full">
        <div class="absolute inset-0 bg-gradient-to-tr from-blue-100 to-purple-100 rounded-3xl transform rotate-3 scale-105 z-0"></div>
        <div class="relative z-10 w-full h-full bg-white border-2 border-gray-100 rounded-2xl shadow-2xl flex items-center justify-center overflow-hidden p-8">
          <img src="../assets/logo.png" alt="Build a Chat Logo" class="w-full h-auto object-contain" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// No script logic needed for this static view yet
</script>
