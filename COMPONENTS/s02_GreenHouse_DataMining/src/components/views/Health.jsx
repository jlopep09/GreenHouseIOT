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
            <h3 className='text-center'>Visión Artificial</h3>
            <ImageCard></ImageCard>
        </div>
    </div>
  );
};

function ImageCard() {
    const [imageSrc, setImageSrc] = useState('');
    
    // Función para obtener y enviar la imagen
    const fetchImage = async () => {
        try {
            // Obtener la imagen desde el primer endpoint
            const captureResponse = await fetch('http://192.168.1.202/capture');
            if (captureResponse.ok) {
                const imageBlob = await captureResponse.blob();
                const imageUrl = URL.createObjectURL(imageBlob);
                setImageSrc(imageUrl); // Establece la URL de la imagen en el estado

                // Enviar la imagen al segundo endpoint
                const formData = new FormData();
                formData.append('image', imageBlob, 'image.jpg');
                const postResponse = await fetch(`${import.meta.env.VITE_DDBB_API_IP}/db/img`,
                    {
                      method: 'POST',
                      headers: {
                        'Authorization': `Bearer ${import.meta.env.VITE_SECRET_TOKEN}`,  // Enviar el token en el header
                      },
                      body: formData,
                    }
                  );

                if (!postResponse.ok) {
                    console.error('Error al enviar la imagen al servidor');
                } else {
                    console.log('Imagen enviada correctamente');
                }
            } else {
                console.error('Error al obtener la imagen');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    };

    // Realiza la petición cuando el componente se monta
    useEffect(() => {
        fetchImage();
    }, []); // Solo se ejecuta una vez cuando el componente se monta

    return (
        <div className="card bg-base-100 w-96 shadow-sm">
            <figure className="px-10 pt-10 h-50">
                <img
                    src={imageSrc || 'loading-icon.svg'} // Imagen predeterminada si no se carga
                    alt="Imagen del invernadero"
                    className="rounded-xl"
                />
            </figure>
            <div className="card-body items-center text-center">
                <h2 className="card-title">Invernadero-01</h2>
                <p>Última actualización del invernadero</p>
                <div className="card-actions flex flex-row">
                    <button className="btn btn-accent" onClick={fetchImage}>
                        Solicitar nueva imagen
                    </button>
                    <button className="btn btn-accent btn-disabled" onClick={fetchImage}>
                        Analizar
                    </button>
                </div>
            </div>
        </div>
    );
}
