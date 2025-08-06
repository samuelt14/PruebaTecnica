const API_URL = 'http://127.0.0.1:8000';

export async function login({ email, password }) {
  try {
    const res = await fetch(`${API_URL}/login/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });

    if (!res.ok) {
      // Si la API responde con error (400 o 401)
      const errorData = await res.json().catch(() => ({}));
      throw new Error(errorData.error || 'Error en login');
    }

    return await res.json();
  } catch (error) {
    throw new Error(error.message || 'Error en la conexión con el servidor');
  }
}

export function getAuthHeaders() {
  const token = localStorage.getItem('token');
  return token
    ? { Authorization: `Token ${token}`, 'Content-Type': 'application/json' }
    : { 'Content-Type': 'application/json' };
}
