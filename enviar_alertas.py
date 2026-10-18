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


# Ajusta a hora UTC para o Horário de Brasília (UTC-3)
data_hoje = datetime.utcnow() - timedelta(hours=3)

print(data_hoje)

dias_decorridos = (data_hoje - DATA_INICIO_ESCALA).days
semana_idx = 0 if dias_decorridos < 0 else dias_decorridos // 7
responsavel = PESSOAS_ESCALA[semana_idx % len(PESSOAS_ESCALA)]

dia_semana = data_hoje.weekday()  # 0=Segunda, 1=Terça, 3=Quinta, 5=Sábado

# Quinta (3), Sábado (5) ou Segunda (0) -> Alerta 1
if dia_semana in [0, 3, 4, 5, 6]:
    msg = (
        f"🗑️ *Lembrete de Lixo!*\n\n"
        f"Atente-se para os lixos do banheiro e cozinha, *{responsavel}*!"
    )
    enviar_mensagem(msg)

# Terça (1) -> Alerta 2
if dia_semana in[1, 6]:
    msg = (
        f"🚨 *Aviso de Fim de Escala!*\n\n"
        f"pipipipi 🚨🚨🚨🚨🚨 desça com o lixo maior, *{responsavel}*!"
    )
    enviar_mensagem(msg)