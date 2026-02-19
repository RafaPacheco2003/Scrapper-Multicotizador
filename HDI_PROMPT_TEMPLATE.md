"""
GUÍA COMPLETA PARA CLOUDFLARE BYPASS Y WEB SCRAPING
====================================================

Esta guía documenta TODO lo necesario para configurar scrapers que pasen Cloudflare
exitosamente, incluyendo casos específicos como HDI con React y formularios complejos.

ÚLTIMA ACTUALIZACIÓN: 19 Febrero 2026
ESTADO: ✅ FUNCIONANDO CON MAPFRE Y HDI MÉXICO
"""

# ============================================================================
# CASO ESPECIAL: HDI SEGUROS - FLUJO COMPLETO Y ANÁLISIS TÉCNICO
# ============================================================================

HDI_FLUJO_COMPLETO = """
# ═══════════════════════════════════════════════════════════════════════════
# HDI SEGUROS - DOCUMENTACIÓN COMPLETA DEL FLUJO DE SCRAPING
# ═══════════════════════════════════════════════════════════════════════════

## RESUMEN EJECUTIVO

HDI requiere un flujo multi-paso con interacciones específicas de React:
1. Selección de vehículo (React-Select asíncrono)
2. Navegación automática a página de cotización
3. Selección de año (radio buttons con eventos React específicos)
4. Procesamiento con reCAPTCHA v3
5. Continuación del flujo

**URLs involucradas:**
- Inicio: https://www.hdiconnect.com.mx/productos/autos
- Cotización: https://www.hdiconnect.com.mx/productos/autos/cotizacion

---

## PASO 1: SELECCIÓN DE VEHÍCULO (React-Select)

### ¿Qué es React-Select?
React-Select es un componente de dropdown asíncrono que:
- NO es un `<select>` HTML nativo
- Carga opciones mediante API call
- Requiere eventos específicos de React
- Usa divs y JavaScript para renderizar

### Estructura HTML de React-Select:

```html
<!-- Container principal -->
<div class="css-b62m3t-container">
  
  <!-- Input que se activa al hacer click -->
  <input 
    id="typeahead-marca_modelo" 
    role="combobox" 
    autocomplete="off"
  />
  
  <!-- Input hidden que almacena el valor seleccionado -->
  <input 
    name="typeahead-marca_modelo" 
    type="hidden" 
    value="DODGE ATTITUDE"
  />
  
  <!-- Menu de opciones (se genera dinámicamente) -->
  <div id="react-select-X-listbox">
    <div id="react-select-X-option-0">DODGE ATTITUDE 2020</div>
    <div id="react-select-X-option-1">DODGE ATTITUDE 2021</div>
    <!-- más opciones... -->
  </div>
</div>
```

### Flujo Correcto de Interacción:

```python
# 1. ENCONTRAR EL CONTAINER (no el input directamente)
select_container = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((
        By.CSS_SELECTOR, 
        'div.css-b62m3t-container, div[class*="container"]'
    ))
)

# 2. HACER CLICK EN EL CONTAINER (activa el dropdown)
select_container.click()
time.sleep(0.5-1.0)  # Esperar animación

# 3. AHORA BUSCAR EL INPUT QUE SE ACTIVÓ
vehicle_input = WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((
        By.CSS_SELECTOR, 
        'input[id^="typeahead-"], input[role="combobox"]'
    ))
)

# 4. TIPEAR COMO HUMANO (React escucha cada keystroke)
def _human_type(element, text):
    element.click()
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.05, 0.15))  # Delay entre teclas

_human_type(vehicle_input, "Dodge Attitude")

# 5. ESPERAR RESPUESTA DEL API (3-4 segundos)
# React-Select hace llamada asíncrona al servidor
time.sleep(random.uniform(3, 4))

# 6. BUSCAR OPCIONES CARGADAS (divs dinámicos)
options = WebDriverWait(driver, 8).until(
    lambda d: d.find_elements(By.CSS_SELECTOR, 'div[id*="-option-"]')
)

# 7. SELECCIONAR PRIMERA OPCIÓN
first_option = options[0]
driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", first_option)
time.sleep(0.5)
first_option.click()  # O con JavaScript: driver.execute_script("arguments[0].click();", first_option)

# 8. VERIFICAR SELECCIÓN (verificar input hidden)
hidden_input = driver.find_element(By.CSS_SELECTOR, 'input[name="typeahead-marca_modelo"]')
selected_value = hidden_input.get_attribute('value')
print(f"✅ Vehículo seleccionado: {selected_value}")
```

### ❗ ERRORES COMUNES EN REACT-SELECT:

❌ **ERROR 1:** Buscar input antes de activar container
```python
# MAL: El input no existe hasta hacer click
vehicle_input = driver.find_element(By.ID, "typeahead-marca_modelo")
```

✅ **CORRECTO:** Click en container primero
```python
select_container.click()  # Ahora sí existe el input
time.sleep(0.5)
vehicle_input = driver.find_element(By.ID, "typeahead-marca_modelo")
```

❌ **ERROR 2:** No esperar a que carguen opciones
```python
# MAL: Buscar opciones inmediatamente
vehicle_input.send_keys("Dodge")
options = driver.find_elements(By.CSS_SELECTOR, 'div[id*="-option-"]')
# options = [] porque API aún no respondió
```

✅ **CORRECTO:** Esperar 3-4 segundos después de tipear
```python
vehicle_input.send_keys("Dodge Attitude")
time.sleep(random.uniform(3, 4))  # Esperar API response
options = driver.find_elements(By.CSS_SELECTOR, 'div[id*="-option-"]')
```

❌ **ERROR 3:** Tipear todo el texto de golpe
```python
# MAL: React puede no detectar todos los eventos
vehicle_input.send_keys("Dodge Attitude")
```

✅ **CORRECTO:** Tipear carácter por carácter
```python
for char in "Dodge Attitude":
    vehicle_input.send_keys(char)
    time.sleep(0.05-0.15)
```

### 🎯 POR QUÉ FUNCIONA ASÍ:

1. **Container click:** React-Select escucha eventos en el container, no en el input
2. **Tipeo humano:** React escucha `onInput` y `onChange` en cada carácter
3. **Espera de API:** El dropdown NO tiene opciones hasta que el servidor responde
4. **Click en div:** Las opciones NO son `<option>` sino `<div>` con event listeners

### 📊 NETWORK CALLS DE REACT-SELECT:

Cuando tipeas en el campo, se disparan estas llamadas:

```
Request: GET https://apim-pefai.hdiconnect.com.mx/.../execute-function/.../operation/...
Headers:
  - User-Agent: Chrome/145.0.7632.76
  - Accept: application/json
  - Referer: https://www.hdiconnect.com.mx/productos/autos

Response: 200 OK
Body: {
  "options": [
    {"label": "DODGE ATTITUDE 2020", "value": "DODGE ATTITUDE"},
    {"label": "DODGE ATTITUDE 2021", "value": "DODGE ATTITUDE"},
    ...
  ]
}
```

El componente React espera esta respuesta para renderizar las opciones.

---

## PASO 2: NAVEGACIÓN AUTOMÁTICA

### ¿Qué sucede después de seleccionar el vehículo?

Cuando seleccionas una opción del dropdown, React automáticamente:
1. Actualiza el input hidden con el valor
2. **Navega a la página de cotización** (sin hacer click en botón)
3. Carga nueva URL: `/productos/autos/cotizacion`

### Código para detectar esto:

```python
# Después de seleccionar vehículo en dropdown
first_option.click()
time.sleep(random.uniform(1, 2))

# Verificar si se seleccionó
hidden_input = driver.find_element(By.CSS_SELECTOR, 'input[name="typeahead-marca_modelo"]')
selected_value = hidden_input.get_attribute('value')

# Esperar transición automática
time.sleep(random.uniform(3, 4))

# Verificar URL actual
current_url = driver.current_url
if '/cotizacion' in current_url:
    print("✅ Navegó automáticamente a página de cotización")
else:
    print("🔍 Buscar botón 'Iniciar mi cotización'")
    # Solo si no navegó automáticamente, buscar el botón
```

### ⚠️ ERROR COMÚN:

No entender que la navegación es AUTOMÁTICA:

```python
# MAL: Buscar botón que puede no existir
submit_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
# Element not found porque ya navegó
```

✅ **CORRECTO:** Verificar si ya avanzó antes de buscar botón:

```python
if '/cotizacion' not in driver.current_url:
    # Solo buscar botón si todavía estamos en página inicial
    try:
        submit_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        submit_button.click()
    except:
        pass  # Ya navegó automáticamente
```

---

## PASO 3: SELECCIÓN DE AÑO (CRÍTICO - RADIO BUTTONS)

### 🚨 PROBLEMA PRINCIPAL: Los clicks en radio buttons NO funcionan

#### ¿Por qué fallan los clicks normales?

```python
# ❌ ESTO NO FUNCIONA:
year_radio = driver.find_element(By.CSS_SELECTOR, 'input[name="ao"][value="2024"]')
year_radio.click()  # Click registrado pero React NO reacciona

# Resultado:
# - Visualmente: Radio button aparece seleccionado ✓
# - Internamente: React NO detecta el cambio
# - Consecuencia: No se disparan las llamadas API necesarias
```

### 🔍 ANÁLISIS TÉCNICO: ¿Por qué NO funciona?

**Estructura HTML Real:**

```html
<label for="Simpleradio-2024">
  <span>2024</span>
  <input 
    id="Simpleradio-2024" 
    name="ao" 
    type="radio" 
    value="2024"
  />
</label>
```

**Lo que hace un usuario REAL:**
1. Mueve el mouse al texto "2024"
2. **Hace click en el LABEL**, NO en el input
3. El navegador propaga el evento del label al input
4. React escucha eventos en el LABEL

**Lo que hace Selenium por defecto:**
1. Busca el `<input>`
2. Hace click DIRECTO en el input
3. El evento NO pasa por el label
4. React NO se entera del cambio

### ✅ SOLUCIÓN COMPLETA: Click en el LABEL

```python
# 1. BUSCAR EL INPUT (para verificar)
year_radio = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((
        By.CSS_SELECTOR,
        'input[name="ao"][value="2024"]'
    ))
)

# 2. BUSCAR EL LABEL ASOCIADO (lo que el usuario clickea)
radio_id = year_radio.get_attribute('id')  # "Simpleradio-2024"
year_label = driver.find_element(By.CSS_SELECTOR, f'label[for="{radio_id}"]')

# 3. HACER SCROLL AL LABEL
driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", year_label)
time.sleep(0.8)

# 4. CLICK EN EL LABEL CON TODOS LOS EVENTOS REACT
driver.execute_script("""
    const label = arguments[0];
    const input = arguments[1];
    
    // Eventos en el LABEL (lo que React escucha)
    label.dispatchEvent(new MouseEvent('mousedown', { bubbles: true, cancelable: true }));
    label.dispatchEvent(new MouseEvent('mouseup', { bubbles: true, cancelable: true }));
    label.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
    
    // Marcar el input como checked
    input.checked = true;
    
    // Eventos en el INPUT (para compatibilidad)
    input.dispatchEvent(new Event('click', { bubbles: true }));
    input.dispatchEvent(new Event('change', { bubbles: true }));
    input.dispatchEvent(new Event('input', { bubbles: true }));
