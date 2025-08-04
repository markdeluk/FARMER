/**
 * Tipi e enums condivisi nell'applicazione frontend
 */

// Enum per i ruoli utente - deve corrispondere al backend
export const UserRole = {
  ADMIN: "admin",
  FARMER: "farmer",
  CONSUMER: "consumer",
  RESTAURANT_OWNER: "restaurant_owner",
  WORKSHOP_HOST: "workshop_host",
  EVENT_ORGANIZER: "event_organizer"
} as const

export type UserRole = (typeof UserRole)[keyof typeof UserRole]

// Mappa per le descrizioni dei ruoli (per la UI)
export const ROLE_DESCRIPTIONS: Record<UserRole, string> = {
  [UserRole.ADMIN]: "Amministratore del sistema con accesso completo",
  [UserRole.FARMER]: "Produttore agricolo che vende direttamente i propri prodotti",
  [UserRole.CONSUMER]: "Utente finale che acquista prodotti dal mercato agricolo",
  [UserRole.RESTAURANT_OWNER]: "Proprietario di ristorante che acquista ingredienti freschi",
  [UserRole.WORKSHOP_HOST]: "Organizzatore di workshop ed eventi educativi",
  [UserRole.EVENT_ORGANIZER]: "Organizzatore di eventi e manifestazioni del mercato"
}

// Mappa per i nomi visualizzati dei ruoli (versione italiana user-friendly)
export const ROLE_DISPLAY_NAMES: Record<UserRole, string> = {
  [UserRole.ADMIN]: "Amministratore",
  [UserRole.FARMER]: "Agricoltore",
  [UserRole.CONSUMER]: "Consumatore",
  [UserRole.RESTAURANT_OWNER]: "Proprietario Ristorante",
  [UserRole.WORKSHOP_HOST]: "Organizzatore Workshop",
  [UserRole.EVENT_ORGANIZER]: "Organizzatore Eventi"
}

// Tipo per le informazioni utente dal backend
export interface User {
  id: number
  email: string
  first_name: string
  last_name: string
  phone: string
  is_active: boolean
  role_id: number
  role_name: UserRole
  role_description?: string
  profile_picture?: string | null
}

// Tipo per il token di autenticazione
export interface AuthToken {
  access_token: string
  token_type: string
  expires_in: number
  user: User
}

// Tipo per i dati di login
export interface LoginCredentials {
  email: string
  password: string
}

// Tipo per i dati di registrazione
export interface RegisterData {
  email: string
  password: string
  first_name: string
  last_name: string
  phone: string
  role_id: number
}

// Funzioni utility per i ruoli
export const getRoleDisplayName = (role: UserRole): string => {
  return ROLE_DISPLAY_NAMES[role] || role
}

export const getRoleDescription = (role: UserRole): string => {
  return ROLE_DESCRIPTIONS[role] || role
}

export const isAdmin = (user: User): boolean => {
  return user.role_name === UserRole.ADMIN
}

export const isFarmer = (user: User): boolean => {
  return user.role_name === UserRole.FARMER
}

export const isConsumer = (user: User): boolean => {
  return user.role_name === UserRole.CONSUMER
}

export const isRestaurantOwner = (user: User): boolean => {
  return user.role_name === UserRole.RESTAURANT_OWNER
}

export const isWorkshopHost = (user: User): boolean => {
  return user.role_name === UserRole.WORKSHOP_HOST
}

export const isEventOrganizer = (user: User): boolean => {
  return user.role_name === UserRole.EVENT_ORGANIZER
}

// Funzione per controllare se un utente ha uno specifico ruolo
export const hasRole = (user: User, role: UserRole): boolean => {
  return user.role_name === role
}

// Funzione per controllare se un utente ha uno dei ruoli specificati
export const hasAnyRole = (user: User, roles: UserRole[]): boolean => {
  return roles.includes(user.role_name)
}
