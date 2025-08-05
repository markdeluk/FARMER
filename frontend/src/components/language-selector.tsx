import { useState } from 'react'
import { useAuth } from '../hooks/use-auth'
import { Language } from '../lib/types'
import { useTranslation } from '../lib/i18n'

export const LanguageSelector = () => {
  const { user } = useAuth()
  const { t } = useTranslation(user?.language)
  const [isLoading, setIsLoading] = useState(false)
  
  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1'

  const handleLanguageChange = async (newLanguage: Language) => {
    if (!user || user.language === newLanguage || isLoading) return
    
    setIsLoading(true)
    try {
      const token = localStorage.getItem('token')
      if (!token) return
      
      const response = await fetch(`${API_BASE_URL}/auth/language`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ language: newLanguage })
      })
      
      if (response.ok) {
        // Ricarica la pagina per aggiornare la lingua in tutta l'app
        window.location.reload()
      } else {
        console.error('Failed to update language')
      }
    } catch (error) {
      console.error('Error updating language:', error)
    } finally {
      setIsLoading(false)
    }
  }

  if (!user) return null

  return (
    <div className="flex items-center space-x-2">
      <span className="text-sm text-gray-600">{t('language')}:</span>
      <div className="flex space-x-1">
        <button
          onClick={() => handleLanguageChange('it')}
          disabled={isLoading}
          className={`px-2 py-1 text-xs rounded ${
            user.language === 'it'
              ? 'bg-blue-600 text-white'
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          } ${isLoading ? 'opacity-50 cursor-not-allowed' : ''}`}
        >
          🇮🇹 {t('italian')}
        </button>
        <button
          onClick={() => handleLanguageChange('en')}
          disabled={isLoading}
          className={`px-2 py-1 text-xs rounded ${
            user.language === 'en'
              ? 'bg-blue-600 text-white'
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          } ${isLoading ? 'opacity-50 cursor-not-allowed' : ''}`}
        >
          🇬🇧 {t('english')}
        </button>
      </div>
    </div>
  )
}
