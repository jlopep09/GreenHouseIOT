import { useEffect, useState } from 'react'
import { useAuth0 } from '@auth0/auth0-react'
import Navbar from '../overlay/Navbar'
import Devicebar from '../overlay/Devicebar'
import Sidebar from '../overlay/Sidebar'

export default function Health() {
  return (
    <div className="drawer">
      <input id="my-drawer" type="checkbox" className="drawer-toggle" />
      <div className="drawer-content flex grow flex-col max-h-lvh overflow-hidden">
        <Navbar />
        <Devicebar />
        <HealthContent />
      </div>
      <Sidebar />
    </div>
  )
}

const HealthContent = () => (
  <div className="flex flex-row grow justify-center overflow-auto flex-wrap">
    <div className="flex flex-col gap-2 justify-start mx-2 my-6">
      <h3 className="text-center">Estado del invernadero</h3>
      <ImageCard />
      <p className="text-sm text-base-300 text-center">
        Las imágenes se actualizan cada 24h
      </p>
    </div>
  </div>
)

function ImageCard() {
  const { user, isAuthenticated } = useAuth0()
  const [imageSrc, setImageSrc] = useState('')
  const [loadingImg, setLoadingImg] = useState(true)
  const [analysis, setAnalysis] = useState(null)
  const [loadingAnalysis, setLoadingAnalysis] = useState(false)
  const [error, setError] = useState(null)

  // Fetch latest image
  const fetchImage = async () => {
    try {
      setLoadingImg(true)
      const response = await fetch(
        `${import.meta.env.VITE_DDBB_API_IP}/db/img/last`,
        {
          method: 'GET',
          headers: { Authorization: `Bearer ${import.meta.env.VITE_SECRET_TOKEN}` },
        }
      )
      if (!response.ok) throw new Error('No se pudo obtener la imagen')
      const data = await response.json()
      setImageSrc(
        data.image_base64
          ? `data:${data.mime_type};base64,${data.image_base64}`
          : ''
      )
    } catch (err) {
      console.error('Error al obtener la imagen:', err)
      setError('Error cargando imagen')
    } finally {
      setLoadingImg(false)
    }
  }

  // Fetch latest reading raw
  const fetchLatestReadRaw = async () => {
    const sub = user.sub
    const resp = await fetch(
      `${import.meta.env.VITE_DDBB_API_IP}/db/reads/`,
      {
        method: 'GET',
        headers: {
          Authorization: `Bearer ${import.meta.env.VITE_SECRET_TOKEN}`,
          UserAuth: sub,
        },
      }
    )
    const resData = await resp.json()
    if (!resData.reads?.length) throw new Error('No hay lecturas disponibles')
    // Seleccionar la más reciente
    return resData.reads.reduce((prev, curr) =>
      new Date(prev.date) > new Date(curr.date) ? prev : curr
    )
  }

  const requestRecommendation = async () => {
    try {
      setLoadingAnalysis(true)
      setError(null)
      setAnalysis(null)

      // Obtener última lectura y usarla sin editar como prompt
      const latestRead = await fetchLatestReadRaw()
      console.log("Solicitando recomendacion con estos datos: "+latestRead)
      const promptRaw = JSON.stringify(latestRead)

      const form = new FormData()
      form.append('prompt', promptRaw)
      form.append('temperature', '0.3')
      form.append('max_tokens', '500')

      const resp = await fetch(
        `${import.meta.env.VITE_DDBB_API_IP}/db/img/forward-last`,
        {
          method: 'POST',
          headers: { Authorization: `Bearer ${import.meta.env.VITE_SECRET_TOKEN}` },
          body: form,
        }
      )
      if (!resp.ok) {
        const text = await resp.text()
        throw new Error(text || 'Error en el servicio de recomendación')
      }
      const result = await resp.json()
      setAnalysis(result.analysis || result.response || JSON.stringify(result))
    } catch (err) {
      console.error('Error al solicitar recomendación:', err)
      setError('Error al solicitar recomendación')
    } finally {
      setLoadingAnalysis(false)
    }
  }

  useEffect(() => {
    fetchImage()
  }, [isAuthenticated])

  return (
    <div className="card bg-base-100 w-96 shadow-sm mx-auto">
      <figure className="px-10 pt-10 h-50 flex items-center justify-center">
        {loadingImg ? (
          <span className="loading loading-spinner text-primary" />
        ) : imageSrc ? (
          <img
            src={imageSrc}
            alt="Imagen del invernadero"
            className="rounded-xl max-h-48 object-contain"
          />
        ) : (
          <div className="flex flex-col items-center">
            {/* Icono y mensaje de sin imagen */}
          </div>
        )}
      </figure>

      <div className="card-body items-center text-center">
        <h2 className="card-title">Invernadero-01</h2>
        <p>Última actualización del invernadero</p>
        <div className="card-actions flex flex-col gap-2">
          <button
            className="btn btn-accent"
            onClick={requestRecommendation}
            disabled={loadingImg || loadingAnalysis || !imageSrc}
          >
            {loadingAnalysis ? 'Solicitando...' : 'Solicitar recomendación'}
          </button>
          {error && <p className="text-error text-sm">{error}</p>}
        </div>
      </div>

      {analysis && (
        <div className="px-6 py-4 bg-base-200 rounded-b-lg text-left text-sm whitespace-pre-wrap break-words">
          {analysis}
        </div>
      )}
    </div>
  )
}
