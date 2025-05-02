import React, { useState, useEffect } from 'react';
import { useAuth0 } from "@auth0/auth0-react"; 
import { Link } from 'react-router';
import Linechart from '../charts/Linechart';

const ContentCard = ({ children }) => (
    <div className="card bg-base-200 shadow-sm min-h-60 col-span-1 p-4">
        <div className='flex flex-col items-center justify-center h-full mb-2'>
            {children}
      </div>
    </div>
  );
  
  const ContentCardLarge = ({ children }) => (
    <div className="card bg-base-200 shadow-sm min-h-60 sm:col-span-2 p-4">
        <div className='flex flex-col items-center justify-center h-full mb-2'>
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
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 p-6">
        <ContentCardLarge>
          <div className="flex flex-row justify-center gap-4">
            <div className="bg-primary w-30 h-30 rounded-md"></div>
            <div className='flex flex-col align-middle justify-center items-start'>
              <strong className="block mb-1 -mt-1">Invernadero</strong>
              <p>GH {latestRead?.gh_id ?? '-'}</p>
              <p>León</p>
              <p>{latestRead ? new Date(latestRead.date).toLocaleDateString() : '-'}</p>
              <p>{latestRead ? "Conextado" : 'Sin conexión'}</p>
            </div>
          </div>
        </ContentCardLarge>
  
        <ContentCard><AirCardContent latestRead={latestRead}/></ContentCard>
        <ContentCard>
        <section className='card bg-base-200 flex flex-col justify-center'>
        <strong className="w-full text-center">Temperatura del aire</strong>
          <Linechart chartWidth={200}></Linechart>
          <button className='btn btn-link'>Ampliar</button>
        </section>
        
        
        </ContentCard>
        <ContentCard><WaterCardContent latestRead={latestRead}/></ContentCard>
        <ContentCard>
        <section className='card bg-base-200 flex flex-col justify-center'>
        <strong className="w-full text-center">Temperatura del agua</strong>
          <Linechart chartWidth={200}></Linechart>
          <button className='btn btn-link'>Ampliar</button>
        </section>
        
        
        </ContentCard>
        <ContentCardLarge>
          <div className='flex flex-col align-start justify-center items-start gap-1'>
              <strong className="block mb-2 -mt-1">Programadores</strong>
              <button className='btn btn-primary font-bold w-full'>Ventilador</button>
              <button className='btn btn-primary font-bold w-full'>Oxigenador</button>
              <button className='btn btn-neutral font-bold w-full'>Luces</button>
          </div>
        </ContentCardLarge>
        <ContentCard><TableCardContent latestRead={latestRead} title={"Luz"} readKey={"light"}/></ContentCard>
        <ContentCard><TableCardContent latestRead={latestRead} title={"Ventiladores"} readKey={"fan"}/></ContentCard>
        <ContentCard><TableCardContent latestRead={latestRead} title={"Bomba"} readKey={"pump"}/></ContentCard>
        <ContentCard><TableCardContent latestRead={latestRead} title={"Oxigenador"} readKey={"oxigen"}/></ContentCard>
        {/* Aquí podrías agregar más ContentCardLarge con gráficas, formularios, etc. */}
      </div>
    );
  };

