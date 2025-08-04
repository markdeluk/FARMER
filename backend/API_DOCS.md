# 🌾 Farmer Market Platform API

API completa per la piattaforma di mercato agricolo con gestione multi-stakeholder.

## 🚀 Quick Start

### 1. Installa le dipendenze
```bash
pip install -r requirements.txt
```

### 2. Avvia il server
```bash
python run_server.py
```

### 3. Accedi alla documentazione
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc  
- **Documentazione Avanzata**: http://localhost:8000/docs-advanced
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 📊 Endpoints Disponibili

### 🔐 Autenticazione (`/api/v1/auth`)
- `POST /register` - Registrazione nuovo utente
- `POST /login` - Login utente
- `GET /me` - Profilo utente corrente
- `POST /refresh` - Rinnova token JWT

### 👥 Stakeholder Endpoints

#### 🛒 Consumer (`/api/v1/consumer`)
- Ricerca prodotti e vendor
- Gestione prenotazioni ristoranti
- Sistema recensioni
- Dashboard personalizzata

#### 🚜 Farmer (`/api/v1/farmer`)
- Gestione prodotti agricoli
- Controllo inventario e disponibilità
- Analytics vendite
- Dashboard produttore

#### 🍽️ Restaurant Owner (`/api/v1/restaurant-owner`)
- Gestione ristoranti e menu
- Sistema prenotazioni tavoli
- Gestione orari e disponibilità
- Dashboard ristorante

#### 🎨 Workshop Host (`/api/v1/workshop-host`)
- Organizzazione workshop/laboratori
- Gestione sessioni e materiali
- Sistema prenotazioni attività
- Analytics partecipanti

#### 🎪 Event Organizer (`/api/v1/event-organizer`)
- Gestione richieste eventi
- Prenotazione location
- Coordinamento vendor
- Gestione partecipanti

#### 👨‍💼 Admin (`/api/v1/admin`)
- Gestione utenti e vendor
- Approvazione richieste
- Monitoring sistema
- Analytics globali

## 🔑 Autenticazione

Tutti gli endpoint (eccetto quelli di autenticazione) richiedono un token JWT:

```bash
Authorization: Bearer <jwt_token>
```

### Ottenere un token:
1. Registrati: `POST /api/v1/auth/register`
2. Login: `POST /api/v1/auth/login`
3. Usa il token restituito negli header

## 📋 Esempi di Utilizzo

### Registrazione
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "farmer@example.com",
    "password": "password123",
    "first_name": "Mario",
    "last_name": "Rossi",
    "phone": "+39123456789",
    "role_id": 2
  }'
```

### Login
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "farmer@example.com", 
    "password": "password123"
  }'
```

### Accesso endpoint protetto
```bash
curl -X GET "http://localhost:8000/api/v1/farmer/products" \
  -H "Authorization: Bearer <jwt_token>"
```

## 🛠️ Struttura Progetto

```
backend/
├── app/
│   ├── api/
│   │   ├── controllers/        # Controller per ogni stakeholder
│   │   └── routes.py          # Router principale
│   ├── core/
│   │   ├── auth.py            # Sistema autenticazione JWT
│   │   └── dependencies.py    # Dipendenze comuni
│   ├── db/
│   │   ├── models/            # Modelli SQLAlchemy
│   │   └── session.py         # Configurazione database
│   ├── schemas/               # Modelli Pydantic per validazione
│   ├── services/              # Business logic
│   └── main.py               # App FastAPI principale
├── run_server.py             # Script per avviare server
└── requirements.txt          # Dipendenze Python
```

## 🔧 Funzionalità

### ✅ Implementate
- ✅ Sistema autenticazione JWT completo
- ✅ Autorizzazione basata su ruoli
- ✅ Documentazione Swagger automatica
- ✅ Validazione dati con Pydantic
- ✅ Controller per tutti gli stakeholder
- ✅ Error handling strutturato
- ✅ CORS configurato per sviluppo

### 🚧 In Sviluppo
- 🔄 Test automatizzati
- 🔄 Rate limiting
- 🔄 Logging avanzato
- 🔄 Cache Redis
- 🔄 File upload
- 🔄 Email notifications

## 🧪 Testing

### Swagger UI
1. Vai su http://localhost:8000/docs
2. Clicca "Authorize" 
3. Inserisci: `Bearer <jwt_token>`
4. Testa gli endpoint interattivamente

### Postman
- Importa la collection da: http://localhost:8000/docs-advanced/postman
- Configura la variabile `jwt_token` dopo il login

## 🔒 Sicurezza

- **Hash password**: bcrypt con salt
- **JWT tokens**: Scadenza 30 minuti
- **Autorizzazione**: Controllo ruoli per ogni endpoint
- **Validazione**: Sanitizzazione input automatica
- **HTTPS**: Configurato per produzione

## 🌍 Deploy

### Sviluppo
```bash
python run_server.py
```

### Produzione
```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## 📞 Support

Per domande o supporto:
- Email: support@farmermarket.com
- Documentazione: http://localhost:8000/docs-advanced
- Issues: GitHub repository

---

**🚀 Sviluppato per il progetto ASP - Farmer Market Platform**
