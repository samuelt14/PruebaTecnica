import { useState } from 'react';
import { createGestion } from '../api/actas';

export default function GestionForm({ compromisoId }) {
  const [description, setDescription] = useState('');
  const [file, setFile]               = useState(null);
  const [date, setDate]               = useState('');
  const [msg, setMsg]                 = useState('');
  const token                         = localStorage.getItem('token');

  const handleSubmit = async e => {
    e.preventDefault();
    setMsg('');

    // Validaciones de tipo y tamaño
    if (!file) {
      setMsg('Selecciona un archivo (.pdf o .jpg).');
      return;
    }
    if (!['application/pdf', 'image/jpeg'].includes(file.type)) {
      setMsg('El archivo debe ser PDF o JPG.');
      return;
    }
    if (file.size > 5 * 1024 * 1024) {
      setMsg('El archivo no puede superar los 5 MB.');
      return;
    }

    try {
      await createGestion(
        { compromiso: compromisoId, date, description, attachment: file },
        token
      );
      setMsg('Gestión creada correctamente.');
      // opcional: limpiar formulario
      setDate('');
      setDescription('');
      setFile(null);
    } catch (error) {
      setMsg(error.message || 'Error al crear gestión.');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h4>Agregar Gestión</h4>

      <label>
        Fecha:
        <input
          type="date"
          value={date}
          onChange={e => setDate(e.target.value)}
          required
        />
      </label>

      <label>
        Descripción:
        <textarea
          placeholder="Descripción"
          value={description}
          onChange={e => setDescription(e.target.value)}
          required
        />
      </label>

      <label>
        Adjunto:
        <input
          type="file"
          accept=".pdf,.jpg"
          onChange={e => setFile(e.target.files[0])}
          required
        />
      </label>

      <button type="submit">Guardar</button>

      {msg && <p style={{ color: msg.startsWith('Gestión creada') ? 'green' : 'red' }}>{msg}</p>}
    </form>
  );
}
