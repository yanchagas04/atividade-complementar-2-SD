# Quiz Distribuído - Sistemas Distribuídos

## Discentes
**Vinícius Fernandes de Oliveira**  
[![GitHub](https://img.shields.io/badge/GitHub-vfdeoliveira1-blue?style=flat-square&logo=github)](https://github.com/vfdeoliveira1)

**Vitor Hugo de Jesus Santos**  
[![GitHub](https://img.shields.io/badge/GitHub-vhjsoficial1-blue?style=flat-square&logo=github)](https://github.com/vhjsoficial1)

**Yan Campêlo das Chagas**  
[![GitHub](https://img.shields.io/badge/GitHub-yanchagas04-blue?style=flat-square&logo=github)](https://github.com/yanchagas04) 

## Descrição
Este projeto implementa um sistema de quiz distribuído onde múltiplos clientes podem se conectar a um servidor central para responder perguntas de diferentes categorias. Desenvolvido como atividade complementar da disciplina de Sistemas Distribuídos, utiliza sockets TCP em Python para comunicação entre os componentes.

## Funcionalidades

### Servidor
- Gerencia múltiplas conexões de clientes simultaneamente
- Oferece diferentes categorias de quiz (Tecnologia, Filmes, etc.)
- Valida respostas e calcula pontuação (1 ponto por acerto)

### Cliente
- Interface para conexão com o servidor
- Exibição de perguntas e opções de resposta
- Envio das respostas selecionadas
- Apresentação da pontuação acumulada

## Tecnologias Utilizadas
- **Linguagem**: Python 3
- **Comunicação**: Sockets TCP
- **Serialização**: JSON

## Estrutura do Projeto
├── server\
│............├── client\
│............│........└── handle_client.py\
│.............├── utils\
│.............│........└── read_questions.py\
│.............├── server.py\
│.............└── questions.json\
├── client.py\
└── README.md\

## Formato das Mensagens
```json
{
    "nome_categoria_1": [
        {
            "question": "pergunta",
            "options": [
                "alternativa 1",
                "alternativa 2",
                "alternativa 3",
                "alternativa 4"
            ],
            "correct": 0 //índice da alterantiva correta (0 ou maior)
        },
        {
            "question": "pergunta",
            "options": [
                "alternativa 1",
                "alternativa 2",
                "alternativa 3",
                "alternativa 4"
            ],
            "correct": 3 //índice da alterantiva correta (0 ou maior)
        }
    ],
    "nome_categoria_2": [
        {
            "question": "pergunta",
            "options": [
                "alternativa 1",
                "alternativa 2",
                "alternativa 3",
                "alternativa 4"
            ],
            "correct": 1 //índice da alterantiva correta (0 ou maior)
        },
        {
            "question": "pergunta",
            "options": [
                "alternativa 1",
                "alternativa 2",
                "alternativa 3",
                "alternativa 4"
            ],
            "correct": 2 //índice da alterantiva correta (0 ou maior)
        }
    ],
}
```

## Vídeo de Apresentação

[![YouTube](https://img.shields.io/badge/YouTube-%23FF0000.svg?style=for-the-badge&logo=YouTube&logoColor=white)](https://youtu.be/VDx4-LBrmeg)
