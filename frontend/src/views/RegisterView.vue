<template>
  <section class="w-full flex justify-center items-center animate-fade-in py-8">
    <div class="card">
      <h2 class="page-title">Registro de usuario</h2>
      <form @submit.prevent="onSubmit" novalidate class="space-y-4">
        <div class="field">
          <label for="username" class="text-sm font-medium text-gray-700 mb-1">Usuario</label>
          <input
            id="username"
            v-model.trim="username"
            class="input"
            name="username"
            type="text"
            autocomplete="username"
            placeholder="Elige un nombre de usuario"
            required
          />
          <span v-if="showErrors && !username" class="text-red-500 text-xs mt-1">El usuario es obligatorio</span>
        </div>

        <div class="field">
          <label for="email" class="text-sm font-medium text-gray-700 mb-1">Correo electrónico</label>
          <input
            id="email"
            v-model.trim="email"
            class="input"
            name="email"
            type="email"
            autocomplete="email"
            placeholder="ejemplo@correo.com"
            required
          />
          <span v-if="showErrors && !email" class="text-red-500 text-xs mt-1">El correo es obligatorio</span>
          <span v-if="showErrors && email && !emailIsValid(email)" class="text-red-500 text-xs mt-1">El correo no es válido</span>
        </div>

        <div class="field">
          <label for="password" class="text-sm font-medium text-gray-700 mb-1">Contraseña</label>
          <input
            id="password"
            v-model="password"
            class="input"
            name="password"
            type="password"
            autocomplete="new-password"
            placeholder="••••••••"
            required
            minlength="6"
          />
          <span v-if="showErrors && !password" class="text-red-500 text-xs mt-1">La contraseña es obligatoria</span>
          <span v-if="showErrors && password && password.length < 6" class="text-red-500 text-xs mt-1">Mínimo 6 caracteres</span>
        </div>

        <div class="field">
          <label for="confirm" class="text-sm font-medium text-gray-700 mb-1">Confirmar contraseña</label>
          <input
            id="confirm"
            v-model="confirm"
            class="input"
            name="confirm"
            type="password"
            autocomplete="new-password"
            placeholder="••••••••"
            required
            minlength="6"
          />
          <span v-if="showErrors && !confirm" class="text-red-500 text-xs mt-1">Confirma tu contraseña</span>
          <span v-if="showErrors && confirm && password !== confirm" class="text-red-500 text-xs mt-1">Las contraseñas no coinciden</span>
        </div>

        <div class="flex gap-3 pt-2">
          <button class="btn bg-gray-200 text-gray-700 hover:bg-gray-300 flex-1" type="button" @click="resetForm" :disabled="loading">
            Limpiar
          </button>
          <button class="btn primary flex-1 flex justify-center items-center gap-2" type="submit" :disabled="loading">
            <svg v-if="loading" class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            {{ loading ? 'Registrando…' : 'Registrarse' }}
          </button>
        </div>
      </form>
      
      <p class="mt-6 text-center text-sm text-gray-600">
        ¿Ya tienes cuenta?
        <RouterLink to="/login" class="font-medium text-blue-600 hover:text-blue-500 transition-colors">Inicia sesión</RouterLink>
      </p>

      <div v-if="message" :class="['mt-4 p-3 rounded-lg text-sm text-center font-medium', messageType === 'error' ? 'bg-red-50 text-red-700 border border-red-200' : 'bg-green-50 text-green-700 border border-green-200']">
        {{ message }}
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { signup } from '../services/api';
import { useRouter } from 'vue-router';

const username = ref('');
const email = ref('');
const password = ref('');
const confirm = ref('');
const loading = ref(false);
const message = ref('');
const messageType = ref<'ok' | 'error'>('ok');
const showErrors = ref(false);
const router = useRouter();

function emailIsValid(email: string) {
  return /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email);
}

async function onSubmit(){
  message.value = '';
  showErrors.value = false;
  if (
    !username.value ||
    !email.value ||
    !password.value ||
    !confirm.value ||
    password.value !== confirm.value ||
    password.value.length < 6 ||
    !emailIsValid(email.value)
  ) {
    showErrors.value = true;
    return;
  }
  loading.value = true;
  try {
    const response = await signup({
      nombre_usuario: username.value,
      email: email.value,
      password: password.value
    });
    if (response.success) {
      message.value = response.msg || '¡Registro exitoso!';
      messageType.value = 'ok';
      resetForm();
      // Navigate to login page after successful registration
      setTimeout(() => {
        router.push('/login');
      }, 1500);
    } else {
      message.value = response.error || 'Error al registrar usuario';
      messageType.value = 'error';
      loading.value = false;
    }
  } catch (error) {
    message.value = error instanceof Error ? error.message : 'Error al registrar usuario';
    messageType.value = 'error';
    loading.value = false;
  }
}

function resetForm(){
  username.value = '';
  email.value = '';
  password.value = '';
  confirm.value = '';
}
</script>


