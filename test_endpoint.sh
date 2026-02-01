#!/usr/bin/env bash
"""
Script para probar el endpoint GET del scraper Mapfre
"""

echo "========================================================================"
echo "🧪 PRUEBAS DEL ENDPOINT /api/v1/scrapers/scrape/mapfre"
echo "========================================================================"
echo ""

# Verificar que el servidor está corriendo
echo "1️⃣  Verificando si el servidor está corriendo..."
if ! curl -s http://localhost:8000/api/v1/scrapers/health > /dev/null 2>&1; then
    echo "❌ El servidor NO está corriendo"
    echo "   Inicia con: source .venv/bin/activate && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"
    exit 1
fi
echo "✅ Servidor está activo"
echo ""

# Test 1: Health check
echo "2️⃣  Test Health Check..."
curl -s http://localhost:8000/api/v1/scrapers/health | python -m json.tool
echo ""
echo ""

# Test 2: Scraper Mapfre
echo "3️⃣  Test Scraper Mapfre..."
echo "   URL: http://localhost:8000/api/v1/scrapers/scrape/mapfre"
echo "   Iniciando scraping..."
echo ""
curl -s http://localhost:8000/api/v1/scrapers/scrape/mapfre | python -m json.tool
echo ""

echo "========================================================================"
echo "✅ PRUEBAS COMPLETADAS"
echo "========================================================================"
