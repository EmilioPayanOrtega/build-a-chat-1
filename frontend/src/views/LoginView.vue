<template>
  <section class="w-full flex justify-center items-center animate-fade-in">
    <div class="card">
      <h2 class="page-title">Inicio de sesión</h2>
      <form @submit.prevent="onSubmit" novalidate class="space-y-6">
        <div class="field">
          <label for="identifier" class="text-sm font-medium text-gray-700 mb-1">Usuario o correo electrónico</label>
          <input
            id="identifier"
            v-model.trim="identifier"
            class="input"
            name="identifier"
            type="text"
            autocomplete="username"
            placeholder="Ingresa tu usuario"
            required
          />
          <span v-if="showErrors && !identifier" class="text-red-500 text-xs mt-1">Campo obligatorio</span>
        </div>

        <div class="field">
          <label for="password" class="text-sm font-medium text-gray-700 mb-1">Contraseña</label>
          <input
            id="password"
            v-model="password"
            class="input"
            name="password"
            type="password"
            autocomplete="current-password"
            placeholder="••••••••"
            required
            minlength="6"
          />
          <span v-if="showErrors && !password" class="text-red-500 text-xs mt-1">Campo obligatorio</span>
          <span v-if="showErrors && password && password.length < 6" class="text-red-500 text-xs mt-1">Mínimo 6 caracteres</span>
        </div>

        <div class="pt-2">
          <button class="btn primary w-full flex justify-center items-center gap-2" type="submit" :disabled="loading">
            <svg v-if="loading" class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            {{ loading ? 'Ingresando…' : 'Iniciar sesión' }}
          </button>
        </div>
      </form>
      
      <p class="mt-6 text-center text-sm text-gray-600">
        ¿No tienes cuenta?
        <RouterLink to="/register" class="font-medium text-blue-600 hover:text-blue-500 transition-colors">Regístrate ya</RouterLink>
      </p>
      
      <div v-if="message" :class="['mt-4 p-3 rounded-lg text-sm text-center font-medium', messageType === 'error' ? 'bg-red-50 text-red-700 border border-red-200' : 'bg-green-50 text-green-700 border border-green-200']">
        {{ message }}
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { login } from '../services/api';
import { useRouter } from 'vue-router';
import { useAuth } from '../store/auth';

const identifier = ref('');
const password = ref('');
const loading = ref(false);
const message = ref('');
const messageType = ref<'ok' | 'error'>('ok');
const showErrors = ref(false);
const router = useRouter();
const { login: authLogin } = useAuth();

async function onSubmit(){
  showErrors.value = false;
  message.value = '';
  if (!identifier.value || !password.value || password.value.length < 6) {
    showErrors.value = true;
    return;
  }
  loading.value = true;
  try {
    const response = await login({
      nombre_usuario: identifier.value,
      password: password.value
    });
    if (response.success) {
      message.value = response.msg || '¡Inicio de sesión exitoso!';
      messageType.value = 'ok';
      
      // Update global auth state
      authLogin(String(response.user_id), identifier.value, response.role);
      
      // Navigate to dashboard after a brief delay
      setTimeout(() => {
        router.push('/dashboard');
      }, 1000);
    } else {
      message.value = response.error || 'Error al iniciar sesión';
      messageType.value = 'error';
      loading.value = false;
    }
  } catch (error) {
    message.value = error instanceof Error ? error.message : 'Error al iniciar sesión';
    messageType.value = 'error';
    loading.value = false;
  }
}
</script>


