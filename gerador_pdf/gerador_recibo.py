from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def create_pdf(receita, tarefas, output_file="recibo.pdf"):
    """
    Gera um PDF de recibo com base nos dados da receita e tarefas fornecidos usando ReportLab.
    
    Args:
        receita (dict): Dicionário contendo dados da receita (cliente, data, oficina, etc).
        tarefas (list): Lista de dicionários, cada um representando uma tarefa (descricao, quantidade, valor).
        output_file (str): Caminho para salvar o arquivo PDF gerado.
    """
    
    doc = SimpleDocTemplate(output_file, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    
    # Estilos personalizados
    title_style = styles['Heading1']
    title_style.alignment = 1 # Center
    
    normal_style = styles['Normal']
    
    # Cabeçalho
    elements.append(Paragraph("Recibo de Serviços", title_style))
    elements.append(Spacer(1, 20))
    
    # Informações da Receita
    info_data = [
        [f"Data: {receita.get('data', '')}"],
        [f"Cliente: {receita.get('cliente', '')}"],
        [f"Oficina: {receita.get('oficina', '')}"],
        [f"Motor/Cabeçote: {receita.get('motor_cabecote', '')}"],
        [f"Placa: {receita.get('placa', '')}"]
    ]
    
    # Adiciona informações como parágrafos para melhor formatação
    for info in info_data:
        elements.append(Paragraph(f"<b>{info[0].split(':')[0]}:</b> {info[0].split(':')[1]}", normal_style))
        elements.append(Spacer(1, 5))
        
    elements.append(Spacer(1, 20))
    elements.append(Paragraph("Detalhes dos serviços prestados:", styles['Heading3']))
    elements.append(Spacer(1, 10))
    
    # Tabela de Tarefas
    table_data = [['Descrição', 'Qtd', 'Valor Unit.', 'Total']]
    
    total_geral = 0
    for t in tarefas:
        total_item = t['quantidade'] * t['valor']
        total_geral += total_item
        
        valor_unit_fmt = f"R$ {t['valor']:.2f}".replace('.', ',')
        total_item_fmt = f"R$ {total_item:.2f}".replace('.', ',')
        
        table_data.append([
            t['descricao'],
            str(t['quantidade']),
            valor_unit_fmt,
            total_item_fmt
        ])
    
    # Estilo da Tabela
    table = Table(table_data, colWidths=[250, 50, 80, 80])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'), # Quantidade e Valores centralizados/direita
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    elements.append(table)
    elements.append(Spacer(1, 20))
    
    # Total Geral
    total_geral_fmt = f"R$ {total_geral:.2f}".replace('.', ',')
    elements.append(Paragraph(f"<b>Total a Pagar: {total_geral_fmt}</b>", styles['Heading2']))
    
    # Gerar PDF
    doc.build(elements)
    print(f"PDF gerado com sucesso: {output_file}")

if __name__ == "__main__":
    # Dados de exemplo para teste
    receita_exemplo = {
        "cliente": "João Silva",
        "data": "25/12/2025",
        "oficina": "Oficina do Pedro",
        "motor_cabecote": "AP 1.8",
        "placa": "ABC-1234"
    }
    
    tarefas_exemplo = [
        {"descricao": "Troca de Óleo", "quantidade": 1, "valor": 150.00},
        {"descricao": "Alinhamento", "quantidade": 1, "valor": 80.00},
        {"descricao": "Balanceamento", "quantidade": 4, "valor": 20.00}
    ]
    
    create_pdf(receita_exemplo, tarefas_exemplo, "exemplo_recibo_reportlab.pdf")
