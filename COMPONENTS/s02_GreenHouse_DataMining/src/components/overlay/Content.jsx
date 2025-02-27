import React, { Children } from 'react'

export const Content = () => {
  return (
    <div className='flex flex-row grow justify-center overflow-auto flex-wrap'>
        <div className='flex flex-col  gap-2 justify-start mx-2 my-6'>
            <h3 className='text-center'>Section</h3>
            <ContentCard>

                <div className='flex flex-row justify-center gap-4'>
                    <div className='bg-primary w-30 h-30'></div>
                    <div>
                        <strong className='m-2'>Invernadero</strong>
                        <p>GH-1-73h2</p>
                        <p>León</p>
                        <p>17/01/2025</p>
                        <p>Conectado</p>
                    </div>
                </div>
            </ContentCard>
            <ContentCard>
                <div className='flex flex-col gap-4 items-center mb-2'>
                    <strong className='m-2'>Luz</strong>
                    <p className='text-2xl btn btn-outline w-30'>On</p>
                </div>
            </ContentCard>

        </div>
        <div className='flex flex-col  gap-2 justify-start mx-2 my-6'>
        <h3 className='text-center'>Section</h3>
        <ContentCard>
                <div className='flex flex-col gap-4 items-center mb-2'>
                    <strong className='m-2'>Nivel de agua</strong>
                    <p className='text-2xl btn btn-outline w-30'>72%</p>
                </div>
            </ContentCard>
            <ContentCard>
                <div className='flex flex-col gap-4 items-center mb-2'>
                    <strong className='m-2'>Humedad del sustrato</strong>
                    <p className='text-2xl btn btn-outline w-30'>23%</p>
                </div>
            </ContentCard>

        </div>
        <div className='flex flex-col  gap-2 justify-start mx-2 my-6'>
        <h3 className='text-center'>Section</h3>
        <ContentCard>
                <div className='flex flex-col gap-4 items-center mb-2'>
                    <strong className='m-2'>Temperatura</strong>
                    <p className='text-2xl btn btn-outline w-30'>21ºC</p>
                </div>

            </ContentCard>
            <ContentCard>

                <div className='flex flex-col gap-4 items-center mb-2'>
                    <strong className='m-2'>Ventiladores</strong>
                    <p className='text-2xl btn btn-outline w-30'>Off</p>
                </div>
            </ContentCard>
        </div>
    </div>

  )
}
const ContentCard = ({children}) =>{
    return (
        <div className='card bg-base-300 shadow-sm min-h-60 w-100 col-span-2 justify-center text-center'>
            {children}
        </div>
    )
}
