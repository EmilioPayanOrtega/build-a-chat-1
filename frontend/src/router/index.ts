import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  { path: '/', name: 'landing', component: () => import('../views/LandingView.vue') },
  { path: '/login', name: 'login', component: () => import('../views/LoginView.vue') },
  { path: '/register', name: 'register', component: () => import('../views/RegisterView.vue') },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: () => import('../views/DashboardView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/chatbot/:id',
    name: 'chatbot',
    component: () => import('../views/ChatbotView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/create-chatbot',
    name: 'create-chatbot',
    component: () => import('../views/CreateChatbotView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/creator/chats',
    name: 'creator-chats',
    component: () => import('../views/CreatorChatView.vue'),
    meta: { requiresAuth: true }
  },
  // Redirect old chat route to dashboard
  { path: '/chat', redirect: '/dashboard' }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

// Navigation guard to protect routes that require authentication
router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
  const isAuthenticated = localStorage.getItem('user_id') !== null;

  if (requiresAuth && !isAuthenticated) {
    next('/login');
  } else {
    next();
  }
});

export default router;


