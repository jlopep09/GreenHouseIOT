
import { ThemeButton } from '../Buttons/ThemeButton'
import LogoutButton from '../accounts/LogoutButton'
import Logo from '../atoms/Logo'
import ThemeModeButton from '../Buttons/ThemeModeButton'
import { Link } from 'react-router'
import React, { useState, useRef, useEffect } from 'react';

export default function Navbar() {

    return (
        <>
            <header className="navbar bg-base-100 shadow-sm border-b-1 border-b-base-200">
                <nav className="navbar-start">
                    <DrawerIcon/>
                    <Link className="btn btn-ghost text-xl" to='/'><Logo/></Link>
                </nav>
                <h1 className="navbar-center">
                    
                </h1>
                <nav className="navbar-end gap-1">
                    <ThemeModeButton></ThemeModeButton>
                    <NotificationMenu/>
                    <ProfileButtonDropdown></ProfileButtonDropdown>
                </nav>
            </header>
        </>
    )
  }
  const NotificationMenu = () => {
    const [open, setOpen] = useState(false);
    const dropdownRef = useRef(null);
  
    // Cierra el dropdown si se hace clic fuera
    useEffect(() => {
      const handleClickOutside = (event) => {
        if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
          setOpen(false);
        }
      };
      document.addEventListener('mousedown', handleClickOutside);
      return () => {
        document.removeEventListener('mousedown', handleClickOutside);
      };
    }, []);
  
    return (
      <div ref={dropdownRef} className={`dropdown dropdown-end ${open ? 'dropdown-open' : ''}`}>
        <button
          className="btn btn-ghost btn-circle"
          onClick={() => setOpen((prev) => !prev)}
        >
          <div className="indicator">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none"
              viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2"
                d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 
                10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 
                1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
            </svg>
          </div>
        </button>
  
        {open && (
          <ul className="dropdown-content menu bg-base-100 rounded-box z-1 w-82 p-2 shadow-sm">
            <li className="menu-title p-4 pb-2 text-xs opacity-60 tracking-wide">Notificaciones</li>
            <NotificationElement title={"Bienvenido"}>
              Bienvenido a GreenhouseIOT. Si encuentra alguna dificultad de uso le recomendamos que visite el link "Ayuda" desde el desplegable izquierdo
            </NotificationElement>
            <NotificationElement title={"Novedad"}>
              Nos complace anunciar la implementación del modo oscuro. Puede probarlo haciendo click en el icono sol/luna junto al botón de notificaciones.
            </NotificationElement>
          </ul>
        )}
      </div>
    );
  };
const NotificationElement = ({children, title}) =>{
    return (
        <li>
            <div className='flex flex-row align-middle'>
                <div className="text-xs uppercase font-semibold opacity-60">{title}</div>
                <p className="list-col-wrap text-xs">
                {children}
                </p>
                <button className="btn btn-square btn-ghost hidden">
                    <svg className="size-[1.2em]" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><g strokeLinejoin="round" strokeLinecap="round" strokeWidth="2" fill="none" stroke="currentColor"><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"></path></g></svg>
                </button>
            </div>
        </li>
    )
}

const SearchIcon = () =>{
    return(                    
        <button className="btn btn-ghost btn-circle">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"> <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /> </svg>
        </button>)
}
const DrawerIcon = () =>{
    return(
        <label htmlFor="my-drawer" className="btn btn-ghost text-xl drawer-button">                        
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"> <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h7" /> </svg> 
        </label> )
}

export const UserSVG = () => {
    return (
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor" className="size-6">
        <path strokeLinecap="round" strokeLinejoin="round" d="M17.982 18.725A7.488 7.488 0 0 0 12 15.75a7.488 7.488 0 0 0-5.982 2.975m11.963 0a9 9 0 1 0-11.963 0m11.963 0A8.966 8.966 0 0 1 12 21a8.966 8.966 0 0 1-5.982-2.275M15 9.75a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
        </svg>

    )
  }
  
  
  export const ProfileButtonDropdown = () => {
    return(
      <div className="flex-none">
        <div className="dropdown dropdown-end">
          {/* Eliminamos la clase avatar que podría estar causando conflictos */}
          <button 
            tabIndex={0} 
            className="btn btn-ghost btn-circle overflow-hidden focus:outline-none"
            style={{ transition: "all 0.3s ease" }}
          >
            <div className="flex items-center justify-center w-full h-full">
              <UserSVG />
            </div>
          </button>
          <ul
            className="menu menu-sm dropdown-content bg-base-100 rounded-box z-1 mt-3 w-32 p-2 shadow">
            <li>
              <Link className="justify-center hidden">
                <p className='text-center'>Perfil</p>
              </Link>
            </li>
            <li className="justify-center"><LogoutButton></LogoutButton></li>
          </ul>
        </div>
      </div>
    )
  }


