import React, { useState, useEffect } from 'react';
import { useAuth0 } from "@auth0/auth0-react"; 

export const Content = () => {
    const [latestRead, setLatestRead] = useState(null);
    const { user, isAuthenticated, getAccessTokenSilently, isLoading } = useAuth0();
    useEffect(() => {
        const fetchLatestRead = async () => {
            if (!isAuthenticated) return;
            try {
                const token = await getAccessTokenSilently();
                const sub = user.sub;
                const response = await fetch(`${import.meta.env.VITE_DDBB_API_IP}/db/reads/`,
                    {
                      method: 'GET',
                      headers: {
                        'Authorization': `Bearer ${import.meta.env.VITE_SECRET_TOKEN}`,  // Enviar el token en el header
                        'UserAuth': `${sub}`,
                      },
                    }
                  );
                const data = await response.json();
                if (data.reads && data.reads.length > 0) {
                    const latest = data.reads.reduce((prev, current) => 
                        new Date(prev.date) > new Date(current.date) ? prev : current
                    );
                    setLatestRead(latest);
                }
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        };

        fetchLatestRead();
    }, [isAuthenticated, getAccessTokenSilently]);
    if (isLoading) return <div>Loading...</div>; // Si estamos esperando que se cargue el estado de autenticación

    if (!isAuthenticated) return <div>Please log in to see the data.</div>; // Si el usuario no está autenticado

    return (
        <div className='flex flex-row grow justify-center overflow-auto flex-wrap'>
            <div className='flex flex-col gap-2 justify-start mx-2 my-6'>
                <ContentCard>
                    <div className='flex flex-row justify-center gap-4'>
                        <div className='bg-primary w-30 h-30'></div>
                        <div>
                            <strong className='m-2'>Invernadero</strong>
                            <p>GH {(latestRead?.gh_id)? '-' : ''} {latestRead?.gh_id || ''} </p>
                            <p>León</p>
                            <p>{latestRead ? new Date(latestRead.date).toLocaleDateString() : '-'}</p>
                            <p>Conectado</p>
                        </div>
                    </div>
                </ContentCard>
                <ContentCard>
                    <div className='flex flex-col gap-4 items-center mb-2'>
                        <strong className='m-2'>Luz</strong>
                        <p className='text-2xl btn btn-outline w-30'>{
                            (latestRead?.light_level === 'True' || latestRead?.light_level === 'False') ?
                        (latestRead?.light_level === 'True' ? 'On' : 'Off') : '-'
                        }</p>
                    </div>
                </ContentCard>
                <ContentCard>
                    <div className='flex flex-col gap-4 items-center mb-2'>
                        <strong className='m-2'>TDS</strong>
                        <p className='text-2xl btn btn-outline w-30'>{latestRead?.tds?? '-'}</p>
                    </div>
                </ContentCard>

            </div>
            <div className='flex flex-col gap-2 justify-start mx-2 my-6'>
                
                <ContentCard>
                    <div className='flex flex-col gap-4 items-center mb-2'>
                        <strong className='m-2'>Nivel de agua</strong>
                        <p className='text-2xl btn btn-outline w-30'>{latestRead?.water_level ?? '-'}%</p>
                    </div>
                </ContentCard>
                <ContentCard>
                    <div className='flex flex-col gap-4 items-center mb-2'>
                        <strong className='m-2'>Humedad del aire</strong>
                        <p className='text-2xl btn btn-outline w-30'>{latestRead?.humidity ?? '-'}%</p>
                    </div>
                </ContentCard>
                <ContentCard>
                    <div className='flex flex-col gap-4 items-center mb-2'>
                        <strong className='m-2'>Temperatura del agua</strong>
                        <p className='text-2xl btn btn-outline w-30'>{latestRead?.water_temperature?? '-'}</p>
                    </div>
                </ContentCard>
            </div>
            <div className='flex flex-col gap-2 justify-start mx-2 my-6'>
                
                <ContentCard>
                    <div className='flex flex-col gap-4 items-center mb-2'>
                        <strong className='m-2'>Temperatura</strong>
                        <p className='text-2xl btn btn-outline w-30'>{latestRead?.temperature ?? '-'}ºC</p>
                    </div>
                </ContentCard>
                {//<ContentCard>
                    //<div className='flex flex-col gap-4 items-center mb-2'>
                        //<strong className='m-2'>Ventiladores</strong>
                        //<p className='text-2xl btn btn-outline w-30'>Off</p>
                    //</div>
                //</ContentCard>
                }
            </div>
        </div>
    );
};

const ContentCard = ({ children }) => {
    return (
        <div className='card bg-base-300 shadow-sm min-h-60 w-100 col-span-2 justify-center text-center'>
            {children}
        </div>
    );
};