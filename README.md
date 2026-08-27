# 🤖 IA em Loja de Fardamentos

Sistema experimental de automação e assistência inteligente desenvolvido para uma operação de fardamentos, com foco em **entrada de informações por linguagem natural, controle operacional, automação de tarefas e evolução progressiva para uma arquitetura baseada em múltiplos agentes de Inteligência Artificial**.

O projeto começou a partir de uma necessidade prática: reduzir a quantidade de operações manuais realizadas durante o atendimento e a gestão interna de uma loja de fardamentos.

A proposta é construir uma ponte entre a maneira como uma pessoa naturalmente se comunica e a forma estruturada como um sistema precisa armazenar e processar essas informações.

---

# 📌 Visão geral

Sistemas tradicionais normalmente exigem que o usuário navegue por telas, selecione campos e preencha formulários.

Este projeto explora outra possibilidade:

```text
Usuário
   │
   │ "Entraram 30 camisas polo azuis tamanho M"
   ▼
Entrada em linguagem natural
   │
   ▼
Interpretação
   │
   ▼
Identificação da operação
   │
   ▼
Dados estruturados
   │
   ▼
Sistema
   │
   ▼
Execução / confirmação
```

A ideia é permitir que determinadas operações sejam realizadas de maneira mais próxima da comunicação humana, sem abandonar a estrutura e o controle necessários em um sistema empresarial.

---

# 🎯 Objetivos

Os principais objetivos do projeto são:

* Reduzir tarefas manuais repetitivas.
* Facilitar a interação com o sistema.
* Permitir entrada de informações por voz.
* Converter linguagem natural em dados estruturados.
* Automatizar operações internas.
* Centralizar informações da operação.
* Manter histórico das movimentações.
* Gerar documentos automaticamente.
* Criar uma base de dados adequada para análises futuras.
* Preparar a aplicação para utilização de Inteligência Artificial em diferentes áreas.
* Permitir uma evolução gradual da automação para sistemas mais autônomos.

---

# 🧠 Conceito central

O projeto não foi pensado inicialmente como um chatbot.

A Inteligência Artificial é utilizada como uma **interface de interpretação** entre o usuário e o sistema.

Por exemplo:

```text
"Saíram 20 camisas pretas tamanho G."
```

pode ser interpretado como:

```text
Intenção:
    SAÍDA_ESTOQUE

Produto:
    Camisa

Cor:
    Preto

Tamanho:
    G

Quantidade:
    20
```

A partir disso, o sistema pode validar os dados e determinar qual operação deve ser executada.

Esse conceito permite separar duas responsabilidades:

**IA**

> Entender o que o usuário quis dizer.

**Sistema**

> Validar, registrar e executar a operação.

Essa separação é fundamental para evitar que a IA tenha controle irrestrito sobre os dados da aplicação.

---

# 🏗️ Arquitetura atual

A arquitetura atual pode ser representada de maneira simplificada:

```text
                         USUÁRIO
                            │
                 ┌──────────┴──────────┐
                 │                     │
                 ▼                     ▼
              TEXTO                  ÁUDIO
                 │                     │
                 │                     ▼
                 │              Gravação local
                 │                     │
                 │                     ▼
                 │                  Whisper
                 │                     │
                 └──────────┬──────────┘
                            ▼
                       Transcrição
                            │
                            ▼
                    Interpretador
                     de intenção
                            │
                            ▼
                    Comando estruturado
                            │
                            ▼
                     Camada de serviço
                            │
                            ▼
                     Banco de dados
                         SQLite
                            │
             ┌──────────────┼──────────────┐
             ▼              ▼              ▼
         Histórico       Estoque         Pedidos
```

A arquitetura foi construída de forma que a camada de IA não precise acessar diretamente o banco de dados.

A comunicação acontece através das camadas da aplicação.

---

# 🛠️ Tecnologias utilizadas

## Linguagem

### Python

Python é utilizado como linguagem principal do projeto.

A escolha permite trabalhar com:

