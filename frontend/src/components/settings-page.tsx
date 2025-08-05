import { useState } from 'react'
import { useAuth } from '@/hooks/use-auth'
import { useTranslation } from '@/lib/i18n'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Label } from '@/components/ui/label'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { Separator } from '@/components/ui/separator'
import type { Language } from '@/lib/types'

export const SettingsPage = () => {
  const { user } = useAuth()
  const { t } = useTranslation(user?.language)
  const [selectedLanguage, setSelectedLanguage] = useState<Language>(user?.language || 'it')
  const [isLoading, setIsLoading] = useState(false)
  const [showSuccess, setShowSuccess] = useState(false)

  console.log('SettingsPage: Rendered') // Debug log

  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1'

  const handleLanguageChange = (newLanguage: Language) => {
    setSelectedLanguage(newLanguage)
  }

  const handleSaveSettings = async () => {
    if (!user || selectedLanguage === user.language) return
    
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
        body: JSON.stringify({ language: selectedLanguage })
      })
      
      if (response.ok) {
        setShowSuccess(true)
        // Ricarica la pagina per aggiornare la lingua in tutta l'app
        setTimeout(() => {
          window.location.reload()
        }, 1500)
      } else {
        console.error('Failed to update language')
      }
    } catch (error) {
      console.error('Error updating language:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const hasChanges = selectedLanguage !== user?.language

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">{t('settingsPageTitle')}</h1>
        <p className="text-muted-foreground mt-2">
          {t('settingsPageDescription')}
        </p>
      </div>

      <Separator />

      <Card>
        <CardHeader>
          <CardTitle>{t('generalSettings')}</CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Language Settings */}
          <div className="space-y-3">
            <div>
              <Label className="text-base font-medium">{t('languageSettings')}</Label>
              <p className="text-sm text-muted-foreground">
                {t('languageSettingsDescription')}
              </p>
            </div>
            
            <div className="grid gap-3">
              <Label htmlFor="language-select" className="text-sm">
                {t('currentLanguage')}: {user?.language === 'it' ? t('italian') : t('english')}
              </Label>
              
              <Select
                value={selectedLanguage}
                onValueChange={handleLanguageChange}
                disabled={isLoading}
              >
                <SelectTrigger id="language-select" className="w-[200px]">
                  <SelectValue placeholder={t('selectLanguageDropdown')} />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="it">
                    <div className="flex items-center space-x-2">
                      <span>🇮🇹</span>
                      <span>{t('italian')}</span>
                    </div>
                  </SelectItem>
                  <SelectItem value="en">
                    <div className="flex items-center space-x-2">
                      <span>🇬🇧</span>
                      <span>{t('english')}</span>
                    </div>
                  </SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          <Separator />

          {/* Save Button */}
          <div className="flex items-center justify-between">
            <div>
              {showSuccess && (
                <div className="text-sm text-green-600 font-medium">
                  ✅ {t('settingsSaved')}
                </div>
              )}
            </div>
            
            <Button 
              onClick={handleSaveSettings}
              disabled={!hasChanges || isLoading}
              className="min-w-[120px]"
            >
              {isLoading ? t('savingSettings') : t('saveChanges')}
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
