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
                    <section className='flex flex-col justify-center align-middle items-center'>
                    <h1 className='my-5 uppercase text-xl font-bold'>Configure su invernadero</h1>
                    <p className='text-sm'>Mediante los siguientes formularios puede modificar automatizaciones de sus inveraderos.</p>
                    <p className='text-sm mb-10'>Es importante destacar que las configuraciones son recupearadas de forma periódica por los módulos. Según la situación de conectividad actual del invernadero, el proceso puede tardar más en efectuarse.</p>
                    <ActuatorForm>
                        <p>Configuración completa</p>
                    </ActuatorForm>

                    </section>
                    
                </div>
                <Sidebar/>
            </div>
        </>
    );
}
