import { useAuth } from './use-auth'
import { UserRole, hasRole, hasAnyRole, isAdmin, isFarmer, isConsumer, isRestaurantOwner } from '../lib/types'

/**
 * Hook personalizzato per la gestione dei ruoli utente
 * Fornisce funzioni utility per controllare i permessi
 */
export const useRole = () => {
  const { user } = useAuth()

  return {
    // Stato dell'utente
    user,
    userRole: user?.role_name as UserRole,
    
    // Controlli specifici per ruolo
    isAdmin: user ? isAdmin(user) : false,
    isFarmer: user ? isFarmer(user) : false,
    isConsumer: user ? isConsumer(user) : false,
    isRestaurantOwner: user ? isRestaurantOwner(user) : false,
    
    // Funzioni di controllo
    hasRole: (role: UserRole) => user ? hasRole(user, role) : false,
    hasAnyRole: (roles: UserRole[]) => user ? hasAnyRole(user, roles) : false,
    
    // Controlli di permesso specifici per le funzionalità
    canManageSystem: user ? isAdmin(user) : false,
    canSellProducts: user ? isFarmer(user) || isAdmin(user) : false,
    canBuyProducts: user ? isConsumer(user) || isRestaurantOwner(user) || isAdmin(user) : false,
    canManageRestaurant: user ? isRestaurantOwner(user) || isAdmin(user) : false,
    canOrganizeEvents: user ? hasAnyRole(user, [UserRole.WORKSHOP_HOST, UserRole.EVENT_ORGANIZER]) || isAdmin(user) : false,
  }
}

/**
 * Hook per controllare se l'utente corrente ha un ruolo specifico
 */
export const useHasRole = (role: UserRole) => {
  const { hasRole } = useRole()
  return hasRole(role)
}

/**
 * Hook per controllare se l'utente corrente ha almeno uno dei ruoli specificati
 */
export const useHasAnyRole = (roles: UserRole[]) => {
  const { hasAnyRole } = useRole()
  return hasAnyRole(roles)
}
