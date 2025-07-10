import { useEffect, useState } from 'react';
import Navbar from '../overlay/Navbar';
import Devicebar from '../overlay/Devicebar';
import Sidebar from '../overlay/Sidebar';

export default function Health() {
    return (
        <div className="drawer">
            <input id="my-drawer" type="checkbox" className="drawer-toggle" />
            <div className="drawer-content flex grow flex-col max-h-lvh overflow-hidden">
                {/* Page content here */}
                <Navbar />
                <Devicebar />
                <HealthContent></HealthContent>
            </div>
            <Sidebar />
        </div>
    );
}

const HealthContent = () => {
  return (
    <div className='flex flex-row grow justify-center overflow-auto flex-wrap'>
        <div className='flex flex-col gap-2 justify-start mx-2 my-6'>
            <h3 className='text-center'>Estado del invernadero</h3>
            <ImageCard></ImageCard>
            <p className='text-sm text-base-300 text-center'>Las imágenes se actualizan cada 24h</p>
        </div>
    </div>
  );
};

function ImageCard() {
    const [imageSrc, setImageSrc] = useState('');
    const url = `${import.meta.env.VITE_DDBB_API_IP}/db/img/last`;
    console.log("URL final que se va a usar:", url);
    const fetchImage = async () => {
        try {
            console.log(`${import.meta.env.VITE_DDBB_API_IP} esta es la variable xd`)
            const response = await fetch(`${import.meta.env.VITE_DDBB_API_IP}/db/img/last/`, {
                
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${import.meta.env.VITE_SECRET_TOKEN}`,
                },
            });

            if (!response.ok) {
                throw new Error('No se pudo obtener la imagen');
            }

            const data = await response.json();

            if (data.image_base64) {
                const base64Data = data.image_base64;
                const fullSrc = `data:image/jpeg;base64,${base64Data}`;
                setImageSrc(fullSrc);
            } else {
                console.warn('No se encontró imagen en la respuesta');
            }
        } catch (error) {
            console.error('Error al obtener la imagen:', error);
        }
    };

    useEffect(() => {
        fetchImage();
    }, []);

    return (
        <div className="card bg-base-100 w-96 shadow-sm">
            <figure className="px-10 pt-10 h-50">
                {imageSrc &&
                    <img
                    src={imageSrc || 'loading.svg'}
                    alt="Imagen del invernadero"
                    className="rounded-xl"
                    />
                }
                {!imageSrc &&
                    <div className='flex flex-col align-middle justify-center items-center'>
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-10">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 12c0-1.232-.046-2.453-.138-3.662a4.006 4.006 0 0 0-3.7-3.7 48.678 48.678 0 0 0-7.324 0 4.006 4.006 0 0 0-3.7 3.7c-.017.22-.032.441-.046.662M19.5 12l3-3m-3 3-3-3m-12 3c0 1.232.046 2.453.138 3.662a4.006 4.006 0 0 0 3.7 3.7 48.656 48.656 0 0 0 7.324 0 4.006 4.006 0 0 0 3.7-3.7c.017-.22.032-.441.046-.662M4.5 12l3 3m-3-3-3 3" />
                        </svg>
                        <p className='text-base-300 text-sm'>No se encontraron imagenes</p>
                    </div>
                  
                }
                
            </figure>
            <div className="card-body items-center text-center">
                <h2 className="card-title">Invernadero-01</h2>
                <p>Última actualización del invernadero</p>
                <div className="card-actions flex flex-row">
                    <button className="btn btn-accent btn-disabled">
                        Analizar
                    </button>
                </div>
            </div>
        </div>
    );
}
