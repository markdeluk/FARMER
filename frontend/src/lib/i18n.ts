import type { Language } from './types'

// Dizionario delle traduzioni
export const translations = {
  it: {
    // Common
    welcome: "Benvenuto",
    email: "Email",
    password: "Password",
    login: "Accedi",
    logout: "Esci",
    language: "Lingua",
    role: "Ruolo",
    phone: "Telefono",
    activeAccount: "Account attivo",
    yes: "Sì",
    no: "No",
    home: "Home",
    inbox: "Posta",
    calendar: "Calendario",
    search: "Cerca",
    settings: "Impostazioni",
    getHelp: "Aiuto",
    account: "Account",
    notifications: "Notifiche",
    application: "Applicazione",
    guestUser: "Utente Ospite",
    profile: "Profilo",
    
    // User info
    roleId: "ID Ruolo",
    userInfo: "Informazioni Utente",
    
    // Language selector
    selectLanguage: "Seleziona lingua",
    italian: "Italiano",
    english: "Inglese",
    languageUpdated: "Lingua aggiornata con successo",
    
    // Login form
    loginToAccount: "Accedi al tuo account",
    enterEmailToLogin: "Inserisci la tua email per accedere al tuo account",
    emailPlaceholder: "m@example.com",
    forgotPassword: "Hai dimenticato la password?",
    loggingIn: "Accesso in corso...",
    dontHaveAccount: "Non hai un account?",
    signUp: "Registrati",
    logOut: "Esci",
    
    // Role-based content
    availableFunctionality: "Funzionalità Disponibili",
    adminPanel: "Pannello Amministrazione",
    fullSystemManagement: "Gestione completa del sistema",
    manageUsers: "Gestisci Utenti",
    configurations: "Configurazioni",
    salesPanel: "Pannello Vendita",
    manageProducts: "Gestisci i tuoi prodotti",
    addProduct: "Aggiungi Prodotto",
    manageInventory: "Gestisci Inventario",
    purchasePanel: "Pannello Acquisti", 
    buyFreshProducts: "Acquista prodotti freschi",
    browseProducts: "Sfoglia Prodotti",
    cart: "Carrello",
    restaurantPanel: "Pannello Ristorante",
    manageRestaurantBookings: "Gestisci ristorante e prenotazioni",
    manageMenu: "Gestisci Menu",
    bookings: "Prenotazioni",
    eventsPanel: "Pannello Eventi",
    organizeEvents: "Organizza workshop e eventi",
    createEvent: "Crea Evento",
    manageWorkshops: "Gestisci Workshop",
    roleInfo: "Informazioni Ruolo",
    currentRole: "Ruolo corrente",
    isAdmin: "È Admin",
    isFarmer: "È Farmer",
    isConsumer: "È Consumer",
    isRestaurantOwner: "È Restaurant Owner",
    
    // Settings page
    settingsPageTitle: "Impostazioni",
    settingsPageDescription: "Gestisci le tue preferenze e impostazioni dell'account",
    generalSettings: "Impostazioni Generali",
    
    // Profile page
    profilePageTitle: "Profilo",
    profilePageDescription: "Gestisci le informazioni del tuo profilo e le preferenze",
    profileSettings: "Impostazioni Profilo",
    personalInfo: "Informazioni Personali",
    languageSettings: "Lingua",
    languageSettingsDescription: "Seleziona la tua lingua preferita per l'interfaccia",
    selectLanguageDropdown: "Seleziona lingua...",
    currentLanguage: "Lingua attuale",
    saveChanges: "Salva modifiche",
    settingsSaved: "Impostazioni salvate con successo",
    savingSettings: "Salvataggio in corso...",
    
    // Roles
    roles: {
      admin: "Amministratore",
      farmer: "Agricoltore", 
      consumer: "Consumatore",
      restaurant_owner: "Proprietario Ristorante",
      workshop_host: "Organizzatore Workshop",
      event_organizer: "Organizzatore Eventi"
    },
    
    // Role descriptions
    roleDescriptions: {
      admin: "Amministratore del sistema con accesso completo",
      farmer: "Produttore agricolo che vende direttamente i propri prodotti",
      consumer: "Utente finale che acquista prodotti dal mercato agricolo", 
      restaurant_owner: "Proprietario di ristorante che acquista ingredienti freschi",
      workshop_host: "Organizzatore di workshop ed eventi educativi",
      event_organizer: "Organizzatore di eventi e manifestazioni del mercato"
    },
    
    // Errors
    errors: {
      loginFailed: "Errore durante l'accesso",
      invalidCredentials: "Email o password non corretti",
      networkError: "Errore di rete"
    }
  },
  
  en: {
    // Common
    welcome: "Welcome",
    email: "Email", 
    password: "Password",
    login: "Login",
    logout: "Logout",
    language: "Language",
    role: "Role",
    phone: "Phone",
    activeAccount: "Active account",
    yes: "Yes",
    no: "No",
    home: "Home",
    inbox: "Inbox",
    calendar: "Calendar",
    search: "Search",
    settings: "Settings",
    getHelp: "Get Help",
    account: "Account",
    notifications: "Notifications",
    application: "Application",
    guestUser: "Guest User",
    profile: "Profile",
    
    // User info
    roleId: "Role ID",
    userInfo: "User Information",
    
    // Language selector  
    selectLanguage: "Select language",
    italian: "Italian",
    english: "English",
    languageUpdated: "Language updated successfully",
    
    // Login form
    loginToAccount: "Login to your account",
    enterEmailToLogin: "Enter your email below to login to your account",
    emailPlaceholder: "m@example.com",
    forgotPassword: "Forgot your password?",
    loggingIn: "Logging in...",
    dontHaveAccount: "Don't have an account?",
    signUp: "Sign up",
    logOut: "Log out",
    
    // Role-based content
    availableFunctionality: "Available Functionality",
    adminPanel: "Administration Panel",
    fullSystemManagement: "Complete system management",
    manageUsers: "Manage Users",
    configurations: "Configurations",
    salesPanel: "Sales Panel",
    manageProducts: "Manage your products",
    addProduct: "Add Product",
    manageInventory: "Manage Inventory",
    purchasePanel: "Purchase Panel", 
    buyFreshProducts: "Buy fresh products",
    browseProducts: "Browse Products",
    cart: "Cart",
    restaurantPanel: "Restaurant Panel",
    manageRestaurantBookings: "Manage restaurant and bookings",
    manageMenu: "Manage Menu",
    bookings: "Bookings",
    eventsPanel: "Events Panel",
    organizeEvents: "Organize workshops and events",
    createEvent: "Create Event",
    manageWorkshops: "Manage Workshops",
    roleInfo: "Role Information",
    currentRole: "Current role",
    isAdmin: "Is Admin",
    isFarmer: "Is Farmer",
    isConsumer: "Is Consumer",
    isRestaurantOwner: "Is Restaurant Owner",
    
    // Settings page
    settingsPageTitle: "Settings",
    settingsPageDescription: "Manage your account preferences and settings",
    generalSettings: "General Settings",
    
    // Profile page
    profilePageTitle: "Profile",
    profilePageDescription: "Manage your profile information and preferences",
    profileSettings: "Profile Settings",
    personalInfo: "Personal Information",
    languageSettings: "Language",
    languageSettingsDescription: "Select your preferred language for the interface",
    selectLanguageDropdown: "Select language...",
    currentLanguage: "Current language",
    saveChanges: "Save changes",
    settingsSaved: "Settings saved successfully",
    savingSettings: "Saving...",
    
    // Roles
    roles: {
      admin: "Administrator",
      farmer: "Farmer",
      consumer: "Consumer", 
      restaurant_owner: "Restaurant Owner",
      workshop_host: "Workshop Host",
      event_organizer: "Event Organizer"
    },
    
    // Role descriptions
    roleDescriptions: {
      admin: "System administrator with full access",
      farmer: "Agricultural producer selling their own products directly",
      consumer: "End user purchasing products from the farmers' market",
      restaurant_owner: "Restaurant owner buying fresh ingredients", 
      workshop_host: "Host of workshops and educational events",
      event_organizer: "Organizer of market events and activities"
    },
    // Errors
    errors: {
      loginFailed: "Login failed",
      invalidCredentials: "Invalid credentials",
      networkError: "Network error"
    }
  }
} as const

export type TranslationKey = keyof typeof translations.it

// Funzione per ottenere la traduzione
export const t = (key: string, language: Language = 'it'): string => {
  const keys = key.split('.')
  let value: any = translations[language]
  
  for (const k of keys) {
    value = value?.[k]
  }
  
  return value || key
}

// Hook per le traduzioni che legge la lingua dall'utente
export const useTranslation = (userLanguage: Language = 'it') => {
  return {
    t: (key: string) => t(key, userLanguage),
    language: userLanguage
  }
}
