# Estrutura Técnica

## Stack Principal
- Python
- CustomTkinter
- SQLite
- Ollama
- Mistral 7B
- Whisper
- PyInstaller

## Estrutura Principal de Pastas

- app/core
- app/models
- app/services
- app/repositories
- app/ui
- app/prompts
- app/validators
- data
- storage
- assets
- tests

## Principais Serviços

### order_service.py
Responsável pelos pedidos.

### stock_service.py
Responsável pelo estoque.

### production_service.py
Responsável pela linha do tempo do pedido.

### message_service.py
Responsável pela geração de mensagens prontas.

### audio_service.py
Responsável pelo upload e tratamento de áudio.

### transcription_service.py
Responsável pela transcrição dos áudios.

### ai_service.py
Responsável pela comunicação com Ollama.