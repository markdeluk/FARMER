from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

router = APIRouter(prefix="/docs-advanced", tags=["📚 Documentation"])

@router.get("/", response_class=HTMLResponse)
def get_advanced_docs():
    """Documentazione avanzata dell'API"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>🌾 Farmer Market Platform - API Documentation</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
            .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }
            h1 { color: #2c5530; border-bottom: 3px solid #4CAF50; padding-bottom: 10px; }
            h2 { color: #4CAF50; margin-top: 30px; }
            .stakeholder { background: #f9f9f9; padding: 15px; margin: 10px 0; border-left: 4px solid #4CAF50; }
            .endpoint { background: #fff; border: 1px solid #ddd; padding: 10px; margin: 5px 0; border-radius: 5px; }
            .method { padding: 2px 8px; border-radius: 3px; color: white; font-weight: bold; }
            .get { background: #61affe; }
            .post { background: #49cc90; }
            .put { background: #fca130; }
            .delete { background: #f93e3e; }
            code { background: #f4f4f4; padding: 2px 5px; border-radius: 3px; }
            .auth-note { background: #fff3cd; border: 1px solid #ffeaa7; padding: 10px; border-radius: 5px; margin: 10px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🌾 Farmer Market Platform API</h1>
            
            <div class="auth-note">
                <strong>🔐 Autenticazione:</strong> Tutti gli endpoint (eccetto quelli di autenticazione) richiedono un token JWT nell'header:<br>
                <code>Authorization: Bearer &lt;token&gt;</code>
            </div>

            <h2>🔐 Autenticazione (/api/v1/auth)</h2>
            <div class="endpoint">
                <span class="method post">POST</span> <code>/register</code> - Registrazione nuovo utente
            </div>
            <div class="endpoint">
                <span class="method post">POST</span> <code>/login</code> - Login utente
            </div>
            <div class="endpoint">
                <span class="method get">GET</span> <code>/me</code> - Profilo utente corrente
            </div>
            <div class="endpoint">
                <span class="method post">POST</span> <code>/refresh</code> - Rinnova token
            </div>

            <h2>👥 Stakeholder Endpoints</h2>

            <div class="stakeholder">
                <h3>🛒 Consumer (/api/v1/consumer)</h3>
                <div class="endpoint">
                    <span class="method get">GET</span> <code>/products</code> - Ricerca prodotti
                </div>
                <div class="endpoint">
                    <span class="method get">GET</span> <code>/restaurants</code> - Lista ristoranti
                </div>
                <div class="endpoint">
                    <span class="method post">POST</span> <code>/bookings</code> - Crea prenotazione
                </div>
                <div class="endpoint">
                    <span class="method get">GET</span> <code>/bookings</code> - Le mie prenotazioni
                </div>
                <div class="endpoint">
                    <span class="method post">POST</span> <code>/reviews</code> - Crea recensione
                </div>
                <div class="endpoint">
                    <span class="method get">GET</span> <code>/dashboard</code> - Dashboard consumer
                </div>
            </div>

            <div class="stakeholder">
                <h3>🚜 Farmer (/api/v1/farmer)</h3>
                <div class="endpoint">
                    <span class="method get">GET</span> <code>/products</code> - I miei prodotti
                </div>
                <div class="endpoint">
                    <span class="method post">POST</span> <code>/products</code> - Crea prodotto
                </div>
                <div class="endpoint">
                    <span class="method put">PUT</span> <code>/products/{id}</code> - Aggiorna prodotto
                </div>
                <div class="endpoint">
                    <span class="method post">POST</span> <code>/products/{id}/availability</code> - Imposta disponibilità
                </div>
                <div class="endpoint">
                    <span class="method get">GET</span> <code>/inventory</code> - Gestione inventario
                </div>
                <div class="endpoint">
                    <span class="method get">GET</span> <code>/analytics</code> - Analytics vendite
                </div>
            </div>

            <div class="stakeholder">
                <h3>🍽️ Restaurant Owner (/api/v1/restaurant-owner)</h3>
                <div class="endpoint">
                    <span class="method get">GET</span> <code>/restaurants</code> - I miei ristoranti
                </div>
                <div class="endpoint">
                    <span class="method post">POST</span> <code>/restaurants</code> - Crea ristorante
                </div>
                <div class="endpoint">
                    <span class="method get">GET</span> <code>/restaurants/{id}/menu</code> - Gestione menu
                </div>
                <div class="endpoint">
                    <span class="method get">GET</span> <code>/restaurants/{id}/bookings</code> - Prenotazioni ristorante
                </div>
                <div class="endpoint">
                    <span class="method post">POST</span> <code>/restaurants/{id}/bookings/{booking_id}/confirm</code> - Conferma prenotazione
                </div>
                <div class="endpoint">
                    <span class="method get">GET</span> <code>/dashboard</code> - Dashboard ristorante
                </div>
            </div>

            <div class="stakeholder">
                <h3>🎨 Workshop Host (/api/v1/workshop-host)</h3>
                <div class="endpoint">
                    <span class="method get">GET</span> <code>/activities</code> - Le mie attività
                </div>
                <div class="endpoint">
                    <span class="method post">POST</span> <code>/activities</code> - Crea attività
                </div>
                <div class="endpoint">
                    <span class="method get">GET</span> <code>/activities/{id}/bookings</code> - Prenotazioni attività
                </div>
                <div class="endpoint">
                    <span class="method get">GET</span> <code>/activities/{id}/sessions</code> - Sessioni attività
                </div>
                <div class="endpoint">
                    <span class="method get">GET</span> <code>/dashboard</code> - Dashboard workshop
                </div>
            </div>

            <div class="stakeholder">
                <h3>🎪 Event Organizer (/api/v1/event-organizer)</h3>
                <div class="endpoint">
                    <span class="method get">GET</span> <code>/requests</code> - Le mie richieste eventi
                </div>
                <div class="endpoint">
                    <span class="method post">POST</span> <code>/requests</code> - Crea richiesta evento
                </div>
                <div class="endpoint">
                    <span class="method get">GET</span> <code>/locations</code> - Cerca location
                </div>
                <div class="endpoint">
                    <span class="method get">GET</span> <code>/vendors</code> - Cerca vendor per eventi
                </div>
                <div class="endpoint">
                    <span class="method get">GET</span> <code>/dashboard</code> - Dashboard eventi
                </div>
            </div>

            <div class="stakeholder">
                <h3>👨‍💼 Admin (/api/v1/admin)</h3>
                <div class="endpoint">
                    <span class="method get">GET</span> <code>/users</code> - Gestione utenti
                </div>
                <div class="endpoint">
                    <span class="method get">GET</span> <code>/vendors</code> - Gestione vendor
                </div>
                <div class="endpoint">
                    <span class="method get">GET</span> <code>/requests/events/pending</code> - Richieste eventi pendenti
                </div>
                <div class="endpoint">
                    <span class="method post">POST</span> <code>/requests/events/{id}/approve</code> - Approva evento
                </div>
                <div class="endpoint">
                    <span class="method get">GET</span> <code>/dashboard</code> - Dashboard amministratore
                </div>
                <div class="endpoint">
                    <span class="method get">GET</span> <code>/system/health</code> - Stato sistema
                </div>
            </div>

            <h2>📊 Caratteristiche Principali</h2>
            <ul>
                <li><strong>Autenticazione JWT:</strong> Token sicuri con scadenza di 30 minuti</li>
                <li><strong>Autorizzazione per ruoli:</strong> Ogni endpoint verifica i permessi utente</li>
                <li><strong>Validazione dati:</strong> Validazione automatica con Pydantic</li>
                <li><strong>Documentazione automatica:</strong> Swagger UI disponibile su /docs</li>
                <li><strong>Error handling:</strong> Messaggi di errore dettagliati e consistenti</li>
                <li><strong>Paginazione:</strong> Supporto paginazione per liste grandi</li>
                <li><strong>Search e Filtri:</strong> Ricerca avanzata per prodotti, utenti, eventi</li>
                <li><strong>Analytics:</strong> Dashboard personalizzate per ogni stakeholder</li>
            </ul>

            <h2>🚀 Per Iniziare</h2>
            <ol>
                <li>Vai su <a href="/docs">/docs</a> per la documentazione Swagger interattiva</li>
                <li>Registrati con <code>POST /api/v1/auth/register</code></li>
                <li>Effettua login con <code>POST /api/v1/auth/login</code></li>
                <li>Usa il token negli header per accedere agli endpoint protetti</li>
                <li>Esplora gli endpoint del tuo ruolo specifico</li>
            </ol>

            <div class="auth-note">
                <strong>💡 Tip:</strong> Usa il pulsante "Authorize" in Swagger UI per impostare automaticamente il token JWT in tutti i test
            </div>
        </div>
    </body>
    </html>
    """

