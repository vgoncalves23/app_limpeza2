import os
from datetime import datetime, timedelta
import requests

# Variáveis de ambiente com fallback para os valores diretos
TELEGRAM_BOT_TOKEN = os.getenv(
    "TELEGRAM_BOT_TOKEN", "8829625966:AAGkEGAlPbgWzLozilGVyK8N6dpZSZryjGU"
)
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "-5515758898")

DATA_INICIO_ESCALA = datetime(2026, 10, 21)
# Sequência ajustada: Malu -> Luísa -> Angélica
PESSOAS_ESCALA = ["Malu", "Luísa", "Angélica"]

def enviar_foto(caminho_imagem, legenda=""):
    """Envia uma imagem acompanhada de legenda para o Telegram."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
    
    if not os.path.exists(caminho_imagem):
        print(f"❌ Imagem não encontrada no caminho: {caminho_imagem}")
        # Envia apenas a mensagem de texto caso a imagem não exista
        return enviar_mensagem(legenda)

    try:
        with open(caminho_imagem, "rb") as foto:
            payload = {
                "chat_id": TELEGRAM_CHAT_ID,
                "caption": legenda,
                "parse_mode": "Markdown",
            }
            files = {"photo": foto}
            response = requests.post(url, data=payload, files=files)
            
            if response.status_code == 200:
                print("✅ Foto e mensagem enviadas com sucesso para o Telegram!")
            else:
                print(f"❌ Erro ao enviar foto ({response.status_code}): {response.text}")
            return response.status_code == 200
    except Exception as e:
        print(f"❌ Erro ao processar envio da foto: {e}")
        return False


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
dia_semana = data_hoje.weekday()  # 0=Segunda, 1=Terça, 2=Quarta, 3=Quinta, 4=Sexta, 5=Sábado, 6=Domingo

dias_decorridos = (data_hoje - DATA_INICIO_ESCALA).days
semana_idx = 0 if dias_decorridos < 0 else dias_decorridos // 7
responsavel = PESSOAS_ESCALA[semana_idx % len(PESSOAS_ESCALA)]

# --- BLOCO DE LOGS ---
print("--- DIAGNÓSTICO DE EXECUÇÃO ---")
print(f"Data/Hora ajustada (Brasília): {data_hoje}")
print(f"Dia da semana (0=Seg, 6=Dom): {dia_semana}")
print(f"Responsável calculated: {responsavel}")
print("--------------------------------")


# --- MENSAGEM DE INÍCIO DE ESCALA NA QUARTA-FEIRA (Dia 2) ---
if dia_semana == 2:
    msg_inicio = (
        f"🔄 *Nova Escala Iniciada!*\n\n"
        f"A responsável da semana é: *{responsavel}* ✨"
    )
    enviar_mensagem(msg_inicio)


# --- BLOCOS DE ALERTAS POR RESPONSÁVEL ---
if responsavel in PESSOAS_ESCALA:
    # Lembrete de Lixo (Quinta [3], Sábado [5] e Segunda [0])
    if dia_semana in [3, 5, 0]:
        msg = (
            f"🗑️ *Lembrete de Lixo ({responsavel})!*\n\n"
            "Atente-se para os lixos do banheiro e cozinha!"
        )
        enviar_mensagem(msg)

    # Fim de Escala / Lixo maior (Terça [1])
   
    if dia_semana == 1:
        msg = (
            f"🚨 *Aviso de Fim de Escala ({responsavel})!*\n\n"
            "pipipipi 🚨🚨🚨🚨🚨 desça com o lixo maior!"
        )
        enviar_mensagem(msg)

        # Fim de Escala / Lixo maior (Terça [1])