""", year_label, year_radio)

print("✅ Click en label ejecutado con eventos React completos")
```

### 📋 EVENTOS DISPARADOS (en orden):

1. **mousedown** en label → React prepara para cambio
2. **mouseup** en label → React confirma intención
3. **click** en label → React registra interacción del usuario
4. **click** en input → Browser marca radio como selected
5. **change** en input → React actualiza estado interno
6. **input** en input → React dispara handlers adicionales

### ⚡ CONSECUENCIAS DE HACER CLICK CORRECTO:

Cuando haces click en el LABEL (no en el input):

```
✓ Radio button se marca visualmente
✓ React actualiza su estado interno
✓ Se dispara reCAPTCHA v3 verificación
✓ Se ejecutan llamadas API:
  - GET /recaptcha/api2/reload
  - POST /utils-api/recaptcha_v3/verify-token  
  - POST /oneapp/v2/submit
✓ Formulario avanza al siguiente paso
```

### 📊 NETWORK CALLS DESPUÉS DE CLICK CORRECTO:

```
1. https://www.google.com/recaptcha/api2/reload?k=6Lfcm6YrAAAA...
   Purpose: Validar que no es un bot
   
2. https://apim-pefai.hdiconnect.com.mx/.../recaptcha_v3/verify-token
   Body: { token: "...", action: "submit" }
   Purpose: Verificar token de reCAPTCHA en backend
   
3. https://apim-pefai.hdiconnect.com.mx/.../oneapp/v2/submit
   Body: { vehiculo: "DODGE ATTITUDE", año: "2024", ... }
   Purpose: Enviar datos del formulario
   
4. Navegación: https://www.hdiconnect.com.mx/productos/autos/cotizacion
   O actualización de la misma página con siguiente paso
```

### ❌ COMPARACIÓN: Click incorrecto vs correcto

**CLICK INCORRECTO (directo en input):**
```python
year_radio.click()
```
Resultado:
- ✓ Radio button marcado visualmente
- ✗ React NO actualiza estado
- ✗ reCAPTCHA NO se dispara
- ✗ API calls NO se ejecutan
- ✗ Formulario NO avanza

**CLICK CORRECTO (en label con eventos):**
```python
driver.execute_script("""
    const label = arguments[0];
    const input = arguments[1];
    label.dispatchEvent(new MouseEvent('click', { bubbles: true }));
    input.checked = true;
    input.dispatchEvent(new Event('change', { bubbles: true }));
