import { useRole } from '../hooks/use-role'
import { UserRole } from '../lib/types'

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

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold">Funzionalità Disponibili</h2>
      
      {/* Pannello amministrazione - solo admin */}
      {canManageSystem && (
        <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
          <h3 className="font-semibold text-red-800">🔧 Pannello Amministrazione</h3>
          <p className="text-red-600 text-sm">Gestione completa del sistema</p>
          <div className="mt-2 space-x-2">
            <button className="px-3 py-1 bg-red-600 text-white rounded text-sm">
              Gestisci Utenti
            </button>
            <button className="px-3 py-1 bg-red-600 text-white rounded text-sm">
              Configurazioni
            </button>
          </div>
        </div>
      )}

      {/* Pannello vendita - farmer e admin */}
      {canSellProducts && (
        <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
          <h3 className="font-semibold text-green-800">🌾 Pannello Vendita</h3>
          <p className="text-green-600 text-sm">Gestisci i tuoi prodotti</p>
          <div className="mt-2 space-x-2">
            <button className="px-3 py-1 bg-green-600 text-white rounded text-sm">
              Aggiungi Prodotto
            </button>
            <button className="px-3 py-1 bg-green-600 text-white rounded text-sm">
              Gestisci Inventario
            </button>
          </div>
        </div>
      )}

      {/* Pannello acquisti - consumer, restaurant_owner e admin */}
      {canBuyProducts && (
        <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
          <h3 className="font-semibold text-blue-800">🛒 Pannello Acquisti</h3>
          <p className="text-blue-600 text-sm">Acquista prodotti freschi</p>
          <div className="mt-2 space-x-2">
            <button className="px-3 py-1 bg-blue-600 text-white rounded text-sm">
              Sfoglia Prodotti
            </button>
            <button className="px-3 py-1 bg-blue-600 text-white rounded text-sm">
              Carrello
            </button>
          </div>
        </div>
      )}

      {/* Pannello ristorante - restaurant_owner e admin */}
      {canManageRestaurant && (
        <div className="p-4 bg-orange-50 border border-orange-200 rounded-lg">
          <h3 className="font-semibold text-orange-800">🍽️ Pannello Ristorante</h3>
          <p className="text-orange-600 text-sm">Gestisci ristorante e prenotazioni</p>
          <div className="mt-2 space-x-2">
            <button className="px-3 py-1 bg-orange-600 text-white rounded text-sm">
              Gestisci Menu
            </button>
            <button className="px-3 py-1 bg-orange-600 text-white rounded text-sm">
              Prenotazioni
            </button>
          </div>
        </div>
      )}

      {/* Pannello eventi - workshop_host, event_organizer e admin */}
      {canOrganizeEvents && (
        <div className="p-4 bg-purple-50 border border-purple-200 rounded-lg">
          <h3 className="font-semibold text-purple-800">🎪 Pannello Eventi</h3>
          <p className="text-purple-600 text-sm">Organizza workshop e eventi</p>
          <div className="mt-2 space-x-2">
            <button className="px-3 py-1 bg-purple-600 text-white rounded text-sm">
              Crea Evento
            </button>
            <button className="px-3 py-1 bg-purple-600 text-white rounded text-sm">
              Gestisci Workshop
            </button>
          </div>
        </div>
      )}

      {/* Informazioni debug sui ruoli */}
      <div className="p-4 bg-gray-50 border border-gray-200 rounded-lg">
        <h3 className="font-semibold text-gray-800">ℹ️ Informazioni Ruolo</h3>
        <div className="mt-2 text-sm text-gray-600 space-y-1">
          <p><strong>Ruolo corrente:</strong> {userRole}</p>
          <p><strong>È Admin:</strong> {isAdmin ? '✅' : '❌'}</p>
          <p><strong>È Farmer:</strong> {isFarmer ? '✅' : '❌'}</p>
          <p><strong>È Consumer:</strong> {isConsumer ? '✅' : '❌'}</p>
          <p><strong>È Restaurant Owner:</strong> {isRestaurantOwner ? '✅' : '❌'}</p>
        </div>
      </div>
    </div>
  )
}
