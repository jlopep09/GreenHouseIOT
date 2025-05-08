import { Link } from "react-router";
import Navbar from "../../../overlay/Navbar";
import Sidebar from "../../../overlay/Sidebar";


export default function Sync() {
    
    return (
        <>
            <div className="drawer">
                <input id="my-drawer" type="checkbox" className="drawer-toggle" />
                <div className="drawer-content flex grow flex-col overflow-hidden">
                    {/* Page content here */}
                    <Navbar/>
                    <section className='flex flex-col justify-center align-middle items-center'>
                        <h1 className='my-5 uppercase text-2xl font-bold'>Guía de sincronización</h1>
                        <p className="mb-5">Aprenda de una forma rápida a como montar su sistema de invernaderos.</p>
                        <Step number={"1"} title={"Monta el sistema de envio"}>
                            <p className="text-gray-400">Este paso puede ser complejo si es la primera vez que lo realizas, contacte con nosotros si no consigue realizarlo. </p>
                            <p>Para que los invernaderos puedan enviar información y recibir configuraciones es necesario configurar un sistema de comunicación entre el módulo y el sistema. Para ello debe iniciar el contenedor docker con el servicio de la capa de origen. Este servicio solicita las lecturas de forma periodica a los módulo y recupera sus configuraciones. Debe modificar en el codigo el listado de invernaderos configurando correctamente sus direcciones ip locales.</p>
                        </Step>
                        <Step number={"2"} title={"Configura los invernaderos"}>
                            <p>Una vez configurado el sistema de envio es necesario configurar cada invernadero de manera individual. Si solo va a usar un invernadero puede saltarse el paso de configurar ip de la sección anterior y de esta.</p>    
                            <p>Es necesario modificar las credenciales wifi que usarán los módulos. Es necesario que el wifi sea el mismo que el usado por el sistema de envío.</p>
                            <p>Una vez haya configurado esos datos el resto de configuraciones que dispone el módulo son opcionales. Recuerde que puede acceder a un servidor web alojado por cada módulo desde su direccion ip local en http://iplocal:80/</p>
                        </Step>
                        <Step number={"3"} title={"Compruebe que se ha configurado correctamente"}>
                            <p>Para sincronizar el invernadero será necesario acceder al menu de sincronización. Debe introducir las credenciales solicitadas y tendrá su sistema funcionando.</p>
                        </Step>
                        <Link to={"/help"}> <button className="btn btn-primary">Volver</button> </Link>
                    </section>
                    
                </div>
                
                <Sidebar/>
                
            </div>
        </>
    );
}


function Step({number, title, children}) {
  return (
    <article className='flex flex-col justify-center align-middle items-center text-center mx-30 mb-10'>
        <h2 className="flex flex-row justify-center align-middle items-center">
            <span className='my-1 text-md font-bold mx-1'>{number}. </span>
            <span className='my-1 text-md font-bold uppercase'>{title}</span>
        </h2>
        <span className='my-1 text-md'>{children}</span>
    </article>
  )
}



