"""
PROMPT GENERAL PARA CLOUDFLARE BYPASS EN NUEVAS PÁGINAS
========================================================

Guía paso a paso para obtener la información necesaria y pasar a GitHub Copilot
para que configure el scraper automáticamente.
"""

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

print(PROMPT_GENERAL)
