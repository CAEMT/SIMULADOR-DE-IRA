from __future__ import annotations

import io

import pandas as pd
import streamlit as st

from ira_core import (
    FREQUENCIA_MINIMA,
    NOTA_APROVACAO,
    Componente,
    calcular_ira,
    calcular_media_necessaria,
    calcular_nota_necessaria,
    calcular_novo_ira,
    pontos_acumulados,
    situacao,
)

st.set_page_config(
    page_title="Calculadora de IRA — UNIFEI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        .block-container {max-width: 1120px; padding-top: 2.2rem; padding-bottom: 3rem;}
        [data-testid="stMetric"] {border: 1px solid rgba(128,128,128,.22); padding: 1rem; border-radius: 14px;}
        .hero {padding: 0.2rem 0 1.1rem 0;}
        .hero h1 {font-size: clamp(2rem, 5vw, 3rem); margin-bottom: .25rem;}
        .muted {opacity: .75;}
        .formula-box {border: 1px solid rgba(128,128,128,.22); border-radius: 14px; padding: 1rem 1.2rem;}
        div[data-testid="stExpander"] {border-radius: 12px;}
    </style>
    """,
    unsafe_allow_html=True,
)

COLUNAS_CSV = ["Disciplina", "Nota", "Carga horária", "Frequência"]


def fmt_num(valor: float, casas: int = 3) -> str:
    return f"{valor:.{casas}f}".replace(".", ",")


def fmt_ch(valor: float) -> str:
    if float(valor).is_integer():
        return f"{int(valor)} h"
    return f"{fmt_num(valor, 1)} h"


def iniciar_estado() -> None:
    if "historico" not in st.session_state:
        st.session_state.historico = []
    if "proximo_id" not in st.session_state:
        st.session_state.proximo_id = 1


def componentes_do_historico() -> list[Componente]:
    return [
        Componente(
            nome=item["nome"],
            nota=float(item["nota"]),
            carga_horaria=float(item["ch"]),
            frequencia=(None if item.get("frequencia") is None else float(item["frequencia"])),
        )
        for item in st.session_state.historico
    ]


def ira_e_ch_historico() -> tuple[float | None, float]:
    componentes = componentes_do_historico()
    if not componentes:
        return None, 0.0
    ira = calcular_ira(componentes)
    _, ch = pontos_acumulados(componentes)
    return ira, ch


def df_historico() -> pd.DataFrame:
    linhas = []
    for item in st.session_state.historico:
        freq = item.get("frequencia")
        linhas.append(
            {
                "ID": item["id"],
                "Disciplina": item["nome"],
                "Nota": float(item["nota"]),
                "Carga horária": float(item["ch"]),
                "Frequência": None if freq is None else float(freq),
                "Situação": situacao(float(item["nota"]), None if freq is None else float(freq)),
                "Nota × CH": float(item["nota"]) * float(item["ch"]),
            }
        )
    return pd.DataFrame(linhas)


def csv_historico() -> bytes:
    df = df_historico()
    if df.empty:
        return b""
    exportar = df[["Disciplina", "Nota", "Carga horária", "Frequência"]]
    return exportar.to_csv(index=False).encode("utf-8-sig")


def carregar_csv(arquivo) -> tuple[int, list[str]]:
    conteudo = arquivo.getvalue()
    df = pd.read_csv(io.BytesIO(conteudo))
    faltantes = [col for col in ["Disciplina", "Nota", "Carga horária"] if col not in df.columns]
    if faltantes:
        raise ValueError("O CSV precisa conter: Disciplina, Nota e Carga horária.")

    avisos: list[str] = []
    novos = []
    for i, row in df.iterrows():
        nome = str(row["Disciplina"]).strip()
        nota = float(row["Nota"])
        ch = float(row["Carga horária"])
        freq = None
        if "Frequência" in df.columns and pd.notna(row["Frequência"]):
            freq = float(row["Frequência"])

        if not nome or nome.lower() == "nan":
            avisos.append(f"Linha {i + 2}: disciplina sem nome ignorada.")
            continue
        if not 0 <= nota <= 10 or ch <= 0 or (freq is not None and not 0 <= freq <= 100):
            avisos.append(f"Linha {i + 2}: valores inválidos; linha ignorada.")
            continue

        novos.append(
            {
                "id": st.session_state.proximo_id,
                "nome": nome,
                "nota": nota,
                "ch": ch,
                "frequencia": freq,
            }
        )
        st.session_state.proximo_id += 1

    st.session_state.historico = novos
    return len(novos), avisos


def seletor_base(prefixo: str) -> tuple[float | None, float | None, bool]:
    ira_hist, ch_hist = ira_e_ch_historico()
    opcoes = ["Informar IRA atual e carga horária"]
    if ira_hist is not None:
        opcoes.insert(0, "Usar histórico cadastrado")

    modo = st.radio(
        "Base do cálculo",
        opcoes,
        horizontal=True,
        key=f"{prefixo}_modo_base",
    )

    if modo == "Usar histórico cadastrado":
        c1, c2 = st.columns(2)
        c1.metric("IRA da base", fmt_num(ira_hist))
        c2.metric("Carga horária da base", fmt_ch(ch_hist))
        return ira_hist, ch_hist, False

    c1, c2 = st.columns(2)
    with c1:
        ira = st.number_input(
            "IRA atual",
            min_value=0.0,
            max_value=10.0,
            value=7.0,
            step=0.001,
            format="%.3f",
            key=f"{prefixo}_ira_manual",
        )
    with c2:
        ch = st.number_input(
            "Carga horária já considerada no IRA",
            min_value=0.0,
            value=800.0,
            step=8.0,
            key=f"{prefixo}_ch_manual",
        )
    st.caption(
        "Neste modo, o resultado pode diferir alguns milésimos do SIGAA se o IRA informado já estiver arredondado."
    )
    return float(ira), float(ch), True


def mostrar_regra() -> None:
    with st.expander("Como o cálculo foi definido"):
        st.markdown(
            """
            <div class="formula-box">
            <b>IRA = Σ(Nota final × Carga horária) ÷ Σ(Carga horária)</b>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.write(
            "A Norma de Graduação da UNIFEI (Resolução CEPEAd nº 17/2025) define o IRA como a média "
            "ponderada do rendimento acadêmico final pela carga horária em todos os componentes concluídos, "
            "com aprovação ou reprovação."
        )
        st.write(
            f"Para a situação acadêmica mostrada no app, usamos nota mínima {NOTA_APROVACAO:.1f} e frequência "
            f"mínima {FREQUENCIA_MINIMA:.0f}%. Em componentes com partes teórica e prática, a norma exige o mínimo "
            "de frequência em cada parte; por isso, a frequência única informada aqui é apenas uma simplificação visual."
        )


iniciar_estado()

with st.sidebar:
    st.subheader("Calculadora de IRA")
    st.caption("UNIFEI · ferramenta independente")
    st.divider()
    st.write("**Privacidade**")
    st.caption(
        "O app não possui banco de dados. As informações ficam na sessão do navegador enquanto ela estiver ativa. "
        "Use o CSV para guardar seu histórico localmente."
    )
    st.write("**Importante**")
    st.caption(
        "Esta ferramenta não é vinculada, mantida ou homologada pela Universidade Federal de Itajubá. "
        "O valor oficial é o exibido nos sistemas institucionais."
    )
    st.link_button("Documentos da PRG/UNIFEI", "https://prg.unifei.edu.br/documentos/", use_container_width=True)

st.markdown(
    """
    <div class="hero">
      <h1>Calculadora de IRA — UNIFEI</h1>
      <div class="muted">Calcule seu IRA, descubra a nota necessária para uma meta e simule o semestre.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

mostrar_regra()

tab_hist, tab_meta, tab_sim = st.tabs(["Histórico e IRA", "Nota necessária", "Simular semestre"])

with tab_hist:
    st.subheader("Histórico acadêmico")
    st.caption(
        "Cadastre cada componente concluído com nota final numérica. Se você cursou a mesma disciplina mais de uma vez, "
        "mantenha cada tentativa concluída como um registro separado."
    )

    with st.form("adicionar_componente", clear_on_submit=True):
        c1, c2, c3, c4 = st.columns([2.8, 1, 1.15, 1.2])
        nome = c1.text_input("Disciplina / componente", placeholder="Ex.: Cálculo I")
        nota = c2.number_input("Nota final", 0.0, 10.0, 6.0, 0.1, format="%.1f")
        ch = c3.number_input("Carga horária", min_value=0.1, value=64.0, step=8.0)
        freq_texto = c4.text_input("Frequência (%)", placeholder="Opcional")
        enviar = st.form_submit_button("Adicionar ao histórico", use_container_width=True)

        if enviar:
            if not nome.strip():
                st.error("Informe o nome do componente.")
            else:
                try:
                    freq = None if not freq_texto.strip() else float(freq_texto.replace(",", "."))
                    if freq is not None and not 0 <= freq <= 100:
                        raise ValueError
                    st.session_state.historico.append(
                        {
                            "id": st.session_state.proximo_id,
                            "nome": nome.strip(),
                            "nota": float(nota),
                            "ch": float(ch),
                            "frequencia": freq,
                        }
                    )
                    st.session_state.proximo_id += 1
                    st.rerun()
                except ValueError:
                    st.error("Frequência inválida. Use um valor entre 0 e 100 ou deixe o campo vazio.")

    st.divider()

    if st.session_state.historico:
        ira, ch_total = ira_e_ch_historico()
        df = df_historico()

        c1, c2, c3 = st.columns(3)
        c1.metric("IRA calculado", fmt_num(ira))
        c2.metric("Carga horária considerada", fmt_ch(ch_total))
        c3.metric("Componentes concluídos", len(st.session_state.historico))

        st.dataframe(
            df.drop(columns=["ID"]).style.format(
                {
                    "Nota": "{:.2f}",
                    "Carga horária": "{:.1f}",
                    "Frequência": lambda x: "—" if pd.isna(x) else f"{x:.1f}%",
                    "Nota × CH": "{:.2f}",
                }
            ),
            use_container_width=True,
            hide_index=True,
        )

        c1, c2, c3 = st.columns([1.4, 1, 1])
        opcoes_remocao = {
            f'{item["id"]} · {item["nome"]} · nota {fmt_num(float(item["nota"]), 1)}': item["id"]
            for item in st.session_state.historico
        }
        escolha = c1.selectbox("Remover um registro", list(opcoes_remocao.keys()))
        if c2.button("Remover", use_container_width=True):
            id_remover = opcoes_remocao[escolha]
            st.session_state.historico = [x for x in st.session_state.historico if x["id"] != id_remover]
            st.rerun()
        if c3.button("Limpar histórico", use_container_width=True):
            st.session_state.historico = []
            st.rerun()

        st.download_button(
            "Baixar histórico em CSV",
            data=csv_historico(),
            file_name="historico_ira_unifei.csv",
            mime="text/csv",
            use_container_width=True,
        )
    else:
        st.info("Adicione ao menos um componente para calcular o IRA.")

    with st.expander("Importar histórico de um CSV"):
        st.caption("Colunas aceitas: Disciplina, Nota, Carga horária e, opcionalmente, Frequência.")
        arquivo = st.file_uploader("Arquivo CSV", type=["csv"], key="csv_historico")
        if arquivo is not None and st.button("Importar e substituir histórico", use_container_width=True):
            try:
                total, avisos = carregar_csv(arquivo)
                st.success(f"{total} registro(s) importado(s).")
                for aviso in avisos:
                    st.warning(aviso)
                st.rerun()
            except Exception as exc:
                st.error(f"Não foi possível importar o arquivo: {exc}")

with tab_meta:
    st.subheader("Qual nota preciso tirar?")
    st.caption("Calcule a nota final necessária em um novo componente para atingir um IRA específico.")

    ira_base, ch_base, _ = seletor_base("meta")
    if ira_base is not None and ch_base is not None:
        st.divider()
        c1, c2 = st.columns(2)
        ch_nova = c1.number_input(
            "Carga horária do componente",
            min_value=0.1,
            value=64.0,
            step=8.0,
            key="meta_ch_nova",
        )
        alvo_padrao = min(10.0, round(float(ira_base) + 0.1, 3))
        ira_alvo = c2.number_input(
            "IRA desejado",
            min_value=0.0,
            max_value=10.0,
            value=alvo_padrao,
            step=0.001,
            format="%.3f",
            key="meta_ira_alvo",
        )

        nota_necessaria = calcular_nota_necessaria(float(ira_base), float(ch_base), float(ch_nova), float(ira_alvo))
        st.write("")

        if nota_necessaria > 10:
            maximo = calcular_novo_ira(float(ira_base), float(ch_base), 10.0, float(ch_nova))
            st.error(
                f"A meta não pode ser atingida apenas com esse componente. A nota matemática necessária seria "
                f"**{fmt_num(nota_necessaria, 2)}**, e com nota 10,0 o IRA chegaria a **{fmt_num(maximo)}**."
            )
        elif nota_necessaria <= 0:
            com_zero = calcular_novo_ira(float(ira_base), float(ch_base), 0.0, float(ch_nova))
            st.success(
                f"Mesmo com nota 0,0, o IRA resultante seria **{fmt_num(com_zero)}**, suficiente para essa meta."
            )
            st.warning(
                f"Isso não significa aprovação: a nota de referência para aprovação é {NOTA_APROVACAO:.1f}, "
                "além da frequência mínima aplicável."
            )
        else:
            st.metric("Nota final necessária", fmt_num(nota_necessaria, 2))
            if nota_necessaria < NOTA_APROVACAO:
                ira_com_6 = calcular_novo_ira(float(ira_base), float(ch_base), NOTA_APROVACAO, float(ch_nova))
                st.info(
                    f"A meta de IRA exige apenas {fmt_num(nota_necessaria, 2)}, mas com nota 6,0 o IRA seria "
                    f"**{fmt_num(ira_com_6)}**."
                )

        st.divider()
        st.write("**Veja o efeito de diferentes notas**")
        notas = [x / 10 for x in range(0, 101)]
        curva = pd.DataFrame(
            {
                "Nota": notas,
                "IRA projetado": [
                    calcular_novo_ira(float(ira_base), float(ch_base), n, float(ch_nova)) for n in notas
                ],
            }
        ).set_index("Nota")
        st.line_chart(curva)

with tab_sim:
    st.subheader("Simular um semestre")
    st.caption(
        "Monte um conjunto de componentes futuros e veja o IRA projetado. As notas podem ser alteradas diretamente na tabela."
    )

    ira_base, ch_base, _ = seletor_base("semestre")
    if ira_base is not None and ch_base is not None:
        st.divider()
        padrao = pd.DataFrame(
            [
                {"Disciplina": "Disciplina 1", "Nota prevista": 7.0, "Carga horária": 64.0},
                {"Disciplina": "Disciplina 2", "Nota prevista": 7.0, "Carga horária": 64.0},
                {"Disciplina": "Disciplina 3", "Nota prevista": 7.0, "Carga horária": 32.0},
            ]
        )
        futuras = st.data_editor(
            padrao,
            num_rows="dynamic",
            use_container_width=True,
            hide_index=True,
            column_config={
                "Disciplina": st.column_config.TextColumn("Disciplina"),
                "Nota prevista": st.column_config.NumberColumn("Nota prevista", min_value=0.0, max_value=10.0, step=0.1),
                "Carga horária": st.column_config.NumberColumn("Carga horária", min_value=0.1, step=8.0),
            },
            key="editor_semestre",
        )

        validas = futuras.dropna(subset=["Nota prevista", "Carga horária"]).copy()
        validas = validas[(validas["Nota prevista"] >= 0) & (validas["Nota prevista"] <= 10) & (validas["Carga horária"] > 0)]

        if validas.empty:
            st.info("Adicione pelo menos um componente futuro válido.")
        else:
            pontos_base = float(ira_base) * float(ch_base)
            pontos_futuros = float((validas["Nota prevista"] * validas["Carga horária"]).sum())
            ch_futura = float(validas["Carga horária"].sum())
            ira_projetado = (pontos_base + pontos_futuros) / (float(ch_base) + ch_futura)
            variacao = ira_projetado - float(ira_base)

            c1, c2, c3 = st.columns(3)
            c1.metric("IRA atual", fmt_num(float(ira_base)))
            c2.metric("IRA projetado", fmt_num(ira_projetado), delta=fmt_num(variacao, 3))
            c3.metric("CH futura simulada", fmt_ch(ch_futura))

            st.divider()
            st.write("**Meta para o semestre**")
            ira_alvo_sem = st.number_input(
                "IRA que você gostaria de atingir ao final deste conjunto de componentes",
                min_value=0.0,
                max_value=10.0,
                value=min(10.0, round(float(ira_base) + 0.1, 3)),
                step=0.001,
                format="%.3f",
                key="semestre_alvo",
            )
            media_necessaria = calcular_media_necessaria(
                float(ira_base), float(ch_base), ch_futura, float(ira_alvo_sem)
            )

            if media_necessaria > 10:
                st.error(
                    f"Para atingir IRA {fmt_num(float(ira_alvo_sem))}, seria necessária média ponderada "
                    f"**{fmt_num(media_necessaria, 2)}** nesse conjunto, acima de 10,0."
                )
            elif media_necessaria <= 0:
                st.success("A meta já seria mantida mesmo com média ponderada 0,0 nesse conjunto.")
            else:
                st.info(
                    f"Para atingir IRA **{fmt_num(float(ira_alvo_sem))}**, a média ponderada necessária nas "
                    f"disciplinas simuladas é **{fmt_num(media_necessaria, 2)}**."
                )

st.divider()
st.caption(
    "Ferramenta independente e não oficial. Referência normativa: Norma de Graduação da UNIFEI, "
    "Resolução CEPEAd nº 17, de 03/12/2025. Consulte o SIGAA e os documentos institucionais para valores oficiais."
)
