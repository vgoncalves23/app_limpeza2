from datetime import datetime, timedelta
import requests

TELEGRAM_BOT_TOKEN = "8829625966:AAGkEGAlPbgWzLozilGVyK8N6dpZSZryjGU"
TELEGRAM_CHAT_ID = "-5578794876"
DATA_INICIO_ESCALA = datetime(2026, 10, 21)
PESSOAS_ESCALA = ["Malu", "Angélica", "Luísa"]


def enviar_mensagem(texto):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": texto,
        "parse_mode": "Markdown",
    }
    requests.post(url, json=payload)


# --- AJUSTES E CÁLCULOS ---
data_utc = datetime.utcnow()
data_hoje = data_utc - timedelta(hours=3)  # Ajusta para Horário de Brasília (UTC-3)
hora_atual = data_hoje.hour  # Pega a hora atual (0 a 23)
dia_semana = data_hoje.weekday()  # 0=Segunda, 1=Terça, ..., 6=Domingo

dias_decorridos = (data_hoje - DATA_INICIO_ESCALA).days
semana_idx = 0 if dias_decorridos < 0 else dias_decorridos // 7
responsavel = PESSOAS_ESCALA[semana_idx % len(PESSOAS_ESCALA)]

# --- BLOCO DE LOGS (Para ver no GitHub Actions) ---
print(f"--- DIAGNÓSTICO DE EXECUÇÃO ---")
print(f"Data/Hora UTC crua: {data_utc}")
print(f"Data/Hora ajustada (Brasília): {data_hoje}")
print(f"Hora atual extraída: {hora_atual}")
print(f"Dia da semana (0=Seg, 6=Dom): {dia_semana}")
print(f"Dias decorridos desde o início: {dias_decorridos}")
print(f"Responsável calculado: {responsavel}")
print(f"--------------------------------")


# --- BLOCO DA MALU ---
if responsavel == "Malu" and hora_atual == 18:
    # Alerta 1 (Lembrete de Lixo)
    if dia_semana in [0, 3, 4, 5, 6]:
        msg = (
            f"🗑️ *Oi eu sou o Faxinometro, estou fazendo um teste! Desculpe transtorno*\n\n"
            f"Atente-se para os lixos do banheiro e cozinha*!"
        )
        enviar_mensagem(msg)

    # Alerta 2 (Fim de Escala / Lixo maior)
    if dia_semana in [1]:
        msg = (
            f"🚨 *Aviso de Fim de Escala!*\n\n"
            f"pipipipi 🚨🚨🚨🚨🚨 desça com o lixo maior, *{responsavel}*!"
        )
        enviar_mensagem(msg)

# --- BLOCO DA ANGÉLICA ---
elif responsavel == "Angélica":
    # Alerta 1 (Lembrete de Lixo)
    if dia_semana in [0, 3, 4, 5, 6]:
        msg = (
            f"🗑️ *Lembrete de Lixo Angélica!*\n\n"
            f"Atente-se para os lixos do banheiro e cozinha, *{responsavel}*!"
        )
        enviar_mensagem(msg)

    # Alerta 2 (Fim de Escala / Lixo maior)
    if dia_semana in [1, 6]:
        msg = (
            f"🚨 *Aviso de Fim de Escala!*\n\n"
            f"pipipipi 🚨🚨🚨🚨🚨 desça com o lixo maior, *{responsavel}*!"
        )
        enviar_mensagem(msg)

# --- BLOCO DA LUÍSA ---
elif responsavel == "Luísa":
    # Alerta 1 (Lembrete de Lixo)
    if dia_semana in [0, 3, 4, 5, 6]:
        msg = (
            f"🗑️ *Lembrete de Lixo Luísa!*\n\n"
            f"Atente-se para os lixos do banheiro e cozinha, *{responsavel}*!"
        )
        enviar_mensagem(msg)

    # Alerta 2 (Fim de Escala / Lixo maior)
    if dia_semana in [1, 6]:
        msg = (
            f"🚨 *Aviso de Fim de Escala!*\n\n"
            f"pipipipi 🚨🚨🚨🚨🚨 desça com o lixo maior, *{responsavel}*!"
        )
        enviar_mensagem(msg)