import json
import uuid
from utils.read_questions import read_questions

def handle_client(conn, addr):
    questions = read_questions()
    print(f"Nova conexão de {addr}")
    player_id = str(uuid.uuid4())
    score = 0
    
    try:
        # Envia mensagem de boas-vindas
        welcome_msg = {
            "message": f"Bem-vindo ao Quiz Server! Seu ID é {player_id}",
            "player_id": player_id,
            "categories": list(questions.keys())
        }
        conn.sendall(json.dumps(welcome_msg).encode('utf-8'))
        
        # Recebe a categoria escolhida pelo cliente
        data = conn.recv(1024).decode('utf-8')
        category = json.loads(data).get("category")
        
        if category not in questions:
            error_msg = {"error": "Categoria inválida", "available_categories": list(questions.keys())}
            conn.sendall(json.dumps(error_msg).encode('utf-8'))
            return
        
        # Inicia o quiz
        conn.sendall(json.dumps({"status": "starting", "category": category}).encode('utf-8'))
        
        for i, question_data in enumerate(questions[category]):
            # Prepara a questão para envio (sem a resposta correta)
            question_to_send = {
                "question_id": i,
                "question": question_data["question"],
                "options": question_data["options"],
                "total_questions": len(questions[category])
            }
            
            # Envia a questão
            conn.sendall(json.dumps(question_to_send).encode('utf-8'))
            
            # Recebe a resposta do cliente
            answer_data = conn.recv(1024).decode('utf-8')
            try:
                answer = json.loads(answer_data)
                selected_option = answer.get("selected_option")
                
                # Verifica a resposta
                if selected_option == question_data["correct"]:
                    score += 1
                    response = {
                        "correct": True,
                        "score": score,
                        "correct_answer": question_data["correct"]
                    }
                else:
                    response = {
                        "correct": False,
                        "score": score,
                        "correct_answer": question_data["correct"]
                    }
                
                # Envia feedback
                conn.sendall(json.dumps(response).encode('utf-8'))
                
            except json.JSONDecodeError:
                error_msg = {"error": "Resposta inválida"}
                conn.sendall(json.dumps(error_msg).encode('utf-8'))
                continue
        
        # Final do quiz - envia resultados finais
        final_result = {
            "status": "finished",
            "total_score": score,
            "total_questions": len(questions[category]),
            "percentage": (score / len(questions[category])) * 100
        }
        conn.sendall(json.dumps(final_result).encode('utf-8'))
        
    except ConnectionResetError:
        print(f"Conexão com {addr} foi resetada pelo cliente")
    except Exception as e:
        print(f"Erro ao lidar com o cliente {addr}: {str(e)}")
    finally:
        print(f"Fechando conexão com {addr}. Pontuação final: {score}")
        conn.close()