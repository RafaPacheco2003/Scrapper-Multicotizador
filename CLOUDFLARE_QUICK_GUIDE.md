# 🔐 GUÍA COMPLETA: Cloudflare Bypass (Actualizada)

**Última actualización**: 19 Febrero 2026  
**Estado**: ✅ FUNCIONANDO con Mapfre México  
**Python**: 3.14 compatible  
**Chrome**: 145.0 compatible

---

## 🚀 Quick Start

### 1. Instalación
```bash
pip install selenium undetected-chromedriver>=3.5.5 beautifulsoup4 setuptools
```

### 2. Código Mínimo que Funciona
```python
import undetected_chromedriver as uc
import time

options = uc.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--start-maximized')
options.add_argument('--lang=es-MX')

driver = uc.Chrome(options=options, use_subprocess=False)
driver.get("https://tusitio.com")
```

**⚠️ IMPORTANTE**: 
- NO usar `version_main=` (auto-detecta la versión)
- Usar `use_subprocess=False`
- Instalar `setuptools` para Python 3.14+

---

## ⚠️ PROBLEMAS RESUELTOS (HE SUFRIDO ESTOS)

### ❌ Error 1: `ModuleNotFoundError: No module named 'distutils'`
**Por qué pasa**: Python 3.12+ removió distutils  
**Solución**: 
```bash
pip install setuptools
```

### ❌ Error 2: `This version of ChromeDriver only supports Chrome version 131`
**Por qué pasa**: Especificaste `version_main=` incorrecto  
**Solución**: 
```python
# ❌ MAL (fuerza versión incorrecta)
driver = uc.Chrome(options=options, version_main=131)

# ✅ BIEN (auto-detecta tu Chrome)
driver = uc.Chrome(options=options, use_subprocess=False)
```

### ❌ Error 3: Logs dicen "Cloudflare pasado" pero realmente NO pasó
**Por qué pasa**: Solo esperó X segundos sin verificar realmente  
**Solución**: Implementar verificación dinámica
```python
def _check_cloudflare(driver, max_attempts=30):
    """Verifica REALMENTE que Cloudflare pasó"""
    for i in range(max_attempts):
        html = driver.page_source.lower()
        
        # Buscar indicadores de Cloudflare
        if any([
            "cloudflare" in html,
            "turnstile" in html,
            "cf-challenge" in html,
            "just a moment" in html
        ]):
            print(f"⏳ Cloudflare detectado ({i+1}/{max_attempts})")
            time.sleep(2)
            continue
            
        # Verificar que la página REAL cargó
        try:
            driver.find_element(By.ID, "tu-elemento-esperado")
            print("✅ Cloudflare REALMENTE pasado")
            return True
        except:
            time.sleep(2)
    
    print("❌ Cloudflare NO pasó")
    return False
```

---

## 🎯 Estrategia COMPLETA que Funciona

### 1️⃣ Acceso Progresivo (CRÍTICO)
```python
# ❌ MAL: Ir directo a URL con parámetros
driver.get("https://sitio.com/page?id=123&param=456")

# ✅ BIEN: Acceso progresivo
driver.get("https://sitio.com")  # Base primero
time.sleep(2)

# Simular comportamiento humano
driver.execute_script("window.scrollBy(0, 300);")
time.sleep(1)

driver.get("https://sitio.com/page?id=123&param=456")  # URL completa después
```

### 2️⃣ Comportamiento Humano
```python
import random

def _simulate_human_behavior(driver):
    """Scrolls aleatorios"""
    scroll = random.randint(100, 500)
    driver.execute_script(f"window.scrollBy(0, {scroll});")
    time.sleep(random.uniform(0.3, 0.7))
    
    driver.execute_script(f"window.scrollBy(0, -{scroll // 2});")
    time.sleep(random.uniform(0.3, 0.7))

def _human_type(element, text):
    """Tipeo carácter por carácter"""
    element.click()
    time.sleep(random.uniform(0.1, 0.3))
    
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.05, 0.15))
```

### 3️⃣ Clicks con Movimiento de Mouse
```python
from selenium.webdriver.common.action_chains import ActionChains

button = driver.find_element(By.ID, "submit")
actions = ActionChains(driver)
actions.move_to_element(button).pause(random.uniform(0.3, 0.7)).click().perform()
```

---

## ✅ Checklist de Éxito

Antes de considerar que funciona:

- [ ] Chrome se abre sin mensaje "automated software"
- [ ] Cloudflare challenge aparece
- [ ] Cloudflare challenge se resuelve automáticamente (espera 5-30 seg)
- [ ] Formulario/contenido real aparece
- [ ] Puedes rellenar campos sin errores
- [ ] Click en botón funciona
- [ ] Navegas a siguiente página exitosamente
- [ ] Se extraen datos correctamente

---

## 📊 Logs Correctos vs Incorrectos

