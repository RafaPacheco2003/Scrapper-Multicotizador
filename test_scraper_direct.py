#!/usr/bin/env python3
"""
Test directo del scraper Mapfre sin FastAPI
Para debuggear Cloudflare sin complejidad adicional
"""
import asyncio
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from scrapers.implementations.mapfre_scraper import MapfreScraper

async def main():
    # URL con parámetros (igual a la del endpoint GET)
    url = "https://cotizadorautos.mapfre.com.mx/rates/car/dodge/dodge-attitude/2024/97289/2003-10-16/m"
    
    print("\n" + "="*70)
    print("🧪 TEST DIRECTO DEL SCRAPER MAPFRE")
    print("="*70)
    print(f"URL: {url}\n")
    
    # Crear scraper con debug=True para ver el navegador
    scraper = MapfreScraper(debug=True, wait_time=10)
    
    try:
        print("⏳ Iniciando scraping...")
        result = await scraper.scrape(url)
        
        print("\n✅ SCRAPING COMPLETADO!")
        print(f"Resultado: {result}\n")
        
        if result.get("success"):
            print("✨ ÉXITO - Datos extraídos correctamente")
            print(f"Pólizas encontradas: {len(result.get('policies', []))}")
            for policy in result.get('policies', []):
                print(f"  - {policy}")
        else:
            print("⚠️  No se pudieron extraer datos")
            print(f"Error: {result.get('error')}")
            
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
