import Layout from "./components/layout"
import { useAuth } from "./hooks/use-auth"
import { Spinner } from "./components/spinner"
import { LoginForm } from "./components/login-form"
import { RoleBasedContent } from "./components/role-based-content"

function App() {
  const { user, loading, isAuthenticated } = useAuth()

  // Mostra un loader mentre verifica l'autenticazione
  if (loading) {
    return (
      <Spinner className="flex items-center justify-center h-screen" />
    )
  }

  // Se non è autenticato, mostra il form di login
  if (!isAuthenticated) {
    return <div className="flex min-h-svh w-full items-center justify-center p-6 md:p-10">
      <div className="w-full max-w-sm">
        <LoginForm />
      </div>
    </div>
  }

  // Se è autenticato, mostra l'app principale
  return (
    <Layout>
      <div className="p-6">
        <h1 className="text-2xl font-bold mb-4">
          Benvenuto, {user?.first_name} {user?.last_name}!
        </h1>
        <div className="space-y-2 mb-6">
          <p className="text-gray-600">
            Email: {user?.email}
          </p>
          <p className="text-gray-600">
            Ruolo: {user?.role_description || user?.role_name}
          </p>
        </div>
        
        {/* Contenuto basato sui ruoli */}
        <RoleBasedContent />
      </div>
    </Layout>
  )
}

export default App