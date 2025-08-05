import { useRole } from '../hooks/use-role'
import { useAuth } from '../hooks/use-auth'
import { useTranslation } from '../lib/i18n'

/**
 * Componente di esempio che mostra come segregare le funzionalità basate sui ruoli
 */
export const RoleBasedContent = () => {
  const { 
    userRole, 
    isAdmin, 
    isFarmer, 
    isConsumer, 
    isRestaurantOwner,
    canManageSystem,
    canSellProducts,
    canBuyProducts,
    canManageRestaurant,
    canOrganizeEvents
  } = useRole()
  
  const { user } = useAuth()
  const { t } = useTranslation(user?.language)

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold">{t("availableFunctionality")}</h2>
      
      {/* Pannello amministrazione - solo admin */}
      {canManageSystem && (
        <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
          <h3 className="font-semibold text-red-800">🔧 {t("adminPanel")}</h3>
          <p className="text-red-600 text-sm">{t("fullSystemManagement")}</p>
          <div className="mt-2 space-x-2">
            <button className="px-3 py-1 bg-red-600 text-white rounded text-sm">
              {t("manageUsers")}
            </button>
            <button className="px-3 py-1 bg-red-600 text-white rounded text-sm">
              {t("configurations")}
            </button>
          </div>
        </div>
      )}

      {/* Pannello vendita - farmer e admin */}
      {canSellProducts && (
        <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
          <h3 className="font-semibold text-green-800">🌾 {t("salesPanel")}</h3>
          <p className="text-green-600 text-sm">{t("manageProducts")}</p>
          <div className="mt-2 space-x-2">
            <button className="px-3 py-1 bg-green-600 text-white rounded text-sm">
              {t("addProduct")}
            </button>
            <button className="px-3 py-1 bg-green-600 text-white rounded text-sm">
              {t("manageInventory")}
            </button>
          </div>
        </div>
      )}

      {/* Pannello acquisti - consumer, restaurant_owner e admin */}
      {canBuyProducts && (
        <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
          <h3 className="font-semibold text-blue-800">🛒 {t("purchasePanel")}</h3>
          <p className="text-blue-600 text-sm">{t("buyFreshProducts")}</p>
          <div className="mt-2 space-x-2">
            <button className="px-3 py-1 bg-blue-600 text-white rounded text-sm">
              {t("browseProducts")}
            </button>
            <button className="px-3 py-1 bg-blue-600 text-white rounded text-sm">
              {t("cart")}
            </button>
          </div>
        </div>
      )}

      {/* Pannello ristorante - restaurant_owner e admin */}
      {canManageRestaurant && (
        <div className="p-4 bg-orange-50 border border-orange-200 rounded-lg">
          <h3 className="font-semibold text-orange-800">🍽️ {t("restaurantPanel")}</h3>
          <p className="text-orange-600 text-sm">{t("manageRestaurantBookings")}</p>
          <div className="mt-2 space-x-2">
            <button className="px-3 py-1 bg-orange-600 text-white rounded text-sm">
              {t("manageMenu")}
            </button>
            <button className="px-3 py-1 bg-orange-600 text-white rounded text-sm">
              {t("bookings")}
            </button>
          </div>
        </div>
      )}

      {/* Pannello eventi - workshop_host, event_organizer e admin */}
      {canOrganizeEvents && (
        <div className="p-4 bg-purple-50 border border-purple-200 rounded-lg">
          <h3 className="font-semibold text-purple-800">🎪 {t("eventsPanel")}</h3>
          <p className="text-purple-600 text-sm">{t("organizeEvents")}</p>
          <div className="mt-2 space-x-2">
            <button className="px-3 py-1 bg-purple-600 text-white rounded text-sm">
              {t("createEvent")}
            </button>
            <button className="px-3 py-1 bg-purple-600 text-white rounded text-sm">
              {t("manageWorkshops")}
            </button>
          </div>
        </div>
      )}

      {/* Informazioni debug sui ruoli */}
      <div className="p-4 bg-gray-50 border border-gray-200 rounded-lg">
        <h3 className="font-semibold text-gray-800">ℹ️ {t("roleInfo")}</h3>
        <div className="mt-2 text-sm text-gray-600 space-y-1">
          <p><strong>{t("currentRole")}:</strong> {userRole}</p>
          <p><strong>{t("isAdmin")}:</strong> {isAdmin ? '✅' : '❌'}</p>
          <p><strong>{t("isFarmer")}:</strong> {isFarmer ? '✅' : '❌'}</p>
          <p><strong>{t("isConsumer")}:</strong> {isConsumer ? '✅' : '❌'}</p>
          <p><strong>{t("isRestaurantOwner")}:</strong> {isRestaurantOwner ? '✅' : '❌'}</p>
        </div>
      </div>
    </div>
  )
}
