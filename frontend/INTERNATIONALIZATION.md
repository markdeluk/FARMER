# Sistema di Internazionalizzazione (i18n)

Questo progetto implementa un sistema completo di internazionalizzazione che supporta italiano (it) e inglese (en).

## Struttura

### File principali:
- `/src/lib/i18n.ts` - Dizionario delle traduzioni e hook principale
- `/src/lib/translation-utils.ts` - Utility per traduzioni dinamiche e specializzate
- `/src/components/language-selector.tsx` - Componente per cambiare lingua
- `/src/components/notification-manager.tsx` - Gestisce le notifiche di cambio lingua

## Come utilizzare

### Hook base per traduzioni
```tsx
import { useTranslation } from '@/lib/i18n'
import { useAuth } from '@/hooks/use-auth'

function MyComponent() {
  const { user } = useAuth()
  const { t } = useTranslation(user?.language)
  
  return <h1>{t('welcome')}</h1>
}
```

### Utility per traduzioni specializzate
```tsx
import { useTranslationUtils } from '@/lib/translation-utils'
import { useAuth } from '@/hooks/use-auth'

function UserRole() {
  const { user } = useAuth()
  const { translateRole, translateRoleDescription } = useTranslationUtils(user?.language)
  
  return (
    <div>
      <h2>{translateRole(user.role_name)}</h2>
      <p>{translateRoleDescription(user.role_name)}</p>
    </div>
  )
}
```

## Aggiungere nuove traduzioni

1. Modifica il file `/src/lib/i18n.ts`:
```typescript
export const translations = {
  it: {
    // ... altre traduzioni
    newKey: "Nuovo testo in italiano"
  },
  en: {
    // ... altre traduzioni  
    newKey: "New text in English"
  }
}
```

2. Usa la nuova chiave nei componenti:
```tsx
const { t } = useTranslation(user?.language)
return <span>{t('newKey')}</span>
```

## Traduzioni annidate

Puoi utilizzare traduzioni annidate usando la dot notation:
```typescript
// In i18n.ts
user: {
  profile: "Profilo"
}

// Nel componente
t('user.profile') // Restituisce "Profilo"
```

## Componenti tradotti

Tutti i componenti principali sono stati aggiornati per supportare le traduzioni:

- ✅ `LoginForm` - Form di accesso
- ✅ `AppSidebar` - Menu laterale
- ✅ `NavUser` - Menu utente
- ✅ `RoleBasedContent` - Contenuti basati sui ruoli
- ✅ `UserInfoCard` - Card informazioni utente
- ✅ `LanguageSelector` - Selettore lingua
- ✅ `Layout` - Layout principale con header tradotto

## Cambio lingua

Il cambio lingua viene gestito automaticamente:
1. L'utente seleziona una lingua dal `LanguageSelector`
2. Viene inviata una richiesta al backend per aggiornare la preferenza
3. Il `NotificationManager` mostra una notifica di conferma
4. Tutti i componenti si aggiornano automaticamente con la nuova lingua

## Lingue supportate

- 🇮🇹 Italiano (`it`) - Lingua predefinita
- 🇬🇧 Inglese (`en`)

## Estensibilità

Per aggiungere una nuova lingua:
1. Aggiungi il nuovo codice lingua al tipo `Language` in `/src/lib/types.ts`
2. Aggiungi le traduzioni complete in `/src/lib/i18n.ts`
3. Aggiorna il `LanguageSelector` per includere la nuova opzione
4. Aggiorna il backend per supportare la nuova lingua
