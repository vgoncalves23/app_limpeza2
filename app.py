from datetime import datetime, timedelta
import json
import os
import requests
import streamlit as st

# --- CONFIGURAÇÃO DO TELEGRAM ---
TELEGRAM_BOT_TOKEN = "8829625966:AAGkEGAlPbgWzLozilGVyK8N6dpZSZryjGU"
TELEGRAM_CHAT_ID = "-5578794876"
ARQUIVO_DADOS = "dados_escala.json"


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
        return response.status_code == 200
    except Exception as e:
        return False


def carregar_dados():
    """Carrega as informações salvas do arquivo JSON."""
    if os.path.exists(ARQUIVO_DADOS):
        try:
            with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

#teste

def salvar_dados(dados):
    """Salva as informações no arquivo JSON."""
    try:
        with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)
    except Exception as e:
        st.error(f"Erro ao salvar dados: {e}")


# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Faxinômetro", page_icon="🧹", layout="centered"
)

# Exibindo a imagem centralizada no topo do app
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    try:
        st.image("logo.jpg", width=350)
    except Exception:
        st.title("🧹 Faxinômetro")

st.markdown("<hr>", unsafe_allow_html=True)

# Configuração da Escala Fixa (de quarta a terça-feira)
DATA_INICIO_ESCALA = datetime(2026, 10, 21)  # Quarta-feira, 21/10/2026
PESSOAS_ESCALA = ["Malu", "Angélica", "Luísa"]

data_hoje = datetime.now()

# Cálculo de semanas decorridas
dias_decorridos = (data_hoje - DATA_INICIO_ESCALA).days
if dias_decorridos < 0:
    semana_atual_idx = 0
else:
    semana_atual_idx = dias_decorridos // 7

responsavel_padrao = PESSOAS_ESCALA[semana_atual_idx % len(PESSOAS_ESCALA)]

inicio_semana_atual = DATA_INICIO_ESCALA + timedelta(
    days=semana_atual_idx * 7
)
fim_semana_atual = inicio_semana_atual + timedelta(days=6)
chave_semana = inicio_semana_atual.strftime("%Y-%m-%d")

# Carrega os dados persistidos
dados_salvos = carregar_dados()

# Verifica se há uma troca manual gravada para a semana atual
tem_troca_manual = (
    "trocas_semana" in dados_salvos
    and chave_semana in dados_salvos["trocas_semana"]
)

responsavel_atual = dados_salvos.get("trocas_semana", {}).get(
    chave_semana, responsavel_padrao
)

# Checklist persistido
if "checklist_dados" not in dados_salvos:
    dados_salvos["checklist_dados"] = [
        {"nome": "Limpeza geral casa (Cozinha: Fogão, Microondas, Beirada Janelas, Parede de Fogão, Chão, Bancadas)", "feita": False},
        {"nome": "Limpeza banheiro (Pia, Vaso, Box, Chão)", "feita": False},
        {"nome": "Descer lixo maior", "feita": False},
    ]

checklist = dados_salvos["checklist_dados"]

# --- ABAS DA APLICAÇÃO ---
aba_hoje, aba_escala_semana, aba_checklist = st.tabs(
    ["🌟 Responsável Atual", "📅 Escala Semanal (Fixa)", "✅ Checklist"]
)

