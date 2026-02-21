source .venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8001


# Echo API - FastAPI Application con Web Scraping

API Echo para recibir y procesar datos de vehículos desde Kafka con arquitectura limpia siguiendo mejores prácticas de FastAPI y SOLID principles. Incluye sistema de web scraping modular para múltiples aseguradoras.

## CLOUDFLARE BYPASS - Solución Implementada

**IMPORTANTE**: Este proyecto incluye la solución para pasar verificaciones de Cloudflare Turnstile sin ser detectado como bot. Aquí está documentado cómo y por qué funciona.

### Problemas Anteriores (Por qué No Funcionaba)

1. **User-Agent desactualizado (Chrome 120.0.0.0)**
   - Cloudflare detecta que Chrome 120 NO EXISTE en enero 2026
   - Chrome real en 2026 es versión 144+
   - Resultado: Cloudflare identifica como BOT → BLOQUEA

2. **Lenguaje y configuración regional incorrectos**
   - Tenía `--lang=es-MX` pero navegador real usaba `es-GB`
   - Cloudflare detecta desajustes entre User-Agent y headers de idioma
   - Resultado: Detecta discrepancia sospechosa → BLOQUEA

3. **Intento de clickear checkbox de Cloudflare**
   - Estrategia anterior: Intentar hacer click en iframe de Cloudflare
   - Problema: Cloudflare analiza CÓMO se hace el click (movimientos de ratón)
   - Click con Selenium = movimientos no-humanos → DETECTADO
   - Resultado: Bloqueo inmediato

4. **Falta de scripts de tracking**
   - Cloudflare ESPERA ver peticiones a servicios de tracking
   - Servicios que DEBE ver: Datadog RUM, Datadog Logs, Google Analytics, Facebook Pixel
   - Sin estas peticiones = "Headless browser sin tracking" → BOT
   - Resultado: BLOQUEA por falta de actividad de usuario real

### ✅ Solución Implementada (Por qué Funciona Ahora)

```
ANTES (BLOQUEADO):
Chrome 120 (falso) + es-MX + Sin tracking + Intento clickear = Cloudflare lo detecta

AHORA (PASA):
Chrome 144 (REAL) + es-GB (correcto) + Tracking permitido + NO clickear = Cloudflare cree usuario real
```

#### 1. User-Agent Correcto (CRÍTICO)
```python
# Chrome 144.0.7559.97 - Versión real de 2026
'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
'AppleWebKit/537.36 (KHTML, like Gecko) '
'Chrome/144.0.7559.97 Safari/537.36'
```
**Por qué funciona**: Coincide con versión real de Chrome en 2026. Cloudflare verifica versión del UA.

#### 2. Idioma Correcto (IMPORTANTE)
```python
options.add_argument('--lang=es-GB')  # Región correcta
options.add_argument('--accept-lang=es-GB,es-MX,es;q=0.9')  # Headers correctos
```
**Por qué funciona**: User-Agent debe coincidir con idioma. Si hay desajuste = bot.

#### 3. Permitir Scripts de Tracking (ESENCIAL)
```python
options.add_argument('--allow-running-insecure-content')  # No bloquea tracking
```
**Por qué funciona**: Permite que se carguen:
- `browser-intake-us3-datadoghq.com/api/v2/rum` (RUM Datadog)
- `browser-intake-us3-datadoghq.com/api/v2/logs` (Logs Datadog)
- `google-analytics.com/g/collect` (Google Analytics)
- `facebook.com/tr/` (Facebook Pixel)

Cloudflare detecta estas peticiones = Usuario real confirmado.

#### 4. Ocultar Propiedades de Selenium (PROTECCIÓN)
```javascript
Object.defineProperty(navigator, 'webdriver', {get: () => false});
Object.defineProperty(navigator, 'languages', {get: () => ['es-GB', 'es-MX', 'es']});
Object.defineProperty(navigator, 'language', {get: () => 'es-GB'});
```
**Por qué funciona**: Elimina flags que detectan automatización.

