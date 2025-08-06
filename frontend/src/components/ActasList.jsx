import React, { useEffect, useState } from 'react';
import { fetchActas } from '../api/actas';
import { Link } from 'react-router-dom';

export default function ActasList() {
  const [actas, setActas]     = useState([]);
  const [filters, setFilters] = useState({ title: '', status: '', date: '' });
  const [loading, setLoading] = useState(true);
  const [error, setError]     = useState('');

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      setError('');
      try {
        const token = localStorage.getItem('token');
        const data  = await fetchActas({ ...filters }, token);
        setActas(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [filters]);

  if (loading) return <p>Cargando actas...</p>;
  if (error)   return <p style={{ color: 'red' }}>{error}</p>;

  return (
    <div>
      <h1>Mis Actas</h1>

      {/* filtros */}
      <div style={{ margin: '1em 0', display: 'flex', gap: '0.5em' }}>
        <input
          placeholder="Título"
          value={filters.title}
          onChange={e => setFilters(f => ({ ...f, title: e.target.value }))}
        />
        <input
          placeholder="Estado"
          value={filters.status}
          onChange={e => setFilters(f => ({ ...f, status: e.target.value }))}
        />
        <input
          type="date"
          value={filters.date}
          onChange={e => setFilters(f => ({ ...f, date: e.target.value }))}
        />
      </div>

      {actas.length === 0
        ? <p>No hay actas disponibles</p>
        : (
          <table border="1" cellPadding="8" style={{ width: '100%' }}>
            <thead>
              <tr>
                <th>Título</th><th>Estado</th><th>Fecha</th><th>Compromisos</th><th>Detalle</th>
              </tr>
            </thead>
            <tbody>
              {actas.map(a => (
                <tr key={a.id}>
                  <td>{a.title}</td>
                  <td>{a.status}</td>
                  <td>{new Date(a.date).toLocaleDateString()}</td>
                  <td>{a.compromisos.length}</td>
                  <td><Link to={`/actas/${a.id}`}>Ver Detalle</Link></td>
                </tr>
              ))}
            </tbody>
          </table>
        )
      }
    </div>
  );
}
