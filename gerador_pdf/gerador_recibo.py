from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer

def gerar_pdf_orcamento(dados_receita, dados_tarefas, nome_arquivo):
    filename = nome_arquivo
    # Margens definidas
    margem_esq = 30
    margem_dir = 30
    doc = SimpleDocTemplate(filename, pagesize=A4, rightMargin=margem_dir, leftMargin=margem_esq, topMargin=30, bottomMargin=30)
    story = []
    
    # Largura útil da página para cálculos de tabela
    largura_util = A4[0] - margem_esq - margem_dir
    
    styles = getSampleStyleSheet()
    
    # --- Estilos Personalizados ---
    # Título principal (texto laranja)
    style_efraim = ParagraphStyle(name='Titulo', parent=styles['Title'], fontSize=18, alignment=TA_CENTER, spaceAfter=6, textColor=colors.orange)
    
    # Subtítulos
    style_subtitulo = ParagraphStyle(name='Subtitulo', parent=styles['Normal'], fontSize=10, alignment=TA_CENTER, leading=12, textColor=colors.black)
    
    style_destaque = ParagraphStyle(name='Destaque', parent=styles['Heading2'], fontSize=14, alignment=TA_CENTER, spaceBefore=15, spaceAfter=10)

    style_normal = ParagraphStyle(name='Normal', parent=styles['Normal'], fontSize=10, leading=12)
    style_negrito = ParagraphStyle(name='Negrito', parent=styles['Normal'], fontSize=10, leading=12, fontName='Helvetica-Bold')

    # --- CABEÇALHO ---
    # Criamos os parágrafos
    p_efraim = Paragraph("<b>EFRAIM RETÍFICA DE MOTORES</b>", style_efraim)
    
    # Agrupamos os parágrafos do subtítulo
    p_localizacao = Paragraph("Av. Dom Almeida Lustosa, 1583 - Parque Albano - Caucaia - Ceará", style_subtitulo)
    p_servicos = Paragraph("Venda - Troca - Recuperação de Cabeçotes e Motores - Nacionais ou Importados", style_subtitulo)
    p_contato = Paragraph("<b>CNPJ: 21.550.087/0001-40 | Contato: (85) 9.8593-2248</b>", style_subtitulo)
    
    # Lista de flowables para a célula inferior (endereço/contato)
    bloco_subtitulo = [p_localizacao, p_servicos, p_contato]

    # --- Linha Orçamento e Data ---
    # Parágrafos
    p_orcamento = Paragraph("ORÇAMENTO", style_destaque)
    p_data = Paragraph(f"Data: {dados_receita.get('data', '')}", style_destaque)

    # Tabela Aninhada para alinhamento horizontal perfeito:
    # [ Espaço Vazio | Orçamento (Centro) | Data (Direita) ]
    # Usamos larguras iguais nas laterais para garantir que o "Orçamento" fique exatamente no centro da página
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

    # --- Dados do Cliente ---
    # Largura dividida por 2 para as duas colunas
    p_cliente = Paragraph(f"<b>Cliente:</b> {dados_receita.get('cliente', '')}", style_normal)
    p_oficina = Paragraph(f"<b>Oficina:</b> {dados_receita.get('oficina', '')}", style_normal)
    p_motor = Paragraph(f"<b>Motor/Cabeçote:</b> {dados_receita.get('motor_cabecote', '')}", style_normal)
    p_placa = Paragraph(f"<b>Placa:</b> {dados_receita.get('placa', '')}", style_normal)

    largura_coluna = largura_util / 2
    t_dados_cliente = Table(
        [
            [p_cliente, p_oficina],
            [p_motor, p_placa]
        ], colWidths = [largura_coluna, largura_coluna]
    )

    t_dados_cliente.setStyle(TableStyle([
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))

    # Estrutura da tabela principal: Linha 1 = Título, Linha 2 = Subtítulos, Linha 3 = Tabela Aninhada (Orcamento/Data)
    dados_cabecalho = [
        [p_efraim],
        [bloco_subtitulo],
        [t_linha_orcamento],
        [t_dados_cliente]
    ]

    # Criamos a tabela ocupando toda a largura útil
    tabela = Table(dados_cabecalho, colWidths=[largura_util])

    # Estilizamos a tabela para ter fundo branco e borda
    tabela.setStyle(TableStyle([
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

    story.append(tabela)
    # -----------------------------------

    story.append(Spacer(1, 10))

    # --- Tabela de Itens ---
    cabecalho = ["QTD", "TAREFA", "VALORES (R$)", "OBSERVAÇÕES"]
    
    dados_itens = []
    total_geral = 0.0

    for item in dados_tarefas:
        qtd = str(item.get('quantidade', ''))
        tarefa = item.get('descricao', '')
        valor_raw = item.get('valor', 0)
        obs = item.get('observacao', '')
        
        try:
            valor_float = float(valor_raw)
        except (ValueError, TypeError):
            valor_float = 0.0
            
        # Calcula total
        total_geral += valor_float

        valor_formatado = f"{valor_float:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        dados_itens.append([qtd, tarefa, valor_formatado, obs])

    if not dados_itens:
        dados_itens.append(["", "", "0,00", ""])

    tabela_dados = [cabecalho] + dados_itens

    # Ajuste fino das colunas
    col_qtd = 35
    col_valor = 80
    col_obs = 140
    col_desc = largura_util - col_qtd - col_valor - col_obs # Calcula o resto para a descrição
    
    tabela = Table(tabela_dados, colWidths=[col_qtd, col_desc, col_valor, col_obs])

    estilo_tabela = TableStyle([
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
    
    for i, row in enumerate(dados_itens):
        try:
            val_str = row[2].replace('.', '').replace(',', '.')
            val = float(val_str)
            if val > 0:
                estilo_tabela.add('FONTNAME', (0, i+1), (-1, i+1), 'Helvetica-Bold')
        except:
            pass

    tabela.setStyle(estilo_tabela)
    story.append(tabela)

    story.append(Spacer(1, 10))

    # --- Total Geral ---
    total_formatado = f"R$ {total_geral:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    dados_total = [
        ["TOTAL GERAL:", total_formatado]
    ]
    # Alinha a tabela de total à direita usando a largura útil
    largura_total_val = 100
    largura_total_desc = largura_util - largura_total_val
    
    tabela_total = Table(dados_total, colWidths=[largura_total_desc, largura_total_val])
    tabela_total.setStyle(TableStyle([
        ('ALIGN', (0,0), (0,0), 'RIGHT'),
        ('ALIGN', (1,0), (1,0), 'RIGHT'),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 12),
        ('topPadding', (0,0), (-1,-1), 5),
        ('BOX', (0,0), (-1,-1), 1, colors.black),
        ('BACKGROUND', (0,0), (-1,-1), colors.whitesmoke)
    ]))
    story.append(tabela_total)

    story.append(Spacer(1, 20))

    # --- Rodapé ---
    texto_garantia = "* Garantia do serviço válida por 90 dias corridos."
    story.append(Paragraph(texto_garantia, ParagraphStyle(name='Garantia', parent=styles['Normal'], fontSize=9, fontName='Helvetica-Oblique')))

    doc.build(story)
    print(f"PDF '{filename}' gerado com sucesso!")
