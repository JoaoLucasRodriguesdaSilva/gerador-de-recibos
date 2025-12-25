from weasyprint import HTML

def create_pdf(receita, tarefas, output_file="recibo.pdf"):
    """
    Gera um PDF de recibo com base nos dados da receita e tarefas fornecidos.
    
    Args:
        receita (dict): Dicionário contendo dados da receita (cliente, data, oficina, etc).
        tarefas (list): Lista de dicionários, cada um representando uma tarefa (descricao, quantidade, valor).
        output_file (str): Caminho para salvar o arquivo PDF gerado.
    """
    
    # Calcular total geral
    total_geral = sum(t['quantidade'] * t['valor'] for t in tarefas)
    
    # Gerar linhas da tabela
    rows_html = ""
    for t in tarefas:
        total_item = t['quantidade'] * t['valor']
        # Formatar valores monetários para o padrão brasileiro (simples)
        valor_unitario_fmt = f"R$ {t['valor']:.2f}".replace('.', ',')
        total_item_fmt = f"R$ {total_item:.2f}".replace('.', ',')
        
        rows_html += f"""
            <tr>
                <td>{t['descricao']}</td>
                <td>{t['quantidade']}</td>
                <td>{valor_unitario_fmt}</td>
                <td>{total_item_fmt}</td>
            </tr>
        """

    # Formatar total geral
    total_geral_fmt = f"R$ {total_geral:.2f}".replace('.', ',')

    html_content = f"""
    <html>
        <head>
            <style>
                body {{ font-family: sans-serif; }}
                h1 {{ color: #333; }}
                .header {{ margin-bottom: 20px; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                .total {{ margin-top: 20px; text-align: right; font-weight: bold; font-size: 1.2em; }}
                .info p {{ margin: 5px 0; }}
                .info {{ margin-bottom: 20px; border-bottom: 1px solid #eee; padding-bottom: 10px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Recibo de Serviços</h1>
                <div class="info">
                    <p><strong>Data:</strong> {receita.get('data', '')}</p>
                    <p><strong>Cliente:</strong> {receita.get('cliente', '')}</p>
                    <p><strong>Oficina:</strong> {receita.get('oficina', '')}</p>
                    <p><strong>Motor/Cabeçote:</strong> {receita.get('motor_cabecote', '')}</p>
                    <p><strong>Placa:</strong> {receita.get('placa', '')}</p>
                </div>
            </div>
            
            <p>Detalhes dos serviços prestados:</p>
            
            <table>
                <thead>
                    <tr>
                        <th>Descrição</th>
                        <th>Quantidade</th>
                        <th>Valor Unitário</th>
                        <th>Total</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                </tbody>
            </table>
            
            <div class="total">
                <p>Total a Pagar: {total_geral_fmt}</p>
            </div>
        </body>
    </html>
    """
    
    HTML(string=html_content).write_pdf(output_file)
    print(f"PDF gerado com sucesso: {output_file}")
