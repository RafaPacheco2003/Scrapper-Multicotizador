# Scraper para Mapfre México con bypass de Cloudflare
# ESTRATEGIA: undetected-chromedriver + comportamiento humano + verificación dinámica

import logging
from typing import Dict, Any
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from scrapers.base import BaseScraper
import time
import random

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
            self.logger.info("🚀 Iniciando scraping con undetected-chromedriver...")
            
            # PASO 1: Configurar Chrome con undetected-chromedriver
            # undetected-chromedriver automáticamente bypasea muchas detecciones
            options = uc.ChromeOptions()
            
            # Opciones básicas
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--start-maximized')
            options.add_argument('--disable-blink-features=AutomationControlled')
            
            # Idioma y región
            options.add_argument('--lang=es-MX')
            options.add_argument('--accept-lang=es-MX,es;q=0.9')
            
            # Crear driver con undetected-chromedriver (auto-detecta versión)
            driver = uc.Chrome(options=options, use_subprocess=False)
            self.logger.info("Chrome iniciado con undetected-chromedriver")
            
            # PASO 2: Acceso NATURAL y progresivo
            self.logger.info("🌐 Accediendo a página base...")
            driver.get(self.base_url)
            
            # Simular comportamiento humano: movimiento del mouse y scroll
            self._simulate_human_behavior(driver)
            time.sleep(random.uniform(2, 4))
            
            self.logger.info("🔄 Navegando a URL con parámetros...")
            driver.get(url)
            time.sleep(random.uniform(1, 2))
            
            # PASO 3: Esperar carga inicial
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # PASO 4: VERIFICAR Y ESPERAR CLOUDFLARE DINÁMICAMENTE
            cloudflare_passed = self._check_and_wait_for_cloudflare(driver)
            
            if not cloudflare_passed:
                self.logger.error(" No se pudo pasar Cloudflare después de múltiples intentos")
                raise Exception("Cloudflare Challenge no pudo ser resuelto")
            
            self.logger.info("Cloudflare pasado exitosamente")
            self.logger.info("Cloudflare pasado exitosamente")
            
            # Simular comportamiento humano después de pasar Cloudflare
            self._simulate_human_behavior(driver)
            time.sleep(random.uniform(1, 2))
            
            # PASO 5: Rellenar formulario de contacto con comportamiento humano
            self.logger.info("Rellenando formulario de contacto...")
            
            # Campo 1: Nombre
            try:
                name_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "contact-name"))
                )
                self._human_type(driver, name_input, "Juan Pérez")
                self.logger.info("Nombre ingresado")
            except Exception as e:
                self.logger.warning(f"No se pudo rellenar nombre: {str(e)}")
            
            time.sleep(random.uniform(0.8, 1.5))
            
            # Campo 2: Email
            try:
                email_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "contact-email"))
                )
                self._human_type(driver, email_input, "juan.perez2024@gmail.com")
                self.logger.info("Email ingresado")
            except Exception as e:
                self.logger.warning(f"No se pudo rellenar email: {str(e)}")
            
            time.sleep(random.uniform(0.8, 1.5))
            
            # Campo 3: Teléfono
            try:
                phone_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "contact-phone"))
                )
                self._human_type(driver, phone_input, "9991234567")
                self.logger.info("Teléfono ingresado")
            except Exception as e:
                self.logger.warning(f"No se pudo rellenar teléfono: {str(e)}")
            
            time.sleep(random.uniform(1.5, 2.5))
            
            # PASO 6: Click en botón Continuar
            self.logger.info("Haciendo click en botón Continuar...")
            try:
                continue_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "confirm-usercontact-button"))
                )
                
                # Mover mouse al botón antes de clickear (comportamiento humano)
                actions = ActionChains(driver)
                actions.move_to_element(continue_button).pause(random.uniform(0.3, 0.7)).click().perform()
                
                self.logger.info("Botón clickeado")
                
                # Esperar carga de página siguiente
                self.logger.info("Esperando carga de página siguiente...")
                time.sleep(random.uniform(3, 5))
                
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                self.logger.info("Página siguiente cargada")
                
            except Exception as e:
                self.logger.error(f"Error al clickear botón: {str(e)}")
                raise
            
            # PASO 7: Extraer datos de la página
            html = driver.page_source
            data = self.parse_response(html)
            self.logger.info("Scraping completado exitosamente")
            
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
    
    def _check_and_wait_for_cloudflare(self, driver, max_attempts: int = 30) -> bool:
        """
        Verifica si Cloudflare está presente y espera hasta que se resuelva.
        Retorna True si pasó, False si no pudo pasar.
        """
        self.logger.info("Verificando presencia de Cloudflare...")
        
        for attempt in range(max_attempts):
            try:
                # PRIMERO: Verificar si el formulario YA está presente (Cloudflare ya pasó)
                try:
                    driver.find_element(By.ID, "contact-name")
                    self.logger.info("Formulario detectado - Cloudflare pasado")
                    return True
                except:
                    pass  # Formulario no encontrado, continuar verificando
                
                # SEGUNDO: Solo si NO hay formulario, verificar si Cloudflare está activo
                html = driver.page_source.lower()
                
                # Verificar SOLO indicadores ACTIVOS de Cloudflare challenge
                active_challenge_indicators = [
                    "just a moment" in html,  # Mensaje activo del challenge
                    "checking your browser" in html,  # Verificación en proceso
                    "<title>just a moment...</title>" in html  # Title del challenge
                ]
                
                if any(active_challenge_indicators):
                    self.logger.warning(f"Cloudflare challenge activo (intento {attempt + 1}/{max_attempts}), esperando...")
                    time.sleep(3)  # Esperar más tiempo para que se resuelva
                    continue
                
                # Si no hay challenge activo pero tampoco formulario, esperar un poco más
                self.logger.info(f"Esperando carga completa (intento {attempt + 1}/{max_attempts})...")
                time.sleep(2)
                    
            except Exception as e:
                self.logger.debug(f"Error en verificación: {str(e)}")
                time.sleep(2)
                continue
        
        self.logger.error("No se pudo pasar Cloudflare después de múltiples intentos")
        return False
    
    def _simulate_human_behavior(self, driver):
        """Simula comportamiento humano: scroll aleatorio y movimientos"""
        try:
            # Scroll aleatorio
            scroll_amount = random.randint(100, 500)
            driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            time.sleep(random.uniform(0.3, 0.7))
            
            # Scroll de vuelta
            driver.execute_script(f"window.scrollBy(0, -{scroll_amount // 2});")
            time.sleep(random.uniform(0.3, 0.7))
            
        except Exception as e:
            self.logger.debug(f"Error en simulación de comportamiento: {str(e)}")
    
    def _human_type(self, driver, element, text: str):
        """Tipea texto con delays aleatorios entre caracteres (más humano)"""
        element.click()
        time.sleep(random.uniform(0.1, 0.3))
        
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.05, 0.15))
        
        time.sleep(random.uniform(0.3, 0.6))
    
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
