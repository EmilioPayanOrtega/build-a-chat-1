import sys
import os

# Add the parent directory to the path so we can import the app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.services import create_chatbot
from app.models import User

app = create_app()

def create_example_chatbots():
    with app.app_context():
        # Find the creator user
        creator = User.query.filter_by(username='creator_demo').first()
        if not creator:
            print("Error: 'creator_demo' user not found. Please run create_creator.py first.")
            return

        examples = [
            {
                "title": "Guía de Python para Principiantes",
                "description": "Aprende los fundamentos de Python, desde variables hasta funciones.",
                "visibility": "public",
                "tree_json": {
                    "label": "Python",
                    "content": "Python es un lenguaje de programación versátil y fácil de aprender.",
                    "children": [
                        {
                            "label": "Variables",
                            "content": "Las variables almacenan datos.",
                            "children": [
                                {"label": "Enteros", "content": "Números sin decimales (ej: 5, -10).", "children": []},
                                {"label": "Cadenas", "content": "Texto entre comillas (ej: 'Hola').", "children": []}
                            ]
                        },
                        {
                            "label": "Control de Flujo",
                            "content": "Decide qué código ejecutar.",
                            "children": [
                                {"label": "If/Else", "content": "Ejecuta código si una condición es verdadera.", "children": []},
                                {"label": "Bucles", "content": "Repite código (for, while).", "children": []}
                            ]
                        },
                        {
                            "label": "Funciones",
                            "content": "Bloques de código reutilizables.",
                            "children": []
                        }
                    ]
                }
            },
            {
                "title": "Historia del Arte: Renacimiento",
                "description": "Explora los artistas y obras clave del Renacimiento italiano.",
                "visibility": "public",
                "tree_json": {
                    "label": "Renacimiento",
                    "content": "Movimiento cultural que marcó el salto de la Edad Media a la Moderna.",
                    "children": [
                        {
                            "label": "Leonardo da Vinci",
                            "content": "El arquetipo del hombre del Renacimiento.",
                            "children": [
                                {"label": "La Mona Lisa", "content": "Famoso retrato en el Louvre.", "children": []},
                                {"label": "La Última Cena", "content": "Mural en Milán.", "children": []}
                            ]
                        },
                        {
                            "label": "Miguel Ángel",
                            "content": "Escultor, pintor y arquitecto.",
                            "children": [
                                {"label": "David", "content": "Escultura de mármol blanco.", "children": []},
                                {"label": "Capilla Sixtina", "content": "Frescos en el Vaticano.", "children": []}
                            ]
                        }
                    ]
                }
            },
            {
                "title": "Recetas Rápidas: Desayunos",
                "description": "Ideas para desayunos nutritivos y rápidos de preparar.",
                "visibility": "public",
                "tree_json": {
                    "label": "Desayunos",
                    "content": "La comida más importante del día.",
                    "children": [
                        {
                            "label": "Dulces",
                            "content": "Opciones para los golosos.",
                            "children": [
                                {"label": "Avena con Frutas", "content": "Avena cocida con plátano y fresas.", "children": []},
                                {"label": "Hotcakes", "content": "Clásicos con miel de maple.", "children": []}
                            ]
                        },
                        {
                            "label": "Salados",
                            "content": "Para empezar con energía.",
                            "children": [
                                {"label": "Huevos Revueltos", "content": "Con jamón o vegetales.", "children": []},
                                {"label": "Tostada de Aguacate", "content": "Pan integral con aguacate y sal.", "children": []}
                            ]
                        }
                    ]
                }
            }
        ]

        print(f"Creating {len(examples)} example chatbots for user '{creator.username}'...")

        for ex in examples:
            try:
                create_chatbot(
                    creator.id,
                    ex['title'],
                    ex['description'],
                    ex['visibility'],
                    ex['tree_json']
                )
                print(f"Created: {ex['title']}")
            except Exception as e:
                print(f"Failed to create '{ex['title']}': {e}")

if __name__ == '__main__':
    create_example_chatbots()