* desenvolvimento da aplicação;
* processamento de áudio;
* Inteligência Artificial;
* APIs;
* banco de dados;
* automações;
* geração de documentos.

---

## 🗣️ Reconhecimento de voz

### Whisper

O projeto utiliza o **Whisper** para transformar áudio em texto.

O fluxo atual trabalha com processamento local:

```text
Áudio
  ↓
Gravação
  ↓
Whisper
  ↓
Texto
```

O reconhecimento de voz é uma das portas de entrada para a interação com o sistema.

Isso permite que o usuário possa realizar determinadas operações sem necessariamente digitar.

---

## 🗄️ Banco de dados

### SQLite

O projeto utiliza SQLite como banco de dados no ambiente atual.

O banco local utilizado pela aplicação é:

```text
app.db
```

A escolha do SQLite é adequada para a etapa atual do projeto porque permite desenvolvimento e testes com baixa complexidade de infraestrutura.

A arquitetura não impede uma futura migração para um banco de dados mais robusto caso os requisitos de implantação mudem.

---

# 🧱 Estrutura da aplicação

A aplicação foi organizada utilizando separação entre diferentes responsabilidades.

Um dos princípios adotados é evitar que as telas ou a Inteligência Artificial manipulem diretamente o banco de dados.

O fluxo esperado é:

```text
Interface
    ↓
Service
    ↓
Repository
    ↓
Database
```

Essa organização facilita:

* manutenção;
* testes;
* reutilização;
* evolução da aplicação;
* integração futura com IA.

---

# 🗂️ Camadas do sistema

## Models

Responsáveis pela representação dos dados utilizados pela aplicação.

---

## Repositories

Responsáveis pela comunicação com o banco de dados.

A camada de IA não deve acessar diretamente essa camada.

---

## Services

Concentram as regras de negócio.

Por exemplo:

```text
IA
 ↓
Service
 ↓
Validação
 ↓
Repository
 ↓
Banco
```

Essa estrutura permite que uma operação realizada pela interface gráfica, por voz ou futuramente por uma API utilize a mesma regra de negócio.

---

## Interface

A aplicação possui uma interface desktop para utilização das funcionalidades administrativas.

A interface representa uma das formas de interação com o sistema, enquanto a camada de serviços permanece independente dela.

---

# 🎙️ Pipeline de voz

Uma das partes experimentais do projeto é o pipeline de interação por voz.

A estrutura foi organizada aproximadamente da seguinte maneira:

```text
app/
└── voice/
    ├── audio_recorder.py
    ├── speech_to_text.py
    ├── intent_parser.py
    ├── command_executor.py
    └── voice_pipeline.py
```

Cada componente possui uma responsabilidade específica.

### `audio_recorder.py`

Responsável pela captura do áudio.

### `speech_to_text.py`

Responsável pela transformação do áudio em texto utilizando Whisper.

### `intent_parser.py`

Responsável pela interpretação da intenção presente na transcrição.

### `command_executor.py`

Responsável por encaminhar a operação identificada para a lógica correspondente.

### `voice_pipeline.py`

Responsável pela coordenação do fluxo.

```text
Áudio
  ↓
Gravação
  ↓
Transcrição
  ↓
Interpretação
  ↓
Intenção
  ↓
Comando
  ↓
Execução
```

---

# 🧠 Interpretação de comandos

Um dos desafios do projeto é transformar uma frase humana em uma operação que o sistema consiga compreender.

Exemplo:

```text
"Coloca mais 50 camisas brancas tamanho M no estoque."
```

A interpretação esperada seria semelhante a:

```text
{
    "intent": "entrada_estoque",
    "produto": "camisa",
    "cor": "branco",
    "tamanho": "M",
    "quantidade": 50
}
```

O sistema então pode validar essas informações antes de executar qualquer alteração.

---

# ⚠️ Confirmação antes da execução

Uma premissa importante da arquitetura é que a Inteligência Artificial não deve possuir liberdade irrestrita para alterar informações críticas.

Por isso, especialmente nas primeiras versões, o fluxo pode utilizar confirmação:

```text
Usuário
   ↓
Comando
   ↓
IA interpreta
   ↓
Sistema apresenta operação
   ↓
Usuário confirma
   ↓
Sistema executa
```

Exemplo:

```text
Você solicitou:

ENTRADA DE ESTOQUE

Produto: Camisa Polo
Cor: Azul
Tamanho: M
Quantidade: 30

Confirmar operação?
```

Somente após a confirmação a operação é executada.

Essa abordagem reduz o risco de uma interpretação incorreta provocar alterações indesejadas.

---

# 📦 Controle operacional

O sistema possui estrutura para trabalhar com operações relacionadas ao controle da loja.

Entre os conceitos trabalhados estão:

* movimentações;
* entradas;
* saídas;
* histórico;
* transferências;
* atualização de informações;
* consulta de dados.

O objetivo é que diferentes interfaces possam utilizar as mesmas regras de negócio.

---

# 📜 Histórico

As operações realizadas pelo sistema podem ser registradas para manter rastreabilidade.

Isso permite futuramente responder perguntas como:

```text
O que aconteceu?

Quando aconteceu?

Qual produto foi alterado?

Qual quantidade foi movimentada?

Qual operação foi realizada?

Quem realizou?

Qual foi a origem da solicitação?
```

A existência de histórico também será importante para futuras aplicações de Inteligência Artificial.

---

# 📄 Geração de documentos

Outra frente do projeto é a automação da geração de documentos relacionados à operação.

A proposta do MVP inclui um fluxo em que informações coletadas pelo sistema possam ser utilizadas para gerar documentos automaticamente.

Um exemplo conceitual:

```text
Solicitação
    ↓
Interpretação
    ↓
Dados estruturados
    ↓
Registro
    ↓
Geração de documento
    ↓
PDF
```

Isso permite reduzir etapas manuais que normalmente acontecem depois da coleta das informações.

---

# 📱 Integração com WhatsApp

Uma das direções do projeto é permitir que determinadas operações possam ser realizadas através do WhatsApp.

A ideia é utilizar o mesmo princípio da interação por voz:

```text
Funcionário
     │
     ▼
WhatsApp
     │
     ▼
Mensagem
     │
     ▼
Sistema de IA
     │
     ▼
Interpretação
     │
     ▼
Sistema
     │
     ▼
Resposta
```

Exemplos de interações futuras:

```text
"Quanto temos da camisa polo azul M?"

"Saíram 15 camisas pretas G."

"Registra entrada de 50 unidades."

"Quais produtos estão abaixo do estoque mínimo?"
```

A integração com WhatsApp é tratada como uma extensão da plataforma, e não como uma substituição do sistema interno.

---

# 🔌 Arquitetura de integrações

Uma característica importante da arquitetura é permitir diferentes canais de entrada.

```text
                       ┌──────────────┐
                       │  Interface   │
                       │   Desktop    │
                       └──────┬───────┘
                              │
                              │
┌──────────────┐              ▼
│    Áudio     │──────►  Camada de
└──────────────┘        Serviços / IA
                              ▲
                              │
┌──────────────┐              │
│  WhatsApp    │──────────────┘
└──────────────┘
                              │
                              ▼
                         Banco de dados
```

O objetivo é que diferentes interfaces compartilhem a mesma lógica central.

---

# 🤖 Inteligência Artificial — presente e futuro

A IA do projeto pode ser dividida conceitualmente em três etapas.

## Etapa 1 — Assistência

A IA entende o que o usuário está solicitando.

```text
Pessoa → IA → Sistema
```

---

## Etapa 2 — Inteligência operacional

A IA passa a analisar dados históricos.

```text
Dados
  ↓
Histórico
  ↓
Análise
  ↓
Informação
  ↓
Recomendação
```

Exemplo:

```text
"O produto X está apresentando aumento
de demanda nas últimas semanas."
```

---

## Etapa 3 — Sistema multiagente

A IA deixa de ser uma única camada e passa a ser composta por diferentes agentes especializados.

