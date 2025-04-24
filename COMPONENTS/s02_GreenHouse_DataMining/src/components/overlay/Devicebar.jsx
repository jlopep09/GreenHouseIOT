import React, { useState, useEffect } from 'react';
import { ArrowSVG } from '../Buttons/ThemeButton';
import AddNewGH from '../Buttons/AddNewGH';
import { useAuth0 } from "@auth0/auth0-react"; 

export default function Devicebar() {
    const [greenhouses, setGreenhouses] = useState([]);
    const [selectedDevice, setSelectedDevice] = useState('');
    const { user, isAuthenticated, getAccessTokenSilently, isLoading } = useAuth0();
    
    const fetchGreenhouses = async () => {
        if (!isAuthenticated) return;
        try {
            const token = await getAccessTokenSilently();
            const response = await fetch(`${import.meta.env.VITE_DDBB_API_IP}/db/gh/`,
                {
                  method: 'GET',
                  headers: {
                    'Authorization': `Bearer ${import.meta.env.VITE_SECRET_TOKEN}`,  // Enviar el token en el header
                    'UserAuth': `${token}`,
                },
                }
              );
            const data = await response.json();
            if (data.greenhouses.length > 0) {
                setGreenhouses(data.greenhouses);
                setSelectedDevice(data.greenhouses[0].name);
            }
        } catch (error) {
            console.error('Error fetching greenhouses:', error);
        }
    };

    useEffect(() => {
        fetchGreenhouses();
    }, [isAuthenticated, getAccessTokenSilently]);
    
    if (isLoading) return <div>Loading...</div>;  // Mostrar cargando mientras se espera la autenticación

    if (!isAuthenticated) return <div>Please log in to see the data.</div>;  // Si el usuario no está autenticado

    if (error) return <div>{error}</div>; // Mostrar el error si existe

    return (
        <>
            <nav className="navbar bg-base-100 shadow-sm flex grow gap-2">
                <div className="dropdown dropdown-bottom flex grow">
                    <div tabIndex={0} role="button" className="btn flex grow justify-start">
                        {selectedDevice} <ArrowSVG />
                    </div>
                    <ul tabIndex={0} className="dropdown-content menu bg-base-100 rounded-box z-1 w-52 p-2 shadow-sm">
                        {greenhouses.map((gh) => (
                            <li key={gh.id}>
                                <a onClick={() => setSelectedDevice(gh.name)}>{gh.name}</a>
                            </li>
                        ))}
                    </ul>
                </div>
                <button className='btn btn-primary' onClick={fetchGreenhouses}>Reload</button>
                <AddNewGH>+</AddNewGH>
            </nav>
        </>
    );
}
