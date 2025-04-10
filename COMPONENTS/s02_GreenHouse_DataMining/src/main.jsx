import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import { BrowserRouter, Route, Routes } from 'react-router'
import Config from './components/views/Config.jsx'
import Params from './components/views/Params.jsx'
import Health from './components/views/Health.jsx'
import Help from './components/views/Help.jsx'
import { Auth0Provider } from '@auth0/auth0-react'
import ProtectedRoute from './components/views/ProtectedRoute.jsx'


createRoot(document.getElementById('root')).render(
      <BrowserRouter>
        <Auth0Provider
            domain="dev-tzc8kzolfvbuc2la.us.auth0.com"
            clientId="uiGcjLMNvMelgABnjD59quwYLnPz5DCm"
          authorizationParams={{
            redirect_uri: window.location.origin
          }}
        >
          <Routes>
            <Route
              path="/"
              element={
                <ProtectedRoute>
                  <App />
                </ProtectedRoute>
              }
            />
            <Route
              path="/params"
              element={
                <ProtectedRoute>
                  <Params />
                </ProtectedRoute>
              }
            />
            <Route
              path="/config"
              element={
                <ProtectedRoute>
                  <Config />
                </ProtectedRoute>
              }
            />
            <Route
              path="/health"
              element={
                <ProtectedRoute>
                  <Health />
                </ProtectedRoute>
              }
            />
            <Route
              path="/help"
              element={
                <ProtectedRoute>
                  <Help />
                </ProtectedRoute>
              }
            />
          </Routes>
        </Auth0Provider>
      </BrowserRouter>
    )
