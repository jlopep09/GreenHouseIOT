import { Link } from 'react-router';
import Navbar from '../../overlay/Navbar';
import Sidebar from '../../overlay/Sidebar';

export default function Help() {
    
    return (
        <>
            <div className="drawer">
                <input id="my-drawer" type="checkbox" className="drawer-toggle" />
                <div className="drawer-content flex grow flex-col overflow-hidden">
                    {/* Page content here */}
                    <Navbar/>
                    <section className='flex flex-col justify-center align-middle items-center'>
                        <h1 className='my-5 uppercase text-2xl font-bold'>Centro de ayuda</h1>
                        <p>En esta sección podrá encontrar guías para aprender a usar la aplicación. Además se responden preguntas flecuentes realizadas por los usuarios.</p>
                        <p>Recuerde que cualquier consulta o sugerencia puede enviarla a jlopep09@estudianes.unileon.es</p>
                        <h2 className='my-5 uppercase text-l font-bold'>Preguntas frecuentes</h2>
                        <div className='card max-w-150 bg-base-100 shadow-md p-5'>
                        <Question title={"¿Qué es Ghouse?"}>GreenhouseIOT es un sistema para el monitoreo de módulos hidropónicos inteligentes.</Question>
                        <Question title={"No puedo sincronizar mi invernadero"}>Recomendamos a los usuarios consultar la guía de sincronización para resolver la mayoría de dudas frecuentes.</Question>
                        <Question title={"¿Qué se puede automatizar?"}>Actualmente puede automatizar las luces, oxigenación, bomba de agua y ventiladores.</Question>
                        <Question title={"¿Cuanto cuesta el servicio?"}>GreenhouseIOT es un servicio gratuito. El único coste que tendrá es la compra o montaje de su invernadero.</Question>
                        <Question title={"¿Como consigo un invernadero?"}>Actualmente no disponemos de compra online de invernaderos pero contacte con nosotros para guiarle en la construcción de uno desde 0</Question>
                        

                        </div>
                        <h2 className='my-5 uppercase text-l font-bold mt-10'>Guías de usuario</h2>
                        <div className='card max-w-150 bg-base-100 shadow-md p-5 mb-30 '>
                            <span className='my-1 text-sm text-center'>Trabajamos constantemente para traer nuevas funcionalidades y guías para nuestros usuarios</span>
                            <Link className="btn btn-primary uppercase text-sm font-bold" to={"/help/sync"}>Guía de sincronización</Link>

                        </div>
                    </section>
                </div>
                
                <Sidebar/>
                
            </div>
        </>
    );
}


function Question({children, title}) {
  return (
    <div className='flex flex-col justify-center align-middle items-center'>
        <span className='my-1 uppercase text-sm font-bold text-primary'>{title}</span>
        <span className='my-1 text-sm'>{children}</span>
    </div>
  )
}


