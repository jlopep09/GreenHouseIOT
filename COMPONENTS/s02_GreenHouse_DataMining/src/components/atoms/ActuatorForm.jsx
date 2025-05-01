import React, { useState, useEffect } from 'react';
import { useAuth0 } from '@auth0/auth0-react';

const ACTUATOR_TYPES = [
  { key: 'pump', label: 'Bomba' },
  { key: 'fan', label: 'Ventilador' },
  { key: 'light', label: 'Luz' },
  { key: 'oxigen', label: 'Oxígeno' },
];

export default function ActuatorForm({ children }) {
  const { user, isAuthenticated, getAccessTokenSilently, isLoading } = useAuth0();

  const [greenhouses, setGreenhouses] = useState([]);
  const [selectedGhId, setSelectedGhId] = useState(null);
  const [configs, setConfigs] = useState({});
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    const fetchGreenhouses = async () => {
      if (!isAuthenticated) return;
      try {
        const sub = user.sub;
        const res = await fetch(
          `${import.meta.env.VITE_DDBB_API_IP}/db/gh/`,
          {
            method: 'GET',
            headers: {
              'Authorization': `Bearer ${import.meta.env.VITE_SECRET_TOKEN}`,
              'UserAuth': `${sub}`,
            },
          }
        );
        const data = await res.json();
        if (data.greenhouses.length > 0) {
          setGreenhouses(data.greenhouses);
          setSelectedGhId(data.greenhouses[0].id);
        }
      } catch (err) {
        console.error('Error fetching greenhouses:', err);
      }
    };
    fetchGreenhouses();
  }, [isAuthenticated, getAccessTokenSilently, user]);

  useEffect(() => {
    const fetchConfigs = async () => {
      if (!isAuthenticated || !selectedGhId) return;
      try {
        const sub = user.sub;
        const res = await fetch(`${import.meta.env.VITE_DDBB_API_IP}/db/ghconfig/`,
          {
            method: 'GET',
            headers: {
              'Authorization': `Bearer ${import.meta.env.VITE_SECRET_TOKEN}`,
              'UserAuth': `${sub}`,
            },
          }
        );
        const result = await res.json();
        const map = {};
        result.configs?.forEach(c => { map[c.name] = c; });
        setConfigs(map);
      } catch (err) {
        console.error('Error fetching actuator configs:', err);
      }
    };
    fetchConfigs();
  }, [isAuthenticated, getAccessTokenSilently, selectedGhId, user]);

  const handleSubmit = async (evt, typeKey) => {
    evt.preventDefault();
    const form = evt.target;
    const selectedMode = form[`mode_${typeKey}`].value;

    const payload = {
      name: typeKey,
      gh_id: selectedGhId,
      auto: selectedMode === 'auto' ? 1 : 0,
      manual_status: selectedMode === 'manual' ? 1 : 0,
      timer_on: form.timer_on.value,
      timer_off: form.timer_off.value,
    };

    try {
      const sub = user.sub;
      const existing = configs[typeKey];
      const method = existing?.id ? 'PUT' : 'POST';
      const url = existing?.id
        ? `${import.meta.env.VITE_DDBB_API_IP}/db/ghconfig/${existing.id}`
        : `${import.meta.env.VITE_DDBB_API_IP}/db/ghconfig/`;

      const res = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${import.meta.env.VITE_SECRET_TOKEN}`,
          'UserAuth': `${sub}`,
        },
        body: JSON.stringify(payload),
      });
      if (!res.ok) throw new Error(`Server responded ${res.status}`);
      const saved = await res.json();
      alert(`Configuración de ${typeKey} guardada`);
      setConfigs(prev => ({ ...prev, [typeKey]: { id: saved.id, ...payload } }));
    } catch (err) {
      console.error('Error saving config:', err);
      alert('Error al guardar la configuración');
    }
  };

  return (
    <>
      <button className="btn btn-primary" onClick={() => setIsOpen(true)}>
        {children || 'Configurar actuadores'}
      </button>

      {isOpen && (
        <dialog className="modal modal-open">
          <div className="modal-box max-w-lg">
            <h2 className="font-bold text-xl mb-4">Configurar Actuadores</h2>

            <div className="mb-4">
              <label className="label">
                <span className="label-text">Invernadero</span>
              </label>
              <select
                className="select select-bordered w-full"
                value={selectedGhId || ''}
                onChange={e => setSelectedGhId(e.target.value)}
              >
                <option value="" disabled>Seleccione un invernadero</option>
                {greenhouses.map(gh => (
                  <option key={gh.id} value={gh.id}>{gh.name}</option>
                ))}
              </select>
            </div>

            {selectedGhId && ACTUATOR_TYPES.map(({ key, label }) => {
              const cfg = configs[key] || {};
              return (
                <form key={key} onSubmit={e => handleSubmit(e, key)} className="mb-6">
                  <h3 className="font-semibold text-lg mb-2">{label}</h3>
                  <div className="grid grid-cols-2 gap-4 items-end">
                    <div className="col-span-2">
                      <label className="label">
                        <span className="label-text">Modo de funcionamiento</span>
                      </label>
                      <div className="flex gap-4">
                        <label className="flex items-center gap-2">
                          <input
                            type="radio"
                            name={`mode_${key}`}
                            value="manual"
                            defaultChecked={cfg.auto !== 1}
                            className="radio"
                          />
                          Manual
                        </label>
                        <label className="flex items-center gap-2">
                          <input
                            type="radio"
                            name={`mode_${key}`}
                            value="auto"
                            defaultChecked={cfg.auto === 1}
                            className="radio"
                          />
                          Auto
                        </label>
                      </div>
                    </div>

                    <div>
                      <label className="label">
                        <span className="label-text">Hora On</span>
                      </label>
                      <input
                        type="time"
                        name="timer_on"
                        defaultValue={cfg.timer_on || '09:00'}
                        className="input input-bordered"
                      />
                    </div>

                    <div>
                      <label className="label">
                        <span className="label-text">Hora Off</span>
                      </label>
                      <input
                        type="time"
                        name="timer_off"
                        defaultValue={cfg.timer_off || '14:00'}
                        className="input input-bordered"
                      />
                    </div>
                  </div>

                  <div className="flex justify-end gap-2 mt-4">
                    <button type="button" className="btn" onClick={() => setIsOpen(false)}>Cancelar</button>
                    <button type="submit" className="btn btn-primary">Guardar {label}</button>
                  </div>
                </form>
              );
            })}

            <button className="btn btn-sm absolute right-2 top-2" onClick={() => setIsOpen(false)}>✕</button>
          </div>
        </dialog>
      )}
    </>
  );
}
