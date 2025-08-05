import { useState, useEffect } from 'react'

export type Route = 'home' | 'profile'

// Mappa le rotte ai path URL
const routeToPath: Record<Route, string> = {
  home: '/',
  profile: '/profile'
}

// Mappa i path URL alle rotte
const pathToRoute: Record<string, Route> = {
  '/': 'home',
  '/profile': 'profile'
}

// Funzione per determinare la rotta dal path corrente
const getRouteFromPath = (path: string): Route => {
  const normalizedPath = path === '/' ? '/' : path.replace(/\/$/, '')
  return pathToRoute[normalizedPath] || 'home'
}

export const useRouter = () => {
  const [currentRoute, setCurrentRoute] = useState<Route>(() => {
    return getRouteFromPath(window.location.pathname)
  })

  useEffect(() => {
    const handleLocationChange = () => {
      const newRoute = getRouteFromPath(window.location.pathname)
      console.log('Router: Location changed - Path:', window.location.pathname, 'Route:', newRoute)
      setCurrentRoute(newRoute)
    }

    // Gestisce back/forward del browser
    window.addEventListener('popstate', handleLocationChange)

    return () => {
      window.removeEventListener('popstate', handleLocationChange)
    }
  }, [])

  const navigate = (route: Route) => {
    const path = routeToPath[route]
    console.log('Router: Navigate called - Route:', route, 'Path:', path, 'Current:', currentRoute)
    
    // Aggiorna URL e stato immediatamente
    window.history.pushState({ route }, '', path)
    setCurrentRoute(route)
    
    console.log('Router: Navigate completed - New route set to:', route)
  }

  const replace = (route: Route) => {
    const path = routeToPath[route]
    window.history.replaceState(null, '', path)
    setCurrentRoute(route)
  }

  console.log('Router: Current route state:', currentRoute)

  return {
    currentRoute,
    navigate,
    replace
  }
}
