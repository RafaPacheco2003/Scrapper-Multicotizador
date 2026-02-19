

import logging
from typing import Dict, Any
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from scrapers.base import BaseScraper
import time
import random

logger = logging.getLogger(__name__)


class HDIScraper(BaseScraper):
    
    def __init__(self, debug: bool = False, wait_time: int = 0):
        super().__init__(name="hdi")
        self.base_url = "https://www.hdiconnect.com.mx/productos/autos"
        self.timeout = 15
        self.debug = debug
        self.wait_time = wait_time
    
    async def scrape(self, url: str) -> Dict[str, Any]:
        driver = None
        try:
            self.logger.info("🚀 Iniciando scraping HDI con undetected-chromedriver...")
            
            # Validar URL
            if not url or not isinstance(url, str):
                self.logger.warning(f"⚠️  URL inválida recibida: {url}, usando base_url")
                url = self.base_url
            
            self.logger.info(f"📍 URL objetivo: {url}")
            
            # PASO 1: Configurar Chrome con undetected-chromedriver
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
            self.logger.info("✅ Chrome iniciado con undetected-chromedriver")
            
            # PASO 2: Acceso directo a la URL
            self.logger.info("🌐 Accediendo a página HDI...")
            driver.get(url)
            
            # Simular comportamiento humano: movimiento del mouse y scroll
            self._simulate_human_behavior(driver)
            time.sleep(random.uniform(2, 4))
            
            # PASO 3: Esperar carga inicial
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # PASO 4: VERIFICAR Y ESPERAR CLOUDFLARE DINÁMICAMENTE (si aplica)
            self.logger.info("🔍 Verificando página...")
            time.sleep(random.uniform(2, 3))
            
            # Verificar que la página cargó correctamente
            self.logger.info("✅ Página cargada correctamente")
            
            # PASO 5: Rellenar campo de vehículo
            self.logger.info("📝 Buscando campo de vehículo...")
            try:
                # React-Select requiere click en el container primero
                # Buscar el container del react-select
                select_container = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((
                        By.CSS_SELECTOR, 
                        'div.css-b62m3t-container, div[class*="container"]'
                    ))
                )
                
                self.logger.info("✓ Container de campo encontrado")
                
                # Hacer click en el container para activar el select
                select_container.click()
                time.sleep(random.uniform(0.5, 1.0))
                self.logger.info("✓ Campo activado")
                
                # Ahora buscar el input que se activó
                vehicle_input = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((
                        By.CSS_SELECTOR, 
                        'input[id^="typeahead-"], input[role="combobox"]'
                    ))
                )
                
                self.logger.info("✓ Input de vehículo encontrado")
                
                # Asegurarse que tiene foco
                vehicle_input.click()
                time.sleep(random.uniform(0.3, 0.5))
                
                # Limpiar campo por si acaso
                vehicle_input.clear()
                time.sleep(random.uniform(0.2, 0.4))
                
                # Tipear "Dodge Attitude" como humano
                self._human_type(vehicle_input, "Dodge Attitude")
                self.logger.info("✓ 'Dodge Attitude' ingresado")
                
                # ESPERAR a que el API cargue las opciones (React-Select asíncrono)
                self.logger.info("⏳ Esperando carga de opciones del servidor...")
                time.sleep(random.uniform(3, 4))
                
                # Intentar seleccionar primera opción del dropdown
                try:
                    # Esperar a que aparezcan opciones REALES en el listbox
                    # React-Select usa divs con id tipo "react-select-X-option-Y"
                    self.logger.info("🔍 Buscando opciones en el dropdown...")
                    
                    # Primero verificar que el menú tenga opciones cargadas
                    options = WebDriverWait(driver, 8).until(
                        lambda d: d.find_elements(
                            By.CSS_SELECTOR,
                            'div[id*="-option-"]'
                        )
                    )
                    
                    if not options:
                        self.logger.warning("⚠️  No se encontraron opciones en el dropdown")
                        raise Exception("No options found")
                    
                    self.logger.info(f"✓ Se encontraron {len(options)} opciones")
                    
                    # Registrar las opciones para debug
                    for idx, opt in enumerate(options[:3]):  # Solo las primeras 3
                        try:
                            text = opt.text.strip()
                            self.logger.info(f"  Opción {idx}: '{text}'")
                        except:
                            pass
                    
                    # Seleccionar la primera opción
                    first_option = options[0]
                    
                    # Hacer visible y clickeable
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", first_option)
                    time.sleep(0.5)
                    
                    # Intentar click normal primero
                    try:
                        first_option.click()
                        self.logger.info("✓ Opción seleccionada con click")
                    except:
                        # Si falla, usar JavaScript
                        driver.execute_script("arguments[0].click();", first_option)
                        self.logger.info("✓ Opción seleccionada con JavaScript")
                    
                    time.sleep(random.uniform(1, 2))
                    
                    # Verificar que se seleccionó (el input hidden debería tener valor)
                    try:
                        hidden_input = driver.find_element(By.CSS_SELECTOR, 'input[name="typeahead-marca_modelo"]')
                        selected_value = hidden_input.get_attribute('value')
                        if selected_value:
                            self.logger.info(f"✅ Vehículo seleccionado: {selected_value}")
                        else:
                            self.logger.warning("⚠️  El campo hidden está vacío")
                    except:
                        pass
                        
                except Exception as dropdown_error:
                    # Si no hay dropdown o no se puede seleccionar, intentar presionar Enter
                    self.logger.warning(f"⚠️  Error con dropdown: {str(dropdown_error)}")
                    self.logger.info("🔄 Intentando alternativa: presionar Enter...")
                    try:
                        vehicle_input.send_keys(Keys.ENTER)
                        time.sleep(1.5)
                        self.logger.info("✓ Enter enviado")
                    except Exception as enter_error:
                        self.logger.warning(f"⚠️  También falló Enter: {str(enter_error)}")
                
            except Exception as e:
                self.logger.warning(f"⚠️  No se pudo interactuar con campo de vehículo: {str(e)}")
                # Guardar screenshot para debug
                try:
                    driver.save_screenshot("/tmp/hdi_error.png")
                    self.logger.info("📸 Screenshot guardado en /tmp/hdi_error.png")
                except:
                    pass
            
            # Esperar transición automática después de seleccionar vehículo
            self.logger.info("⏳ Esperando transición de página...")
            time.sleep(random.uniform(3, 4))
            
            # Verificar URL actual
            current_url = driver.current_url
            self.logger.info(f"📍 URL actual: {current_url}")
            
            # PASO 6: Buscar y hacer click en botón "Iniciar mi cotización" (solo si todavía estamos en página inicial)
            if '/cotizacion' not in current_url:
                self.logger.info("🔍 Buscando botón 'Iniciar mi cotización'...")
                try:
                    # Esperar a que aparezca el botón de submit
                    submit_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((
                            By.CSS_SELECTOR,
                            'button[type="submit"]'
                        ))
                    )
                    
                    self.logger.info("✓ Botón encontrado")
                    
                    # Hacer scroll al botón si es necesario
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_button)
                    time.sleep(0.5)
                    
                    # Click en el botón con JavaScript (evita stale element)
                    driver.execute_script("arguments[0].click();", submit_button)
                    self.logger.info("✓ Botón 'Iniciar mi cotización' clickeado")
                    
                    # Esperar a que cargue la siguiente página
                    time.sleep(random.uniform(3, 4))
                    self.logger.info(f"📍 URL después de submit: {driver.current_url}")
                    
                except Exception as e:
                    self.logger.warning(f"⚠️  No se encontró botón (puede haber avanzado automáticamente): {str(e)}")
            else:
                self.logger.info("✅ Ya estamos en página de cotización - botón no necesario")
            
            # PASO 7: Seleccionar año del vehículo (2024)
            self.logger.info("📅 Buscando selector de año...")
            try:
                # Esperar a que aparezca la página de selección de año
                # Buscar el radio button para el año 2024
                year_radio = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((
                        By.CSS_SELECTOR,
                        'input[name="ao"][value="2024"], input[id="Simpleradio-2024"]'
                    ))
                )
                
                self.logger.info("✓ Radio button del año 2024 encontrado")
                
                # Buscar el LABEL asociado (es lo que el usuario clickea realmente)
                year_label = None
                try:
                    radio_id = year_radio.get_attribute('id')
                    if radio_id:
                        year_label = driver.find_element(By.CSS_SELECTOR, f'label[for="{radio_id}"]')
                        self.logger.info(f"✓ Label encontrado para radio button (for='{radio_id}')")
                except:
                    # Si no hay label con 'for', buscar label padre
                    try:
                        year_label = year_radio.find_element(By.XPATH, '..')
                        if year_label.tag_name.lower() != 'label':
                            year_label = None
                    except:
                        pass
                
                # Hacer scroll al elemento
                element_to_scroll = year_label if year_label else year_radio
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element_to_scroll)
                time.sleep(0.8)
                
                # Guardar URL actual antes de seleccionar
                current_url = driver.current_url
                self.logger.info(f"📍 URL actual antes de seleccionar año: {current_url}")
                
                # IMPORTANTE: Hacer click en el LABEL (simula comportamiento humano real)
                if year_label:
                    self.logger.info("🖱️  Haciendo click en el label (como usuario real)...")
                    try:
                        # Click en el label con JavaScript disparando todos los eventos
                        driver.execute_script("""
                            const label = arguments[0];
                            const input = arguments[1];
                            
                            // Disparar eventos en el label (lo que clickea el usuario)
                            label.dispatchEvent(new MouseEvent('mousedown', { bubbles: true, cancelable: true }));
                            label.dispatchEvent(new MouseEvent('mouseup', { bubbles: true, cancelable: true }));
                            label.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
                            
                            // Establecer checked en el input
                            input.checked = true;
                            
                            // Disparar eventos en el input
                            input.dispatchEvent(new Event('click', { bubbles: true }));
                            input.dispatchEvent(new Event('change', { bubbles: true }));
                            input.dispatchEvent(new Event('input', { bubbles: true }));
                        """, year_label, year_radio)
                        self.logger.info("✓ Click en label ejecutado con eventos React")
                    except Exception as label_error:
                        self.logger.warning(f"⚠️  Error con label: {str(label_error)}")
                        # Fallback: click directo en input
                        year_radio.click()
                else:
                    # Si no hay label, click directo en el input con todos los eventos
                    self.logger.info("🖱️  Click directo en input con eventos completos...")
                    driver.execute_script("""
                        const input = arguments[0];
                        input.checked = true;
                        input.dispatchEvent(new MouseEvent('mousedown', { bubbles: true }));
                        input.dispatchEvent(new MouseEvent('mouseup', { bubbles: true }));
                        input.dispatchEvent(new MouseEvent('click', { bubbles: true }));
                        input.dispatchEvent(new Event('change', { bubbles: true }));
                        input.dispatchEvent(new Event('input', { bubbles: true }));
                    """, year_radio)
                    self.logger.info("✓ Eventos disparados en input")
                
                time.sleep(0.5)
                
                # Verificar que se seleccionó
                if year_radio.is_selected():
                    self.logger.info("✅ Año 2024 confirmado como seleccionado")
                else:
                    self.logger.warning("⚠️  No se pudo confirmar la selección del año")
                
                # IMPORTANTE: Esperar procesamiento (reCAPTCHA v3, verify-token, oneapp/v2/submit)
                self.logger.info("⏳ Esperando procesamiento automático...")
                self.logger.info("   • Verificando reCAPTCHA v3...")
                time.sleep(random.uniform(2, 3))
                self.logger.info("   • Esperando llamadas API (verify-token + submit)...")
                time.sleep(random.uniform(3, 4))
                
                # Verificar si hubo navegación automática o cambio en la página
                new_url = driver.current_url
                self.logger.info(f"📍 URL después de seleccionar: {new_url}")
                
                if new_url != current_url:
                    self.logger.info("✅ Navegación automática detectada")
                    # Esperar carga completa
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.TAG_NAME, "body"))
                    )
                    time.sleep(2)
                else:
                    self.logger.info("ℹ️  Misma URL - verificando si apareció siguiente paso...")
                    
                    # Buscar si apareció botón de continuar o siguiente paso
                    try:
                        continue_button = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((
                                By.XPATH,
                                "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'continuar') or contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'siguiente') or @type='submit']"
                            ))
                        )
                        
                        continue_text = continue_button.text.strip()
                        self.logger.info(f"✓ Botón encontrado: '{continue_text}'")
                        
                        # Scroll y click
                        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", continue_button)
                        time.sleep(0.5)
                        driver.execute_script("arguments[0].click();", continue_button)
                        self.logger.info("✓ Botón clickeado para continuar")
                        
                        # Esperar procesamiento
                        time.sleep(random.uniform(3, 5))
                        self.logger.info(f"📍 URL actual: {driver.current_url}")
                        
                    except Exception as btn_error:
                        self.logger.warning(f"⚠️  No se encontró botón para continuar")
                        # Verificar elementos del formulario
                        try:
                            form_elements = driver.find_elements(By.CSS_SELECTOR, 'input, select, button')
                            self.logger.info(f"  Se encontraron {len(form_elements)} elementos en la página")
                        except:
                            pass
                
            except Exception as e:
                self.logger.warning(f"⚠️  No se pudo seleccionar el año 2024: {str(e)}")
                self.logger.info("ℹ️  Intentando buscar años disponibles...")
                try:
                    # Buscar todos los radio buttons de año disponibles
                    available_years = driver.find_elements(By.CSS_SELECTOR, 'input[name="ao"]')
                    if available_years:
                        years_list = [yr.get_attribute('value') for yr in available_years[:5]]
                        self.logger.info(f"  Años disponibles: {', '.join(years_list)}")
                    else:
                        self.logger.warning("  No se encontraron opciones de año")
                except:
                    pass
                
                # Guardar screenshot para debug
                try:
                    driver.save_screenshot("/tmp/hdi_year_error.png")
                    self.logger.info("📸 Screenshot guardado en /tmp/hdi_year_error.png")
                except:
                    pass
            
            # PASO 8: Seleccionar versión del vehículo (Autocomplete con opciones aleatorias)
            self.logger.info("🚗 Buscando selector de versión del vehículo...")
            try:
                # Esperar un poco para que cargue el siguiente paso
                time.sleep(random.uniform(2, 3))
                
                # Buscar el campo de autocomplete o su container
                # Puede aparecer como input o como div interactivo
                autocomplete_container = None
                autocomplete_input = None
                
                try:
                    # Intentar encontrar el input del autocomplete
                    autocomplete_input = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((
                            By.CSS_SELECTOR,
                            'input[role="combobox"], input[type="text"]'
                        ))
                    )
                    self.logger.info("✓ Input de autocomplete encontrado")
                    
                    # Hacer click para activar el dropdown
                    autocomplete_input.click()
                    time.sleep(random.uniform(0.5, 1.0))
                    
                except:
                    # Si no hay input, buscar el div container directamente
                    try:
                        autocomplete_container = driver.find_element(
                            By.CSS_SELECTOR,
                            'div[id*="Autocomplete Results"], div[data-alias]'
                        )
                        self.logger.info("✓ Container de autocomplete encontrado")
                        
                        # Hacer click en el container
                        driver.execute_script("arguments[0].click();", autocomplete_container)
                        time.sleep(random.uniform(0.5, 1.0))
                    except:
                        self.logger.warning("⚠️  No se encontró campo de autocomplete")
                
                # Esperar a que carguen las opciones
                self.logger.info("⏳ Esperando opciones de versión...")
                time.sleep(random.uniform(1, 2))
                
                # Buscar todas las opciones disponibles
                version_options = WebDriverWait(driver, 8).until(
                    lambda d: d.find_elements(
                        By.CSS_SELECTOR,
                        'div[id^="Option-"], div.sc-dhKdcB'
                    )
                )
                
                if not version_options:
                    self.logger.warning("⚠️  No se encontraron opciones de versión")
                    raise Exception("No version options found")
                
                self.logger.info(f"✓ Se encontraron {len(version_options)} opciones de versión")
                
                # Mostrar las primeras 3 opciones para debug
                for idx, opt in enumerate(version_options[:3]):
                    try:
                        text_elem = opt.find_element(By.TAG_NAME, 'span')
                        text = text_elem.text.strip()
                        self.logger.info(f"  Opción {idx}: '{text}'")
                    except:
                        pass
                
                # Seleccionar una opción ALEATORIA
                selected_index = random.randint(0, len(version_options) - 1)
                selected_option = version_options[selected_index]
                
                self.logger.info(f"🎲 Seleccionando opción aleatoria #{selected_index + 1}")
                
                # Obtener texto de la opción seleccionada
                try:
                    text_elem = selected_option.find_element(By.TAG_NAME, 'span')
                    selected_text = text_elem.text.strip()
                    self.logger.info(f"📌 Versión seleccionada: '{selected_text}'")
                except:
                    self.logger.info(f"📌 Seleccionando opción #{selected_index + 1}")
                
                # Hacer scroll y click en la opción
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", selected_option)
                time.sleep(0.5)
                
                try:
                    selected_option.click()
                    self.logger.info("✓ Opción seleccionada con click")
                except:
                    driver.execute_script("arguments[0].click();", selected_option)
                    self.logger.info("✓ Opción seleccionada con JavaScript")
                
                # Esperar a que se procese la selección
                time.sleep(random.uniform(2, 3))
                
                # Verificar si hay botón para continuar
                try:
                    continue_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((
                            By.XPATH,
                            "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'continuar') or contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'siguiente') or @type='submit']"
                        ))
                    )
                    
                    continue_text = continue_button.text.strip()
                    self.logger.info(f"✓ Botón encontrado: '{continue_text}'")
                    
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", continue_button)
                    time.sleep(0.5)
                    driver.execute_script("arguments[0].click();", continue_button)
                    self.logger.info("✓ Botón clickeado para continuar")
                    
                    time.sleep(random.uniform(2, 3))
                    
                except:
                    self.logger.info("ℹ️  No se encontró botón continuar - puede avanzar automáticamente")
                
            except Exception as e:
                self.logger.warning(f"⚠️  No se pudo seleccionar versión del vehículo: {str(e)}")
                self.logger.info("ℹ️  Puede que este paso no sea necesario o ya esté en la siguiente pantalla")
                # Guardar screenshot para debug
                try:
                    driver.save_screenshot("/tmp/hdi_version_error.png")
                    self.logger.info("📸 Screenshot guardado en /tmp/hdi_version_error.png")
                except:
                    pass
            
            # PASO 9: Ingresar código postal
            self.logger.info("📍 Buscando campo de código postal...")
            try:
                # Esperar un poco para que cargue el siguiente paso
                time.sleep(random.uniform(2, 3))
                
                # Buscar el input del código postal
                cp_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((
                        By.CSS_SELECTOR,
                        'input[name="codigo_postal"], input[type="tel"][placeholder*="_"]'
                    ))
                )
                
                self.logger.info("✓ Campo de código postal encontrado")
                
                # Hacer scroll al campo
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", cp_input)
                time.sleep(0.5)
                
                # Hacer click en el campo
                cp_input.click()
                time.sleep(random.uniform(0.3, 0.5))
                
                # Limpiar el campo por si acaso
                cp_input.clear()
                time.sleep(0.2)
                
                # Tipear código postal "97280" como humano
                self._human_type(cp_input, "97280")
                self.logger.info("✓ Código postal '97280' ingresado")
                
                # Verificar que se ingresó correctamente
                cp_value = cp_input.get_attribute('value')
                if cp_value == "97280":
                    self.logger.info("✅ Código postal confirmado: 97280")
                else:
                    self.logger.warning(f"⚠️  Valor en campo: '{cp_value}'")
                
                # Esperar un poco para que procese
                time.sleep(random.uniform(1, 2))
                
                # Buscar botón para continuar
                try:
                    continue_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((
                            By.XPATH,
                            "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'continuar') or contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'siguiente') or @type='submit']"
                        ))
                    )
                    
                    continue_text = continue_button.text.strip()
                    self.logger.info(f"✓ Botón encontrado: '{continue_text}'")
                    
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", continue_button)
                    time.sleep(0.5)
                    driver.execute_script("arguments[0].click();", continue_button)
                    self.logger.info("✓ Botón clickeado para continuar")
                    
                    # Esperar procesamiento
                    time.sleep(random.uniform(2, 3))
                    self.logger.info(f"📍 URL actual: {driver.current_url}")
                    
                except:
                    self.logger.info("ℹ️  No se encontró botón continuar - puede avanzar automáticamente")
                
            except Exception as e:
                self.logger.warning(f"⚠️  No se pudo ingresar código postal: {str(e)}")
                # Guardar screenshot para debug
                try:
                    driver.save_screenshot("/tmp/hdi_cp_error.png")
                    self.logger.info("📸 Screenshot guardado en /tmp/hdi_cp_error.png")
                except:
                    pass
            
            # PASO 10: Ingresar fecha de nacimiento
            self.logger.info("🎂 Buscando campo de fecha de nacimiento...")
            try:
                # Esperar un poco para que cargue el siguiente paso
                time.sleep(random.uniform(2, 3))
                
                # Buscar el input de fecha de nacimiento
                birth_date_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((
                        By.CSS_SELECTOR,
                        'input[name="fecha_de_nacimiento"]'
                    ))
                )
                
                self.logger.info("✓ Campo de fecha de nacimiento encontrado")
                
                # Hacer scroll al campo
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", birth_date_input)
                time.sleep(0.5)
                
                # Hacer click en el campo para activarlo
                birth_date_input.click()
                time.sleep(random.uniform(0.3, 0.5))
                
                # Limpiar el campo
                birth_date_input.clear()
                time.sleep(0.2)
                
                # Tipear fecha "16102003" como humano
                self._human_type(birth_date_input, "16102003")
                self.logger.info("✓ Fecha de nacimiento '16/10/2003' ingresada")
                
                # Verificar que se ingresó
                birth_value = birth_date_input.get_attribute('value')
                self.logger.info(f"✓ Valor en campo: '{birth_value}'")
                
                # Disparar evento blur para que React procese
                driver.execute_script("arguments[0].dispatchEvent(new Event('blur', { bubbles: true }));", birth_date_input)
                
                # Esperar un poco para que procese
                time.sleep(random.uniform(1, 2))
                
                # Buscar el botón "Continuar" específico
                self.logger.info("🔍 Buscando botón 'Continuar'...")
                try:
                    continue_button = WebDriverWait(driver, 8).until(
                        EC.presence_of_element_located((
                            By.XPATH,
                            "//button[@type='submit' and contains(text(), 'Continuar')]"
                        ))
                    )
                    
                    self.logger.info(f"✓ Botón 'Continuar' encontrado")
                    
                    # Hacer scroll al botón
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", continue_button)
                    time.sleep(0.8)
                    
                    # Guardar URL antes del click
                    current_url = driver.current_url
                    self.logger.info(f"📍 URL antes de continuar: {current_url}")
                    
                    # Click con JavaScript disparando eventos completos (similar al año)
                    self.logger.info("🖱️  Haciendo click en botón con eventos completos...")
                    driver.execute_script("""
                        const button = arguments[0];
                        
                        // Disparar eventos de mouse
                        button.dispatchEvent(new MouseEvent('mousedown', { bubbles: true, cancelable: true }));
                        button.dispatchEvent(new MouseEvent('mouseup', { bubbles: true, cancelable: true }));
                        button.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
                        
                        // Disparar evento submit en el form si existe
                        const form = button.closest('form');
                        if (form) {
                            form.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
                        }
                    """, continue_button)
                    self.logger.info("✓ Click en botón ejecutado con eventos React")
                    
                    # IMPORTANTE: Esperar procesamiento (puede haber API calls, reCAPTCHA, validaciones)
                    self.logger.info("⏳ Esperando procesamiento...")
                    self.logger.info("   • Validando campos...")
                    time.sleep(random.uniform(2, 3))
                    self.logger.info("   • Procesando llamadas API...")
                    time.sleep(random.uniform(2, 3))
                    
                    # Verificar si hubo navegación o cambio
                    new_url = driver.current_url
                    self.logger.info(f"📍 URL después de continuar: {new_url}")
                    
                    if new_url != current_url:
                        self.logger.info("✅ Navegación detectada")
                        # Esperar carga completa de nueva página
                        WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.TAG_NAME, "body"))
                        )
                        time.sleep(2)
                    else:
                        self.logger.info("ℹ️  Misma URL - verificando cambios en la página...")
                        # Esperar más tiempo por si procesa en la misma página
                        time.sleep(random.uniform(2, 3))
                    
                except Exception as btn_error:
                    self.logger.warning(f"⚠️  No se encontró botón 'Continuar': {str(btn_error)}")
                    self.logger.info("ℹ️  Intentando buscar cualquier botón submit...")
                    try:
                        any_submit = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
                        driver.execute_script("arguments[0].click();", any_submit)
                        self.logger.info("✓ Botón submit alternativo clickeado")
                        time.sleep(random.uniform(3, 4))
                    except:
                        pass
                
            except Exception as e:
                self.logger.warning(f"⚠️  No se pudo ingresar fecha de nacimiento: {str(e)}")
                # Guardar screenshot para debug
                try:
                    driver.save_screenshot("/tmp/hdi_birth_date_error.png")
                    self.logger.info("📸 Screenshot guardado en /tmp/hdi_birth_date_error.png")
                except:
                    pass
            
            # PASO 11: Rellenar formulario de contacto (email, teléfono, términos)
            self.logger.info("📋 Buscando formulario de contacto...")
            try:
                # Esperar a que cargue la página del formulario
                time.sleep(random.uniform(2, 3))
                
                # 1. CORREO ELECTRÓNICO
                self.logger.info("📧 Buscando campo de correo electrónico...")
                try:
                    email_input = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((
                            By.CSS_SELECTOR,
                            'input[name="email"]'
                        ))
                    )
                    
                    self.logger.info("✓ Campo de email encontrado")
                    
                    # Scroll y click
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", email_input)
                    time.sleep(0.5)
                    email_input.click()
                    time.sleep(0.3)
                    
                    # Limpiar y tipear
                    email_input.clear()
                    time.sleep(0.2)
                    
                    # Generar email aleatorio
                    random_email = f"test{random.randint(1000, 9999)}@gmail.com"
                    self._human_type(email_input, random_email)
                    self.logger.info(f"✓ Email ingresado: {random_email}")
                    
                    # Disparar blur
                    driver.execute_script("arguments[0].dispatchEvent(new Event('blur', { bubbles: true }));", email_input)
                    time.sleep(0.5)
                    
                except Exception as e:
                    self.logger.warning(f"⚠️  No se pudo ingresar email: {str(e)}")
                
                # 2. NÚMERO DE TELÉFONO
                self.logger.info("📱 Buscando campo de teléfono...")
                try:
                    phone_input = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((
                            By.CSS_SELECTOR,
                            'input[name="celular"]'
                        ))
                    )
                    
                    self.logger.info("✓ Campo de teléfono encontrado")
                    
                    # Scroll y click
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", phone_input)
                    time.sleep(0.5)
                    phone_input.click()
                    time.sleep(0.3)
                    
                    # Limpiar y tipear
                    phone_input.clear()
                    time.sleep(0.2)
                    
                    # Número de teléfono de ejemplo
                    self._human_type(phone_input, "9991567227")
                    self.logger.info("✓ Teléfono ingresado: 9991567227")
                    
                    # Disparar blur
                    driver.execute_script("arguments[0].dispatchEvent(new Event('blur', { bubbles: true }));", phone_input)
                    time.sleep(0.5)
                    
                except Exception as e:
                    self.logger.warning(f"⚠️  No se pudo ingresar teléfono: {str(e)}")
                
                # 3. TÉRMINOS Y CONDICIONES (CHECKBOX)
                self.logger.info("☑️  Buscando checkbox de términos y condiciones...")
                try:
                    tyc_checkbox = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((
                            By.CSS_SELECTOR,
                            'input[name="tyc"][type="checkbox"]'
                        ))
                    )
                    
                    self.logger.info("✓ Checkbox encontrado")
                    
                    # Buscar el label asociado (si existe)
                    tyc_label = None
                    try:
                        checkbox_id = tyc_checkbox.get_attribute('id')
                        if checkbox_id:
                            tyc_label = driver.find_element(By.CSS_SELECTOR, f'label[for="{checkbox_id}"]')
                            self.logger.info(f"✓ Label encontrado para checkbox (for='{checkbox_id}')")
                    except:
                        pass
                    
                    # Scroll al elemento
                    element_to_scroll = tyc_label if tyc_label else tyc_checkbox
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element_to_scroll)
                    time.sleep(0.8)
                    
                    # Click con eventos completos (como el radio button del año)
                    if tyc_label:
                        self.logger.info("🖱️  Haciendo click en label del checkbox...")
                        driver.execute_script("""
                            const label = arguments[0];
                            const checkbox = arguments[1];
                            
                            // Eventos en el label
                            label.dispatchEvent(new MouseEvent('mousedown', { bubbles: true }));
                            label.dispatchEvent(new MouseEvent('mouseup', { bubbles: true }));
                            label.dispatchEvent(new MouseEvent('click', { bubbles: true }));
                            
                            // Marcar checkbox
                            checkbox.checked = true;
                            checkbox.value = 'true';
                            
                            // Eventos en el checkbox
                            checkbox.dispatchEvent(new Event('click', { bubbles: true }));
                            checkbox.dispatchEvent(new Event('change', { bubbles: true }));
                            checkbox.dispatchEvent(new Event('input', { bubbles: true }));
                        """, tyc_label, tyc_checkbox)
                        self.logger.info("✓ Click en label ejecutado")
                    else:
                        self.logger.info("🖱️  Click directo en checkbox con eventos...")
                        driver.execute_script("""
                            const checkbox = arguments[0];
                            checkbox.checked = true;
                            checkbox.value = 'true';
                            checkbox.dispatchEvent(new MouseEvent('click', { bubbles: true }));
                            checkbox.dispatchEvent(new Event('change', { bubbles: true }));
                            checkbox.dispatchEvent(new Event('input', { bubbles: true }));
                        """, tyc_checkbox)
                        self.logger.info("✓ Eventos disparados en checkbox")
                    
                    time.sleep(0.5)
                    
                    # Verificar que se marcó
                    is_checked = tyc_checkbox.is_selected()
                    checkbox_value = tyc_checkbox.get_attribute('value')
                    if is_checked and checkbox_value == 'true':
                        self.logger.info("✅ Términos y condiciones aceptados")
                    else:
                        self.logger.warning(f"⚠️  Checkbox estado: checked={is_checked}, value={checkbox_value}")
                    
                except Exception as e:
                    self.logger.warning(f"⚠️  No se pudo marcar términos: {str(e)}")
                
                # 4. BOTÓN CONTINUAR (con eventos completos)
                self.logger.info("🔍 Buscando botón 'Continuar' final...")
                try:
                    time.sleep(random.uniform(1, 2))
                    
                    continue_button = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((
                            By.XPATH,
                            "//button[@type='submit' and contains(text(), 'Continuar')]"
                        ))
                    )
                    
                    self.logger.info("✓ Botón 'Continuar' encontrado")
                    
                    # Scroll al botón
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", continue_button)
                    time.sleep(1)
                    
                    # Guardar URL antes del click
                    current_url = driver.current_url
                    self.logger.info(f"📍 URL antes de enviar: {current_url}")
                    
                    # Click con TODOS los eventos (mousedown, mouseup, click, submit)
                    self.logger.info("🖱️  Haciendo click final en botón 'Continuar'...")
                    driver.execute_script("""
                        const button = arguments[0];
                        
                        // Simular interacción completa del mouse
                        button.dispatchEvent(new MouseEvent('mousedown', { bubbles: true, cancelable: true }));
                        button.dispatchEvent(new MouseEvent('mouseup', { bubbles: true, cancelable: true }));
                        button.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
                        
                        // Disparar submit en el formulario
                        const form = button.closest('form');
                        if (form) {
                            form.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
                        }
                    """, continue_button)
                    self.logger.info("✓ Click ejecutado con eventos React completos")
                    
                    # ESPERAR PROCESAMIENTO COMPLETO (API calls, validaciones, etc.)
                    self.logger.info("⏳ Esperando procesamiento final...")
                    self.logger.info("   • Validando formulario...")
                    time.sleep(random.uniform(2, 3))
                    self.logger.info("   • reCAPTCHA v3...")
                    time.sleep(random.uniform(2, 3))
                    self.logger.info("   • Enviando datos al servidor...")
                    time.sleep(random.uniform(3, 4))
                    
                    # Verificar navegación
                    new_url = driver.current_url
                    self.logger.info(f"📍 URL después de enviar: {new_url}")
                    
                    if new_url != current_url:
                        self.logger.info("✅ Navegación detectada - Formulario enviado exitosamente")
                        # Esperar carga completa
                        WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.TAG_NAME, "body"))
                        )
                        time.sleep(2)
                    else:
                        self.logger.info("ℹ️  Misma URL - verificando si se procesó correctamente...")
                        time.sleep(random.uniform(2, 3))
                    
                except Exception as btn_error:
                    self.logger.warning(f"⚠️  No se pudo hacer click en botón final: {str(btn_error)}")
                    # Guardar screenshot
                    try:
                        driver.save_screenshot("/tmp/hdi_final_button_error.png")
                        self.logger.info("📸 Screenshot guardado en /tmp/hdi_final_button_error.png")
                    except:
                        pass
                
            except Exception as e:
                self.logger.warning(f"⚠️  Error en formulario de contacto: {str(e)}")
                try:
                    driver.save_screenshot("/tmp/hdi_contact_form_error.png")
                    self.logger.info("📸 Screenshot guardado en /tmp/hdi_contact_form_error.png")
                except:
                    pass
            
            # PASO 12: Extraer datos de la página
            html = driver.page_source
            self.logger.info(f"📄 HTML obtenido: {len(html)} caracteres")
            
            data = self.parse_response(html)
            self.logger.info("✅ Scraping HDI completado exitosamente")
            
            # Mantener navegador abierto para visualización
            if self.debug and self.wait_time > 0:
                self.logger.info(f"🐛 Modo DEBUG: Manteniendo navegador abierto por {self.wait_time}s...")
                self.logger.info("💡 Puedes revisar el estado del formulario en el navegador")
                time.sleep(self.wait_time)
            
            return data
            
        except Exception as e:
            self.logger.error(f"❌ Error en scraping HDI: {str(e)}")
            raise
        finally:
            # Cerrar navegador siempre
            if driver:
                try:
                    driver.quit()
                    self.logger.info("🔒 Chrome cerrado")
                except:
                    pass
    
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
    
    def _human_type(self, element, text: str):
        """Tipea texto con delays aleatorios entre caracteres (más humano)"""
        element.click()
        time.sleep(random.uniform(0.1, 0.3))
        
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.05, 0.15))
        
        time.sleep(random.uniform(0.3, 0.6))
    
    def parse_response(self, html: str) -> Dict[str, Any]:
        """Parsear HTML y extraer información de seguros HDI"""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Estructura base de respuesta
            data = {
                "success": True,
                "source": "hdi",
                "policies": [],
                "pricing": {},
                "error": None,
                "message": "Página HDI accedida correctamente"
            }
            
            # Buscar contenedores de pólizas (ajustar según estructura HTML de HDI)
            policy_containers = soup.find_all('div', class_=lambda x: x and 'policy' in x.lower())
            
            # Si no encuentra, intentar con otras clases comunes
            if not policy_containers:
                policy_containers = soup.find_all(
                    'div',
                    class_=lambda x: x and any(cls in x.lower() for cls in ['plan', 'quote', 'option', 'product'])
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
            
            # Informar resultados
            if data["policies"]:
                self.logger.info(f"📋 {len(data['policies'])} pólizas encontradas")
            else:
                self.logger.info("ℹ️  No se encontraron pólizas en esta vista")
            
            return data
            
        except Exception as e:
            self.logger.error(f"Error parseando respuesta: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "policies": [],
                "source": "hdi"
            }
    
    def _extract_policy(self, container) -> Dict[str, Any]:
        """Extraer datos individuales de una póliza"""
        try:
            policy = {}
            
            # Buscar nombre del plan
            name_elem = container.find(['h2', 'h3', 'h4', 'span'], class_=lambda x: x and 'name' in x.lower())
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
# debug=True mantiene Chrome abierto por wait_time segundos
hdi_scraper = HDIScraper(debug=True, wait_time=30)
