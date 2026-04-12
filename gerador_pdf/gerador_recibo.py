from typing import List, Dict, Any

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer

from database.receita_tarefa import get_valor_total_from_receita, get_tarefas_from_receita
from database.receitas import get_receita_by_id

def format_currency(value: float) -> str:
    """Formata um valor float para o padrão monetário brasileiro (R$ X.XXX,XX)."""
    return f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def get_custom_styles():
    """Retorna um dicionário com os estilos personalizados para o relatório."""
    styles = getSampleStyleSheet()
    return {
        'titulo': ParagraphStyle(name='Titulo', parent=styles['Title'], fontSize=18, alignment=TA_CENTER, spaceAfter=6, textColor=colors.orange),
        'subtitulo': ParagraphStyle(name='Subtitulo', parent=styles['Normal'], fontSize=10, alignment=TA_CENTER, leading=12, textColor=colors.black),
        'destaque': ParagraphStyle(name='Destaque', parent=styles['Heading2'], fontSize=14, alignment=TA_CENTER, spaceBefore=15, spaceAfter=10),
        'normal': ParagraphStyle(name='Normal', parent=styles['Normal'], fontSize=10, leading=12),
        'garantia': ParagraphStyle(name='Garantia', parent=styles['Normal'], fontSize=9, fontName='Helvetica-Oblique')
    }

