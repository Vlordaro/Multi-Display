from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import keyboard
import time
from screeninfo import get_monitors
from threading import Timer, Lock, Thread
import os
import psutil
import sys
from dotenv import load_dotenv

load_dotenv()

DISPLAY_CONFIG = {
  'Dashboard': {
      'monitor': 2,
      'url': os.getenv('DASHBOARD_URL'),
      'senha_mestra': os.getenv('DASH_MASTER_PWD'),
      'senha_encerrar': os.getenv('DASH_EXIT_PWD'), 
      'senha_reiniciar': os.getenv('DASH_RESTART_PWD')
  },
  'Kiosk': {
      'monitor': 1,
      'url': os.getenv('KIOSK_URL'),
      'senha_mestra': os.getenv('KIOSK_MASTER_PWD'),
      'senha_encerrar': os.getenv('KIOSK_EXIT_PWD'),
      'senha_reiniciar': os.getenv('KIOSK_RESTART_PWD')
  }
}

buffer_teclas = ""
keyboard_lock = Lock() 
displays = {}

class Display:
  def __init__(self, nome):
      config = DISPLAY_CONFIG[nome]
      self.nome = nome
      self.monitor = config['monitor'] - 1
      self.url = config['url']
      self.senha_mestra = config['senha_mestra']
      self.senha_encerrar = config['senha_encerrar']
      self.senha_reiniciar = config['senha_reiniciar']

      self.bloqueios_ativos = True
      self.tempo_desbloqueio = 60
      self.teclas_bloqueadas = ['alt', 'f11', 'esc', 'windows', 'tab', 'ctrl']

      self.driver = None
      self.encerrar_flag = False
      self.iniciar_flag = True
      self.iniciar_chrome()

  def iniciar_chrome(self):
      monitors = get_monitors()
      if self.monitor >= len(monitors):
          print(f"Monitor {self.monitor + 1} não encontrado.")
          return

      selected_monitor = monitors[self.monitor]

      chrome_options = Options()
      chrome_options.add_argument("--kiosk")
      chrome_options.add_argument("--start-maximized")
      chrome_options.add_argument("--disable-features=TranslateUI")
      chrome_options.add_argument("--disable-save-password-bubble")
      chrome_options.add_argument("--disable-popup-blocking")
      chrome_options.add_argument(f"--window-position={selected_monitor.x},{selected_monitor.y}")
      chrome_options.add_argument(f"--app={self.url}")
      chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
      chrome_options.add_experimental_option('useAutomationExtension', False)
      chrome_options.add_argument(f"--user-data-dir=C:\\Safe\\ChromeData\\{self.nome}")

      try:
          self.driver = webdriver.Chrome(options=chrome_options)
      except Exception as e:
          print(f"Erro ao iniciar Chrome para {self.nome}: {e}")
          self.driver = None

  def executar(self):
      while not self.encerrar_flag:
          try:
              if self.driver and self.driver.service.process:
                  self.driver.current_url
                  if self.bloqueios_ativos:
                      self.driver.fullscreen_window()
              else:
                  print(f"Reiniciando navegador para {self.nome}.")
                  self.reiniciar_chrome()
              time.sleep(0.1)
          except Exception as e:
              print(f"Erro no navegador {self.nome}: {e}")
              self.reiniciar_chrome()
      
      self.encerrar()

  def reiniciar_chrome(self):
      self.encerrar()
      self.iniciar_chrome()

  def encerrar(self):
      try:
          if self.driver:
              processo = psutil.Process(self.driver.service.process.pid)
              for proc in processo.children(recursive=True):
                  proc.kill()
              processo.kill()
              self.driver = None
              print(f"{self.nome} encerrado.")
      except Exception as e:
          print(f"Erro ao encerrar {self.nome}: {e}")

def bloquear_teclas():
  teclas = ['alt', 'f11', 'esc', 'windows', 'tab', 'ctrl']
  for tecla in teclas:
      keyboard.block_key(tecla)

def desbloquear_teclas():
  teclas = ['alt', 'f11', 'esc', 'windows', 'tab', 'ctrl']
  for tecla in teclas:
      keyboard.unblock_key(tecla)

def verificar_senha(e):
  global buffer_teclas

  if e.event_type == 'down':
      buffer_teclas += e.name
      print(f"Buffer de teclas: {buffer_teclas}")

      for nome, display in list(displays.items()):
          if display.senha_encerrar in buffer_teclas:
              print(f"Encerrando {nome}...")
              display.encerrar_flag = True
              display.iniciar_flag = False
              buffer_teclas = ""
              break
          elif display.senha_mestra in buffer_teclas:
              print(f"Desbloqueio ativado para {nome}.")
              display.bloqueios_ativos = False
              desbloquear_teclas()
              Timer(display.tempo_desbloqueio, lambda: setattr(display, 'bloqueios_ativos', True)).start()
              buffer_teclas = ""
              break
          elif display.senha_reiniciar in buffer_teclas and display.encerrar_flag:
              print(f"Reiniciando {nome}...")
              display.encerrar_flag = False
              display.iniciar_flag = True
              thread = Thread(target=executar_display, args=(nome,))
              thread.start()
              buffer_teclas = ""
              break

def executar_display(nome):
  display = Display(nome)
  displays[nome] = display
  if display.iniciar_flag:
      display.executar()

if __name__ == "__main__":
  keyboard.hook(verificar_senha)
  bloquear_teclas()

  threads = []
  for nome in DISPLAY_CONFIG:
      thread = Thread(target=executar_display, args=(nome,))
      threads.append(thread)
      thread.start()

  for thread in threads:
      thread.join()

  print("Programa encerrado.")
