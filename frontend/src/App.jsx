import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Login from './components/Login';
import ActasList from './components/ActasList';
import ActaDetail from './components/ActaDetail';

function PrivateRoute({ children }) {
  const token = localStorage.getItem('token');
  return token ? children : <Navigate to="/login" />;
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="/login"
          element={<Login onLogin={() => window.location.href = '/actas'} />}
        />
        <Route
          path="/actas"
          element={
            <PrivateRoute>
              <ActasList onSelect={id => window.location.href = `/actas/${id}`} />
            </PrivateRoute>
          }
        />
        <Route
          path="/actas/:id"
          element={
            <PrivateRoute>
              <ActaDetail />
            </PrivateRoute>
          }
        />
        <Route path="*" element={<Navigate to="/login" />} />
      </Routes>
    </BrowserRouter>
  );
}
