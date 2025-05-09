import React, { useState, useEffect } from 'react';
import { useAuth0 } from '@auth0/auth0-react';
import { FormGhSelector, FormCloseButton, FormTemplate } from './ActuatorForm';

// Define available actuator types if not imported
const ACTUATOR_TYPES = [
  { key: 'pump', label: 'Bomba' },
  { key: 'fan', label: 'Ventilador' },
  { key: 'light', label: 'Luz' },
  { key: 'oxigen', label: 'Oxígeno' },
];

/**
 * SingleActuatorForm
 * @param {{ actuatorType: string, children?: React.ReactNode }} props
 * actuatorType: key of the actuator to render (e.g. 'pump')
 * children: button label or icon
 */
export default function SingleActuatorForm({ actuatorType, children, version }) {
  const { user, isAuthenticated, getAccessTokenSilently, isLoading } = useAuth0();

  const [greenhouses, setGreenhouses] = useState([]);
  const [selectedGhId, setSelectedGhId] = useState(null);
  const [configs, setConfigs] = useState({});
  const [isOpen, setIsOpen] = useState(false);

  // Find label for this actuator
  const actuatorConfig = ACTUATOR_TYPES.find(a => a.key === actuatorType) || {};
  const label = actuatorConfig.label || actuatorType;

  // Fetch greenhouses for user
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
              'UserAuth': sub,
            },
          }
        );
        const data = await res.json();
        if (data.greenhouses?.length) {
          setGreenhouses(data.greenhouses);
          setSelectedGhId(data.greenhouses[0].id);
        }
      } catch (err) {
        console.error('Error fetching greenhouses:', err);
      }
    };
    fetchGreenhouses();
  }, [isAuthenticated, user]);

  // Fetch existing configs when greenhouse changes
  useEffect(() => {
    const fetchConfigs = async () => {
      if (!isAuthenticated || !selectedGhId) return;
      try {
        const sub = user.sub;
        const res = await fetch(
          `${import.meta.env.VITE_DDBB_API_IP}/db/ghconfig/`,
          {
            method: 'GET',
            headers: {
              'Authorization': `Bearer ${import.meta.env.VITE_SECRET_TOKEN}`,
              'UserAuth': sub,
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
  }, [isAuthenticated, user, selectedGhId]);

  // Submit handler
  const handleSubmit = async (evt) => {
    evt.preventDefault();
    const form = evt.target;

    const payload = {
      name: actuatorType,
      gh_id: selectedGhId,
      auto: form.auto.checked ? 1 : 0,
      manual_status: form.manual_status.checked ? 1 : 0,
      timer_on: form.timer_on.value,
      timer_off: form.timer_off.value,
    };

    try {
      const sub = user.sub;
      const existing = configs[actuatorType];
      const method = existing?.id ? 'PUT' : 'POST';
      const url = existing?.id
        ? `${import.meta.env.VITE_DDBB_API_IP}/db/ghconfig/${existing.id}`
        : `${import.meta.env.VITE_DDBB_API_IP}/db/ghconfig/`;

      const res = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${import.meta.env.VITE_SECRET_TOKEN}`,
          'UserAuth': sub,
        },
        body: JSON.stringify(payload),
      });

      if (res.status === 304) {
        alert(`La configuración de ${label} ya está actualizada`);
      } else if (res.ok) {
        const saved = await res.json();
        alert(`Configuración de ${label} guardada`);
        setConfigs(prev => ({ ...prev, [actuatorType]: { id: saved.id, ...payload } }));
      } else {
        throw new Error(`Server responded ${res.status}`);
      }
    } catch (err) {
      console.error('Error saving config:', err);
      alert('Error al guardar la configuración');
    }
  };
  const variante = version == "dark" ?"btn btn-neutral font-bold w-full" :"btn btn-primary font-bold w-full"
  return (
    <>
      <button className={variante} onClick={() => setIsOpen(true)}>
        {children || `Configurar ${label}`}
      </button>

      {isOpen && (
        <dialog className="modal modal-open">
          <div className="modal-box max-w-lg">
            <h2 className="font-bold text-xl mb-4">Configurar {label}</h2>

            <FormGhSelector
              setSelectedGhId={setSelectedGhId}
              selectedGhId={selectedGhId}
              greenhouses={greenhouses}
            />

            {selectedGhId && (
              <FormTemplate
                keyValue={actuatorType}
                label={label}
                handleSubmit={handleSubmit}
                configs={configs}
                setIsOpen={setIsOpen}
              />
            )}

            <FormCloseButton setIsOpen={setIsOpen} />
          </div>
        </dialog>
      )}
    </>
  );
}