@router.get("/postman")
def get_postman_collection():
    """Collection Postman per testing API"""
    return {
        "info": {
            "name": "🌾 Farmer Market Platform API",
            "description": "Collection completa per testare l'API",
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
        },
        "auth": {
            "type": "bearer",
            "bearer": [
                {
                    "key": "token",
                    "value": "{{jwt_token}}",
                    "type": "string"
                }
            ]
        },
        "variable": [
            {
                "key": "base_url",
                "value": "http://localhost:8000/api/v1",
                "type": "string"
            },
            {
                "key": "jwt_token",
                "value": "",
                "type": "string"
            }
        ],
        "item": [
            {
                "name": "🔐 Auth",
                "item": [
                    {
                        "name": "Register",
                        "request": {
                            "method": "POST",
                            "header": [],
                            "body": {
                                "mode": "raw",
                                "raw": '{\n  "email": "test@example.com",\n  "password": "password123",\n  "first_name": "Mario",\n  "last_name": "Rossi",\n  "phone": "+39123456789",\n  "role_id": 2\n}',
                                "options": {
                                    "raw": {
                                        "language": "json"
                                    }
                                }
                            },
                            "url": {
                                "raw": "{{base_url}}/auth/register",
                                "host": ["{{base_url}}"],
                                "path": ["auth", "register"]
                            }
                        }
                    },
                    {
                        "name": "Login",
                        "request": {
                            "method": "POST",
                            "header": [],
                            "body": {
                                "mode": "raw",
                                "raw": '{\n  "email": "test@example.com",\n  "password": "password123"\n}',
                                "options": {
                                    "raw": {
                                        "language": "json"
                                    }
                                }
                            },
                            "url": {
                                "raw": "{{base_url}}/auth/login",
                                "host": ["{{base_url}}"],
                                "path": ["auth", "login"]
                            }
                        }
                    }
                ]
            },
            {
                "name": "🛒 Consumer",
                "item": [
                    {
                        "name": "Get Products",
                        "request": {
                            "method": "GET",
                            "header": [],
                            "url": {
                                "raw": "{{base_url}}/consumer/products",
                                "host": ["{{base_url}}"],
                                "path": ["consumer", "products"]
                            }
                        }
                    },
                    {
                        "name": "Create Booking",
                        "request": {
                            "method": "POST",
                            "header": [],
                            "body": {
                                "mode": "raw",
                                "raw": '{\n  "restaurant_id": 1,\n  "booking_date": "2025-08-15",\n  "booking_time": "19:30",\n  "party_size": 4,\n  "special_requests": "Tavolo vicino alla finestra"\n}',
                                "options": {
                                    "raw": {
                                        "language": "json"
                                    }
                                }
                            },
                            "url": {
                                "raw": "{{base_url}}/consumer/bookings",
                                "host": ["{{base_url}}"],
                                "path": ["consumer", "bookings"]
                            }
                        }
                    }
                ]
            }
        ]
    }
