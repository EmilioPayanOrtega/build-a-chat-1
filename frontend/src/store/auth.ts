import { reactive, computed } from 'vue';

interface AuthState {
    userId: string | null;
    username: string | null;
}

const state = reactive<AuthState>({
    userId: localStorage.getItem('user_id'),
    username: localStorage.getItem('username'),
});

const isAuthenticated = computed(() => !!state.userId);

function login(userId: string, username: string) {
    state.userId = userId;
    state.username = username;
    localStorage.setItem('user_id', userId);
    localStorage.setItem('username', username);
}

function logout() {
    state.userId = null;
    state.username = null;
    localStorage.removeItem('user_id');
    localStorage.removeItem('username');
}

export const useAuth = () => {
    return {
        state,
        isAuthenticated,
        login,
        logout,
    };
};
