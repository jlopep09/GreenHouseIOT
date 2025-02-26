import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import { BrowserRouter, Route, Routes } from 'react-router'
import Config from './components/views/Config.jsx'
import Params from './components/views/Params.jsx'
import Health from './components/views/Health.jsx'
import Help from './components/views/Help.jsx'


createRoot(document.getElementById('root')).render(
      <BrowserRouter>
            <Routes>
                  <Route path="/" element={<App />} />
                  <Route path="/params" element={<Params />} />
                  <Route path="/config" element={<Config />} />
                  <Route path="/health" element={<Health />} />
                  <Route path="/help" element={<Help />} />
            </Routes>
    </BrowserRouter>
)
