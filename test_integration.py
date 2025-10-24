#!/usr/bin/env python3
"""
Script de test d'intégration pour vérifier que Streamlit et FastAPI communiquent correctement
"""

import requests
import time
import sys
from typing import Dict, Any


def test_api_health(api_url: str = "http://localhost:8000") -> bool:
    """Teste si l'API FastAPI est accessible"""
    try:
        response = requests.get(f"{api_url}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Health: {data['status']}")
            print(f"   Model loaded: {data['model_loaded']}")
            print(f"   Version: {data['version']}")
            return True
        else:
            print(f"❌ API Health: Status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ API Health: {e}")
        return False


def test_api_prediction(api_url: str = "http://localhost:8000") -> bool:
    """Teste l'endpoint de prédiction de l'API"""
    test_data = {
        "sex": "M",
        "length": 0.455,
        "diameter": 0.365,
        "height": 0.095,
        "whole_weight": 0.514,
        "shucked_weight": 0.2245,
        "viscera_weight": 0.101,
        "shell_weight": 0.15
    }
    
    try:
        response = requests.post(f"{api_url}/predict", json=test_data, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Prediction: Success")
            print(f"   Predicted rings: {data.get('predicted_rings', 'N/A')}")
            print(f"   Predicted age: {data.get('predicted_age', 'N/A')}")
            return True
        else:
            print(f"❌ API Prediction: Status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ API Prediction: {e}")
        return False


def test_streamlit_health(streamlit_url: str = "http://localhost:8501") -> bool:
    """Teste si Streamlit est accessible"""
    try:
        response = requests.get(f"{streamlit_url}/_stcore/health", timeout=5)
        if response.status_code == 200:
            print(f"✅ Streamlit Health: OK")
            return True
        else:
            print(f"❌ Streamlit Health: Status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Streamlit Health: {e}")
        return False


def main():
    """Fonction principale de test"""
    print("🧪 Test d'Intégration MLOps - Streamlit + FastAPI")
    print("=" * 50)
    
    # Configuration
    api_url = "http://localhost:8000"
    streamlit_url = "http://localhost:8501"
    
    print(f"\n🔍 Test de l'API FastAPI ({api_url})")
    print("-" * 30)
    api_health_ok = test_api_health(api_url)
    api_prediction_ok = test_api_prediction(api_url)
    
    print(f"\n🔍 Test de Streamlit ({streamlit_url})")
    print("-" * 30)
    streamlit_ok = test_streamlit_health(streamlit_url)
    
    print(f"\n📊 Résumé des Tests")
    print("=" * 20)
    print(f"API Health:     {'✅' if api_health_ok else '❌'}")
    print(f"API Prediction: {'✅' if api_prediction_ok else '❌'}")
    print(f"Streamlit:      {'✅' if streamlit_ok else '❌'}")
    
    # Test d'intégration complet
    if api_health_ok and api_prediction_ok and streamlit_ok:
        print(f"\n🎉 Intégration complète: SUCCÈS!")
        print("   - L'API FastAPI fonctionne correctement")
        print("   - Les prédictions sont opérationnelles")
        print("   - Streamlit est accessible")
        print("   - L'interface utilisateur peut communiquer avec l'API")
        return 0
    else:
        print(f"\n⚠️  Intégration partielle ou échec")
        if not api_health_ok:
            print("   - Démarrer l'API: uv run python src/web_service/main.py")
        if not streamlit_ok:
            print("   - Démarrer Streamlit: uv run streamlit run streamlit_app.py")
        return 1


if __name__ == "__main__":
    sys.exit(main())
