import React from 'react'
import { appName } from '../../../constants'
import { Link } from 'react-router'

export default function Sidebar () {
    return (
        <div className="drawer-side ">
            <label htmlFor="my-drawer" aria-label="close sidebar" className="drawer-overlay"/>
            <ul className="menu bg-base-200 text-base-content h-full w-80 p-4">
                {/* Sidebar content here */}
                <SidebarLinks/>
                <div className='flex flex-col justify-end grow text-neutral'>
                    <p className='ms-3 brightness-180'>© 2025 - {appName}</p>
                </div>
                
            </ul>
        </div>
    )
}
const SidebarLinks = () => {
    return (
        <li>
            <h2 className="menu-title">Navegación</h2>
            <ul>
                <li><Link to="/">General</Link></li>
                <li><Link to="/params">Parámetros</Link></li>
                <li><Link to="/health">Salud</Link></li>
            </ul>
            <h2 className="menu-title">Otros</h2>
            <ul>
                <li><Link to="/config">Configuración</Link></li>
                <li><Link to="/help">Ayuda</Link></li>
            </ul>
        </li>
    )
}