```text
                       ORQUESTRADOR
                            │
          ┌─────────────────┼─────────────────┐
          │                 │                 │
          ▼                 ▼                 ▼
       Agente            Agente            Agente
       Estoque           Vendas           Produção
          │                 │                 │
          └─────────────────┼─────────────────┘
                            │
                            ▼
                         Sistema
```

Essa terceira etapa representa uma possibilidade de evolução de longo prazo.

---

# 🧬 Visão futura: "neurônios" trabalhando juntos

Uma das ideias arquiteturais futuras do projeto é utilizar diferentes componentes especializados de IA.

O termo **neurônio** é utilizado como uma representação conceitual desses componentes.

Cada neurônio teria uma função específica.

Por exemplo:

### 🧠 Neurônio de Estoque

Responsável por analisar:

* níveis de estoque;
* movimentações;
* produtos parados;
* velocidade de saída;
* necessidade de reposição.

---

### 🧠 Neurônio de Vendas

Responsável por analisar:

* volume de vendas;
* produtos com maior saída;
* tendências;
* comportamento histórico;
* períodos de maior demanda.

---

### 🧠 Neurônio de Produção

Responsável por relacionar:

* demanda;
* pedidos;
* estoque;
* capacidade;
* prioridades.

---

### 🧠 Neurônio de Atendimento

Responsável por interpretar solicitações realizadas pelos usuários.

Por exemplo:

```text
"Preciso separar 30 peças para o cliente X."
```

O agente poderia interpretar a solicitação e transformar a linguagem natural em informações estruturadas.

---

### 🧠 Neurônio Analítico

Responsável por cruzar informações e procurar padrões que não sejam imediatamente perceptíveis.

---

# 🔗 Comunicação entre os neurônios

O objetivo não seria simplesmente possuir várias IAs independentes.

A possibilidade mais interessante seria permitir que elas trabalhassem em conjunto.

Exemplo:

```text
                 Demanda aumentou
                       │
                       ▼
                ┌──────────────┐
                │ IA de Vendas │
                └──────┬───────┘
                       │
                       ▼
                 IA de Estoque
                       │
                       ▼
              Estoque insuficiente
                       │
                       ▼
               IA de Produção
                       │
                       ▼
              Verifica capacidade
                       │
                       ▼
                IA Financeira
                       │
                       ▼
                Avalia impacto
                       │
                       ▼
                  Orquestrador
                       │
                       ▼
                   Resposta
```

Nesse modelo, cada agente contribui com uma parte da análise.

O resultado final pode ser mais contextualizado do que uma análise isolada.

---

# 🎛️ Orquestrador de IA

O orquestrador seria responsável por coordenar os diferentes agentes.

Possíveis responsabilidades:

* identificar qual agente deve atuar;
* enviar informações relevantes;
* combinar respostas;
* solicitar novas análises;
* controlar contexto;
* controlar permissões;
* registrar decisões;
* encaminhar ações para aprovação.

A arquitetura futura poderia se aproximar de:

```text
                       Usuário
                          │
                          ▼
                   Orquestrador IA
                          │
          ┌───────────────┼───────────────┐
          ▼               ▼               ▼
       Estoque          Vendas         Produção
          │               │               │
          └───────────────┼───────────────┘
                          │
                          ▼
                     Consolidação
                          │
                          ▼
                       Resposta
```

---

# 🔐 Autonomia progressiva

Uma possível evolução do sistema seria aumentar a autonomia da IA gradualmente.

## Nível 1 — Consulta

A IA apenas responde perguntas.

```text
"Quantas unidades existem?"
```

---

## Nível 2 — Análise

A IA interpreta dados e identifica situações.

```text
"Esse produto está com estoque baixo."
```

---

## Nível 3 — Recomendação

A IA sugere uma ação.

```text
"Recomenda-se reposição de aproximadamente
50 unidades."
```

---

## Nível 4 — Aprovação

A IA prepara a operação, mas aguarda autorização humana.

```text
"Posso registrar a reposição?"
```

---

## Nível 5 — Automação

