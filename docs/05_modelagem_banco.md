# Modelagem do Banco de Dados

## Tabelas Principais

### clients
Armazena os dados dos clientes.

Campos:
- id
- name
- phone
- city
- created_at

### orders
Armazena os pedidos.

Campos:
- id
- client_id
- model
- fabric
- type
- quantity
- deadline
- priority
- total_value
- paid
- notes
- current_stage
- created_at

### order_items
Armazena os tamanhos e quantidades do pedido.

Campos:
- id
- order_id
- size
- gender
- quantity

### order_stages
Armazena as etapas do pedido.

Campos:
- id
- order_id
- stage_name
- status
- notes
- responsible
- started_at
- finished_at

### stock_items
Armazena os itens do estoque.

Campos:
- id
- model
- fabric
- color
- size
- gender
- quantity
- created_at

### stock_movements
Armazena entradas e saídas do estoque.

Campos:
- id
- stock_item_id
- movement_type
- quantity
- notes
- created_at

### attachments
Armazena arquivos enviados.

Campos:
- id
- order_id
- file_name
- file_type
- file_path
- uploaded_at

### generated_messages
Armazena mensagens prontas geradas.

Campos:
- id
- order_id
- sector
- message_text
- created_at