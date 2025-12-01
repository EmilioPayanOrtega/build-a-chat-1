type ApiResponse<T = unknown> = T & { success?: boolean; error?: string };

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api';

async function request<T>(path: string, options: RequestInit): Promise<ApiResponse<T>> {
  const res = await fetch(`${API_BASE_URL}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    ...options
  });

  const contentType = res.headers.get('content-type') || '';
  const body = contentType.includes('application/json') ? await res.json() : await res.text();
  if (!res.ok) {
    const msg = typeof body === 'string' ? body : body?.error || 'Request failed';
    throw new Error(msg);
  }
  return body as ApiResponse<T>;
}

export function login(payload: { nombre_usuario: string; password: string }) {
  return request<{ msg: string; user_id: number }>(`/auth/login`, {
    method: 'POST',
    body: JSON.stringify({
      username: payload.nombre_usuario,
      password: payload.password
    })
  });
}

export function signup(payload: { nombre_usuario: string; email: string; password: string }) {
  return request<{ msg: string }>(`/auth/register`, {
    method: 'POST',
    body: JSON.stringify({
      username: payload.nombre_usuario,
      email: payload.email,
      password: payload.password
    })
  });
}


