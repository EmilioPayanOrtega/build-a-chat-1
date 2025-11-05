<template>
  <section class="auth-page">
    <div class="card">
      <h2 class="page-title">Inicio de sesión</h2>
      <form @submit.prevent="onSubmit" novalidate>
        <div class="field">
          <label for="identifier">Usuario o correo electrónico</label>
          <input
            id="identifier"
            v-model.trim="identifier"
            class="input"
            name="identifier"
            type="text"
            autocomplete="username"
            placeholder="Usuario o correo electrónico"
            required
          />
          <span v-if="showErrors && !identifier" class="input-error">Campo obligatorio</span>
        </div>

        <div class="field">
          <label for="password">Contraseña</label>
          <input
            id="password"
            v-model="password"
            class="input"
            name="password"
            type="password"
            autocomplete="current-password"
            placeholder="Contraseña"
            required
            minlength="6"
          />
          <span v-if="showErrors && !password" class="input-error">Campo obligatorio</span>
          <span v-if="showErrors && password && password.length < 6" class="input-error">Mínimo 6 caracteres</span>
        </div>

        <div style="display:flex; justify-content:center; margin-top:.5rem">
          <button class="btn primary" type="submit" :disabled="loading">
            {{ loading ? 'Ingresando…' : 'Iniciar sesión' }}
          </button>
        </div>
      </form>
      <p class="helper">
        ¿No tienes cuenta?
        <RouterLink to="/register">Regístrate ya</RouterLink>
      </p>
      <p v-if="message" :style="{marginTop: '12px', color: messageType === 'error' ? '#b91c1c' : '#166534'}">{{ message }}</p>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { login } from '../services/api';
import { useRouter } from 'vue-router';

const identifier = ref('');
const password = ref('');
const loading = ref(false);
const message = ref('');
const messageType = ref<'ok' | 'error'>('ok');
const showErrors = ref(false);
const router = useRouter();

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
      // Store user info (you can enhance this with proper session management)
      localStorage.setItem('user_id', String(response.user_id));
      localStorage.setItem('username', identifier.value);
      // Navigate to chat page after a brief delay
      setTimeout(() => {
        router.push('/chat');
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

<style scoped>
.auth-page{width:100%; display:flex; justify-content:center}
label{font-size:.95rem; color:#374151}
.input-error {
  color: #b91c1c;
  font-size: .93rem;
  padding-top: 2px;
}
</style>