""", year_label, year_radio)
```
Resultado:
- ✓ Radio button marcado visualmente
- ✓ React actualiza estado
- ✓ reCAPTCHA se dispara
- ✓ API calls se ejecutan
- ✓ Formulario avanza

---

## PASO 4: TIMING Y ESPERAS

### Tiempos críticos en el flujo de HDI:

```python
# Después de seleccionar vehículo del dropdown
first_option.click()
time.sleep(random.uniform(1, 2))  # Esperar que React actualice

# Esperar transición de página
time.sleep(random.uniform(3, 4))  # Esperar navegación automática

# Después de hacer click en año
year_label.click()  # (mediante JavaScript con eventos)
time.sleep(random.uniform(2, 3))  # Esperar reCAPTCHA v3
time.sleep(random.uniform(3, 4))  # Esperar API calls (verify-token + submit)
```

### ⏱️ ¿Por qué estos tiempos específicos?

1. **1-2s después de selección:** React necesita actualizar el DOM
2. **3-4s transición:** Navegación puede tomar tiempo en red lenta
3. **2-3s reCAPTCHA:** Google valida el navegador
4. **3-4s API calls:** Servidor procesa y responde

### 🎯 OPTIMIZACIÓN: Esperas inteligentes vs fijas

❌ **MAL - Esperas fijas:**
```python
time.sleep(5)  # Siempre espera 5s, incluso si ya terminó
```

✅ **MEJOR - Esperas con verificación:**
```python
# Esperar hasta que termine reCAPTCHA O timeout
for i in range(10):
    if self._is_recaptcha_complete(driver):
        break
    time.sleep(0.5)
```

✅ **ÓPTIMO - WebDriverWait con condiciones:**
```python
# Esperar hasta que aparezca el siguiente elemento
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "siguiente-paso"))
)
```

---

## PASO 5: VERIFICACIÓN Y DEBUGGING

### Cómo verificar que todo funcionó:

```python
# 1. Verificar selección de vehículo
hidden_input = driver.find_element(By.CSS_SELECTOR, 'input[name="typeahead-marca_modelo"]')
assert hidden_input.get_attribute('value') == "DODGE ATTITUDE"

# 2. Verificar URL correcta
assert '/cotizacion' in driver.current_url

# 3. Verificar que radio button está seleccionado
year_radio = driver.find_element(By.CSS_SELECTOR, 'input[name="ao"][value="2024"]')
assert year_radio.is_selected()

# 4. Verificar que apareció siguiente paso del formulario
try:
    next_step_element = driver.find_element(By.ID, "siguiente-campo")
    print("✅ Formulario avanzó al siguiente paso")
except:
    print("❌ Formulario NO avanzó")
```

### Screenshots para debugging:

```python
try:
    year_label.click()  # Intentar acción
except Exception as e:
    # Guardar evidencia del error
    driver.save_screenshot("/tmp/hdi_error.png")
    with open("/tmp/hdi_error.html", "w") as f:
        f.write(driver.page_source)
    print(f"Error: {str(e)}")
    print("Screenshots guardados en /tmp/")
```

---

## RESUMEN: FLUJO COMPLETO OPTIMIZADO

```python
async def scrape_hdi(driver, url):
    # PASO 1: Acceder a página
    driver.get(url)
    _simulate_human_behavior(driver)
    time.sleep(random.uniform(2, 4))
    
    # PASO 2: Seleccionar vehículo (React-Select)
    select_container = driver.find_element(By.CSS_SELECTOR, 'div.css-b62m3t-container')
    select_container.click()
    time.sleep(1)
    
    vehicle_input = driver.find_element(By.CSS_SELECTOR, 'input[role="combobox"]')
    _human_type(vehicle_input, "Dodge Attitude")
    
    time.sleep(random.uniform(3, 4))  # Esperar API
    
    options = driver.find_elements(By.CSS_SELECTOR, 'div[id*="-option-"]')
    options[0].click()
    time.sleep(2)
    
    # PASO 3: Verificar navegación
    time.sleep(random.uniform(3, 4))
    if '/cotizacion' not in driver.current_url:
        # Buscar botón submit solo si es necesario
        try:
            submit_btn = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
            submit_btn.click()
            time.sleep(4)
        except:
            pass
    
    # PASO 4: Seleccionar año (click en LABEL)
    year_radio = driver.find_element(By.CSS_SELECTOR, 'input[name="ao"][value="2024"]')
    radio_id = year_radio.get_attribute('id')
    year_label = driver.find_element(By.CSS_SELECTOR, f'label[for="{radio_id}"]')
    
    driver.execute_script("""
        const label = arguments[0];
        const input = arguments[1];
        label.dispatchEvent(new MouseEvent('click', { bubbles: true }));
        input.checked = true;
        input.dispatchEvent(new Event('change', { bubbles: true }));
    """, year_label, year_radio)
    
    # PASO 5: Esperar procesamiento
    time.sleep(random.uniform(2, 3))  # reCAPTCHA
    time.sleep(random.uniform(3, 4))  # API calls
    
    # PASO 6: Verificar siguiente paso
    try:
        continue_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Continuar')]")
        continue_btn.click()
    except:
        pass  # Puede avanzar automáticamente
    
    return driver.page_source
```

---

## LECCIONES APRENDIDAS

### ✅ LO QUE FUNCIONA:

1. **Click en container antes de buscar input** (React-Select)
2. **Tipeo carácter por carácter** con delays humanos
3. **Esperar 3-4s después de tipear** para que API responda
4. **Click en LABEL, NO en input** para radio buttons
5. **Disparar TODOS los eventos** (mousedown, mouseup, click, change, input)
6. **Verificar URL** para detectar navegación automática
7. **Esperas separadas** para reCAPTCHA (2-3s) y API (3-4s)

### ❌ LO QUE NO FUNCIONA:

1. Buscar input before de activar container
2. send_keys() todo el texto de golpe
3. Buscar opciones inmediatamente sin esperar API
4. Click directo en radio input
5. Solo disparar evento 'click' o 'change'
6. Asumir que hay botón submit siempre
7. Esperar navegación cuando el formulario se procesa en misma página

### 🎓 CONCEPTOS CLAVE:

- **React-Select**: Dropdown asíncrono que requiere flujo específico
- **Label-for-Input**: Relación HTML donde usuario clickea label
- **Event Bubbling**: Eventos se propagan de label → input
- **reCAPTCHA v3**: Validación invisible que toma 2-3 segundos
- **SPA (Single Page Application)**: Formulario puede actualizar sin cambiar URL

---

## TROUBLESHOOTING ESPECÍFICO DE HDI

### Problema: "Opciones no aparecen en dropdown"
**Causa**: No esperaste suficiente para API response
**Solución**: Aumentar tiempo después de tipear a 4-5 segundos

### Problema: "Año se selecciona visualmente pero no avanza"  
**Causa**: Click en input directo, React no detecta
**Solución**: Click en label con dispatchEvent

### Problema: "Element is stale"
**Causa**: DOM se actualizó después de buscar el elemento
**Solución**: Buscar elemento justo antes de usarlo

### Problema: "No se encuentra botón submit"
**Causa**: Ya navegó automáticamente
**Solución**: Verificar URL antes de buscar botón

---

## CÓDIGO COMPLETO REFERENCIA

Ver archivo: `/scrapers/implementations/hdi_scraper.py`

Clase: `HDIScraper`
Método principal: `async def scrape(self, url: str)`
Pasos implementados: 8 pasos completos con verificaciones

"""

