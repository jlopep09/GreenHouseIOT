import Navbar from '../overlay/Navbar';
import Devicebar from '../overlay/Devicebar';
import Sidebar from '../overlay/Sidebar';
import ActuatorForm from '../atoms/ActuatorForm';



export default function Config() {
    
    return (
        <>
            <div className="drawer">
                <input id="my-drawer" type="checkbox" className="drawer-toggle" />
                <div className="drawer-content flex grow flex-col max-h-lvh overflow-hidden">
                    {/* Page content here */}
                    <Navbar/>
                    <Devicebar/>
                    <ActuatorForm>
                        <p>Config</p>
                    </ActuatorForm>
                </div>
                <Sidebar/>
            </div>
        </>
    );
}