def gerar_pdf_orcamento(receita_id: int, nome_arquivo: str):
    """Gera o PDF do orçamento buscando os dados no banco de dados pelo ID da receita."""
    
    # Busca dados da receita no banco
    receita_tuple = get_receita_by_id(receita_id)
    if not receita_tuple:
        print(f"Erro: Receita ID {receita_id} não encontrada.")
        return

    # Mapeia tupla para dicionário (id, cliente, oficina, motor_cabecote, placa, data)
    dados_receita = {
        'cliente': receita_tuple[1],
        'oficina': receita_tuple[2],
        'motor_cabecote': receita_tuple[3],
        'placa': receita_tuple[4],
        'data': receita_tuple[5]
    }

    # Busca tarefas da receita no banco
    tarefas_tuples = get_tarefas_from_receita(receita_id)
    # Mapeia tuplas para lista de dicionários (id, nome, quantidade, valor, observacoes)
    dados_tarefas = []
    for t in tarefas_tuples:
        dados_tarefas.append({
            'descricao': t[1],
            'quantidade': t[2],
            'valor': t[3],
            'observacao': t[4]
        })

    # Configuração do Documento
    margem_esq = 30
    margem_dir = 30
    doc = SimpleDocTemplate(nome_arquivo, pagesize=A4, rightMargin=margem_dir, leftMargin=margem_esq, topMargin=30, bottomMargin=30)
    story = []
    largura_util = A4[0] - margem_esq - margem_dir
    
    estilos = get_custom_styles()

    # --- CABEÇALHO ---
    p_efraim = Paragraph("<b>EFRAIM RETÍFICA DE MOTORES</b>", estilos['titulo'])
    
    bloco_subtitulo = [
        Paragraph("Av. Dom Almeida Lustosa, 1583 - Parque Albano - Caucaia - Ceará", estilos['subtitulo']),
        Paragraph("Venda - Troca - Recuperação de Cabeçotes e Motores - Nacionais ou Importados", estilos['subtitulo']),
        Paragraph("<b>CNPJ: 21.550.087/0001-40 | Contato: (85) 9.8593-2248</b>", estilos['subtitulo'])
    ]

    # --- ORÇAMENTO E DATA ---
    p_orcamento = Paragraph("ORÇAMENTO", estilos['destaque'])
    p_data = Paragraph(f"Data: {dados_receita.get('data', '')}", estilos['destaque'])

    largura_lateral = 130
    largura_centro = largura_util - (2 * largura_lateral)
    
    t_linha_orcamento = Table(
        [[None, p_orcamento, p_data]], 
        colWidths=[largura_lateral, largura_centro, largura_lateral]
    )
    t_linha_orcamento.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))

    # --- DADOS DO CLIENTE ---
    p_cliente = Paragraph(f"<b>Cliente:</b> {dados_receita.get('cliente', '')}", estilos['normal'])
    p_oficina = Paragraph(f"<b>Oficina:</b> {dados_receita.get('oficina', '')}", estilos['normal'])
    p_motor = Paragraph(f"<b>Motor/Cabeçote:</b> {dados_receita.get('motor_cabecote', '')}", estilos['normal'])
    p_placa = Paragraph(f"<b>Placa:</b> {dados_receita.get('placa', '')}", estilos['normal'])

    largura_coluna = largura_util / 2
    t_dados_cliente = Table(
        [
            [p_cliente, p_oficina],
            [p_motor, p_placa]
        ], colWidths=[largura_coluna, largura_coluna]
    )
    t_dados_cliente.setStyle(TableStyle([
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))

    # Estrutura da tabela principal (Cabeçalho completo)
    dados_cabecalho = [
        [p_efraim],
        [bloco_subtitulo],
        [t_linha_orcamento],
        [t_dados_cliente]
    ]

    tabela_cabecalho = Table(dados_cabecalho, colWidths=[largura_util])
    tabela_cabecalho.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 1), colors.white),   
        ('BACKGROUND', (0, 2), (-1, 2), colors.bisque),   
        ('BOX', (0, 0), (-1, -1), 1, colors.black),       
        ('INNERGRID', (0, 0), (-1, -1), 1.0, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),            
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),           
        ('TOPPADDING', (0, 0), (-1, -1), 5),              
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))

    story.append(tabela_cabecalho)
    story.append(Spacer(1, 10))

    # --- TABELA DE ITENS ---
    cabecalho_itens = ["QTD", "TAREFA", "VALORES (R$)", "OBSERVAÇÕES"]
    dados_itens_tabela = [cabecalho_itens]
    
    # Cálculo do Total
    total_geral = get_valor_total_from_receita(receita_id)

    for item in dados_tarefas:
        qtd = str(item.get('quantidade', ''))
        tarefa = item.get('descricao', '')
        valor_raw = item.get('valor', 0)
        obs = item.get('observacao', '')
        
        try:
            valor_float = float(valor_raw)
        except (ValueError, TypeError):
            valor_float = 0.0
            
        dados_itens_tabela.append([qtd, tarefa, format_currency(valor_float), obs])

    if len(dados_itens_tabela) == 1:
        dados_itens_tabela.append(["", "", "0,00", ""])

    # Colunas
    col_qtd = 35
    col_valor = 80
    col_obs = 140
    col_desc = largura_util - col_qtd - col_valor - col_obs
    
    tabela_itens = Table(dados_itens_tabela, colWidths=[col_qtd, col_desc, col_valor, col_obs])

    estilo_tabela_itens = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ])
    
    # Negrito para itens com valor ou quantidade
    for i, row in enumerate(dados_itens_tabela[1:], start=1):
        qtd = row[0]
        try:
            val_str = row[2].replace('.', '').replace(',', '.')
            val = float(val_str)
            if val > 0 or (qtd and qtd != "0"):
                estilo_tabela_itens.add('FONTNAME', (0, i), (-1, i), 'Helvetica-Bold')
        except:
            pass

    tabela_itens.setStyle(estilo_tabela_itens)
    story.append(tabela_itens)
    story.append(Spacer(1, 10))

    # --- TOTAL GERAL ---
    dados_total = [["TOTAL GERAL:", f"R$ {format_currency(total_geral)}"]]
    largura_total_val = 100
    largura_total_desc = largura_util - largura_total_val
    
    tabela_total = Table(dados_total, colWidths=[largura_total_desc, largura_total_val])
    tabela_total.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'RIGHT'),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 12),
        ('BOX', (0,0), (-1,-1), 1, colors.black),
        ('BACKGROUND', (0,0), (-1,-1), colors.whitesmoke),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(tabela_total)
    story.append(Spacer(1, 20))

    # --- RODAPÉ ---
    story.append(Paragraph("* Garantia do serviço válida por 90 dias corridos.", estilos['garantia']))

    try:
        doc.build(story)
        print(f"PDF '{nome_arquivo}' gerado com sucesso!")
    except Exception as e:
        print(f"Erro ao gerar PDF: {e}")