# ============================================================================
# PARTE 1: CONFIGURACIÓN TÉCNICA QUE FUNCIONA
# ============================================================================

CONFIGURACION_EXITOSA = """
## STACK TECNOLÓGICO QUE FUNCIONA

### Librerías Requeridas (requirements.txt):
```
selenium==4.15.2
undetected-chromedriver>=3.5.5
beautifulsoup4==4.12.2
setuptools  # CRÍTICO para Python 3.14+
```

### Versiones de Python:
- Python 3.14: ✅ COMPATIBLE (con setuptools)
- Python 3.12+: ✅ COMPATIBLE (con setuptools)
- Python 3.10-3.11: ✅ COMPATIBLE

### Código Base que Funciona:

```python
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import random

# CONFIGURACIÓN DE CHROME
options = uc.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--start-maximized')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--lang=es-MX')
options.add_argument('--accept-lang=es-MX,es;q=0.9')

# CREAR DRIVER (auto-detecta versión de Chrome)
driver = uc.Chrome(options=options, use_subprocess=False)
```

### ⚠️ ERRORES COMUNES Y SOLUCIONES

#### Error 1: "ModuleNotFoundError: No module named 'distutils'"
**Causa**: Python 3.12+ removió distutils
**Solución**: 
```bash
pip install setuptools
```

#### Error 2: "This version of ChromeDriver only supports Chrome version X"
**Causa**: version_main= forzado a versión incorrecta
**Solución**: 
```python
# ❌ MAL: driver = uc.Chrome(options=options, version_main=131)
# ✅ BIEN: driver = uc.Chrome(options=options, use_subprocess=False)
```

#### Error 3: "Cloudflare Turnstile detectado" pero logs dicen que pasó
**Causa**: No verifica realmente si Cloudflare se resolvió
**Solución**: Implementar verificación dinámica (ver código abajo)
"""

