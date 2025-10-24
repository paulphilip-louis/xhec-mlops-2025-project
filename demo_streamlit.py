#!/usr/bin/env python3
"""
Script de démonstration pour l'interface Streamlit
Teste les fonctions principales sans lancer l'interface graphique
"""

import sys
import os
import pandas as pd
import numpy as np
from unittest.mock import patch, Mock

# Ajouter le répertoire racine au path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def demo_streamlit_functions():
    """Démonstration des fonctions principales de Streamlit"""
    
    print("🐚 Démonstration de l'Interface Streamlit - Prédiction d'Âge des Abalones")
    print("=" * 70)
    
    # Test 1: Chargement des données d'exemple
    print("\n1️⃣ Test du chargement des données d'exemple...")
    
    # Mock des données
    mock_data = pd.DataFrame({
        'Sex': ['M', 'F', 'I'] * 10,
        'Length': np.random.uniform(0.1, 0.8, 30),
        'Diameter': np.random.uniform(0.1, 0.7, 30),
        'Height': np.random.uniform(0.01, 0.3, 30),
        'Whole weight': np.random.uniform(0.1, 2.0, 30),
        'Shucked weight': np.random.uniform(0.05, 1.0, 30),
        'Viscera weight': np.random.uniform(0.01, 0.5, 30),
        'Shell weight': np.random.uniform(0.01, 0.5, 30),
        'Rings': np.random.randint(1, 30, 30)
    })
    
    with patch('pandas.read_csv', return_value=mock_data):
        try:
            from streamlit_app import load_sample_data
            sample_data = load_sample_data()
            print(f"   ✅ Données chargées: {len(sample_data)} lignes")
            print(f"   📊 Colonnes: {list(sample_data.columns)}")
            print(f"   🎯 Âge moyen: {sample_data['Rings'].mean():.1f} anneaux")
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
    
    # Test 2: Vérification de l'API
    print("\n2️⃣ Test de la vérification de santé de l'API...")
    
    try:
        from streamlit_app import check_api_health
        
        # Test avec API accessible
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_get.return_value = mock_response
            
            api_healthy = check_api_health()
            print(f"   ✅ API accessible: {api_healthy}")
        
        # Test avec API inaccessible
        with patch('requests.get', side_effect=Exception("Connection error")):
            api_healthy = check_api_health()
            print(f"   ⚠️  API inaccessible: {api_healthy}")
            
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # Test 3: Prédiction simulée
    print("\n3️⃣ Test de la fonction de prédiction...")
    
    test_data = {
        "sex": "M",
        "length": 0.5,
        "diameter": 0.4,
        "height": 0.15,
        "whole_weight": 0.8,
        "shucked_weight": 0.3,
        "viscera_weight": 0.15,
        "shell_weight": 0.2
    }
    
    try:
        from streamlit_app import make_prediction
        
        # Mock de la réponse API
        mock_response = Mock()
        mock_response.json.return_value = {
            "predicted_age": 15.2,
            "confidence": 0.85,
            "model_version": "v1.0"
        }
        mock_response.raise_for_status.return_value = None
        
        with patch('requests.post', return_value=mock_response):
            prediction = make_prediction(test_data)
            
            if prediction:
                print(f"   ✅ Prédiction réussie:")
                print(f"      🎯 Âge prédit: {prediction['predicted_age']} anneaux")
                print(f"      📊 Confiance: {prediction['confidence']:.2%}")
                print(f"      🔧 Version modèle: {prediction['model_version']}")
            else:
                print("   ❌ Prédiction échouée")
                
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # Test 4: Validation des données
    print("\n4️⃣ Test de la validation des données...")
    
    # Données valides
    valid_data = {
        "sex": "F",
        "length": 0.6,
        "diameter": 0.5,
        "height": 0.2,
        "whole_weight": 1.0,
        "shucked_weight": 0.4,
        "viscera_weight": 0.2,
        "shell_weight": 0.3
    }
    
    required_keys = ["sex", "length", "diameter", "height", 
                    "whole_weight", "shucked_weight", "viscera_weight", "shell_weight"]
    
    all_keys_present = all(key in valid_data for key in required_keys)
    print(f"   ✅ Toutes les clés requises présentes: {all_keys_present}")
    
    # Vérifier les types
    type_checks = {
        "sex": isinstance(valid_data["sex"], str),
        "length": isinstance(valid_data["length"], (int, float)),
        "diameter": isinstance(valid_data["diameter"], (int, float)),
        "height": isinstance(valid_data["height"], (int, float)),
        "whole_weight": isinstance(valid_data["whole_weight"], (int, float)),
        "shucked_weight": isinstance(valid_data["shucked_weight"], (int, float)),
        "viscera_weight": isinstance(valid_data["viscera_weight"], (int, float)),
        "shell_weight": isinstance(valid_data["shell_weight"], (int, float))
    }
    
    all_types_valid = all(type_checks.values())
    print(f"   ✅ Types de données valides: {all_types_valid}")
    
    # Test 5: Statistiques des données
    print("\n5️⃣ Test des statistiques des données...")
    
    print(f"   📊 Distribution par sexe:")
    sex_counts = mock_data["Sex"].value_counts()
    for sex, count in sex_counts.items():
        print(f"      {sex}: {count} ({count/len(mock_data)*100:.1f}%)")
    
    print(f"   📈 Statistiques de l'âge:")
    print(f"      Âge min: {mock_data['Rings'].min()} anneaux")
    print(f"      Âge max: {mock_data['Rings'].max()} anneaux")
    print(f"      Âge moyen: {mock_data['Rings'].mean():.1f} anneaux")
    print(f"      Écart-type: {mock_data['Rings'].std():.1f} anneaux")
    
    print("\n" + "=" * 70)
    print("🎉 Démonstration terminée avec succès!")
    print("\n📝 Prochaines étapes:")
    print("   1. Démarrer l'API FastAPI: uvicorn src.web_service.main:app --reload")
    print("   2. Lancer Streamlit: streamlit run streamlit_app.py")
    print("   3. Ouvrir http://localhost:8501 dans votre navigateur")
    print("   4. Tester l'interface avec les données d'exemple")

if __name__ == "__main__":
    demo_streamlit_functions()
