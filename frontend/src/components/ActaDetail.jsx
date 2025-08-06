import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { fetchActa } from '../api/actas';
import GestionForm from './GestionForm';

export default function ActaDetail() {
  const { id } = useParams();
  const nav    = useNavigate();
  const [acta, setActa]         = useState(null);
  const [loading, setLoading]   = useState(true);
  const [error, setError]       = useState('');
  const [showForm, setShowForm] = useState(false);
  
  useEffect(() => {
    (async () => {
      setLoading(true);
      try {
        const token = localStorage.getItem('token');
        const data  = await fetchActa(id, token);
        setActa(data);
      } catch (e) {
        setError(e.message);
      } finally {
        setLoading(false);
      }
    })();
  }, [id]);

  if (loading) return <p>Cargando...</p>;
  if (error)   return <p style={{ color: 'red' }}>{error}</p>;

  const userRole = localStorage.getItem('role');
  const userId   = localStorage.getItem('userId');
  const puede    =
    userRole === 'Administrador' ||
    acta.compromisos.some(c => c.responsible.id.toString() === userId);

  return (
    <div>
      <button onClick={() => nav(-1)} style={{ marginBottom: '1em' }}>← Volver</button>
      <h1>{acta.title}</h1>
      <p><strong>Estado:</strong> {acta.status}</p>
      <p><strong>Fecha:</strong> {new Date(acta.date).toLocaleDateString()}</p>
      {acta.pdf && (
        <p><a href={`/media/${acta.pdf}`} target="_blank" rel="noreferrer">Ver PDF</a></p>
      )}

      {puede && (
        <button
          onClick={() => setShowForm(f => !f)}
          style={{ margin: '1em 0', padding: '0.5em 1em' }}
        >
          {showForm ? 'Cancelar gestión' : 'Agregar gestión'}
        </button>
      )}

      {showForm && <GestionForm compromisoId={acta.compromisos[0]?.id} />}

      <h2>Compromisos</h2>
      {acta.compromisos.length === 0
        ? <p>No hay compromisos</p>
        : (
          <ul>
            {acta.compromisos.map(c => (
              <li key={c.id}>
                {c.description} — Responsable: {c.responsible.username}
              </li>
            ))}
          </ul>
        )
      }
    </div>
  );
}