# ============================================================================
# PARTE 2: ESTRATEGIA DE CLOUDFLARE BYPASS
# ============================================================================

ESTRATEGIA_BYPASS = """
## ESTRATEGIA COMPLETA PARA PASAR CLOUDFLARE

### 1. USAR UNDETECTED-CHROMEDRIVER
- NO usar selenium normal (detectado inmediatamente)
- undetected-chromedriver modifica el binario de Chrome

### 2. ACCESO PROGRESIVO (MUY IMPORTANTE)
```python
# Paso 1: Ir primero a la página base
driver.get("https://sitio.com")
time.sleep(random.uniform(2, 4))

# Paso 2: Simular comportamiento humano
_simulate_human_behavior(driver)

# Paso 3: Entonces navegar a URL completa
driver.get("https://sitio.com/page?params=...")
```

### 3. VERIFICACIÓN DINÁMICA DE CLOUDFLARE

```python
def _check_and_wait_for_cloudflare(driver, max_attempts=30):
    for attempt in range(max_attempts):
        html = driver.page_source.lower()
        
        # Verificar indicadores de Cloudflare
        cloudflare_indicators = [
            "cloudflare" in html,
            "turnstile" in html,
            "cf-challenge" in html,
            "challenge-platform" in html,
            "just a moment" in html
        ]
        
        if any(cloudflare_indicators):
            print(f"Cloudflare detectado (intento {attempt + 1}), esperando...")
            time.sleep(2)
            continue
        
        # Verificar si formulario está presente (pasó Cloudflare)
        try:
            driver.find_element(By.ID, "tu-elemento-esperado")
            print("✅ Cloudflare pasado")
            return True
        except:
            time.sleep(2)
            continue
    
    return False
```

### 4. COMPORTAMIENTO HUMANO

```python
def _simulate_human_behavior(driver):
    # Scroll aleatorio
    scroll_amount = random.randint(100, 500)
    driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
    time.sleep(random.uniform(0.3, 0.7))
    
    # Scroll de vuelta
    driver.execute_script(f"window.scrollBy(0, -{scroll_amount // 2});")
    time.sleep(random.uniform(0.3, 0.7))

def _human_type(driver, element, text):
    element.click()
    time.sleep(random.uniform(0.1, 0.3))
    
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.05, 0.15))
```

### 5. CLICKS CON MOVIMIENTO DE MOUSE

```python
from selenium.webdriver.common.action_chains import ActionChains

button = driver.find_element(By.ID, "submit-button")
actions = ActionChains(driver)
actions.move_to_element(button).pause(random.uniform(0.3, 0.7)).click().perform()
```
"""

