import {useState} from 'react';
import Navbar from './components/overlay/Navbar';
import Sidebar from './components/overlay/Sidebar';
import Devicebar from './components/overlay/Devicebar';
import { Content } from './components/overlay/Content';


export default function App() {
    
    return (
        <>
            <div className="drawer">
                <input id="my-drawer" type="checkbox" className="drawer-toggle" />
                <div className="drawer-content flex grow flex-col max-h-lvh overflow-hidden">
                    {/* Page content here */}
                    <Navbar/>
                    <Devicebar/>
                    <Content/>
                </div>
                <Sidebar/>
            </div>
        </>
    );
}
