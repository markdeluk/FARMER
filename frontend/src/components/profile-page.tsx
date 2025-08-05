import { useState } from 'react'
import { useAuth } from '@/hooks/use-auth'
import { useTranslation } from '@/lib/i18n'
import { useTranslationUtils } from '@/lib/translation-utils'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Label } from '@/components/ui/label'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { Separator } from '@/components/ui/separator'
import type { Language } from '@/lib/types'

export const ProfilePage = () => {
  const { user } = useAuth()
  const { t } = useTranslation(user?.language)
  const { translateRole, translateBoolean } = useTranslationUtils(user?.language)
  const [selectedLanguage, setSelectedLanguage] = useState<Language>(user?.language || 'it')
  const [isLoading, setIsLoading] = useState(false)
  const [showSuccess, setShowSuccess] = useState(false)

  console.log('ProfilePage: Component rendered')

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

  if (!user) {
    return null
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">{t('profilePageTitle')}</h1>
        <p className="text-muted-foreground mt-2">
          {t('profilePageDescription')}
        </p>
      </div>

      <Separator />

      {/* Personal Information Card */}
      <Card>
        <CardHeader>
          <CardTitle>{t('personalInfo')}</CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="flex items-center space-x-4">
            <Avatar className="h-20 w-20">
              <AvatarImage 
                src={user.profile_picture ? `data:image/jpeg;base64,${user.profile_picture}` : undefined}
                alt={`${user.first_name} ${user.last_name}`}
              />
              <AvatarFallback className="text-lg">
                {user.first_name?.[0]}{user.last_name?.[0]}
              </AvatarFallback>
            </Avatar>
            <div className="space-y-1">
              <h3 className="text-lg font-semibold">{user.first_name} {user.last_name}</h3>
              <p className="text-sm text-muted-foreground">{user.email}</p>
              <p className="text-sm text-muted-foreground">
                {translateRole(user.role_name)}
              </p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <Label className="text-sm font-medium text-muted-foreground">{t('phone')}</Label>
              <p className="text-sm">{user.phone || '-'}</p>
            </div>
            
            <div>
              <Label className="text-sm font-medium text-muted-foreground">{t('activeAccount')}</Label>
              <p className="text-sm">{translateBoolean(user.is_active)}</p>
            </div>
            
            <div>
              <Label className="text-sm font-medium text-muted-foreground">{t('roleId')}</Label>
              <p className="text-sm">{user.role_id}</p>
            </div>
            
            <div>
              <Label className="text-sm font-medium text-muted-foreground">{t('currentLanguage')}</Label>
              <p className="text-sm">{user.language === 'it' ? t('italian') : t('english')}</p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Profile Settings Card */}
      <Card>
        <CardHeader>
          <CardTitle>{t('profileSettings')}</CardTitle>
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
              <Select
                value={selectedLanguage}
                onValueChange={handleLanguageChange}
                disabled={isLoading}
              >
                <SelectTrigger className="w-[200px]">
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