# ============================================================================
# PARTE 3: PROMPT PARA NUEVAS PÁGINAS
# ============================================================================

PROMPT_GENERAL = """
# Configurar Scraper para Nueva Página con Cloudflare

Necesito que configures un scraper para: [NOMBRE DEL SITIO]

## INFORMACIÓN TÉCNICA DEL NAVEGADOR

### 1. User-Agent Real
[Abre el navegador → F12 → Network → Cualquier request → Headers → user-agent]
[Copia el valor EXACTO]

User-Agent: 

### 2. Accept-Language
[En los mismos Headers, busca "accept-language"]

Accept-Language: 

### 3. Otros Headers Importantes (opcional)
[Si hay algo especial en Headers, pégalo aquí]

Headers adicionales:
- 
- 

## INFORMACIÓN DE LA PÁGINA

### 4. URL Principal
URL: 

### 5. ¿Aparece Cloudflare Challenge?
☐ Sí, aparece checkbox de Cloudflare
☐ Sí, aparece puzzle de Cloudflare
☐ Sí, aparece otra verificación
☐ No, se accede directamente

Si aparece: Describe qué ves exactamente

### 6. Formularios que Necesito Rellenar

[Abre el navegador manualmente en la página]
[F12 → Elements → Busca los inputs]
[Para cada input, proporciona]:

**Campo 1:**
- Label/Nombre: 
- Type (text, email, tel, etc.): 
- ID: 
- Class: 
- Valor de ejemplo: 

**Campo 2:**
- Label/Nombre: 
- Type: 
- ID: 
- Class: 
- Valor de ejemplo: 

[Repite para todos los campos]

### 7. Botones para Continuar
[F12 → Elements → Busca los buttons]

**Botón 1:**
- Texto visible: 
- ID: 
- Class: 
- Función: 

### 8. Screenshots de Network

[Abre DevTools → Network tab]
[Recarga la página (Cmd+R o Ctrl+R)]
[Toma screenshot mostrando]:

1. Primeros 10 requests (con User-Agent visible)
2. Todos los requests de tracking (Datadog, GA, Facebook, etc.)
3. URL final que se carga después de pasar Cloudflare

[Pega descripción o adjunta screenshots]

Network requests:
- Datadog RUM: [URL]
- Datadog Logs: [URL]
- Google Analytics: [URL]
- Facebook Pixel: [URL]
- Otros:

### 9. Estructura HTML de Cloudflare (si aplica)

[Si aparece challenge]
[F12 → Elements → Busca iframe de Cloudflare]
[Copia el HTML o describe la estructura]

HTML o descripción:

### 10. Información Adicional

¿Hay algo especial que debo saber?
- ¿Requiere JavaScript específico?
- ¿Hay captchas adicionales?
- ¿Hay validaciones especiales?
- ¿Los datos están en iframes?

Información adicional:

---

## CHECKLIST ANTES DE ENVIAR

☐ Incluí User-Agent correcto
☐ Incluí Accept-Language
☐ Incluí todos los campos del formulario con ID/Class
☐ Incluí botones con ID/Class
☐ Tomé screenshots de Network mostrando tracking
☐ Describo si aparece Cloudflare y de qué tipo
☐ Indico la URL de la página principal

"""

# ============================================================================
# PARTE 4: TROUBLESHOOTING Y DEBUG
# ============================================================================