### ✅ Logs que indican ÉXITO REAL
```
🚀 Iniciando scraping con undetected-chromedriver...
✅ Chrome iniciado con undetected-chromedriver
🌐 Accediendo a página base...
🔄 Navegando a URL con parámetros...
🔍 Verificando presencia de Cloudflare...
⏳ Cloudflare detectado (intento 1/30), esperando...
⏳ Cloudflare detectado (intento 2/30), esperando...
✅ Formulario detectado - Cloudflare pasado
✅ Cloudflare pasado exitosamente
📝 Rellenando formulario de contacto...
✓ Nombre ingresado
✓ Email ingresado
✓ Teléfono ingresado
✅ Scraping completado exitosamente
```

### ❌ Logs que indican FALLO (aunque digan "pasado")
```
⚠️ Cloudflare Turnstile detectado, esperando...
Cloudflare pasado correctamente  ← MENTIRA, no verificó nada
⚠️ No se pudo rellenar nombre: Element not found  ← Formulario no existe
❌ Error al clickear botón: Timeout
```

**LECCIÓN**: No confíes en mensajes sin verificar realmente

---

## 📚 Estructura Completa del Scraper

```python
import logging
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import random

class CloudflareScraper:
    
    def __init__(self, debug=False):
        self.base_url = "https://tusitio.com"
        self.debug = debug
        self.logger = logging.getLogger(__name__)
    
    async def scrape(self, url: str):
        driver = None
        try:
            self.logger.info("🚀 Iniciando scraping...")
            
            # 1. Setup Chrome
            driver = self._setup_chrome()
            
            # 2. Acceso progresivo
            self._progressive_access(driver, url)
            
            # 3. Verificar Cloudflare
            if not self._check_cloudflare(driver):
                raise Exception("❌ No se pudo pasar Cloudflare")
            
            self.logger.info("✅ Cloudflare pasado")
            
            # 4. Interactuar con página
            self._interact_with_page(driver)
            
            # 5. Extraer datos
            html = driver.page_source
            data = self._parse_data(html)
            
            self.logger.info("✅ Scraping completado")
            return data
            
        except Exception as e:
            self.logger.error(f"❌ Error: {str(e)}")
            if driver:
                driver.save_screenshot("error.png")
            raise
        finally:
            if driver and not self.debug:
                driver.quit()
    
    def _setup_chrome(self):
        """Configurar Chrome con undetected-chromedriver"""
        options = uc.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--start-maximized')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--lang=es-MX')
        options.add_argument('--accept-lang=es-MX,es;q=0.9')
        
        driver = uc.Chrome(options=options, use_subprocess=False)
        self.logger.info("✅ Chrome iniciado")
        return driver
    
    def _progressive_access(self, driver, url):
        """Acceso progresivo a la página"""
        # Paso 1: Base URL
        self.logger.info("🌐 Accediendo a página base...")
        driver.get(self.base_url)
        time.sleep(random.uniform(2, 4))
        
        # Paso 2: Comportamiento humano
        self._simulate_human_behavior(driver)
        
        # Paso 3: URL completa
        self.logger.info("🔄 Navegando a URL objetivo...")
        driver.get(url)
        time.sleep(random.uniform(1, 2))
        
        # Paso 4: Esperar carga
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
    
    def _check_cloudflare(self, driver, max_attempts=30):
        """Verificar REALMENTE que Cloudflare pasó"""
        self.logger.info("🔍 Verificando presencia de Cloudflare...")
        
        for attempt in range(max_attempts):
            html = driver.page_source.lower()
            
            # Indicadores de Cloudflare
            cloudflare_indicators = [
                "cloudflare" in html,
                "turnstile" in html,
                "cf-challenge" in html,
                "challenge-platform" in html,
                "just a moment" in html
            ]
            
            if any(cloudflare_indicators):
                self.logger.warning(
                    f"⏳ Cloudflare detectado (intento {attempt + 1}/{max_attempts})"
                )
                time.sleep(2)
                continue
            
            # Verificar elemento esperado (AJUSTA SEGÚN TU SITIO)
            try:
                driver.find_element(By.ID, "contact-name")  # Cambia esto
                self.logger.info("✅ Formulario detectado - Cloudflare pasado")
                return True
            except:
                self.logger.info(f"⏳ Esperando formulario ({attempt + 1}/{max_attempts})")
                time.sleep(2)
                continue
        
        self.logger.error("❌ No se pudo pasar Cloudflare")
        return False
    
    def _simulate_human_behavior(self, driver):
        """Simular comportamiento humano"""
        try:
            scroll = random.randint(100, 500)
            driver.execute_script(f"window.scrollBy(0, {scroll});")
            time.sleep(random.uniform(0.3, 0.7))
            
            driver.execute_script(f"window.scrollBy(0, -{scroll // 2});")
            time.sleep(random.uniform(0.3, 0.7))
        except Exception as e:
            self.logger.debug(f"Error en simulación: {e}")
    
    def _human_type(self, element, text):
        """Tipear como humano"""
        element.click()
        time.sleep(random.uniform(0.1, 0.3))
        
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.05, 0.15))
    
    def _interact_with_page(self, driver):
        """Interactuar con formularios/botones"""
        self.logger.info("📝 Rellenando formulario...")
        
        # Ejemplo: rellenar nombre
        try:
            name_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "contact-name"))
            )
            self._human_type(name_input, "Juan Pérez")
            self.logger.info("✓ Nombre ingresado")
        except Exception as e:
            self.logger.warning(f"⚠️ No se pudo rellenar nombre: {e}")
        
        time.sleep(random.uniform(0.8, 1.5))
        
        # Ejemplo: click en botón
        try:
            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "submit-button"))
            )
            
            actions = ActionChains(driver)
            actions.move_to_element(button).pause(0.5).click().perform()
            
            self.logger.info("✓ Botón clickeado")
            time.sleep(random.uniform(3, 5))
        except Exception as e:
            self.logger.error(f"❌ Error al clickear: {e}")
            raise
    
    def _parse_data(self, html):
        """Parsear datos de la página"""
        # Tu lógica aquí
        return {"success": True, "data": []}
```

