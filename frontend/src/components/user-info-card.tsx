import { useAuth } from '@/hooks/use-auth'
import { useTranslation } from '@/lib/i18n'
import { useTranslationUtils } from '@/lib/translation-utils'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

export const UserInfoCard = () => {
  const { user, isAuthenticated } = useAuth()
  const { t } = useTranslation(user?.language)
  const { translateRole, translateRoleDescription, translateBoolean } = useTranslationUtils(user?.language)

  if (!isAuthenticated || !user) {
    return null
  }

  return (
    <Card className="w-full max-w-md">
      <CardHeader>
        <CardTitle>{t("userInfo")}</CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">
        <div>
          <label className="text-sm font-medium text-gray-500">{t("email")}</label>
          <p className="text-sm">{user.email}</p>
        </div>
        
        <div>
          <label className="text-sm font-medium text-gray-500">{t("phone")}</label>
          <p className="text-sm">{user.phone || '-'}</p>
        </div>
        
        <div>
          <label className="text-sm font-medium text-gray-500">{t("role")}</label>
          <p className="text-sm font-medium">{translateRole(user.role_name)}</p>
          <p className="text-xs text-gray-500">{translateRoleDescription(user.role_name)}</p>
        </div>
        
        <div>
          <label className="text-sm font-medium text-gray-500">{t("activeAccount")}</label>
          <p className="text-sm">{translateBoolean(user.is_active)}</p>
        </div>
        
        <div>
          <label className="text-sm font-medium text-gray-500">{t("language")}</label>
          <p className="text-sm">{user.language === 'it' ? t("italian") : t("english")}</p>
        </div>
      </CardContent>
    </Card>
  )
}
