import Layout from "./components/layout"
import { useAuth } from "./hooks/use-auth"
import { useRouter } from "./hooks/use-router"
import { Spinner } from "./components/spinner"
import { LoginForm } from "./components/login-form"
import { UserInfoCard } from "./components/user-info-card"
import { RoleBasedContent } from "./components/role-based-content"
import { ProfilePage } from "./components/profile-page"
import { NotificationManager } from "./components/notification-manager"
import { useTranslation } from "./lib/i18n"

function App() {
  const { user, loading, isAuthenticated } = useAuth()
  const { currentRoute, navigate } = useRouter()
  const { t } = useTranslation(user?.language)

  console.log('App: Component rendered with route:', currentRoute)

  console.log('App: Rendering with route:', currentRoute)

  // Mostra un loader mentre verifica l'autenticazione
  if (loading) {
    return (
      <NotificationManager>
        <Spinner className="flex items-center justify-center h-screen" />
      </NotificationManager>
    )
  }

  // Se non è autenticato, mostra il form di login
  if (!isAuthenticated) {
    return (
      <NotificationManager>
        <div className="flex min-h-svh w-full items-center justify-center p-6 md:p-10">
          <div className="w-full max-w-sm">
            <LoginForm />
          </div>
        </div>
      </NotificationManager>
    )
  }

  // Renderizza la pagina in base alla route
  const renderPage = () => {
    console.log('App: renderPage called with route:', currentRoute)
    switch (currentRoute) {
      case 'profile':
        console.log('App: Rendering ProfilePage')
        return <ProfilePage />
      case 'home':
      default:
        console.log('App: Rendering Home page')
        return (
          <div className="space-y-6">
            <div className="flex flex-col space-y-4">
              <h1 className="text-3xl font-bold">
                {t('welcome')}, {user?.first_name} {user?.last_name}!
              </h1>
              
              <div className="mb-4">
                <button 
                  onClick={() => navigate('profile')}
                  className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
                >
                  Vai al Profilo (Test)
                </button>
              </div>
              
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <UserInfoCard />
                <div className="space-y-4">
                  <RoleBasedContent />
                </div>
              </div>
            </div>
          </div>
        )
    }
  }

  // Se è autenticato, mostra l'app principale con routing
  return (
    <NotificationManager>
      <Layout key={currentRoute}>
        {renderPage()}
      </Layout>
    </NotificationManager>
  )
}

export default App