Operações previamente autorizadas podem ser executadas automaticamente.

```text
Evento
  ↓
IA analisa
  ↓
Regra conhecida
  ↓
Ação automática
```

A autonomia deve crescer conforme a confiabilidade do sistema também cresce.

---

# 🛡️ Segurança e controle

Quanto maior a autonomia de uma IA, maior deve ser o controle sobre suas ações.

Por isso, a arquitetura futura deverá considerar:

* autenticação;
* autorização;
* permissões por agente;
* logs;
* histórico de ações;
* auditoria;
* confirmação de operações críticas;
* isolamento de responsabilidades;
* controle de acesso aos dados;
* registro das decisões tomadas pela IA.

Um agente responsável por analisar estoque, por exemplo, não deveria automaticamente possuir permissão para alterar informações financeiras.

---

# 🧪 Desenvolvimento experimental

O projeto também funciona como um ambiente de experimentação de diferentes conceitos relacionados a Inteligência Artificial.

Entre eles:

* reconhecimento de voz;
* processamento de linguagem natural;
* interpretação de intenções;
* automação;
* integração entre IA e sistemas tradicionais;
* arquitetura baseada em serviços;
* agentes especializados;
* orquestração;
* análise de dados;
* sistemas humano + IA.

A intenção é evoluir essas ideias de forma prática, começando por problemas simples e aumentando a complexidade conforme a arquitetura amadurece.

---

# 🗺️ Roadmap

## 🟢 Fase 1 — Fundação

* [x] Aplicação principal em Python
* [x] Banco SQLite
* [x] Estrutura de models
* [x] Repositories
* [x] Services
* [x] Interface desktop
* [x] Histórico de operações
* [x] Estrutura de movimentações

---

## 🟢 Fase 2 — Voz

* [x] Gravação de áudio
* [x] Integração com Whisper
* [x] Transcrição local
* [x] Pipeline de voz
* [x] Separação entre transcrição e interpretação
* [ ] Evolução do interpretador de intenções
* [ ] Maior cobertura de comandos
* [ ] Melhor tratamento de ambiguidades

---

## 🟡 Fase 3 — Automação

* [ ] Automação de operações
* [ ] Geração de documentos
* [ ] Fluxos automatizados
* [ ] Melhor integração entre IA e serviços
* [ ] Confirmações inteligentes
* [ ] Logs específicos das operações realizadas pela IA

---

## 🟡 Fase 4 — Integrações

* [ ] Integração com WhatsApp
* [ ] Entrada de mensagens
* [ ] Interpretação automática
* [ ] Respostas automáticas
* [ ] Execução controlada de operações
* [ ] Notificações

---

## 🔵 Fase 5 — Inteligência operacional

* [ ] Análise histórica
* [ ] Identificação de padrões
* [ ] Análise de movimentações
* [ ] Previsões
* [ ] Recomendações
* [ ] Detecção de anomalias

---

## 🔵 Fase 6 — Arquitetura multiagente

* [ ] Orquestrador
* [ ] Agente de estoque
* [ ] Agente de vendas
* [ ] Agente de produção
* [ ] Agente de atendimento
* [ ] Agente analítico
* [ ] Memória compartilhada
* [ ] Comunicação entre agentes
* [ ] Sistema de permissões
* [ ] Supervisão humana

---

# 🔮 Visão de longo prazo

A evolução desejada pode ser resumida em:

```text
          SISTEMA TRADICIONAL
                  │
                  ▼
             AUTOMAÇÃO
                  │
                  ▼
          ASSISTENTE DE IA
                  │
                  ▼
         IA OPERACIONAL
                  │
                  ▼
        MÚLTIPLOS AGENTES
                  │
                  ▼
         SISTEMA INTELIGENTE
```

A diferença fundamental está na função que o sistema exerce.

Inicialmente:

> O sistema registra aquilo que aconteceu.

Depois:

> O sistema ajuda a realizar aquilo que precisa ser feito.

Em uma etapa posterior:

> O sistema pode analisar o que está acontecendo e sugerir o que deveria acontecer.

