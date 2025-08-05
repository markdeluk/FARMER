import type { Language } from './types'
import { translations } from './i18n'

/**
 * Utility per ottenere traduzioni per i ruoli dall'API
 */
export const translateRole = (roleName: string, language: Language = 'it'): string => {
  const roleKey = roleName as keyof typeof translations.it.roles
  return translations[language].roles[roleKey] || roleName
}

/**
 * Utility per ottenere descrizioni tradotte dei ruoli
 */
export const translateRoleDescription = (roleName: string, language: Language = 'it'): string => {
  const roleKey = roleName as keyof typeof translations.it.roleDescriptions
  return translations[language].roleDescriptions[roleKey] || roleName
}

/**
 * Utility per tradurre messaggi di errore dall'API
 */
export const translateError = (errorKey: string, language: Language = 'it'): string => {
  const errorPath = errorKey.split('.')
  let value: any = translations[language]
  
  for (const key of errorPath) {
    value = value?.[key]
  }
  
  return value || errorKey
}

/**
 * Utility per tradurre valori booleani
 */
export const translateBoolean = (value: boolean, language: Language = 'it'): string => {
  return value ? translations[language].yes : translations[language].no
}

/**
 * Hook per traduzioni reattive che si aggiornano quando cambia la lingua
 */
export const useTranslationUtils = (language: Language = 'it') => {
  return {
    translateRole: (roleName: string) => translateRole(roleName, language),
    translateRoleDescription: (roleName: string) => translateRoleDescription(roleName, language),
    translateError: (errorKey: string) => translateError(errorKey, language),
    translateBoolean: (value: boolean) => translateBoolean(value, language),
  }
}
