<template>
  <section class="auth-page">
    <div class="card">
      <h2 class="page-title">Registro de usuario</h2>
      <form @submit.prevent="onSubmit" novalidate>
        <div class="field">
          <label for="username">Usuario</label>
          <input
            id="username"
            v-model.trim="username"
            class="input"
            name="username"
            type="text"
            autocomplete="username"
            placeholder="Usuario"
            required
          />
          <span v-if="showErrors && !username" class="input-error">El usuario es obligatorio</span>
        </div>

        <div class="field">
          <label for="email">Correo electrónico</label>
          <input
            id="email"
            v-model.trim="email"
            class="input"
            name="email"
            type="email"
            autocomplete="email"
            placeholder="Correo electrónico"
            required
          />
          <span v-if="showErrors && !email" class="input-error">El correo es obligatorio</span>
          <span v-if="showErrors && email && !emailIsValid(email)" class="input-error">El correo no es válido</span>
        </div>

        <div class="field">
          <label for="password">Contraseña</label>
          <input
            id="password"
            v-model="password"
            class="input"
            name="password"
            type="password"
            autocomplete="new-password"
            placeholder="Contraseña"
            required
            minlength="6"
          />
          <span v-if="showErrors && !password" class="input-error">La contraseña es obligatoria</span>
          <span v-if="showErrors && password && password.length < 6" class="input-error">Mínimo 6 caracteres</span>
        </div>

        <div class="field">
          <label for="confirm">Confirmar contraseña</label>
          <input
            id="confirm"
            v-model="confirm"
            class="input"
            name="confirm"
            type="password"
            autocomplete="new-password"
            placeholder="Confirmar contraseña"
            required
            minlength="6"
          />
          <span v-if="showErrors && !confirm" class="input-error">Confirma tu contraseña</span>
          <span v-if="showErrors && confirm && password !== confirm" class="input-error">Las contraseñas no coinciden</span>
        </div>

        <div style="display:flex; justify-content:center; margin-top:.5rem; gap:.5rem">
          <button class="btn" type="button" @click="resetForm" :disabled="loading">Limpiar</button>
          <button class="btn primary" type="submit" :disabled="loading">
            {{ loading ? 'Registrando…' : 'Registrarse' }}
          </button>
        </div>
      </form>
      <p class="helper">
        ¿Ya tienes cuenta?
        <RouterLink to="/login">Inicia sesión</RouterLink>
      </p>

      <p v-if="message" :style="{marginTop: '12px', color: messageType === 'error' ? '#b91c1c' : '#166534'}">{{ message }}</p>
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

<style scoped>
.auth-page{width:100%; display:flex; justify-content:center}
label{font-size:.95rem; color:#374151}
.input-error {
  color: #b91c1c;
  font-size: .93rem;
  padding-top: 2px;
}
</style>