# --- ABA 1: RESPONSÁVEL ATUAL ---
with aba_hoje:
    st.markdown(
        f"### Período Atual: **{inicio_semana_atual.strftime('%d/%m')} a {fim_semana_atual.strftime('%d/%m/%Y')}**"
    )

    if tem_troca_manual:
        st.success(
            f"### 🧹 Responsável nesta semana: **{responsavel_atual}** *(Troca Manual)*"
        )
    else:
        st.success(
            f"### 🧹 Responsável nesta semana: **{responsavel_atual}** *(Padrão da Escala)*"
        )

    st.markdown("---")

    # --- SEÇÃO DE TROCA DE RESPONSÁVEL ---
    with st.expander("🔄 Precisa trocar de pessoa esta semana?"):
        nova_pessoa = st.selectbox(
            "Selecionar novo responsável:",
            options=PESSOAS_ESCALA,
            index=PESSOAS_ESCALA.index(responsavel_atual),
            key="sel_novo_resp",
        )

        if nova_pessoa != responsavel_atual:
            if st.button("Aplicar Troca e Notificar Telegram"):
                antigo_resp = responsavel_atual

                # Atualiza e salva no arquivo JSON
                if "trocas_semana" not in dados_salvos:
                    dados_salvos["trocas_semana"] = {}
                dados_salvos["trocas_semana"][chave_semana] = nova_pessoa
                salvar_dados(dados_salvos)

                # Envio automático da notificação para o Telegram
                msg_troca = (
                    f"🔄 *Troca Automática na Escala de Limpeza!*\n\n"
                    f"• *Anterior:* {antigo_resp}\n"
                    f"• *Novo Responsável:* *{nova_pessoa}*\n"
                    f"• *Período:* {inicio_semana_atual.strftime('%d/%m')} a {fim_semana_atual.strftime('%d/%m')}\n\n"
                    f"✨ A escala foi atualizada no Faxinômetro!"
                )
                enviar_notificacao_telegram(msg_troca)

                st.success(
                    f"Responsável alterado para **{nova_pessoa}** e salvo com sucesso!"
                )
                st.rerun()
        else:
            st.info("A pessoa selecionada já é a responsável atual da semana.")

        # Botão para Restaurar a Escala Padrão se houver uma troca manual ativa
        if tem_troca_manual:
            st.markdown("---")
            if st.button("↩️ Voltar ao Padrão da Escala Semanal"):
                antigo_resp = responsavel_atual
                del dados_salvos["trocas_semana"][chave_semana]
                salvar_dados(dados_salvos)

                msg_restaurar = (
                    f"↩️ *Escala Restaurada para o Padrão!*\n\n"
                    f"• *Responsável Padrão:* *{responsavel_padrao}*\n"
                    f"• *Período:* {inicio_semana_atual.strftime('%d/%m')} a {fim_semana_atual.strftime('%d/%m')}\n\n"
                    f"✨ A escala voltou à programação normal no Faxinômetro!"
                )
                enviar_notificacao_telegram(msg_restaurar)

                st.success(
                    f"Escala restaurada para o responsável padrão (**{responsavel_padrao}**)!"
                )
                st.rerun()

    st.markdown("---")
    st.info(
        "🤖 **Alertas Automáticos:** Os lembretes de lixo e término de escala são enviados diretamente no grupo do Telegram todos os dias às 14:00."
    )

# --- ABA 2: ESCALA SEMANAL FIXA ---
with aba_escala_semana:
    st.subheader("📅 Tabela de Escala (Quarta a Terça-feira)")

    tabela_escala = []
    for i in range(12):
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
        f"Marque abaixo as tarefas conforme forem concluídas por **{responsavel_atual}**:"
    )

    st.markdown("---")

    todos_cumpridos_antes = (
        all(item["feita"] for item in checklist) if checklist else False
    )

    for idx, item in enumerate(checklist):
        estado_anterior = item["feita"]

        status = st.checkbox(
            item["nome"], value=item["feita"], key=f"chk_{idx}"
        )

        if status and not estado_anterior:
            checklist[idx]["feita"] = True
            dados_salvos["checklist_dados"] = checklist
            salvar_dados(dados_salvos)

            data_hora_conclusao = datetime.now().strftime("%d/%m/%Y às %H:%M")

            todos_cumpridos_agora = all(t["feita"] for t in checklist)

            if todos_cumpridos_agora and not todos_cumpridos_antes:
                msg_telegram = (
                    f"🎉 🎆 *TODOS OS CHECKLISTS CUMPRIDOS!* 🎆 🎉\n\n"
                    f"🧹 Parabéns *{responsavel_atual}*!\n"
                    f"Todas as tarefas da escala da semana foram concluídas com sucesso!\n"
                    f"🗓️ *Data de conclusão:* {data_hora_conclusao}\n\n"
                    f"✨ Casa limpa e organizada! 👏✨"
                )
            else:
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
            checklist[idx]["feita"] = False
            dados_salvos["checklist_dados"] = checklist
            salvar_dados(dados_salvos)
            st.rerun()