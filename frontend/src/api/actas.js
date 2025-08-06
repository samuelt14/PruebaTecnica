const API_URL = 'http://127.0.0.1:8000';

export async function fetchActas(filters = {}, token) {
  const query = new URLSearchParams(filters).toString();
  const res = await fetch(`${API_URL}/actas/?${query}`, {
    headers: { 'Authorization': `Token ${token}` },
  });

  if (!res.ok) {
    const errorText = await res.text();
    console.error('Error al cargar actas:', res.status, errorText); // 🔍 para depurar
    throw new Error('Error al cargar actas');
  }

  return res.json();
}

export async function fetchActa(id, token) {
  const res = await fetch(`${API_URL}/actas/${id}/`, {
    headers: { 'Authorization': `Token ${token}` },
  });

  if (!res.ok) throw new Error('Error al cargar acta');
  return res.json();
}

export async function createGestion(data, token) {
  const form = new FormData();
  form.append('compromiso', data.compromiso);
  form.append('date', data.date);
  form.append('description', data.description);
  form.append('attachment', data.attachment);

  const res = await fetch(`${API_URL}/gestiones/`, {
    method: 'POST',
    headers: { 'Authorization': `Token ${token}` },
    body: form,
  });

  if (!res.ok) throw new Error('Error al crear gestión');
  return res.json();
}