#### 5. Acceso Lento y Natural (COMPORTAMIENTO HUMANO)
```python
driver.get(base_url)        # Ir a página principal
time.sleep(2)               # Esperar como humano
time.sleep(3)               # Esperar más
driver.get(url_completa)    # Ir a URL con parámetros
```
**Por qué funciona**: Simula navegación humana. Acceso directo a URL completa = sospechoso.

#### 6. NO Clickear el Checkbox (CLAVE)
- **ANTES**: Intentar clickear iframe de Cloudflare = DETECTADO COMO BOT
- **AHORA**: Dejar que Cloudflare se resuelva automáticamente
- **Resultado**: Con headers correctos, Cloudflare se resuelve sin requerir click

### 📋 Información Requerida para Otros Sitios con Cloudflare

Para adaptar esta solución a otras páginas, necesito que me proporciones:

#### 1. User-Agent Real (CRÍTICO)
```
Abre tu navegador → F12 (DevTools) → Network tab
Haz cualquier request → Headers
Busca: "user-agent"
Copia EXACTAMENTE lo que dice
```
Ejemplo: `Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.7559.97 Safari/537.36`

#### 2. Accept-Language (IMPORTANTE)
```
En los mismos Headers → "accept-language"
Ejemplo: es-GB,es-MX,es;q=0.9
```

#### 3. Screenshot de Network Tab Completo
```
Cuando Twiraces LA PÁGINA MANUALMENTE en tu navegador:
- F12 → Network tab
- Recarga la página (Ctrl+R o Cmd+R)
- Toma screenshot mostrando:
  * Primeros 10 requests (con User-Agent visible)
  * Todos los requests de tracking (Datadog, GA, Facebook, etc.)
  * URL final que se carga
```

#### 4. Estructura HTML de Cloudflare (si aplica)
```
Si aparece un challenge de Cloudflare:
- F12 → Elements/Inspector
- Busca: <iframe class="cf-challenge"> o similar
- Describe: ¿Es un checkbox? ¿Es un puzzle? ¿Es prueba de PoW?
```

#### 5. Formularios y Elementos de la Página
```
Una vez que pasa Cloudflare:
- ¿Qué formularios hay?
- ¿Qué campos tienen (id, class, name)?
- ¿Qué botones hay para continuar? (id, class)
- URLs que se cargan en cada paso
```

### 🎯 Resumen de la Estrategia

**La clave es MIMIFICAR EXACTAMENTE lo que hace tu navegador real:**

1. ✅ User-Agent correcto (debe coincidir con Chrome real)
2. ✅ Idioma correcto (debe coincidir con locale del navegador)
3. ✅ Permitir tracking scripts (Datadog, GA, Facebook)
4. ✅ Ocultar propiedades de Selenium
5. ✅ Acceso lento y natural
6. ✅ NO intentar clickear iframes de Cloudflare
7. ✅ Permitir que se resuelva automáticamente

Con esto, **Cloudflare creerá que es usuario real y NO bloqueará** ✅

---

## 📌 Documentos de Referencia

### Para Nuevas Páginas con Cloudflare

- **[CLOUDFLARE_QUICK_GUIDE.md](CLOUDFLARE_QUICK_GUIDE.md)**: Guía rápida (30 segundos) con checklist
- **[CLOUDFLARE_PROMPT_TEMPLATE.py](CLOUDFLARE_PROMPT_TEMPLATE.py)**: Prompt completo para copiar/pegar

**Flujo:**
1. Abre [CLOUDFLARE_QUICK_GUIDE.md](CLOUDFLARE_QUICK_GUIDE.md)
2. Recopila información de la nueva página
3. Copia [CLOUDFLARE_PROMPT_TEMPLATE.py](CLOUDFLARE_PROMPT_TEMPLATE.py)
4. Completa con la información
5. Pasa a GitHub Copilot para configurar scraper

## 🏗️ Estructura del Proyecto

