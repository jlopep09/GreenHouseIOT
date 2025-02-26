import React from 'react'
import { ArrowSVG } from '../Buttons/ThemeButton'

export default function Devicebar() {

    const selectedDevice = "GH-1-73h2"

    return (
        <>
            <nav className="navbar bg-base-100 shadow-sm flex grow gap-2">
            <div className="dropdown dropdown-bottom flex grow">
                        <div tabIndex={0} role="button" className="btn  flex grow justify-start">{selectedDevice}<ArrowSVG/> </div>
                        <ul tabIndex={0} className="dropdown-content menu bg-base-100 rounded-box z-1 w-52 p-2 shadow-sm">
                            <li><a>Item 1</a></li>
                            <li><a>Item 2</a></li>
                        </ul>
                    </div>
                    <button className='btn btn-primary'>Reload</button>
                    <button className='btn btn-primary'>+</button>
            </nav>
        </>
    )
  }

