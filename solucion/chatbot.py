import os
import requests
from openai import OpenAI
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from typing import List, Dict

# Cargar variables de entorno
load_dotenv()

# Configuración de APIs
SERPER_API_KEY = os.getenv('SERPER_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

class Chatbot:
    def __init__(self):
        self.conversation_history = []
        self.sources = []
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def search_internet(self, query: str) -> List[Dict]:
        """Realiza búsqueda en Google usando Serper API"""
        headers = {
            'X-API-KEY': SERPER_API_KEY,
            'Content-Type': 'application/json'
        }
        url = 'https://google.serper.dev/search'
        payload = {'q': query}
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            results = response.json()
            return results.get('organic', [])[:5]  # Obtener los primeros 5 resultados
        except Exception as e:
            print(f"Error en la búsqueda: {e}")
            return []

    def extract_text(self, url: str) -> str:
        """Extrae el texto principal de una URL"""
        try:
            response = requests.get(url, timeout=5)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Eliminar scripts y estilos
            for script in soup(['script', 'style']):
                script.decompose()
            
            return soup.get_text()
        except Exception as e:
            print(f"Error extrayendo texto de {url}: {e}")
            return ""

    def generate_response(self, query: str, context: str) -> str:
        """Genera una respuesta usando OpenAI"""
        try:
            messages = self.conversation_history + [
                {"role": "user", "content": f"Pregunta: {query}\nContexto de búsqueda: {context}"}
            ]
            
            stream = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                stream=True,
                temperature=0.7
            )
            
            # Procesar respuesta en streaming
            full_response = ""
            print("Chatbot: ", end="", flush=True)
            
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    print(content, end="", flush=True)
                    full_response += content
            
            print("\n")
            return full_response
            
        except Exception as e:
            print(f"Error generando respuesta: {e}")
            return "Lo siento, hubo un error al generar la respuesta."

    def chat(self):
        """Función principal del chatbot"""
        print("¡Hola! Soy tu chatbot asistente. Escribe 'salir' para terminar.")
        
        while True:
            user_input = input("\nTú: ")
            if user_input.lower() == 'salir':
                print("¡Hasta luego!")
                break
            
            # Guardar pregunta en el historial
            self.conversation_history.append({"role": "user", "content": user_input})
            
            # Realizar búsqueda
            print("\n** Buscando en internet **")
            search_results = self.search_internet(user_input)
            
            # Recopilar información de las fuentes
            context = ""
            self.sources = []
            
            for result in search_results:
                if 'link' in result:
                    self.sources.append({
                        'title': result.get('title', ''),
                        'link': result.get('link', '')
                    })
                    extracted_text = self.extract_text(result['link'])
                    context += f"\nFuente: {result['title']}\n{extracted_text[:500]}"
            
            # Generar y mostrar respuesta
            response = self.generate_response(user_input, context)
            self.conversation_history.append({"role": "assistant", "content": response})
            
            # Mostrar fuentes
            print("\nFuentes consultadas:")
            for source in self.sources:
                print(f"- {source['title']}: {source['link']}")

if __name__ == "__main__":
    chatbot = Chatbot()
    chatbot.chat()
