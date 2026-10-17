from datetime import datetime, timedelta
import requests
import streamlit as st
#teste

# --- CONFIGURAÇÃO DO TELEGRAM ---
TELEGRAM_BOT_TOKEN = "8829625966:AAGkEGAlPbgWzLozilGVyK8N6dpZSZryjGU"
TELEGRAM_CHAT_ID = "-5515758898"


def enviar_notificacao_telegram(mensagem):
    """Envia uma mensagem de texto usando a API do Telegram."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mensagem,
        "parse_mode": "Markdown",
    }

    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return True
        else:
            st.error(f"Erro ao enviar Telegram: {response.text}")
            return False
    except Exception as e:
        st.error(f"Erro de conexão com o Telegram: {e}")
        return False


# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Escala de Limpeza", page_icon="🧹", layout="centered"
)

st.title("🧹 Escala de Limpeza da Casa")

# Configuração da Escala Fixa (de quarta a terça-feira)
DATA_INICIO_ESCALA = datetime(2026, 10, 21)  # Quarta-feira, 21/10/2026
PESSOAS_ESCALA = ["Malu", "Angélica", "Luísa"]

data_hoje = datetime.now()

# Cálculo de semanas decorridas a partir da data inicial
dias_decorridos = (data_hoje - DATA_INICIO_ESCALA).days
if dias_decorridos < 0:
    semana_atual_idx = 0
else:
    semana_atual_idx = dias_decorridos // 7

# Responsável da semana atual
responsavel_atual = PESSOAS_ESCALA[semana_atual_idx % len(PESSOAS_ESCALA)]

# Datas de início (quarta) e fim (terça) da semana atual
inicio_semana_atual = DATA_INICIO_ESCALA + timedelta(
    days=semana_atual_idx * 7
)
fim_semana_atual = inicio_semana_atual + timedelta(days=6)

# Estado de Sessão para o Checklist Fixo
if "checklist" not in st.session_state:
    st.session_state["checklist"] = [
        {"nome": "Limpeza geral casa", "feita": False},
        {"nome": "Limpeza banheiro", "feita": False},
        {"nome": "Descer lixo maior", "feita": False},
    ]

# --- ABAS DA APLICAÇÃO ---
aba_hoje, aba_escala_semana, aba_checklist = st.tabs(
    ["🌟 Responsável Atual", "📅 Escala Semanal (Fixa)", "✅ Checklist"]
)

# --- ABA 1: RESPONSÁVEL ATUAL & ALERTAS ESPECÍFICOS ---
with aba_hoje:
    st.markdown(
        f"### Período Atual: **{inicio_semana_atual.strftime('%d/%m')} a {fim_semana_atual.strftime('%d/%m/%Y')}**"
    )
    st.success(
        f"### 🧹 Responsável de quarta a terça-feira: **{responsavel_atual}**"
    )

    st.markdown("---")
    st.subheader("🔔 Disparar Alertas Específicos no Telegram")

    dia_semana_atual = data_hoje.weekday()  # 0=Seg, 1=Ter, 3=Qui, 5=Sáb...

    col1, col2 = st.columns(2)

    with col1:
        # Alerta 1: Quintas (3), Sábados (5) e Segundas (0)
        eh_dia_lixo_geral = dia_semana_atual in [0, 3, 5]
        if eh_dia_lixo_geral:
            st.info("💡 Hoje é dia de retirar os lixos (Alerta 1 recomendado).")

        if st.button("🗑️ Enviar Alerta de Lixos"):
            msg_lixo = (
                f"🗑️ *Lembrete de Lixo!*\n\n"
                f"Atente-se para os lixos do banheiro e cozinha, *{responsavel_atual}*!"
            )
            if enviar_notificacao_telegram(msg_lixo):
                st.success("Alerta de lixos enviado no Telegram!")

    with col2:
        # Alerta 2: Terças-feiras (1)
        eh_terca = dia_semana_atual == 1
        if eh_terca:
            st.warning("⚠️ Hoje é terça-feira (Alerta 2 recomendado).")

        if st.button("🚨 Enviar Alerta de Terça"):
            msg_terca = (
                f"🚨 *Aviso de Fim de Escala!*\n\n"
                f"pipipip desça com o lixo maior, *{responsavel_atual}*!"
            )
            if enviar_notificacao_telegram(msg_terca):
                st.success("Alerta de terça enviado no Telegram!")

    # Verificação automática de pendências na terça-feira
    pendentes = [
        t["nome"] for t in st.session_state["checklist"] if not t["feita"]
    ]
    if eh_terca and pendentes:
        st.markdown("---")
        st.warning(
            "⚠️ **Atenção!** Hoje é terça-feira e ainda existem tarefas pendentes no checklist!"
        )
        if st.button("📲 Enviar Alerta Geral de Pendências"):
            lista_pendentes = "\n".join([f"• {p}" for p in pendentes])
            msg_alerta = (
                f"🚨 *Alerta de Fim de Escala (Terça-feira)!*\n\n"
                f"Atenção *{responsavel_atual}*, hoje é o último dia da sua escala e ainda há pendências:\n\n"
                f"{lista_pendentes}"
            )
            if enviar_notificacao_telegram(msg_alerta):
                st.info("Alerta de pendências enviado!")

# --- ABA 2: ESCALA SEMANAL FIXA ---
with aba_escala_semana:
    st.subheader("📅 Tabela de Escala (Quarta a Terça-feira)")

    tabela_escala = []
    for i in range(12):  # Mostra 12 semanas
        inicio_periodo = DATA_INICIO_ESCALA + timedelta(days=i * 7)
        fim_periodo = inicio_periodo + timedelta(days=6)
        resp = PESSOAS_ESCALA[i % len(PESSOAS_ESCALA)]

        destaque = " (Atual)" if i == semana_atual_idx else ""

        tabela_escala.append(
            {
                "Semana": f"{i + 1}{destaque}",
                "Período": f"{inicio_periodo.strftime('%d/%m')} a {fim_periodo.strftime('%d/%m')}",
                "Responsável": resp,
            }
        )

    st.table(tabela_escala)

# --- ABA 3: CHECKLIST FIXO ---
with aba_checklist:
    st.subheader("✅ Checklist de Limpeza Semanal")
    st.write(
        "Marque abaixo as tarefas conforme forem concluídas durante a semana:"
    )

    st.markdown("---")

    todos_cumpridos_antes = (
        all(item["feita"] for item in st.session_state["checklist"])
        if st.session_state["checklist"]
        else False
    )

    for idx, item in enumerate(st.session_state["checklist"]):
        estado_anterior = item["feita"]

        status = st.checkbox(
            item["nome"], value=item["feita"], key=f"chk_{idx}"
        )

        # Se a tarefa foi marcada como concluída neste momento
        if status and not estado_anterior:
            st.session_state["checklist"][idx]["feita"] = True
            data_hora_conclusao = datetime.now().strftime("%d/%m/%Y às %H:%M")

            todos_cumpridos_agora = all(
                t["feita"] for t in st.session_state["checklist"]
            )

            if todos_cumpridos_agora and not todos_cumpridos_antes:
                # Alerta festivo com fogos de artifício no Telegram
                msg_telegram = (
                    f"🎉 🎆 *TODOS OS CHECKLISTS CUMPRIDOS!* 🎆 🎉\n\n"
                    f"🧹 Parabéns *{responsavel_atual}*!\n"
                    f"Todas as tarefas da escala da semana foram concluídas com sucesso!\n"
                    f"🗓️ *Data de conclusão:* {data_hora_conclusao}\n\n"
                    f"✨ Casa limpa e organizada! 👏✨"
                )
            else:
                # Notificação individual de item concluído
                msg_telegram = (
                    f"✅ *Checklist Concluído!*\n\n"
                    f"• *Item:* {item['nome']}\n"
                    f"• *Responsável da semana:* {responsavel_atual}\n"
                    f"• *Data de conclusão:* {data_hora_conclusao}"
                )

            enviar_notificacao_telegram(msg_telegram)
            st.toast("Notificação enviada no Telegram!")
            st.rerun()

        elif not status and estado_anterior:
            st.session_state["checklist"][idx]["feita"] = False
            st.rerun()

    st.markdown("---")
    if st.button("🔄 Reiniciar Checklist para a Nova Semana"):
        for item in st.session_state["checklist"]:
            item["feita"] = False
        st.success("Checklist resetado para a próxima semana!")
        st.rerun()