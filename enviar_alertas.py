import os
from datetime import datetime, timedelta
import requests

# Variáveis de ambiente com fallback para os valores diretos
TELEGRAM_BOT_TOKEN = os.getenv(
    "TELEGRAM_BOT_TOKEN", "8829625966:AAGkEGAlPbgWzLozilGVyK8N6dpZSZryjGU"
)
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "-5578794876")

DATA_INICIO_ESCALA = datetime(2026, 10, 21)
PESSOAS_ESCALA = ["Malu", "Angélica", "Luísa"]


def enviar_mensagem(texto):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": texto,
        "parse_mode": "Markdown",
    }
    response = requests.post(url, json=payload)

    # Imprime no log se o Telegram aceitou ou recusou a mensagem
    if response.status_code == 200:
        print("✅ Mensagem enviada com sucesso para o Telegram!")
    else:
        print(f"❌ Erro ao enviar mensagem ({response.status_code}): {response.text}")




# --- AJUSTES E CÁLCULOS ---
data_utc = datetime.utcnow()
data_hoje = data_utc - timedelta(hours=3)  # Ajusta para Horário de Brasília (UTC-3)
dia_semana = data_hoje.weekday()  # 0=Segunda, 1=Terça, ..., 6=Domingo

'''
# --- EXCEÇÕES MANUAIS DE ÚLTIMA HORA (Opcional) ---
# Se estiver entre 04/11/2026 e 10/11/2026, força a Angélica
if datetime(2026, 11, 4) <= data_hoje <= datetime(2026, 11, 10):
    responsavel = "Angélica"
else:
    # Cálculo automático normal
    dias_decorridos = (data_hoje - DATA_INICIO_ESCALA).days
    semana_idx = 0 if dias_decorridos < 0 else dias_decorridos // 7
    responsavel = PESSOAS_ESCALA[semana_idx % len(PESSOAS_ESCALA)]

'''

dias_decorridos = (data_hoje - DATA_INICIO_ESCALA).days
semana_idx = 0 if dias_decorridos < 0 else dias_decorridos // 7
responsavel = PESSOAS_ESCALA[semana_idx % len(PESSOAS_ESCALA)]

# --- BLOCO DE LOGS ---
print("--- DIAGNÓSTICO DE EXECUÇÃO ---")
print(f"Data/Hora ajustada (Brasília): {data_hoje}")
print(f"Dia da semana (0=Seg, 6=Dom): {dia_semana}")
print(f"Responsável calculado: {responsavel}")
print("--------------------------------")


# --- BLOCO DA MALU ---
if responsavel == "Malu":
    # Alerta 1 (Lembrete de Lixo)
    if dia_semana in [6, 3, 5]:
        msg = (
            "🗑️ *Oi eu sou o Faxinômetro, estou fazendo um teste! Desculpe o transtorno*\n\n"
            "Atente-se para os lixos do banheiro e cozinha!"
        )
        enviar_mensagem(msg)

    # Alerta 2 (Fim de Escala / Lixo maior)
    if dia_semana in [0, 1]:
        msg = (
            "🚨 *Aviso de Fim de Escala!*\n\n"
            f"pipipipi 🚨🚨🚨🚨🚨 desça com o lixo maior"
        )
        enviar_mensagem(msg)

# --- BLOCO DA ANGÉLICA ---
elif responsavel == "Angélica":
    # Alerta 1 (Lembrete de Lixo)
    if dia_semana in [1]:
        msg = (
            "🗑️ *Lembrete de Lixo*\n\n"
            f"Atente-se para os lixos do banheiro e cozinha!"
        )
        enviar_mensagem(msg)

    # Alerta 2 (Fim de Escala / Lixo maior)
    if dia_semana in [0, 1]:
        msg = (
            "🚨 *Aviso de Fim de Escala!*\n\n"
            f"pipipipi 🚨🚨🚨🚨🚨 desça com o lixo maior!"
        )
        enviar_mensagem(msg)

# --- BLOCO DA LUÍSA ---
elif responsavel == "Luísa":
    # Alerta 1 (Lembrete de Lixo)
    if dia_semana in [1]:
        msg = (
            "🗑️ *Lembrete de Lixo Luísa!*\n\n"
            f"Atente-se para os lixos do banheiro e cozinha!"
        )
        enviar_mensagem(msg)

    # Alerta 2 (Fim de Escala / Lixo maior)
    if dia_semana in [0, 1]:
        msg = (
            "🚨 *Aviso de Fim de Escala!*\n\n"
            f"pipipipi 🚨🚨🚨🚨🚨 desça com o lixo maior!"
        )
        enviar_mensagem(msg)