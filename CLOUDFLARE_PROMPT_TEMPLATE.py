"""
GUÍA COMPLETA PARA CLOUDFLARE BYPASS EN WEB SCRAPING
=====================================================

Esta guía documenta TODO lo necesario para configurar scrapers que pasen Cloudflare
exitosamente, incluyendo soluciones a problemas comunes.

ÚLTIMA ACTUALIZACIÓN: 19 Febrero 2026
ESTADO: ✅ FUNCIONANDO CON MAPFRE MÉXICO
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