```
.
├── main.py                      # Aplicación principal FastAPI
├── src/
│   ├── core/
│   │   ├── config.py            # Configuración centralizada
│   │   └── database.py          # Conexión a PostgreSQL
│   ├── schemas/
│   │   ├── QuotationDetail.py  # Modelo de respuesta Quotation
│   │   └── request_schemas.py  # Modelos de request
│   ├── repositories/
│   │   └── quotation_repository.py  # Queries a base de datos
│   ├── services/
│   │   ├── quotation_service.py     # Lógica de negocio Quotation
│   │   ├── scraper_service.py       # Orquestador de scrapers (OCP)
│   │   ├── chrome_driver.py         # Gestor Chrome WebDriver
│   │   ├── logger.py                # Logger visual scraping
│   │   ├── interfaces.py            # Interfaces SOLID (ABC)
│   │   └── extendScrapers/          # Estrategias por scraper (OCP)
│   │       ├── __init__.py          # ScraperStrategy base
│   │       ├── scraper_mapfre.py    # Estrategia Mapfre
│   │       └── scraper_hdi.py       # Estrategia HDI
│   ├── api/
│   │   └── endpoints/
│   │       ├── __init__.py          # Router principal
│   │       ├── heald_router.py      # Health check & DB
│   │       ├── quotation_router.py  # Quotation endpoints
│   │       └── scraper_router.py    # Scraper endpoints
│   └── consumers/
│       └── kafka_consumer.py        # Consumer de eventos NestJS
├── scrapers/
│   └── implementations/
│       ├── mapfre_scraper.py        # Scraper Mapfre (Cloudflare bypass)
│       └── hdi_scraper.py           # Scraper HDI
├── utils/
│   ├── helpers.py                   # Utilidades generales
│   └── logging_config.py            # Configuración logging
├── requirements.txt                 # Dependencias Python
├── .env                             # Variables de entorno
└── README.md                        # Este archivo
```

## 📋 Características

- ✅ **Arquitectura en capas**: Router → Service → Repository
- ✅ **SOLID Principles - Open/Closed**: Scrapers extensibles sin modificar código base
- ✅ **Dependency Injection**: Constructor-based DI (db flows through layers)
- ✅ **Web Scraping con Cloudflare Bypass**: Chrome 144 + tracking permitido
- ✅ **Strategy Pattern**: Scrapers con estrategias independientes (Mapfre/HDI)
- ✅ **Selenium Integration**: Chrome WebDriver con configuración anti-detección
- ✅ **PostgreSQL Integration**: SQLAlchemy 2.0 + Pydantic V2
- ✅ **Kafka Consumer**: Recibe eventos de productor NestJS
- ✅ **Type-safe Returns**: QuotationDetail con validación Pydantic
- ✅ **Health Endpoints**: Database connection check
- ✅ **Configuración centralizada**: Pydantic Settings con .env
- ✅ **Documentación automática**: OpenAPI/Swagger integrado
- ✅ **Logging visual**: Sistema de logging para scraping
- ✅ **CORS**: Configuración flexible

## 🚀 Instalación y Arranque

### 1. Clonar repositorio
```bash
git clone <repo-url>
cd Scrapping
```

### 2. Crear y activar entorno virtual
```bash
python3.14 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# o
.venv\Scripts\activate  # Windows
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
```bash
# Crear archivo .env con:
DATABASE_URL=postgresql://cotiza360_user:tu_password_seguro@localhost:5432/cotiza360_db
APP_NAME=Echo API - Cotiza360
APP_VERSION=1.0.0
HOST=0.0.0.0
PORT=8001
DEBUG=true
LOG_LEVEL=INFO
```

### 5. Asegurar que Docker esté corriendo
```bash
# Kafka debe estar en localhost:9092
docker ps | grep kafka-cotiza360

# PostgreSQL debe estar en localhost:5432
docker ps | grep postgres-cotiza360
```

### 6. Arrancar el sistema
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

### 7. Verificar que todo funcione
```
 Deberías ver en consola:
- INFO: Uvicorn running on http://0.0.0.0:8001
- Iniciando Kafka consumer en background...
- Kafka consumer conectado a localhost:9092
- Topic: quotations-created | Group: fastapi-quotation-group
```

### 8. Probar endpoints
```bash
# Health check
curl http://localhost:8001/health/database

# Quotation (reemplaza {uuid} con ID real)
curl http://localhost:8001/api/v1/quotations/{uuid}

