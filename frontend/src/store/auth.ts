import { reactive, computed } from 'vue';

interface AuthState {
    userId: string | null;
    username: string | null;
    role: string | null;
}

const state = reactive<AuthState>({
    userId: localStorage.getItem('user_id'),
    username: localStorage.getItem('username'),
    role: localStorage.getItem('role'),
});

const isAuthenticated = computed(() => !!state.userId);
const canCreateChatbots = computed(() => state.role === 'creator' || state.role === 'admin');

function login(userId: string, username: string, role: string) {
    state.userId = userId;
    state.username = username;
    state.role = role;
    localStorage.setItem('user_id', userId);
    localStorage.setItem('username', username);
    localStorage.setItem('role', role);
}

function logout() {
    state.userId = null;
    state.username = null;
    state.role = null;
    localStorage.removeItem('user_id');
    localStorage.removeItem('username');
    localStorage.removeItem('role');
}

export const useAuth = () => {
    return {
        state,
        isAuthenticated,
        canCreateChatbots,
        login,
        logout,
    };
};