export const TableRow = ({children, title}) => {
  const rowClassNames = "flex flex-row justify-between w-full px-5 border-t-1 border-base-400 py-1"
  const spanClassNames  = "text-lg  text-center min-w-16"
  return(
    <>
      <div className={rowClassNames}>
        <span>{title} </span>
        <span className={spanClassNames}>
        {
          children
          }
        </span>
      </div>
    </>
  )

}
export const TableCardContent = ({latestRead, title, readKey}) => {
    const { user, isAuthenticated, getAccessTokenSilently, isLoading } = useAuth0();
  
    const [greenhouses, setGreenhouses] = useState([]);
    const [selectedGhId, setSelectedGhId] = useState(null);
    const [configs, setConfigs] = useState({});
    
      useEffect(() => {
        const fetchGreenhouses = async () => {
          if (!isAuthenticated) return;
          try {
            const sub = user.sub;
            const res = await fetch(
              `${import.meta.env.VITE_DDBB_API_IP}/db/gh/`,
              {
                method: 'GET',
                headers: {
                'Authorization': `Bearer ${import.meta.env.VITE_SECRET_TOKEN}`,  // Enviar el token en el header
                'UserAuth': `${sub}`,
                },
              }
            );
            const data = await res.json();
            if (data.greenhouses.length > 0) {
                setGreenhouses(data.greenhouses);
                setSelectedGhId(data.greenhouses[0].id);
            }
          } catch (err) {
            console.error('Error fetching greenhouses:', err);
          }
        };
        fetchGreenhouses();
      }, [isAuthenticated, getAccessTokenSilently, user]);
    
      // Fetch configs cuando cambie el invernadero seleccionado
      useEffect(() => {
        const fetchConfigs = async () => {
          if (!isAuthenticated || !selectedGhId) return;
          try {
            const sub = user.sub;
            const res = await fetch(`${import.meta.env.VITE_DDBB_API_IP}/db/ghconfig/`,
                {
                  method: 'GET',
                  headers: {
                    'Authorization': `Bearer ${import.meta.env.VITE_SECRET_TOKEN}`,  // Enviar el token en el header
                    'UserAuth': `${sub}`,
                },
                }
              );
            const result = await res.json();
            const map = {};
            result.configs?.forEach(c => { map[c.name] = c; });
            setConfigs(map);
          } catch (err) {
            console.error('Error fetching actuator configs:', err);
          }
        };
        fetchConfigs();
      }, [isAuthenticated, getAccessTokenSilently, selectedGhId, user]);
  
  const cfg = configs[readKey] || {};
  return (
    <>
      <strong className="m-2">{title}</strong>
      <div className='min-w-4xs h-full'>
        <TableRow title={"Estado actual:"}>{
          (latestRead?.light_level === 'True' || latestRead?.light_level === 'False')
              ? (latestRead?.light_level === 'True' ? 'On' : 'Off') : '-'
          }</TableRow>
        <TableRow title={"Modo auto:"}>{(cfg.auto === 1 ||cfg.auto === 0)?((cfg.auto === 1)? 'Activado' : 'Desactivado'):"-"}</TableRow>
        <TableRow title={"Hora de encendido:"}>{(cfg.auto === 1 ||cfg.auto === 0)?secondsToTimeString(cfg.timer_on):"-"}</TableRow>
        <TableRow title={"Hora de apagado:"}>{(cfg.auto === 1 ||cfg.auto === 0)?secondsToTimeString(cfg.timer_off):"-"}</TableRow>
        
      </div>

    </>
  )
}
const secondsToTimeString = (seconds) => {
  if (!seconds && seconds !== 0) return null;
  
  // Asegurarse de que seconds sea un número
  const totalSeconds = parseInt(seconds, 10);
  
  const hours = Math.floor(totalSeconds / 3600);
  const minutes = Math.floor((totalSeconds % 3600) / 60);
  
  return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}`;
};
export const WaterCardContent = ({latestRead}) => {
  return (
    <>
      <strong className="m-2">Agua</strong>

      <div className=' min-w-4xs h-full'>
        <TableRow title={"Temperatura:"}>{
          (latestRead?.light_level === 'True' || latestRead?.light_level === 'False')
              ? (latestRead?.light_level === 'True' ? 'On' : 'Off') : '-'
          }</TableRow>
        <TableRow title={"TDS:"}>{
          (latestRead?.readKey === 'True' || latestRead?.readKey === 'False')
              ? (latestRead?.readKey === 'True' ? 'On' : 'Off') : '-'
          }</TableRow>
                  <TableRow title={"Necesita llenado:"}>{
          (latestRead?.readKey === 'True' || latestRead?.readKey === 'False')
              ? (latestRead?.readKey === 'True' ? 'On' : 'Off') : '-'
          }</TableRow>
          <div className='flex flex-row w-full justify-center align-middle mt-2'>
            <button className="btn btn-primary">Bomba de agua</button>
          </div>
          
      </div>

    </>
  )
}
export const AirCardContent = ({latestRead}) => {
  return (
    <>
      <strong className="m-2">Aire</strong>

      <div className=' min-w-4xs h-full'>
        <TableRow title={"Temperatura:"}>{
          (latestRead?.light_level === 'True' || latestRead?.light_level === 'False')
              ? (latestRead?.light_level === 'True' ? 'On' : 'Off') : '-'
          }</TableRow>
        <TableRow title={"Humedad:"}>{
          (latestRead?.readKey === 'True' || latestRead?.readKey === 'False')
              ? (latestRead?.readKey === 'True' ? 'On' : 'Off') : '-'
          }</TableRow>
          <div className='flex flex-row w-full justify-center align-middle mt-2'>
            <Link to='/config' className="btn btn-link font-bold text-md">Configurar ventiladores</Link>
          </div>
          
      </div>

    </>
  )
}


  