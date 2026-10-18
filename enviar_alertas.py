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
hora_atual = data_hoje.hour  # Pega a hora atual (0 a 23)
dia_semana = data_hoje.weekday()  # 0=Segunda, 1=Terça, ..., 6=Domingo

dias_decorridos = (data_hoje - DATA_INICIO_ESCALA).days
semana_idx = 0 if dias_decorridos < 0 else dias_decorridos // 7
responsavel = PESSOAS_ESCALA[semana_idx % len(PESSOAS_ESCALA)]

# --- REGRAS ESPECÍFICAS POR PESSOA ---

# Exemplo para a Malu (alertas às 14:00 nos dias específicos)
if responsavel == "Malu":
    # Dispara apenas se forem 14 horas da tarde e nos dias de lixo (Segunda, Quinta, Sábado)
    if hora_atual == 10 and dia_semana in [0, 3, 5]:
        msg = (
            f"🗑️ *Lembrete da Malu!*\n\n"
            f"Olá Malu, lembrete dos lixos do banheiro e cozinha às 14:00!"
        )
        enviar_mensagem(msg)

    # Alerta de fim de escala para a Malu na terça-feira às 14:00
    elif hora_atual == 14 and dia_semana == 1:
        msg = (
            f"🚨 *Fim de Escala - Malu!*\n\n"
            f"Hora de descer com o lixo maior, Malu!"
        )
        enviar_mensagem(msg)

# Exemplo para a Angélica (pode ter horários ou dias diferentes)
elif responsavel == "Angélica":
    if hora_atual == 14 and dia_semana in [0, 3, 5]:
        msg = (
            f"🗑️ *Lembrete da Angélica!*\n\n"
            f"Oi Angélica, hora de cuidar dos lixos da casa!"
        )
        enviar_mensagem(msg)

# Exemplo para a Luísa
elif responsavel == "Luísa":
    if hora_atual == 14 and dia_semana in [0, 3, 5]:
        msg = (
            f"🗑️ *Lembrete da Luísa!*\n\n"
            f"Oi Luísa, lembrete dos lixos de hoje!"
        )
        enviar_mensagem(msg)