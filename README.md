# Gerenciador de Navegadores Kiosk Multi-Display

Sistema para gerenciar múltiplos navegadores Chrome em modo kiosk com controles de segurança.

## Funcionalidades

- Execução em múltiplos monitores
- Bloqueio de teclas por display
- Senhas para controle (mestra, encerramento, reinício)
- Monitoramento e reinício automático
- Proteção contra interferência do usuário

## Requisitos

- Python 3.x
- Chrome/Chromium
- Bibliotecas Python:
  - selenium
  - keyboard
  - screeninfo 
  - psutil
  - python-dotenv

## Instalação

1. Clone o repositório
2. Instale as dependências:
  pip install selenium keyboard screeninfo psutil python-dotenv

## Configuração

Copie .env.example para .env
Configure as URLs e senhas no .env
Ajuste monitores em DISPLAY_CONFIG se necessário

## Uso

Execute: python main.py
Controles:

Digite senha mestra: Desbloqueia teclado por 60s
Digite senha encerrar: Fecha display específico
Digite senha reiniciar: Reinicia display fechado



## Segurança

Bloqueia teclas de sistema (Alt, Windows, etc)
Desbloqueio temporário com timeout
Senhas configuráveis por display
Proteção contra fechamento acidental

## Licensa
MIT
