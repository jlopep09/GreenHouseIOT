import React, { useState, useEffect } from 'react';
import { ArrowSVG } from '../Buttons/ThemeButton';
import AddNewGH from '../Buttons/AddNewGH';
import { ddbbApiIp } from '../../../constants';


export default function Devicebar() {
    const [greenhouses, setGreenhouses] = useState([]);
    const [selectedDevice, setSelectedDevice] = useState('');

    const fetchGreenhouses = async () => {
        try {
            const response = await fetch(ddbbApiIp + '/db/gh/');
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
    }, []);

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