# Scraper Mapfre
curl "http://localhost:8001/api/v1/scrapers/scrape/mapfre?marca=NISSAN&submarca=VERSA&year=2024&codigo=12345&fecha=2024-01-01&genero=M"
```

## ▶️ Ejecución

### 1. Activar entorno virtual
```bash
source .venv/bin/activate  # En macOS/Linux
# o
.venv\Scripts\activate  # En Windows
```

### 2. Iniciar FastAPI en modo desarrollo (con auto-reload)
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

### 3. Verificar que el servicio esté corriendo
```bash
# El servidor debería mostrar:
# ✅ Kafka consumer conectado a localhost:9092
# 📡 Topic: quotations-created | Group: fastapi-quotation-group
# INFO: Uvicorn running on http://0.0.0.0:8001
```

### 4. Acceder a la documentación
- **Swagger UI**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc

## 📚 Documentación API

Una vez iniciado el servidor, accede a:

- **Swagger UI**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc
- **OpenAPI JSON**: http://localhost:8001/openapi.json

## 🔌 Endpoints Principales

### Health Check
```http
GET /health/database
```
Verifica conexión con PostgreSQL

### Quotation (Consultar cotización)
```http
GET /api/v1/quotations/{quotation_id}
```
Retorna detalles de cotización con joins (Branch, Model, Description)

### Scraper Mapfre
```http
GET /api/v1/scrapers/scrape/mapfre?marca=NISSAN&submarca=VERSA&year=2024&codigo=12345&fecha=2024-01-01&genero=M
```
Ejecuta scraper de Mapfre con Cloudflare bypass

### Scraper HDI
```http
GET /api/v1/scrapers/scrape/hdi
```
Ejecuta scraper de HDI (acceso directo)

## 🏛️ Arquitectura

### Capas de la aplicación

1. **API Layer** (`app/api/`)
   - Define endpoints y rutas
   - Maneja requests/responses HTTP
   - Validación inicial de datos

2. **Service Layer** (`app/services/`)
   - Lógica de negocio
   - Procesamiento de datos
   - Interacción con sistemas externos

3. **Schema Layer** (`app/schemas.py`)
   - Modelos Pydantic
   - Validación de datos
   - Serialización/deserialización

4. **Configuration** (`app/config.py`)
   - Variables de entorno
   - Configuración centralizada
   - Settings con Pydantic

5. **Utils** (`utils/`)
   - Funciones auxiliares
   - Helpers reutilizables
   - Configuración de logging

## 🔧 Configuración

Las variables de entorno se gestionan en `.env`:

```env
APP_NAME=Echo API
APP_VERSION=1.0.0
HOST=0.0.0.0
PORT=8000
DEBUG=true
LOG_LEVEL=INFO
```

## 📝 Buenas Prácticas Implementadas

1. **Separación de responsabilidades**: Cada capa tiene su función específica
2. **Dependency Injection**: Servicios inyectables
3. **Type Hints**: Tipado fuerte en todo el código
4. **Documentación**: Docstrings y ejemplos en OpenAPI
5. **Manejo de errores**: HTTPExceptions estructuradas
6. **Logging**: Sistema de logging configurado
7. **Validación**: Pydantic para validación robusta
8. **Configuración**: Variables de entorno centralizadas

## 🧪 Testing

```bash
# Probar endpoint de salud
curl http://localhost:8000/health

# Probar endpoint echo
curl -X POST http://localhost:8000/api/v1/echo \
  -H "Content-Type: application/json" \
  -d '{"id":"test","branch":{"id":"1","name":"Toyota"},"model":{"id":"1","name":"Corolla"},"description":{"id":"1","name":"Sedan"}}'
```

## � Dependencias Principales

- **FastAPI**: Framework web moderno
- **Uvicorn**: Servidor ASGI
- **Pydantic**: Validación de datos
- **Pydantic-Settings**: Gestión de configuración

## 🤝 Contribuir

Para agregar nuevas funcionalidades:

1. Crear nuevos schemas en `app/schemas.py`
2. Implementar lógica en `app/services/`
3. Crear endpoints en `app/api/routes.py`
4. Documentar en docstrings

## 📄 Licencia

Este proyecto es de uso interno.
# Scrapper-Multicotizador
