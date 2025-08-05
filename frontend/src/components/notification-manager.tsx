import { useState, useEffect } from 'react'
import { useTranslation } from '@/lib/i18n'
import { useAuth } from '@/hooks/use-auth'

interface ToastProps {
  message: string
  isVisible: boolean
  onClose: () => void
}

const Toast = ({ message, isVisible, onClose }: ToastProps) => {
  useEffect(() => {
    if (isVisible) {
      const timer = setTimeout(() => {
        onClose()
      }, 3000)
      return () => clearTimeout(timer)
    }
  }, [isVisible, onClose])

  if (!isVisible) return null

  return (
    <div className="fixed top-4 right-4 bg-green-600 text-white px-4 py-2 rounded-md shadow-lg z-50 animate-in slide-in-from-top">
      {message}
    </div>
  )
}

interface NotificationManagerProps {
  children: React.ReactNode
}

export const NotificationManager = ({ children }: NotificationManagerProps) => {
  const { user } = useAuth()
  const { t } = useTranslation(user?.language)
  const [showToast, setShowToast] = useState(false)
  const [previousLanguage, setPreviousLanguage] = useState(user?.language)

  useEffect(() => {
    if (user?.language && previousLanguage && user.language !== previousLanguage) {
      setShowToast(true)
      setPreviousLanguage(user.language)
    } else if (user?.language && !previousLanguage) {
      setPreviousLanguage(user.language)
    }
  }, [user?.language, previousLanguage])

  const handleCloseToast = () => {
    setShowToast(false)
  }

  return (
    <>
      {children}
      <Toast 
        message={t("languageUpdated")} 
        isVisible={showToast} 
        onClose={handleCloseToast} 
      />
    </>
  )
}