TROUBLESHOOTING = """
## TROUBLESHOOTING: PROBLEMAS Y SOLUCIONES

### Problema: Cloudflare sigue detectando el bot
**Síntomas**: 
- Aparece "Just a moment..."
- Se queda en challenge infinito
- Logs dicen "pasado" pero en realidad no

**Soluciones**:
1. ✅ Verificar que estás usando undetected-chromedriver (no selenium normal)
2. ✅ Implementar acceso progresivo (base URL primero)
3. ✅ Agregar comportamiento humano (scrolls, movimientos)
4. ✅ Verificar DINÁMICAMENTE que Cloudflare se resolvió
5. ✅ Aumentar tiempo de espera (hasta 60 segundos)
6. ✅ Verificar que use_subprocess=False

### Problema: Error de versión de Chrome
**Error**: "This version of ChromeDriver only supports Chrome version X"

**Solución**:
```python
# NO especificar version_main, dejar que auto-detecte
driver = uc.Chrome(options=options, use_subprocess=False)
```

### Problema: Python 3.14+ con distutils
**Error**: "ModuleNotFoundError: No module named 'distutils'"

**Solución**:
```bash
pip install setuptools undetected-chromedriver>=3.5.5
```

### Problema: El captcha/challenge aparece pero no se resuelve
**Posibles causas**:
1. Versión vieja de undetected-chromedriver
2. No hay suficiente tiempo de espera
3. Falta comportamiento humano

**Solución completa**:
```python
# 1. Actualizar librería
pip install undetected-chromedriver --upgrade

# 2. Aumentar MAX_ATTEMPTS en verificación
cloudflare_passed = _check_and_wait_for_cloudflare(driver, max_attempts=40)

# 3. Agregar más delays aleatorios
time.sleep(random.uniform(3, 6))
```

### Problema: Funciona localmente pero falla en servidor
**Causas comunes**:
- Servidor no tiene display (headless mode detectado)
- IP del servidor bloqueada
- Diferentes versiones de Chrome

**Soluciones**:
```python
# Si necesitas headless (menos recomendado):
options.add_argument('--headless=new')  # Modo headless moderno

# Mejor: usar servidor con display o Xvfb
sudo apt-get install xvfb
xvfb-run python scraper.py
```

### Problema: Funciona a veces, falla otras veces
**Causa**: Detección por volumen o patrón

**Soluciones**:
1. Aumentar delays aleatorios
2. Rotar User-Agents (cuidado, debe coincidir con Chrome real)
3. Usar proxies rotativos
4. Implementar rate limiting

## VERIFICACIÓN DE QUE TODO FUNCIONA

### Checklist antes de considerar que funciona:

✅ Chrome se abre correctamente
✅ No aparece "Chrome is being controlled by automated software"
✅ Cloudflare challenge aparece Y se resuelve solo
✅ Formulario de contacto aparece después del challenge
✅ Se pu pueden rellenar campos sin errores
✅ Click en botón funciona y navega a siguiente página
✅ Se extraen datos correctamente

### Logs que indican ÉXITO real:

```
✅ Chrome iniciado con undetected-chromedriver
🌐 Accediendo a página base...
🔄 Navegando a URL con parámetros...
🔍 Verificando presencia de Cloudflare...
⏳ Cloudflare detectado (intento 1/30), esperando...
⏳ Esperando formulario (intento 2/30)...
✅ Formulario detectado - Cloudflare pasado
✅ Cloudflare pasado exitosamente
📝 Rellenando formulario de contacto...
✓ Nombre ingresado
✓ Email ingresado
✓ Teléfono ingresado
🖱️ Haciendo click en botón Continuar...
✓ Botón clickeado
✅ Scraping completado exitosamente
```

### Logs que indican FALLO:

```
❌ No se pudo pasar Cloudflare después de múltiples intentos
❌ Error en scraping: Timeout waiting for element
⚠️ Cloudflare Turnstile detectado, esperando... (y se queda ahí)
```
"""

# ============================================================================
# PARTE 5: CÓDIGO COMPLETO DE EJEMPLO
# ============================================================================

