// src/components/ProtectedRoute.jsx
import { useAuth0 } from '@auth0/auth0-react'

export default function ProtectedRoute({ children }) {
  const { isAuthenticated, isLoading, loginWithRedirect } = useAuth0()

  if (isLoading) {
    return <div>Loading...</div> // puedes poner un spinner o similar
  }

  if (!isAuthenticated) {
    loginWithRedirect() // Redirige automáticamente al login
    return null
  }

  return children
}
