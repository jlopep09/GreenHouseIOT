import Navbar from '../overlay/Navbar';
import Sidebar from '../overlay/Sidebar';

export default function Help() {
    
    return (
        <>
            <div className="drawer">
                <input id="my-drawer" type="checkbox" className="drawer-toggle" />
                <div className="drawer-content flex grow flex-col max-h-lvh overflow-hidden">
                    {/* Page content here */}
                    <Navbar/>
                </div>
                <Sidebar/>
            </div>
        </>
    );
}