EJEMPLO_COMPLETO = """
## EJEMPLO COMPLETO: SCRAPER CON CLOUDFLARE BYPASS

```python
import logging
from typing import Dict, Any
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import random

logger = logging.getLogger(__name__)

class CloudflareScraper:
    
    def __init__(self):
        self.base_url = "https://tusitio.com"
        self.logger = logger
    
    async def scrape(self, url: str) -> Dict[str, Any]:
        driver = None
        try:
            self.logger.info("🚀 Iniciando scraping...")
            
            # 1. Configurar Chrome
            options = uc.ChromeOptions()
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--start-maximized')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument('--lang=es-MX')
            options.add_argument('--accept-lang=es-MX,es;q=0.9')
            
            driver = uc.Chrome(options=options, use_subprocess=False)
            self.logger.info("✅ Chrome iniciado")
            
            # 2. Acceso progresivo
            self.logger.info("🌐 Accediendo a página base...")
            driver.get(self.base_url)
            self._simulate_human_behavior(driver)
            time.sleep(random.uniform(2, 4))
            
            self.logger.info("🔄 Navegando a URL objetivo...")
            driver.get(url)
            time.sleep(random.uniform(1, 2))
            
            # 3. Esperar carga
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # 4. Verificar y esperar Cloudflare
            if not self._check_and_wait_for_cloudflare(driver):
                raise Exception("No se pudo pasar Cloudflare")
            
            self.logger.info("✅ Cloudflare pasado")
            
            # 5. Interactuar con página (rellenar formularios, etc.)
            self._interact_with_page(driver)
            
            # 6. Extraer datos
            html = driver.page_source
            data = self._parse_data(html)
            
            return data
            
        except Exception as e:
            self.logger.error(f"❌ Error: {str(e)}")
            raise
        finally:
            if driver:
                driver.quit()
    
    def _check_and_wait_for_cloudflare(self, driver, max_attempts=30):
        self.logger.info("🔍 Verificando Cloudflare...")
        
        for attempt in range(max_attempts):
            html = driver.page_source.lower()
            
            cloudflare_indicators = [
                "cloudflare" in html,
                "turnstile" in html,
                "cf-challenge" in html,
                "just a moment" in html
            ]
            
            if any(cloudflare_indicators):
                self.logger.warning(f"⏳ Cloudflare detectado ({attempt + 1}/{max_attempts})")
                time.sleep(2)
                continue
            
            # Verificar elemento esperado
            try:
                driver.find_element(By.ID, "tu-elemento")
                self.logger.info("✅ Formulario detectado")
                return True
            except:
                time.sleep(2)
        
        return False
    
    def _simulate_human_behavior(self, driver):
        try:
            scroll = random.randint(100, 500)
            driver.execute_script(f"window.scrollBy(0, {scroll});")
            time.sleep(random.uniform(0.3, 0.7))
            driver.execute_script(f"window.scrollBy(0, -{scroll // 2});")
            time.sleep(random.uniform(0.3, 0.7))
        except:
            pass
    
    def _human_type(self, element, text):
        element.click()
        time.sleep(random.uniform(0.1, 0.3))
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.05, 0.15))
    
    def _interact_with_page(self, driver):
        # Ejemplo: rellenar formulario
        try:
            name_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "name"))
            )
            self._human_type(name_input, "Juan Pérez")
            
            submit_btn = driver.find_element(By.ID, "submit")
            actions = ActionChains(driver)
            actions.move_to_element(submit_btn).pause(0.5).click().perform()
        except Exception as e:
            self.logger.error(f"Error interactuando: {e}")
    
    def _parse_data(self, html):
        # Tu lógica de parsing aquí
        return {"success": True, "data": []}
```
"""

# ============================================================================
# PARTE 6: RECURSOS Y REFERENCIAS
# ============================================================================

RECURSOS = """
## RECURSOS ÚTILES

### Documentación:
- undetected-chromedriver: https://github.com/ultrafunkamsterdam/undetected-chromedriver
- Selenium: https://selenium-python.readthedocs.io/

### Debugging:
1. Usar modo debug para ver el navegador:
   ```python
   scraper = MapfreScraper(debug=True, wait_time=30)
   ```

2. Tomar screenshots cuando haya error:
   ```python
   driver.save_screenshot("error.png")
   ```

3. Guardar HTML para análisis:
   ```python
   with open("page.html", "w") as f:
       f.write(driver.page_source)
   ```

### Herramientas útiles:
- Chrome DevTools (F12): Para inspeccionar requests y elementos
- Network tab: Ver qué requests hace Cloudflare
- Console tab: Ver errores JavaScript que puedan ayudar

## NOTAS FINALES

- Cloudflare se actualiza constantemente, esta guía es de Febrero 2026
- Lo que funciona hoy puede dejar de funcionar mañana
- Siempre verifica logs cuidadosamente
- No confíes en logs que "dicen" que pasó sin verificar realmente
- El comportamiento humano es clave
- undetected-chromedriver es tu mejor amigo

¡ÉXITO! 🚀
"""

# ============================================================================
# IMPRIMIR GUÍA COMPLETA
# ============================================================================

if __name__ == "__main__":
    print(CONFIGURACION_EXITOSA)
    print("\n" + "="*80 + "\n")
    print(ESTRATEGIA_BYPASS)
    print("\n" + "="*80 + "\n")
    print(PROMPT_GENERAL)
    print("\n" + "="*80 + "\n")
    print(TROUBLESHOOTING)
    print("\n" + "="*80 + "\n")
    print(EJEMPLO_COMPLETO)
    print("\n" + "="*80 + "\n")
    print(RECURSOS)