E, em cenários controlados:

> O sistema pode executar determinadas ações previamente autorizadas.

---

# 📐 Princípios do projeto

## Separação entre IA e regras de negócio

A IA interpreta e auxilia.

As regras do sistema continuam sendo responsabilidade da aplicação.

---

## Evolução incremental

A plataforma não depende de uma grande implementação de IA para gerar valor.

Cada etapa deve funcionar antes que a próxima camada de complexidade seja adicionada.

---

## Dados estruturados

A qualidade da futura Inteligência Artificial depende diretamente da qualidade dos dados disponíveis.

Por isso, histórico, registros e estrutura de dados são tratados como parte fundamental do projeto.

---

## Controle humano

Operações críticas devem permanecer sob supervisão até que exista confiança suficiente para sua automação.

---

## Modularidade

Novos componentes devem poder ser adicionados sem obrigatoriamente reconstruir todo o sistema.

---

# 📊 O papel dos dados

Um dos princípios mais importantes do projeto é que **IA não começa no modelo de IA**.

Ela começa nos dados.

```text
Operação
   ↓
Registro
   ↓
Histórico
   ↓
Dados estruturados
   ↓
Análise
   ↓
Modelo de IA
   ↓
Decisão
```

Sem histórico confiável, previsões e recomendações podem se tornar pouco confiáveis.

Por isso, a construção da infraestrutura de dados é uma parte essencial da evolução do projeto.

---

# 🧩 Estado atual x visão futura

Para evitar confusão sobre o estágio de desenvolvimento:

| Componente                       | Estado             |
| -------------------------------- | ------------------ |
| Aplicação Python                 | Implementado       |
| Banco SQLite                     | Implementado       |
| Models / Repositories / Services | Estruturado        |
| Interface desktop                | Implementado       |
| Histórico e movimentações        | Implementado       |
| Gravação de áudio                | Implementado       |
| Whisper                          | Integrado          |
| Pipeline de voz                  | Estruturado        |
| Interpretação de comandos        | Em desenvolvimento |
| Automação avançada               | Planejada          |
| WhatsApp                         | Planejado          |
| IA analítica                     | Planejada          |
| Múltiplos agentes                | Visão futura       |
| Orquestrador                     | Visão futura       |

---

# 🚀 Conclusão

Este projeto representa uma tentativa de aproximar sistemas empresariais da maneira como as pessoas realmente trabalham e se comunicam.

Em vez de exigir que toda informação seja inserida manualmente em estruturas rígidas, a plataforma explora a possibilidade de utilizar **voz, linguagem natural e Inteligência Artificial como interfaces de interação**.

A arquitetura atual fornece a base para essa experimentação.

A visão futura é ampliar essa capacidade através de agentes especializados, capazes de analisar diferentes partes da operação e trabalhar de forma coordenada.

O objetivo final não é simplesmente adicionar um chatbot ao sistema.

É explorar a construção de uma plataforma na qual:

```text
              DADOS
                │
                ▼
             CONTEXTO
                │
                ▼
          INTELIGÊNCIA
                │
                ▼
           RECOMENDAÇÃO
                │
                ▼
            AUTOMAÇÃO
                │
                ▼
       DECISÃO ASSISTIDA
```

A arquitetura de múltiplos "neurônios" permanece como uma direção futura de pesquisa e desenvolvimento. Ela será construída somente quando a base de dados, as regras de negócio e os mecanismos de controle estiverem maduros o suficiente para suportá-la.

---

## 👨‍💻 Sobre o desenvolvimento

Projeto desenvolvido como aplicação prática de conceitos de:

* Python;
* desenvolvimento de software;
* arquitetura em camadas;
* bancos de dados;
* processamento de áudio;
* reconhecimento de voz;
* Inteligência Artificial;
* automação;
* integração de sistemas;
* agentes inteligentes;
* engenharia de software.

O projeto permanece em desenvolvimento e suas funcionalidades podem evoluir conforme novos experimentos e necessidades da operação forem identificados.
