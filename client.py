import socket
import json

class QuizClient:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.player_id = None
        self.score = 0
    
    def connect(self):
        """Conecta ao servidor de quiz"""
        try:
            self.socket.connect((self.host, self.port))
            print(f"Conectado ao servidor em {self.host}:{self.port}")
            
            # Recebe a mensagem de boas-vindas
            welcome_data = self._receive_data()
            self.player_id = welcome_data.get('player_id')
            print(f"\n{welcome_data['message']}")
            
            # Mostra categorias disponíveis
            print("\nCategorias disponíveis:")
            for i, category in enumerate(welcome_data['categories'], 1):
                print(f"{i}. {category}")
            
            # Seleciona categoria
            while True:
                try:
                    choice = int(input("\nEscolha uma categoria (número): ")) - 1
                    if 0 <= choice < len(welcome_data['categories']):
                        selected_category = welcome_data['categories'][choice]
                        break
                    else:
                        print("Número inválido. Tente novamente.")
                except ValueError:
                    print("Por favor, digite um número válido.")
            
            # Envia a categoria escolhida
            self._send_data({"category": selected_category})
            
            # Recebe confirmação de início
            start_msg = self._receive_data()
            print(f"\nIniciando quiz de {selected_category}...")
            print(f"Total de perguntas: {start_msg.get('total_questions', 'desconhecido')}")
            
            # Começa o quiz
            self._run_quiz()
            
        except ConnectionRefusedError:
            print("Não foi possível conectar ao servidor. Verifique se o servidor está rodando.")
        except Exception as e:
            print(f"Erro durante a conexão: {str(e)}")
        finally:
            self.socket.close()
    
    def _run_quiz(self):
        """Executa o fluxo principal do quiz"""
        while True:
            try:
                # Recebe a pergunta
                question_data = self._receive_data()
                
                if question_data.get('status') == 'finished':
                    # Quiz terminado
                    self._show_final_results(question_data)
                    break
                
                if 'error' in question_data:
                    print(f"\nErro: {question_data['error']}")
                    continue
                
                # Mostra a pergunta
                self._display_question(question_data)
                
                # Obtém resposta do usuário
                while True:
                    try:
                        answer = int(input("\nSua resposta (número): ")) - 1
                        if 0 <= answer < len(question_data['options']):
                            break
                        print("Opção inválida. Tente novamente.")
                    except ValueError:
                        print("Por favor, digite um número válido.")
                
                # Envia a resposta
                self._send_data({
                    "question_id": question_data['question_id'],
                    "selected_option": answer
                })
                
                # Recebe feedback
                feedback = self._receive_data()
                self._display_feedback(feedback)
                
            except KeyboardInterrupt:
                print("\nQuiz interrompido pelo usuário.")
                break
            except Exception as e:
                print(f"\nErro durante o quiz: {str(e)}")
                break
    
    def _display_question(self, question_data):
        """Mostra a pergunta na tela"""
        print(f"\nPergunta {question_data['question_id'] + 1}/{question_data['total_questions']}:")
        print(f"{question_data['question']}\n")
        
        for i, option in enumerate(question_data['options'], 1):
            print(f"{i}. {option}")
    
    def _display_feedback(self, feedback):
        """Mostra o feedback da resposta"""
        if feedback.get('correct'):
            print("\n✅ Resposta correta!")
            self.score += 1
        else:
            print("\n❌ Resposta incorreta!")
            print(f"A resposta correta era: {feedback['correct_answer'] + 1}")
        
        print(f"Pontuação atual: {feedback['score']}")
    
    def _show_final_results(self, results):
        """Mostra os resultados finais"""
        print("\n" + "="*50)
        print("QUIZ CONCLUÍDO!")
        print("="*50)
        print(f"\nPontuação final: {results['total_score']}/{results['total_questions']}")
        print(f"Percentual de acertos: {results['percentage']:.1f}%")
        
        if results['percentage'] >= 70:
            print("\n🏆 Excelente desempenho!")
        elif results['percentage'] >= 50:
            print("\n👍 Bom trabalho!")
        else:
            print("\n📚 Continue estudando!")
    
    def _send_data(self, data):
        """Envia dados para o servidor no formato JSON"""
        try:
            self.socket.sendall(json.dumps(data).encode('utf-8'))
        except Exception as e:
            print(f"Erro ao enviar dados: {str(e)}")
            raise
    
    def _receive_data(self):
        """Recebe dados do servidor e decodifica o JSON"""
        try:
            data = self.socket.recv(4096).decode('utf-8')
            return json.loads(data)
        except json.JSONDecodeError:
            print("Erro ao decodificar resposta do servidor")
            raise
        except Exception as e:
            print(f"Erro ao receber dados: {str(e)}")
            raise


if __name__ == "__main__":
    print("=== CLIENTE DO QUIZ ===")
    
    # Configurações de conexão (pode ser alterado para conectar a outros servidores)
    host = input("Endereço do servidor (deixe em branco para localhost): ") or 'localhost'
    port = input("Porta do servidor (deixe em branco para 12345): ") or 12345
    
    try:
        port = int(port)
    except ValueError:
        print("Porta inválida. Usando 12345 como padrão.")
        port = 12345
    
    client = QuizClient(host, port)
    client.connect()