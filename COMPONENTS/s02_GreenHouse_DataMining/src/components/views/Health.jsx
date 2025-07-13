import { useEffect, useState } from 'react'
import Navbar from '../overlay/Navbar'
import Devicebar from '../overlay/Devicebar'
import Sidebar from '../overlay/Sidebar'

export default function Health() {
  return (
    <div className="drawer">
      <input id="my-drawer" type="checkbox" className="drawer-toggle" />
      <div className="drawer-content flex grow flex-col max-h-lvh overflow-hidden">
        {/* Page content here */}
        <Navbar />
        <Devicebar />
        <HealthContent />
      </div>
      <Sidebar />
    </div>
  )
}

const HealthContent = () => {
  return (
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
}

function ImageCard() {
  const [imageSrc, setImageSrc] = useState('')
  const [loadingImg, setLoadingImg] = useState(true)
  const [analysis, setAnalysis] = useState(null)
  const [loadingAnalysis, setLoadingAnalysis] = useState(false)
  const [error, setError] = useState(null)

  const fetchImage = async () => {
    try {
      setLoadingImg(true)
      const response = await fetch(
        `${import.meta.env.VITE_DDBB_API_IP}/db/img/last`,
        {
          method: 'GET',
          headers: {
            Authorization: `Bearer ${import.meta.env.VITE_SECRET_TOKEN}`,
          },
        }
      )

      if (!response.ok) {
        throw new Error('No se pudo obtener la imagen')
      }

      const data = await response.json()
      if (data.image_base64) {
        setImageSrc(`data:${data.mime_type};base64,${data.image_base64}`)
      } else {
        console.warn('No se encontró imagen en la respuesta')
      }
    } catch (err) {
      console.error('Error al obtener la imagen:', err)
      setError('Error cargando imagen')
    } finally {
      setLoadingImg(false)
    }
  }

  const requestRecommendation = async () => {
    try {
      setLoadingAnalysis(true)
      setError(null)
      setAnalysis(null)

      const form = new FormData()
      form.append(
        'prompt',
        'Temperatura del agua 27 grados, humedad del aire 12 porciento, tds 829'
      )
      form.append('temperature', '0.3')
      form.append('max_tokens', '1000')

      const resp = await fetch(
        `${import.meta.env.VITE_DDBB_API_IP}/db/img/forward-last`,
        {
          method: 'POST',
          headers: {
            Authorization: `Bearer ${import.meta.env.VITE_SECRET_TOKEN}`,
          },
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
  }, [])

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
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              strokeWidth="1.5"
              stroke="currentColor"
              className="w-10 h-10"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M19.5 12c0-1.232-.046-2.453-.138-3.662a4.006 4.006 0 0 0-3.7-3.7 48.678 48.678 0 0 0-7.324 0 4.006 4.006 0 0 0-3.7 3.7c-.017.22-.032.441-.046.662M19.5 12l3-3m-3 3-3-3m-12 3c0 1.232.046 2.453.138 3.662a4.006 4.006 0 0 0 3.7 3.7 48.656 48.656 0 0 0 7.324 0 4.006 4.006 0 0 0 3.7-3.7c.017-.22.032-.441.046-.662M4.5 12l3 3m-3-3-3 3"
              />
            </svg>
            <p className="text-base-300 text-sm mt-2">
              No se encontraron imágenes
            </p>
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

      {/* Recommendation section moved inside card with fixed width and wrapping */}
      {analysis && (
        <div className="px-6 py-4 bg-base-200 rounded-b-lg text-left text-sm whitespace-pre-wrap break-words">
          {analysis}
        </div>
      )}
    </div>
  )
}