---

## 🐛 Debugging

### Modo Debug (mantener navegador abierto)
```python
scraper = CloudflareScraper(debug=True)
result = await scraper.scrape(url)
# El navegador NO se cierra, puedes inspeccionarlo
```

### Guardar evidencia en errores
```python
try:
    driver.get(url)
except Exception as e:
    driver.save_screenshot("error.png")
    with open("page_source.html", "w") as f:
        f.write(driver.page_source)
    raise
```

---

## 🔧 Configuración en Producción

### Variables de Entorno
```bash
export SCRAPER_DEBUG=false
export CLOUDFLARE_MAX_WAIT=60
export CHROME_HEADLESS=false  # No usar headless con Cloudflare
```

### Docker (si aplica)
```dockerfile
FROM python:3.14

RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    xvfb

COPY requirements.txt .
RUN pip install -r requirements.txt

# Ejecutar con display virtual
CMD ["xvfb-run", "python", "scraper.py"]
```

---

## 📝 Checklist para Nuevas Páginas

Cuando necesites agregar una nueva página con Cloudflare:

### 1. Información del Navegador
- [ ] User-Agent (F12 → Network → Headers)
- [ ] Accept-Language (F12 → Network → Headers)

### 2. Información de la Página
- [ ] URL base (ej: `https://sitio.com`)
- [ ] URL completa con parámetros
- [ ] ¿Aparece Cloudflare? (checkbox/puzzle/otro)

### 3. Elementos de la Página
Para cada input:
- [ ] ID del elemento
- [ ] Class del elemento  
- [ ] Type (text/email/tel/etc)
- [ ] Valor de ejemplo

Para cada botón:
- [ ] ID del botón
- [ ] Class del botón
- [ ] Texto visible

### 4. Verificación
- [ ] Screenshot de Network mostrando tracking (Datadog, GA, etc)
- [ ] Identificar elemento único que indique que Cloudflare pasó

---

## 💡 Tips Importantes

1. **NO uses `version_main=`** - deja que auto-detecte
2. **Siempre verifica dinámicamente** - no confíes en delays fijos
3. **Acceso progresivo** - base URL primero, URL completa después
4. **Comportamiento humano** - scrolls, tipeo natural, movimientos
5. **Logs claros** - usa emojis para identificar estados fácilmente
6. **Debug mode** - mantén navegador abierto para inspeccionar
7. **Screenshots en error** - guarda evidencia siempre

---

## 🆘 Si Nada Funciona

1. Verifica versión de Chrome: `google-chrome --version`
2. Actualiza librería: `pip install -U undetected-chromedriver`
3. Revisa logs CUIDADOSAMENTE (no confíes sin verificar)
4. Toma screenshots y guarda HTML
5. Aumenta `max_attempts` a 60
6. Prueba con delays más largos
7. Verifica que `setuptools` esté instalado (Python 3.14+)

---

## 📚 Referencias

- **undetected-chromedriver**: https://github.com/ultrafunkamsterdam/undetected-chromedriver
- **Selenium Docs**: https://selenium-python.readthedocs.io/
- **Archivo completo**: `CLOUDFLARE_PROMPT_TEMPLATE.py`

---

## 🎉 Estado Actual

**Última prueba**: 19 Febrero 2026  
**Sitio**: Mapfre México (cotizadorautos.mapfre.com.mx)  
**Chrome**: 145.0.7632.76  
**Python**: 3.14  
**Estado**: ✅ FUNCIONANDO PERFECTAMENTE

**¡Éxito! 🚀** Todo documentado para que no vuelvas a sufrir.

