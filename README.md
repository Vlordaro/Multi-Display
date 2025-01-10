# Gerenciador de Navegadores Kiosk Multi-Display

## Visão Geral
Script Python para gerenciar múltiplos navegadores Chrome em modo kiosk, com controles avançados de teclado e recursos de segurança.

## Funcionalidades Principais
- Inicia navegadores Chrome em modo kiosk em diferentes monitores
- Bloqueia teclado especificamente para cada display
- Senha mestra para desbloquear temporariamente controles de teclado
- Reinício e fechamento individual de displays
- Monitora a saúde do navegador e reinicia automaticamente, se necessário

## Requisitos
- Python 3.x
- Selenium
- keyboard
- screeninfo
- psutil

## Configuração
1. Instale as dependências:
  pip install selenium keyboard screeninfo psutil
2. Configure as configurações de display em `DISPLAY_CONFIG`
3. Execute o script

## Uso
- Fechar display: Use a senha de encerramento específica
- Desbloquear display: Digite a senha mestra
- Reiniciar display fechado: Use a senha de reinício

## Segurança
- Impede atalhos como Alt+Tab, tecla Windows e outros
- Desbloqueio temporário de teclado com temporizador
