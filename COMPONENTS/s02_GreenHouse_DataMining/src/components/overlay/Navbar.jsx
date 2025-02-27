import React from 'react'
import { ThemeButton } from '../Buttons/ThemeButton'
import { appName } from '../../../constants'


export default function Navbar() {

    return (
        <>
            <header className="navbar bg-base-100 shadow-sm">
                <nav className="navbar-start">
                    <DrawerIcon/>
                </nav>
                <h1 className="navbar-center">
                    <a className="btn btn-ghost text-xl">{appName}</a>
                </h1>
                <nav className="navbar-end">
                    <SearchIcon/>
                    <ThemeButton/>
                    <NotificationMenu/>
                </nav>
            </header>
        </>
    )
  }
const NotificationMenu = () =>{
    return(   
        <div className="dropdown dropdown-end">
            <button className="btn btn-ghost btn-circle">
                <div className="indicator">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"> <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" /> </svg>
                    <span className="badge badge-xs badge-primary indicator-item"></span>
                </div>
            </button>
        <ul className="dropdown-content menu bg-base-100 rounded-box z-1 w-82 p-2 shadow-sm">
        
            <li className="menu-title p-4 pb-2 text-xs opacity-60 tracking-wide">Notificaciones</li>
            <NotificationElement/>
            <NotificationElement/>

        </ul>
        </div>                 
        )
}
const NotificationElement = () =>{
    return (
        <li>
            <div className='flex flex-row align-middle'>
                <div className="text-xs uppercase font-semibold opacity-60">Remaining Reason</div>
                <p className="list-col-wrap text-xs">
                Bienvenido a GreenhouseIOT. Si encuentra alguna dificultad de uso le recomendamos que visite el link "Ayuda" desde el desplegable iquierdo
                </p>
                <button className="btn btn-square btn-ghost">
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

