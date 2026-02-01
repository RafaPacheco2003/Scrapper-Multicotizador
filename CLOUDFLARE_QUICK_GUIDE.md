# GUÍA RÁPIDA: QUÉ PASAR PARA CLOUDFLARE BYPASS

## En 30 Segundos

Cuando encuentres una página con Cloudflare, necesito:

1. **User-Agent** (F12 → Network → Headers → user-agent)
   - Copia exactamente lo que dice

2. **Accept-Language** (F12 → Network → Headers → accept-language)
   - Copia exactamente lo que dice

3. **URL de la página**
   - https://ejemplo.com

4. **Formularios** (F12 → Elements)
   - Para cada input: ID, Class, Type, Ejemplo de valor
   - Para cada botón: ID, Class, Texto

5. **Screenshot de Network**
   - Mostrando primer 10 requests
   - Mostrando todos los requests de tracking

---

## Ejemplo Real: Mapfre

```
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.7559.97 Safari/537.36

Accept-Language: es-GB,es-MX,es;q=0.9

URL: https://cotizadorautos.mapfre.com.mx

Formularios:
- contact-name (text) → "Juan Pérez"
- contact-email (email) → "juan.perez2024@gmail.com"
- contact-phone (tel) → "9991234567"

Botón:
- confirm-usercontact-button → "Continuar"

Tracking visto:
- Datadog RUM ✓
- Datadog Logs ✓
- Google Analytics ✓
- Facebook Pixel ✓
```

---

## Checklist Rápido

```
□ User-Agent copiado exactamente
□ Accept-Language copiado exactamente
□ URL de la página
□ IDs de inputs (name, email, phone, etc.)
□ IDs de botones
□ Screenshot de Network mostrando tracking
□ ¿Aparece Cloudflare? (sí/no y tipo)
```

**Con esto es SUFICIENTE para que el scraper funcione!** 🚀
