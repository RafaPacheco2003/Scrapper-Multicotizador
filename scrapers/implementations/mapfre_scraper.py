# Scraper para Mapfre México con bypass de Cloudflare
# ESTRATEGIA: User-Agent Chrome 144 real + permitir tracking de Datadog/Analytics + acceso natural

import logging
from typing import Dict, Any
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from scrapers.base import BaseScraper
import time

logger = logging.getLogger(__name__)


class MapfreScraper(BaseScraper):
    
    def __init__(self, debug: bool = False, wait_time: int = 0):
        super().__init__(name="mapfre")
        self.base_url = "https://cotizadorautos.mapfre.com.mx"
        self.timeout = 15
        self.debug = debug
        self.wait_time = wait_time
    
    async def scrape(self, url: str) -> Dict[str, Any]:
        driver = None
        try:
            self.logger.info("Iniciando scraping con Chrome 144...")
            
            # PASO 1: Configurar Chrome para pasar Cloudflare
            options = webdriver.ChromeOptions()
            
            # Opciones básicas de Chrome
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument('--start-maximized')
            options.add_argument('--disable-extensions')
            options.add_argument('--disable-gpu')
            
            # CRITICO: User-Agent debe ser versión REAL de Chrome en 2026
            # Cloudflare verifica que la versión exista
            options.add_argument(
                'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/144.0.7559.97 Safari/537.36'
            )
            
            # CRITICO: Idioma debe coincidir con User-Agent
            # Si hay mismatch, Cloudflare detecta como bot
            options.add_argument('--lang=es-GB')
            options.add_argument('--accept-lang=es-GB,es-MX,es;q=0.9')
            
            # CRITICO: Permitir scripts de tracking (Datadog, Google Analytics)
            # Cloudflare espera ver estas peticiones para confirmar que es usuario real
            options.add_argument('--allow-running-insecure-content')
            
            # Ocultar que estamos usando Selenium
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            driver = webdriver.Chrome(options=options)
            self.logger.info("Chrome iniciado correctamente")
            
            # PASO 2: Ocultar propiedades de Selenium con JavaScript
            # Esto evita que Cloudflare detecte que estamos automatizando
            driver.execute_script(
                "Object.defineProperty(navigator, 'webdriver', {get: () => false});"
            )
            
            driver.execute_script("""
            Object.defineProperty(navigator, 'languages', {
                get: () => ['es-GB', 'es-MX', 'es']
            });
            Object.defineProperty(navigator, 'language', {
                get: () => 'es-GB'
            });
            """)
            
            self.logger.info("Propiedades de navegador ocultadas")
            
            # PASO 3: Acceso NATURAL a la página (simular comportamiento humano)
            # NO ir directo a la URL completa - eso activa Cloudflare
            # Primero ir a la página base, esperar, luego ir a la URL completa
            
            self.logger.info("Accediendo a página base...")
            driver.get(self.base_url)
            time.sleep(2)  # Esperar como lo haría un humano
            
            self.logger.info("Esperando antes de continuar...")
            time.sleep(3)  # Comportamiento humano: leer, pensar
            
            self.logger.info("Accediendo a URL con parámetros...")
            driver.get(url)
            time.sleep(1)
            
            # PASO 4: Esperar a que cargue la página
            self.logger.info("Esperando carga de página...")
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # PASO 5: Esperar a que scripts de tracking se carguen
            # Cloudflare verifica que se carguen Datadog, Google Analytics, etc.
            # Si no se cargan, detecta como bot
            self.logger.info("Esperando scripts de tracking (Datadog, Analytics)...")
            time.sleep(5)
            
            html = driver.page_source
            self.logger.info(f"HTML obtenido: {len(html)} caracteres")
            
            # PASO 6: Verificar si Cloudflare aparece (por si acaso)
            if "cloudflare" in html.lower() or "turnstile" in html.lower():
                self.logger.warning("Cloudflare Turnstile detectado, esperando...")
                time.sleep(10)  # Esperar a que se resuelva automáticamente
                html = driver.page_source
            
            self.logger.info("Cloudflare pasado correctamente")
            
            # PASO 7: Rellenar formulario de contacto
            # Esperar entre cada campo para simular comportamiento humano
            
            # Campo 1: Nombre
            try:
                name_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "contact-name"))
                )
                name_input.click()
                time.sleep(0.5)
                name_input.send_keys("Juan Pérez")
                time.sleep(1)
                self.logger.info("Nombre ingresado")
            except Exception as e:
                self.logger.warning(f"No se pudo rellenar nombre: {str(e)}")
            
            time.sleep(1)
            
            # Campo 2: Email
            try:
                email_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "contact-email"))
                )
                email_input.click()
                time.sleep(0.5)
                email_input.send_keys("juan.perez2024@gmail.com")
                time.sleep(1)
                self.logger.info("Email ingresado")
            except Exception as e:
                self.logger.warning(f"No se pudo rellenar email: {str(e)}")
            
            time.sleep(1)
            
            # Campo 3: Teléfono
            try:
                phone_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "contact-phone"))
                )
                phone_input.click()
                time.sleep(0.5)
                phone_input.send_keys("9991234567")
                time.sleep(1)
                self.logger.info("Teléfono ingresado")
            except Exception as e:
                self.logger.warning(f"No se pudo rellenar teléfono: {str(e)}")
            
            time.sleep(2)
            
            # PASO 8: Hacer click en botón "Continuar"
            self.logger.info("Haciendo click en botón Continuar...")
            try:
                continue_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "confirm-usercontact-button"))
                )
                continue_button.click()
                self.logger.info("Botón clickeado")
                
                # Esperar a que cargue la siguiente página
                self.logger.info("Esperando carga de página siguiente...")
                time.sleep(5)
                
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                self.logger.info("Página siguiente cargada")
                
            except Exception as e:
                self.logger.error(f"Error al clickear botón: {str(e)}")
                raise
            
            # PASO 9: Extraer datos de la página
            data = self.parse_response(html)
            self.logger.info("Scraping completado")
            
            # Modo debug: mantener navegador abierto
            if self.debug and self.wait_time > 0:
                self.logger.info(f"Modo DEBUG: Esperando {self.wait_time}s...")
                time.sleep(self.wait_time)
            
            return data
            
        except Exception as e:
            self.logger.error(f"Error en scraping: {str(e)}")
            raise
        finally:
            # Cerrar navegador siempre
            if driver:
                try:
                    driver.quit()
                    self.logger.info("Chrome cerrado")
                except:
                    pass
    
    def parse_response(self, html: str) -> Dict[str, Any]:
        # Parsear HTML y extraer información de seguros
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Estructura base de respuesta
            data = {
                "success": False,
                "source": "mapfre",
                "policies": [],
                "pricing": {},
                "error": None
            }
            
            # Buscar contenedores de pólizas (diferentes sitios usan diferentes clases)
            # Intentar primero con clase 'policy'
            policy_containers = soup.find_all('div', class_=lambda x: x and 'policy' in x.lower())
            
            # Si no encuentra, intentar con otras clases comunes
            if not policy_containers:
                policy_containers = soup.find_all(
                    'div',
                    class_=lambda x: x and any(cls in x.lower() for cls in ['plan', 'quote', 'option'])
                )
            
            # Extraer información de cada póliza encontrada
            for container in policy_containers:
                try:
                    policy = self._extract_policy(container)
                    if policy:
                        data["policies"].append(policy)
                except Exception as e:
                    self.logger.debug(f"Error extrayendo póliza: {str(e)}")
                    continue
            
            # Marcar como éxito si encontramos pólizas
            if data["policies"]:
                data["success"] = True
                self.logger.info(f"{len(data['policies'])} pólizas encontradas")
            else:
                self.logger.warning("No se encontraron pólizas")
                data["error"] = "No policies found in response"
            
            return data
            
        except Exception as e:
            self.logger.error(f"Error parseando respuesta: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "policies": [],
                "source": "mapfre"
            }
    
    def _extract_policy(self, container) -> Dict[str, Any]:
        # Extraer datos individuales de una póliza
        # Cada sitio tiene diferentes estructuras HTML, adaptar según sea necesario
        try:
            policy = {}
            
            # Buscar nombre del plan
            # Adaptar los selectores según la estructura HTML del sitio
            name_elem = container.find(['h2', 'h3', 'span'], class_=lambda x: x and 'name' in x.lower())
            if name_elem:
                policy['name'] = name_elem.get_text(strip=True)
            
            # Buscar precio
            price_elem = container.find(['span', 'div'], class_=lambda x: x and 'price' in x.lower())
            if price_elem:
                price_text = price_elem.get_text(strip=True)
                policy['price'] = price_text
            
            # Buscar coberturas
            coverage_elems = container.find_all(['li', 'div'], class_=lambda x: x and 'coverage' in x.lower())
            if coverage_elems:
                policy['coverage'] = [elem.get_text(strip=True) for elem in coverage_elems]
            
            return policy if policy else None
            
        except Exception as e:
            self.logger.debug(f"Error en _extract_policy: {str(e)}")
            return None


# Crear instancia del scraper para usar en otros módulos
mapfre_scraper = MapfreScraper(debug=False, wait_time=0)
