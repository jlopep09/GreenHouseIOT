import React, { useState, useEffect } from 'react';
import { useAuth0 } from "@auth0/auth0-react"; 

const ContentCard = ({ children }) => (
    <div className="card bg-base-200 shadow-sm min-h-60 col-span-1 p-4">
        <div className='flex flex-col items-center justify-center gap-2 h-full mb-2'>
            {children}
      </div>
    </div>
  );
  
  const ContentCardLarge = ({ children }) => (
    <div className="card bg-base-200 shadow-sm min-h-60 col-span-2 p-4">
        <div className='flex flex-col items-center justify-center gap-2 h-full mb-2'>
            {children}
        </div>
    </div>
  );
  
  export const Content = () => {
    const [latestRead, setLatestRead] = useState(null);
    const { user, isAuthenticated, getAccessTokenSilently, isLoading } = useAuth0();
  
    useEffect(() => {
      const fetchLatestRead = async () => {
        if (!isAuthenticated) return;
        try {
          const token = await getAccessTokenSilently();
          const sub = user.sub;
          const response = await fetch(`${import.meta.env.VITE_DDBB_API_IP}/db/reads/`, {
            method: 'GET',
            headers: {
              'Authorization': `Bearer ${import.meta.env.VITE_SECRET_TOKEN}`,
              'UserAuth': `${sub}`,
            },
          });
          const data = await response.json();
          if (data.reads?.length > 0) {
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
  
    if (isLoading) return <div>Loading...</div>;
    if (!isAuthenticated) return <div>Please log in to see the data.</div>;
  
    return (
      <div className="grid grid-cols-2 md:grid-cols-2 lg:grid-cols-4 gap-4 p-6">
        <ContentCardLarge>
          <div className="flex flex-row justify-center gap-4">
            <div className="bg-primary w-20 h-20 rounded-full"></div>
            <div>
              <strong className="block mb-1">Invernadero</strong>
              <p>GH {latestRead?.gh_id ?? '-'}</p>
              <p>León</p>
              <p>{latestRead ? new Date(latestRead.date).toLocaleDateString() : '-'}</p>
              <p>Conectado</p>
            </div>
          </div>
        </ContentCardLarge>
  
        <ContentCard>
          
            <strong className="m-2">Luz</strong>
            <p className="text-2xl btn btn-outline w-30">
                {
                (latestRead?.light_level === 'True' || latestRead?.light_level === 'False')
                    ? (latestRead?.light_level === 'True' ? 'On' : 'Off') : '-'
                }
            </p>
          
        </ContentCard>
  
        <ContentCard>
          <strong className="m-2">TDS</strong>
          <p className="text-2xl btn btn-outline w-30">{latestRead?.tds ?? '-'}</p>
        </ContentCard>
  
        <ContentCard>
          <strong className="m-2">Nivel de agua</strong>
          <p className="text-2xl btn btn-outline w-30">{latestRead?.water_level ?? '-'}%</p>
        </ContentCard>
  
        <ContentCard>
          <strong className="m-2">Humedad del aire</strong>
          <p className="text-2xl btn btn-outline w-30">{latestRead?.humidity ?? '-'}%</p>
        </ContentCard>
  
        <ContentCard>
          <strong className="m-2">Temperatura</strong>
          <p className="text-2xl btn btn-outline w-30">{latestRead?.temperature ?? '-'}ºC</p>
        </ContentCard>
  
        <ContentCard>
          <strong className="m-2">Temperatura del agua</strong>
          <p className="text-2xl btn btn-outline w-30">{latestRead?.water_temperature ?? '-'}</p>
        </ContentCard>
  
        {/* Aquí podrías agregar más ContentCardLarge con gráficas, formularios, etc. */}
      </div>
    );
  };
  