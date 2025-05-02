import React, { useState } from 'react';
import { useAuth0 } from '@auth0/auth0-react';
import { Link } from 'react-router';

export default function AddNewGH({ children }) {
  const [isOpen, setIsOpen] = useState(false);
  const { user, isAuthenticated, getAccessTokenSilently, isLoading } = useAuth0();

  const handleSubmit = async (event) => {
    event.preventDefault();
    const form = event.target;
    const name = form.elements.name.value;
    const sync_code = form.elements.sync_code.value;

    const payload = { name, sync_code };

    try {

      const url = `${import.meta.env.VITE_DDBB_API_IP}/db/syncgh/`;
      const res = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${import.meta.env.VITE_SECRET_TOKEN}`,  // Enviar el token en el header
            'UserAuth': `${user.sub}`,
        },
        body: JSON.stringify(payload),
      });

      if (!res.ok) {
        throw new Error(`Server responded ${res.status}`);
      }

      await res.json();
      alert('Configuración guardada');
      setIsOpen(false);
    } catch (err) {
      console.error('Sync error:', err);
      alert('Error al sincronizar');
    }
  };

  if (isLoading) return <button className="btn btn-primary" disabled>Cargando...</button>;
  if (!isAuthenticated) return <button className="btn btn-primary" onClick={() => loginWithRedirect()}>Inicia sesión</button>;

  return (
    <>
      <button className="btn btn-primary" onClick={() => setIsOpen(true)}>
        {children}
      </button>

      {isOpen && (
        <dialog className="modal modal-open">
          <div className="modal-box">
            <h3 className="font-bold text-lg">Sincroniza tu invernadero</h3>
            <form onSubmit={handleSubmit} className="flex flex-col gap-4 mt-4">
              <input
                type="text"
                name="name"
                placeholder="Nombre"
                className="input input-bordered w-full"
                required
              />
              <input
                type="text"
                name="sync_code"
                placeholder="Código de sincronización"
                className="input input-bordered w-full"
                required
              />
              <div className="flex justify-between gap-2">
                <Link to={"/help"}><p className='btn btn-link'>Guía de sincronización</p> </Link>
                <div className='flex gap-2'>
                    <button
                    type="button"
                    className="btn"
                    onClick={() => setIsOpen(false)}
                    >
                    Cancelar
                    </button>
                    <button type="submit" className="btn btn-primary">
                    Enviar
                    </button>
                </div>
              </div>
            </form>
            
          </div>
        </dialog>
      )}
    </>
  );
}
