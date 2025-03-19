
# from flask import Flask, render_template, request, redirect, url_for, session, jsonify
# import pandas as pd
# from datetime import datetime
# import json
#
# app = Flask(__name__)
# app.secret_key = 'sua_chave_secreta_aqui'
#
# USUARIO_VALIDO = "cliente"
# SENHA_VALIDA = "senha123"
# CSV_PATH = r'C:\Users\Z\PycharmProjects\GuilhermeDir\Complete.csv'
#
# # Colunas que não precisam de filtro
# COLUNAS_SEM_FILTRO = ['Precatório', 'Autos do precatório', 'Processo Originário', 'Ordem', 'Processo Originário']
# import re
#
#
# def parse_number(value):
#     """Converte números formatados com pontos e vírgulas para float."""
#     if pd.isna(value) or value == '':
#         return None
#
#     if isinstance(value, (int, float)):
#         return float(value)
#
#     if isinstance(value, str):
#         # Remove espaços, símbolos monetários e caracteres não numéricos
#         value = value.strip().replace('R$', '').replace(' ', '')
#
#         # Substitui vírgula por ponto se houver apenas uma vírgula
#         if ',' in value and '.' not in value:
#             value = value.replace(',', '.')
#         # Remove pontos se houver vírgula como separador decimal
#         elif ',' in value and '.' in value:
#             value = value.replace('.', '').replace(',', '.')
#
#         # Remove qualquer caractere não numérico restante
#         value = re.sub(r'[^\d.]', '', value)
#
#         try:
#             return float(value)
#         except ValueError:
#             return None  # Retorna None se não for possível converter
#     return None  # Retorna None para valores inválidos
#
#
#
# def format_number(x):
#     """Formata números com separadores de milhar e duas casas decimais."""
#     try:
#         if pd.isna(x):
#             return ''
#         value_str = f"{float(x):,.2f}"
#         return value_str.replace(",", "X").replace(".", ",").replace("X", ".")
#     except (ValueError, TypeError):
#         return x
#
# import logging
# import logging
#
# logging.basicConfig(level=logging.DEBUG)
#
# import logging
#
# logging.basicConfig(level=logging.DEBUG)
#
# import logging
#
# logging.basicConfig(level=logging.DEBUG)
#
# import logging
#
# logging.basicConfig(level=logging.DEBUG)
#
# def apply_filters(df, filter_params):
#     logging.debug(f"Applying filters: {filter_params}")
#
#     # Certifica-se de que "Valor Deferido" está em formato numérico
#     if 'Valor Deferido' in df.columns:
#         df['Valor Deferido'] = df['Valor Deferido'].apply(parse_number)
#         df['Valor Deferido'] = pd.to_numeric(df['Valor Deferido'], errors='coerce')
#         logging.debug(f"'Valor Deferido' após conversão: {df['Valor Deferido'].head()}")
#
#     for column, filter_value in filter_params.items():
#         if column in df.columns and filter_value:
#             logging.debug(f"Filtering column '{column}' with value: {filter_value}")
#             if isinstance(filter_value, dict):  # Filtros numéricos ou de data
#                 if 'min' in filter_value or 'max' in filter_value:
#                     if pd.api.types.is_datetime64_any_dtype(df[column]):
#                         if filter_value.get('min'):
#                             df = df[df[column] >= pd.to_datetime(filter_value['min'])]
#                         if filter_value.get('max'):
#                             df = df[df[column] <= pd.to_datetime(filter_value['max'])]
#                     else:
#                         # Converte valores do filtro para float
#                         min_value = parse_number(filter_value.get('min')) if filter_value.get('min') else None
#                         max_value = parse_number(filter_value.get('max')) if filter_value.get('max') else None
#
#                         logging.debug(f"Filtrando '{column}' com min: {min_value}, max: {max_value}")
#
#                         # Aplica o filtro apenas em linhas válidas (não NaN)
#                         if min_value is not None and max_value is not None:
#                             df = df[df[column].notna() & (df[column] >= min_value) & (df[column] <= max_value)]
#                         elif min_value is not None:
#                             df = df[df[column].notna() & (df[column] >= min_value)]
#                         elif max_value is not None:
#                             df = df[df[column].notna() & (df[column] <= max_value)]
#
#                         logging.debug(f"DataFrame após filtro em '{column}': {df.head()}")
#             elif isinstance(filter_value, list):  # Filtros categóricos
#                 df = df[df[column].isin(filter_value)]
#
#     logging.debug(f"Filtered DataFrame final: {df.head()}")
#     return df
#
#
#
#
#
#
# def get_column_filters():
#     df = pd.read_csv(CSV_PATH, delimiter=';', on_bad_lines='skip')
#     filters = {}
#     df['Apresentação'] = pd.to_datetime(df['Apresentação'])
#
#     # Converte "Valor Deferido" para float
#     if 'Valor Deferido' in df.columns:
#         df['Valor Deferido'] = df['Valor Deferido'].apply(parse_number)
#         df['Valor Deferido'] = pd.to_numeric(df['Valor Deferido'], errors='coerce')
#
#     for column in df.columns:
#         if column not in COLUNAS_SEM_FILTRO:
#             if column == 'Apresentação':
#                 filters[column] = {
#                     'type': 'date',
#                     'min': df[column].min().strftime('%Y-%m-%d'),
#                     'max': df[column].max().strftime('%Y-%m-%d')
#                 }
#             elif column == 'Local':
#                 filters[column] = {
#                     'type': 'categorical',
#                     'values': sorted(df[column].unique().tolist())
#                 }
#             elif df[column].dtype in ['int64', 'float64'] or column == 'Valor Deferido':
#                 filters[column] = {
#                     'type': 'numeric',
#                     'min': float(df[column].min()),
#                     'max': float(df[column].max())
#                 }
#             elif column in ['Prioridade', 'Regime', 'Natureza']:
#                 filters[column] = {
#                     'type': 'categorical',
#                     'values': sorted(df[column].unique().tolist())
#                 }
#     return filters
#
#
# def load_csv(page=1, page_size=100, sort_column=None, ascending=True, filter_params=None):
#     df = pd.read_csv(CSV_PATH, delimiter=';', on_bad_lines='skip')
#     df['Apresentação'] = pd.to_datetime(df['Apresentação'])
#
#     # Exclui as colunas indesejadas
#     df = df.drop(columns=['Ordem', 'Precatório', 'Processo Originário'], errors='ignore')
#
#     # Converte a coluna "Valor Deferido" para float
#     if 'Valor Deferido' in df.columns:
#         df['Valor Deferido'] = df['Valor Deferido'].apply(parse_number)
#         df['Valor Deferido'] = pd.to_numeric(df['Valor Deferido'], errors='coerce')
#
#     # Convertendo "Orçamento" para int
#     if "Orçamento" in df.columns:
#         df["Orçamento"] = (
#             pd.to_numeric(df["Orçamento"], errors="coerce")
#             .fillna(0)
#             .astype(int)
#         )
#
#     if filter_params:
#         df = apply_filters(df, filter_params)
#     if sort_column:
#         df = df.sort_values(by=sort_column, ascending=ascending)
#
#     total = len(df)
#     start = (page - 1) * page_size
#     return df.iloc[start:start + page_size], total
#
#
#
#
#
# @app.route('/api/filters', methods=['GET'])
# def get_filters():
#     if not session.get('logged_in'):
#         return jsonify({'error': 'Not authenticated'}), 401
#     return jsonify(get_column_filters())
#
#
# @app.route('/api/apply_filters', methods=['POST'])
# def apply_filters_route():
#     if not session.get('logged_in'):
#         return jsonify({'error': 'Not authenticated'}), 401
#
#     filters = request.json
#     page = int(filters.pop('page', 1))
#     page_size = int(filters.pop('page_size', 100))
#     sort_column = filters.pop('sort_column', None)
#     ascending = filters.pop('ascending', True)
#
#     session['filters'] = filters
#
#     df, total = load_csv(
#         page=page,
#         page_size=page_size,
#         sort_column=sort_column,
#         ascending=ascending,
#         filter_params=filters
#     )
#
#     # Formata "Valor Deferido" corretamente
#     formatters = {"Valor Deferido": format_number} if "Valor Deferido" in df.columns else {}
#
#     table_html = df.to_html(
#         classes='styled-table',
#         index=False,
#         justify='center',
#         border=0,
#         formatters=formatters,
#         float_format="%.2f"
#     )
#
#     return jsonify({
#         'table_html': table_html,
#         'total': total,
#         'page': page,
#         'page_size': page_size
#     })
#
#
# @app.route('/', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         if username == USUARIO_VALIDO and password == SENHA_VALIDA:
#             session['logged_in'] = True
#             # Limpa filtros anteriores ao logar
#             session.pop('filters', None)
#             return redirect(url_for('home'))
#         else:
#             return render_template('login.html', error="Usuário ou senha incorretos")
#     return render_template('login.html')
#
#
# @app.route('/home')
# def home():
#     if not session.get('logged_in'):
#         return redirect(url_for('login'))
#     page = int(request.args.get('page', 1))
#     page_size = int(request.args.get('page_size', 100))
#     # Recupera os filtros aplicados (se houver) na sessão
#     filters = session.get('filters', None)
#     df, total = load_csv(page=page, page_size=page_size, filter_params=filters)
#     numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
#     formatters = {col: format_number for col in numeric_cols}
#     columns_to_hide = ['Ordem', 'Precatório', 'Processo Originário']
#     df = df.drop(columns=columns_to_hide, errors='ignore')
#
#     table_html = df.to_html(classes='styled-table', index=False, justify='center', border=0,
#                             formatters=formatters)
#
#     return render_template('home.html', table_html=table_html, total=total,
#                            page=page, page_size=page_size)
#
# if __name__ == '__main__':
#     app.run(debug=True)


# from flask import Flask, render_template, request, redirect, url_for, session, jsonify
# import pandas as pd
# from datetime import datetime
# import json
# import os
# import sys
# import webbrowser
# import threading
# import re
# import logging
#
# # Configuração de logging
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
#
# app = Flask(__name__)
# app.secret_key = 'minha_chave_pessoal'  # Chave fixa para uso pessoal
#
# USUARIO_VALIDO = "cliente"
# SENHA_VALIDA = "senha123"
#
# # Ajuste do CSV_PATH
# if getattr(sys, 'frozen', False):
#     base_path = os.path.dirname(sys.executable)
# else:
#     base_path = os.path.dirname(__file__)
# CSV_PATH = os.path.join(base_path, 'dadosnovos.csv')
#
# # Vedadrifica se o CSV e os templates existem
# if not os.path.exists(CSV_PATH):
#     logging.error(f"Arquivo CSV não encontrado em: {CSV_PATH}")
# else:
#     logging.info(f"Arquivo CSV encontrado em: {CSV_PATH}")
#
# TEMPLATES_DIR = os.path.join(base_path, 'templates')
# if not os.path.exists(TEMPLATES_DIR):
#     logging.error(f"Pasta 'templates' não encontrada em: {TEMPLATES_DIR}")
# else:
#     for template in ['login.html', 'home.html']:
#         template_path = os.path.join(TEMPLATES_DIR, template)
#         if not os.path.exists(template_path):
#             logging.error(f"Template não encontrado: {template_path}")
#         else:
#             logging.info(f"Template encontrado: {template_path}")
#
# # Colunas que não precisam de filtro
# COLUNAS_SEM_FILTRO = ['Precatório', 'Autos do precatório', 'Processo Originário', 'Ordem', 'Processo Originário']
#
# def parse_number(value):
#     if pd.isna(value) or value == '':
#         return None
#     if isinstance(value, (int, float)):
#         return float(value)
#     if isinstance(value, str):
#         value = value.strip().replace('R$', '').replace(' ', '')
#         if ',' in value and '.' not in value:
#             value = value.replace(',', '.')
#         elif ',' in value and '.' in value:
#             value = value.replace('.', '').replace(',', '.')
#         value = re.sub(r'[^\d.]', '', value)
#         try:
#             return float(value)
#         except ValueError:
#             return None
#     return None
#
# def format_number(x):
#     try:
#         if pd.isna(x):
#             return ''
#         value_str = f"{float(x):,.2f}"
#         return value_str.replace(",", "X").replace(".", ",").replace("X", ".")
#     except (ValueError, TypeError):
#         return x
#
#
# def apply_filters(df, filter_params):
#     logging.debug(f"Applying filters: {filter_params}")
#
#     # Aplica filtro na coluna 'Valor Deferido', se necessário
#     if 'Valor Deferido' in df.columns:
#         df['Valor Deferido'] = df['Valor Deferido'].apply(parse_number)
#         df['Valor Deferido'] = pd.to_numeric(df['Valor Deferido'], errors='coerce')
#
#     # Aplica filtros gerais
#     for column, filter_value in filter_params.items():
#         if column in df.columns and filter_value:
#             if isinstance(filter_value, dict):
#                 if 'min' in filter_value or 'max' in filter_value:
#                     if pd.api.types.is_datetime64_any_dtype(df[column]):
#                         if filter_value.get('min'):
#                             df = df[df[column] >= pd.to_datetime(filter_value['min'])]
#                         if filter_value.get('max'):
#                             df = df[df[column] <= pd.to_datetime(filter_value['max'])]
#                     else:
#                         min_value = parse_number(filter_value.get('min')) if filter_value.get('min') else None
#                         max_value = parse_number(filter_value.get('max')) if filter_value.get('max') else None
#                         if min_value is not None and max_value is not None:
#                             df = df[df[column].notna() & (df[column] >= min_value) & (df[column] <= max_value)]
#                         elif min_value is not None:
#                             df = df[df[column].notna() & (df[column] >= min_value)]
#                         elif max_value is not None:
#                             df = df[df[column].notna() & (df[column] <= max_value)]
#             elif isinstance(filter_value, list):
#                 logging.debug(f"Filtering {column} with values: {filter_value}")
#                 df = df[df[column].isin(filter_value)]
#     return df
#
# def get_column_filters():
#     try:
#         df = pd.read_csv("dadosnovos.csv", delimiter=';')
#         filters = {}
#         if 'Situação' in df.columns:
#             situacoes_validas = ["Requisitado", "Pagamento em Processamento", 'Indefinido']
#             df = df[df['Situação'].isin(situacoes_validas)]
#             filters['Situação'] = {
#                 'type': 'categorical',
#                 'values': situacoes_validas
#             }
#         if 'Valor Deferido' in df.columns:
#             df['Valor Deferido'] = df['Valor Deferido'].apply(parse_number)
#             df['Valor Deferido'] = pd.to_numeric(df['Valor Deferido'], errors='coerce')
#         for column in df.columns:
#             if column not in COLUNAS_SEM_FILTRO and column != 'Apresentação':
#                 if column == 'Local' or column == 'Tribunal de Origem':
#                     unique_values = sorted(df[column].dropna().unique().tolist())  # Adicionei dropna() para evitar valores nulos
#                     logging.info(f"Unique values for {column}: {unique_values}")
#                     filters[column] = {'type': 'categorical', 'values': unique_values}
#                 elif df[column].dtype in ['int64', 'float64'] or column == 'Valor Deferido':
#                     filters[column] = {'type': 'numeric', 'min': float(df[column].min()), 'max': float(df[column].max())}
#                 elif column in ['Prioridade', 'Regime', 'Natureza']:
#                     filters[column] = {'type': 'categorical', 'values': sorted(df[column].dropna().unique().tolist())}
#         return filters
#     except Exception as e:
#         logging.error(f"Erro em get_column_filters: {str(e)}")
#         raise
#
#
#
#
#
#
#
#
# def load_csv(page=1, page_size=100, sort_column=None, ascending=True, filter_params=None):
#     try:
#         pd.options.mode.chained_assignment = None
#         logging.info(f"Lendo CSV de: {CSV_PATH}")
#         df = pd.read_csv(CSV_PATH, delimiter=';', on_bad_lines='skip')
#         logging.info(f"CSV lido com sucesso. Total de linhas: {len(df)}")
#
#         # Limpeza de colunas desnecessárias
#         if set(['Ordem', 'Precatório', 'Processo Originário']).issubset(df.columns):
#             df = df.drop(columns=['Ordem', 'Precatório', 'Processo Originário', 'Apresentação'], errors='ignore')
#             logging.info("Colunas desnecessárias removidas")
#
#         # Ajustando a coluna 'Valor Deferido'
#         if 'Valor Deferido' in df.columns:
#             df['Valor Deferido'] = df['Valor Deferido'].apply(parse_number)
#             df['Valor Deferido'] = pd.to_numeric(df['Valor Deferido'], errors='coerce')
#             logging.info("Coluna 'Valor Deferido' convertida para número")
#
#         # Convertendo a coluna 'Orçamento' para numérica
#         if "Orçamento" in df.columns:
#             df["Orçamento"] = pd.to_numeric(df["Orçamento"], errors="coerce").fillna(0).astype(int)
#             logging.info("Coluna 'Orçamento' convertida para número inteiro")
#
#         total_antes_filtros = len(df)
#         logging.info(f"Total de linhas antes dos filtros: {total_antes_filtros}")
#
#         # Filtros básicos da situação
#         if 'Situação' in df.columns:
#             situacoes_validas = ["Requisitado", "Pagamento em Processamento", "Pago Superpreferência", "Indefinido"]
#             df = df[df['Situação'].isin(situacoes_validas)]
#             logging.info(f"Após filtro de situação: {len(df)} linhas")
#
#         # Aplica os filtros adicionais, se houver
#         if filter_params:
#             logging.info(f"Aplicando filtros adicionais: {filter_params}")
#             df = apply_filters(df, filter_params)
#             logging.info(f"Após aplicar filtros adicionais: {len(df)} linhas")
#
#         total = len(df)
#
#         # Ordenação das linhas, se solicitado
#         if sort_column and sort_column in df.columns:
#             df = df.sort_values(by=sort_column, ascending=ascending)
#             logging.info(f"Ordenado por {sort_column} ({ascending=})")
#
#         # Paginação
#         start = (page - 1) * page_size
#         end = start + page_size
#
#         logging.info(f"Retornando linhas {start} até {end} de {total}")
#         return df.iloc[start:min(end, total)], total
#
#     except Exception as e:
#         logging.error(f"Erro em load_csv: {str(e)}")
#         import traceback
#         logging.error(traceback.format_exc())
#         raise
#
#
#
# @app.route('/api/filters', methods=['GET'])
# def get_filters():
#     try:
#         if not session.get('logged_in'):
#             return jsonify({'error': 'Not authenticated'}), 401
#         return jsonify(get_column_filters())
#     except Exception as e:
#         logging.error(f"Erro em /api/filters: {str(e)}")
#         raise
#
# @app.route('/api/apply_filters', methods=['POST'])
# def apply_filters_route():
#     try:
#         if not session.get('logged_in'):
#             return jsonify({'error': 'Not authenticated'}), 401
#         filters = request.json
#         page = int(filters.pop('page', 1))
#         page_size = int(filters.pop('page_size', 100))
#         sort_column = filters.pop('sort_column', None)
#         ascending = filters.pop('ascending', True)
#         session['filters'] = filters
#         df, total = load_csv(page=page, page_size=page_size, sort_column=sort_column, ascending=ascending, filter_params=filters)
#         formatters = {"Valor Deferido": format_number} if "Valor Deferido" in df.columns else {}
#         table_html = df.to_html(classes='styled-table', index=False, justify='center', border=0, formatters=formatters, float_format="%.2f")
#         return jsonify({'table_html': table_html, 'total': total, 'page': page, 'page_size': page_size})
#     except Exception as e:
#         logging.error(f"Erro em /api/apply_filters: {str(e)}")
#         raise
#
# @app.route('/', methods=['GET', 'POST'])
# def login():
#     logging.info("Acessando rota /login")
#     try:
#         logging.debug("Verificando método da requisição")
#         if request.method == 'POST':
#             username = request.form['username']
#             password = request.form['password']
#             logging.debug(f"Tentativa de login - username: {username}")
#             if username == USUARIO_VALIDO and password == SENHA_VALIDA:
#                 logging.debug("Credenciais válidas, definindo sessão")
#                 session['logged_in'] = True
#                 session.pop('filters', None)
#                 logging.info("Login bem-sucedido, redirecionando para /home")
#                 return redirect(url_for('home'))
#             else:
#                 logging.warning("Falha no login: credenciais inválidas")
#                 return render_template('login.html', error="Usuário ou senha incorretos")
#         logging.debug("Renderizando login.html para GET")
#         return render_template('login.html')
#     except Exception as e:
#         logging.error(f"Erro na rota /login: {str(e)}")
#         raise
#
#
# @app.route('/home')
# def home():
#     try:
#         if not session.get('logged_in'):
#             return redirect(url_for('login'))
#
#         page = int(request.args.get('page', 1))
#         page_size = int(request.args.get('page_size', 100))
#         sort_column = request.args.get('sort_column')
#         ascending = request.args.get('ascending', 'true').lower() == 'true'
#
#         # Get filters from session or query parameters
#         filters = {}
#
#         # First try to get filters from query parameters
#         filter_params = request.args.get('filters')
#         if filter_params:
#             try:
#                 filters = json.loads(filter_params)
#             except json.JSONDecodeError:
#                 logging.error("Failed to parse filters from query parameters")
#                 filters = {}
#         # If no filters in query params, use session filters
#         elif 'filters' in session:
#             filters = session['filters']
#
#         # Store current filters in session
#         session['filters'] = filters
#
#         # Load data with current filters
#         df, total = load_csv(
#             page=page,
#             page_size=page_size,
#             sort_column=sort_column,
#             ascending=ascending,
#             filter_params=filters
#         )
#
#         # Calculate total pages
#         total_pages = (total // page_size) + (1 if total % page_size > 0 else 0)
#
#         # Format numeric columns
#         formatters = {"Valor Deferido": format_number} if "Valor Deferido" in df.columns else {}
#
#         table_html = df.to_html(
#             classes='styled-table',
#             index=False,
#             justify='center',
#             border=0,
#             formatters=formatters,
#             float_format="%.2f"
#         )
#
#         # Encode filters for template
#         encoded_filters = json.dumps(filters)
#
#         return render_template(
#             'home.html',
#             table_html=table_html,
#             total=total,
#             total_pages=total_pages,
#             page=page,
#             page_size=page_size,
#             active_filters=encoded_filters,
#             sort_column=sort_column,
#             ascending=ascending
#         )
#
#     except Exception as e:
#         logging.error(f"Erro em /home: {str(e)}")
#         raise
#
# def open_browser():
#     threading.Timer(1.0, lambda: webbrowser.open('http://127.0.0.1:5000')).start()
#
# if __name__ == '__main__':
#     logging.info("Iniciando aplicação")
#     try:
#         open_browser()
#         app.run(debug=False, host='127.0.0.1', port=5000)
#     except Exception as e:
#         print('hehe')

# from flask import Flask, render_template, request, redirect, url_for, session, jsonify
# import pandas as pd
# from datetime import datetime
# import json
#
# app = Flask(__name__)
# app.secret_key = 'sua_chave_secreta_aqui'
#
# USUARIO_VALIDO = "cliente"
# SENHA_VALIDA = "senha123"
# CSV_PATH = r'C:\Users\Z\PycharmProjects\GuilhermeDir\Complete.csv'
#
# # Colunas que não precisam de filtro
# COLUNAS_SEM_FILTRO = ['Precatório', 'Autos do precatório', 'Processo Originário', 'Ordem', 'Processo Originário']
# import re
#
#
# def parse_number(value):
#     """Converte números formatados com pontos e vírgulas para float."""
#     if pd.isna(value) or value == '':
#         return None
#
#     if isinstance(value, (int, float)):
#         return float(value)
#
#     if isinstance(value, str):
#         # Remove espaços, símbolos monetários e caracteres não numéricos
#         value = value.strip().replace('R$', '').replace(' ', '')
#
#         # Substitui vírgula por ponto se houver apenas uma vírgula
#         if ',' in value and '.' not in value:
#             value = value.replace(',', '.')
#         # Remove pontos se houver vírgula como separador decimal
#         elif ',' in value and '.' in value:
#             value = value.replace('.', '').replace(',', '.')
#
#         # Remove qualquer caractere não numérico restante
#         value = re.sub(r'[^\d.]', '', value)
#
#         try:
#             return float(value)
#         except ValueError:
#             return None  # Retorna None se não for possível converter
#     return None  # Retorna None para valores inválidos
#
#
#
# def format_number(x):
#     """Formata números com separadores de milhar e duas casas decimais."""
#     try:
#         if pd.isna(x):
#             return ''
#         value_str = f"{float(x):,.2f}"
#         return value_str.replace(",", "X").replace(".", ",").replace("X", ".")
#     except (ValueError, TypeError):
#         return x
#
# import logging
# import logging
#
# logging.basicConfig(level=logging.DEBUG)
#
# import logging
#
# logging.basicConfig(level=logging.DEBUG)
#
# import logging
#
# logging.basicConfig(level=logging.DEBUG)
#
# import logging
#
# logging.basicConfig(level=logging.DEBUG)
#
# def apply_filters(df, filter_params):
#     logging.debug(f"Applying filters: {filter_params}")
#
#     # Certifica-se de que "Valor Deferido" está em formato numérico
#     if 'Valor Deferido' in df.columns:
#         df['Valor Deferido'] = df['Valor Deferido'].apply(parse_number)
#         df['Valor Deferido'] = pd.to_numeric(df['Valor Deferido'], errors='coerce')
#         logging.debug(f"'Valor Deferido' após conversão: {df['Valor Deferido'].head()}")
#
#     for column, filter_value in filter_params.items():
#         if column in df.columns and filter_value:
#             logging.debug(f"Filtering column '{column}' with value: {filter_value}")
#             if isinstance(filter_value, dict):  # Filtros numéricos ou de data
#                 if 'min' in filter_value or 'max' in filter_value:
#                     if pd.api.types.is_datetime64_any_dtype(df[column]):
#                         if filter_value.get('min'):
#                             df = df[df[column] >= pd.to_datetime(filter_value['min'])]
#                         if filter_value.get('max'):
#                             df = df[df[column] <= pd.to_datetime(filter_value['max'])]
#                     else:
#                         # Converte valores do filtro para float
#                         min_value = parse_number(filter_value.get('min')) if filter_value.get('min') else None
#                         max_value = parse_number(filter_value.get('max')) if filter_value.get('max') else None
#
#                         logging.debug(f"Filtrando '{column}' com min: {min_value}, max: {max_value}")
#
#                         # Aplica o filtro apenas em linhas válidas (não NaN)
#                         if min_value is not None and max_value is not None:
#                             df = df[df[column].notna() & (df[column] >= min_value) & (df[column] <= max_value)]
#                         elif min_value is not None:
#                             df = df[df[column].notna() & (df[column] >= min_value)]
#                         elif max_value is not None:
#                             df = df[df[column].notna() & (df[column] <= max_value)]
#
#                         logging.debug(f"DataFrame após filtro em '{column}': {df.head()}")
#             elif isinstance(filter_value, list):  # Filtros categóricos
#                 df = df[df[column].isin(filter_value)]
#
#     logging.debug(f"Filtered DataFrame final: {df.head()}")
#     return df
#
#
#
#
#
#
# def get_column_filters():
#     df = pd.read_csv(CSV_PATH, delimiter=';', on_bad_lines='skip')
#     filters = {}
#     df['Apresentação'] = pd.to_datetime(df['Apresentação'])
#
#     # Converte "Valor Deferido" para float
#     if 'Valor Deferido' in df.columns:
#         df['Valor Deferido'] = df['Valor Deferido'].apply(parse_number)
#         df['Valor Deferido'] = pd.to_numeric(df['Valor Deferido'], errors='coerce')
#
#     for column in df.columns:
#         if column not in COLUNAS_SEM_FILTRO:
#             if column == 'Apresentação':
#                 filters[column] = {
#                     'type': 'date',
#                     'min': df[column].min().strftime('%Y-%m-%d'),
#                     'max': df[column].max().strftime('%Y-%m-%d')
#                 }
#             elif column == 'Local':
#                 filters[column] = {
#                     'type': 'categorical',
#                     'values': sorted(df[column].unique().tolist())
#                 }
#             elif df[column].dtype in ['int64', 'float64'] or column == 'Valor Deferido':
#                 filters[column] = {
#                     'type': 'numeric',
#                     'min': float(df[column].min()),
#                     'max': float(df[column].max())
#                 }
#             elif column in ['Prioridade', 'Regime', 'Natureza']:
#                 filters[column] = {
#                     'type': 'categorical',
#                     'values': sorted(df[column].unique().tolist())
#                 }
#     return filters
#
#
# def load_csv(page=1, page_size=100, sort_column=None, ascending=True, filter_params=None):
#     df = pd.read_csv(CSV_PATH, delimiter=';', on_bad_lines='skip')
#     df['Apresentação'] = pd.to_datetime(df['Apresentação'])
#
#     # Exclui as colunas indesejadas
#     df = df.drop(columns=['Ordem', 'Precatório', 'Processo Originário'], errors='ignore')
#
#     # Converte a coluna "Valor Deferido" para float
#     if 'Valor Deferido' in df.columns:
#         df['Valor Deferido'] = df['Valor Deferido'].apply(parse_number)
#         df['Valor Deferido'] = pd.to_numeric(df['Valor Deferido'], errors='coerce')
#
#     # Convertendo "Orçamento" para int
#     if "Orçamento" in df.columns:
#         df["Orçamento"] = (
#             pd.to_numeric(df["Orçamento"], errors="coerce")
#             .fillna(0)
#             .astype(int)
#         )
#
#     if filter_params:
#         df = apply_filters(df, filter_params)
#     if sort_column:
#         df = df.sort_values(by=sort_column, ascending=ascending)
#
#     total = len(df)
#     start = (page - 1) * page_size
#     return df.iloc[start:start + page_size], total
#
#
#
#
#
# @app.route('/api/filters', methods=['GET'])
# def get_filters():
#     if not session.get('logged_in'):
#         return jsonify({'error': 'Not authenticated'}), 401
#     return jsonify(get_column_filters())
#
#
# @app.route('/api/apply_filters', methods=['POST'])
# def apply_filters_route():
#     if not session.get('logged_in'):
#         return jsonify({'error': 'Not authenticated'}), 401
#
#     filters = request.json
#     page = int(filters.pop('page', 1))
#     page_size = int(filters.pop('page_size', 100))
#     sort_column = filters.pop('sort_column', None)
#     ascending = filters.pop('ascending', True)
#
#     session['filters'] = filters
#
#     df, total = load_csv(
#         page=page,
#         page_size=page_size,
#         sort_column=sort_column,
#         ascending=ascending,
#         filter_params=filters
#     )
#
#     # Formata "Valor Deferido" corretamente
#     formatters = {"Valor Deferido": format_number} if "Valor Deferido" in df.columns else {}
#
#     table_html = df.to_html(
#         classes='styled-table',
#         index=False,
#         justify='center',
#         border=0,
#         formatters=formatters,
#         float_format="%.2f"
#     )
#
#     return jsonify({
#         'table_html': table_html,
#         'total': total,
#         'page': page,
#         'page_size': page_size
#     })
#
#
# @app.route('/', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         if username == USUARIO_VALIDO and password == SENHA_VALIDA:
#             session['logged_in'] = True
#             # Limpa filtros anteriores ao logar
#             session.pop('filters', None)
#             return redirect(url_for('home'))
#         else:
#             return render_template('login.html', error="Usuário ou senha incorretos")
#     return render_template('login.html')
#
#
# @app.route('/home')
# def home():
#     if not session.get('logged_in'):
#         return redirect(url_for('login'))
#     page = int(request.args.get('page', 1))
#     page_size = int(request.args.get('page_size', 100))
#     # Recupera os filtros aplicados (se houver) na sessão
#     filters = session.get('filters', None)
#     df, total = load_csv(page=page, page_size=page_size, filter_params=filters)
#     numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
#     formatters = {col: format_number for col in numeric_cols}
#     columns_to_hide = ['Ordem', 'Precatório', 'Processo Originário']
#     df = df.drop(columns=columns_to_hide, errors='ignore')
#
#     table_html = df.to_html(classes='styled-table', index=False, justify='center', border=0,
#                             formatters=formatters)
#
#     return render_template('home.html', table_html=table_html, total=total,
#                            page=page, page_size=page_size)
#
# if __name__ == '__main__':
#     app.run(debug=True)




from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import pandas as pd
from datetime import datetime
import json
import os
import sys
import webbrowser
import threading
import re
import logging

# Configuração de logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
app.secret_key = 'minha_chave_pessoal'  # Chave fixa para uso pessoal

USUARIO_VALIDO = "cliente"
SENHA_VALIDA = "senha123"

# Dicionário para armazenar os caminhos dos arquivos CSV
CSV_FILES = {
    'TJPR': 'dadosnovostjpr.csv',
    'TJSC': 'TJSC.csv',
    'TJRS': 'TJRS.csv'
}

# Ajuste do CSV_PATH
if getattr(sys, 'frozen', False):
    base_path = os.path.dirname(sys.executable)
else:
    base_path = os.path.dirname(__file__)
CSV_PATH = os.path.join(base_path, "dadosnovos.csv")

# Vedadrifica se o CSV e os templates existem
if not os.path.exists(CSV_PATH):
    logging.error(f"Arquivo CSV não encontrado em: {CSV_PATH}")
else:
    logging.info(f"Arquivo CSV encontrado em: {CSV_PATH}")

TEMPLATES_DIR = os.path.join(base_path, 'templates')
if not os.path.exists(TEMPLATES_DIR):
    logging.error(f"Pasta 'templates' não encontrada em: {TEMPLATES_DIR}")
else:
    for template in ['login.html', 'home.html']:
        template_path = os.path.join(TEMPLATES_DIR, template)
        if not os.path.exists(template_path):
            logging.error(f"Template não encontrado: {template_path}")
        else:
            logging.info(f"Template encontrado: {template_path}")
# Função para carregar o CSV correto com base na aba selecionada
def get_csv_path(sheet_name):
    base_path = os.path.dirname(__file__)
    return os.path.join(base_path, CSV_FILES.get(sheet_name, 'dadosnovos.csv'))

# Ajuste do CSV_PATH
def get_current_csv_path():
    return get_csv_path(session.get('current_sheet', 'TJPR'))

@app.route('/switch_sheet/<sheet_name>', methods=['POST'])
def switch_sheet(sheet_name):
    if sheet_name in CSV_FILES:
        session['current_sheet'] = sheet_name
        # Limpar os filtros atuais ao trocar de aba
        session.pop('filters', None)
        # Recarregar os filtros do novo CSV
        filters = get_column_filters()
        return jsonify({'status': 'success', 'sheet': sheet_name, 'filters': filters})
    return jsonify({'status': 'error', 'message': 'Sheet not found'}), 404
# Colunas que não precisam de filtro
COLUNAS_SEM_FILTRO = ['Precatório', 'Autos do precatório', 'Processo Originário', 'Ordem', 'Processo Originário']

def parse_number(value):
    if pd.isna(value) or value == '':
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        value = value.strip().replace('R$', '').replace(' ', '')
        if ',' in value and '.' not in value:
            value = value.replace(',', '.')
        elif ',' in value and '.' in value:
            value = value.replace('.', '').replace(',', '.')
        value = re.sub(r'[^\d.]', '', value)
        try:
            return float(value)
        except ValueError:
            return None
    return None

def format_number(x):
    try:
        if pd.isna(x):
            return ''
        value_str = f"{float(x):,.2f}"
        return value_str.replace(",", "X").replace(".", ",").replace("X", ".")
    except (ValueError, TypeError):
        return x


def apply_filters(df, filter_params):
    logging.debug(f"Applying filters: {filter_params}")

    # Aplica filtro na coluna 'Valor Deferido', se necessário
    if 'Valor Deferido' in df.columns:
        df['Valor Deferido'] = df['Valor Deferido'].apply(parse_number)
        df['Valor Deferido'] = pd.to_numeric(df['Valor Deferido'], errors='coerce')

    # Aplica filtros gerais
    for column, filter_value in filter_params.items():
        if column in df.columns and filter_value:
            if isinstance(filter_value, dict):
                if 'min' in filter_value or 'max' in filter_value:
                    if pd.api.types.is_datetime64_any_dtype(df[column]):
                        if filter_value.get('min'):
                            df = df[df[column] >= pd.to_datetime(filter_value['min'])]
                        if filter_value.get('max'):
                            df = df[df[column] <= pd.to_datetime(filter_value['max'])]
                    else:
                        min_value = parse_number(filter_value.get('min')) if filter_value.get('min') else None
                        max_value = parse_number(filter_value.get('max')) if filter_value.get('max') else None
                        if min_value is not None and max_value is not None:
                            df = df[df[column].notna() & (df[column] >= min_value) & (df[column] <= max_value)]
                        elif min_value is not None:
                            df = df[df[column].notna() & (df[column] >= min_value)]
                        elif max_value is not None:
                            df = df[df[column].notna() & (df[column] <= max_value)]
            elif isinstance(filter_value, list):
                logging.debug(f"Filtering {column} with values: {filter_value}")
                df = df[df[column].isin(filter_value)]
    return df

def get_column_filters():
    try:
        csv_path = get_current_csv_path()
        df = pd.read_csv(csv_path)
        filters = {}
        if 'Situação' in df.columns:
            situacoes_validas = ["Requisitado", "Pagamento em Processamento", 'Indefinido']
            df = df[df['Situação'].isin(situacoes_validas)]
            filters['Situação'] = {
                'type': 'categorical',
                'values': situacoes_validas
            }
        if 'Valor Deferido' in df.columns:
            df['Valor Deferido'] = df['Valor Deferido'].apply(parse_number)
            df['Valor Deferido'] = pd.to_numeric(df['Valor Deferido'], errors='coerce')
        for column in df.columns:
            if column not in COLUNAS_SEM_FILTRO and column != 'Apresentação':
                if column == 'Local' or column == 'Tribunal de Origem':
                    unique_values = sorted(df[column].dropna().unique().tolist())
                    logging.info(f"Unique values for {column}: {unique_values}")
                    filters[column] = {'type': 'categorical', 'values': unique_values}
                elif df[column].dtype in ['int64', 'float64'] or column == 'Valor Deferido':
                    filters[column] = {'type': 'numeric', 'min': float(df[column].min()), 'max': float(df[column].max())}
                elif column in ['Prioridade', 'Regime', 'Natureza']:
                    filters[column] = {'type': 'categorical', 'values': sorted(df[column].dropna().unique().tolist())}
        return filters
    except Exception as e:
        logging.error(f"Erro em get_column_filters: {str(e)}")
        raise








def load_csv(page=1, page_size=100, sort_column=None, ascending=True, filter_params=None):
    try:
        pd.options.mode.chained_assignment = None
        csv_path = get_current_csv_path()
        logging.info(f"Lendo CSV de: {csv_path}")
        df = pd.read_csv(csv_path, on_bad_lines='skip')
        logging.info(f"CSV lido com sucesso. Total de linhas: {len(df)}")

        # Limpeza de colunas desnecessárias
        if set(['Ordem', 'Precatório', 'Processo Originário']).issubset(df.columns):
            df = df.drop(columns=['Ordem', 'Precatório', 'Processo Originário', 'Apresentação'], errors='ignore')
            logging.info("Colunas desnecessárias removidas")

        # Ajustando a coluna 'Valor Deferido'
        if 'Valor Deferido' in df.columns:
            df['Valor Deferido'] = df['Valor Deferido'].apply(parse_number)
            df['Valor Deferido'] = pd.to_numeric(df['Valor Deferido'], errors='coerce')
            logging.info("Coluna 'Valor Deferido' convertida para número")

        # Convertendo a coluna 'Orçamento' para numérica
        if "Orçamento" in df.columns:
            df["Orçamento"] = pd.to_numeric(df["Orçamento"], errors="coerce").fillna(0).astype(int)
            logging.info("Coluna 'Orçamento' convertida para número inteiro")

        total_antes_filtros = len(df)
        logging.info(f"Total de linhas antes dos filtros: {total_antes_filtros}")

        # Filtros básicos da situação
        if 'Situação' in df.columns:
            situacoes_validas = ["Requisitado", "Pagamento em Processamento", "Pago Superpreferência", 'Indefinido'] #aqui tem indefinido mas apaguei
            df = df[df['Situação'].isin(situacoes_validas)]
            logging.info(f"Após filtro de situação: {len(df)} linhas")

        # Aplica os filtros adicionais, se houver
        if filter_params:
            logging.info(f"Aplicando filtros adicionais: {filter_params}")
            df = apply_filters(df, filter_params)
            logging.info(f"Após aplicar filtros adicionais: {len(df)} linhas")

        total = len(df)

        # Ordenação das linhas, se solicitado
        if sort_column and sort_column in df.columns:
            df = df.sort_values(by=sort_column, ascending=ascending)
            logging.info(f"Ordenado por {sort_column} ({ascending=})")

        # Paginação
        start = (page - 1) * page_size
        end = start + page_size

        logging.info(f"Retornando linhas {start} até {end} de {total}")
        return df.iloc[start:min(end, total)], total

    except Exception as e:
        logging.error(f"Erro em load_csv: {str(e)}")
        import traceback
        logging.error(traceback.format_exc())
        raise



@app.route('/api/filters', methods=['GET'])
def get_filters():
    try:
        if not session.get('logged_in'):
            return jsonify({'error': 'Not authenticated'}), 401
        return jsonify(get_column_filters())
    except Exception as e:
        logging.error(f"Erro em /api/filters: {str(e)}")
        raise

@app.route('/api/apply_filters', methods=['POST'])
def apply_filters_route():
    try:
        if not session.get('logged_in'):
            return jsonify({'error': 'Not authenticated'}), 401
        filters = request.json
        page = int(filters.pop('page', 1))
        page_size = int(filters.pop('page_size', 100))
        sort_column = filters.pop('sort_column', None)
        ascending = filters.pop('ascending', True)
        session['filters'] = filters
        df, total = load_csv(page=page, page_size=page_size, sort_column=sort_column, ascending=ascending, filter_params=filters)
        formatters = {"Valor Deferido": format_number} if "Valor Deferido" in df.columns else {}
        table_html = df.to_html(classes='styled-table', index=False, justify='center', border=0, formatters=formatters, float_format="%.2f")
        return jsonify({'table_html': table_html, 'total': total, 'page': page, 'page_size': page_size})
    except Exception as e:
        logging.error(f"Erro em /api/apply_filters: {str(e)}")
        raise

@app.route('/', methods=['GET', 'POST'])
def login():
    logging.info("Acessando rota /login")
    try:
        logging.debug("Verificando método da requisição")
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            logging.debug(f"Tentativa de login - username: {username}")
            if username == USUARIO_VALIDO and password == SENHA_VALIDA:
                logging.debug("Credenciais válidas, definindo sessão")
                session['logged_in'] = True
                session.pop('filters', None)
                logging.info("Login bem-sucedido, redirecionando para /home")
                return redirect(url_for('home'))
            else:
                logging.warning("Falha no login: credenciais inválidas")
                return render_template('login.html', error="Usuário ou senha incorretos")
        logging.debug("Renderizando login.html para GET")
        return render_template('login.html')
    except Exception as e:
        logging.error(f"Erro na rota /login: {str(e)}")
        raise


@app.route('/home')
def home():
    try:
        if not session.get('logged_in'):
            return redirect(url_for('login'))

        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 100))
        sort_column = request.args.get('sort_column')
        ascending = request.args.get('ascending', 'true').lower() == 'true'

        # Get filters from session or query parameters
        filters = {}

        # First try to get filters from query parameters
        filter_params = request.args.get('filters')
        if filter_params:
            try:
                filters = json.loads(filter_params)
            except json.JSONDecodeError:
                logging.error("Failed to parse filters from query parameters")
                filters = {}
        # If no filters in query params, use session filters
        elif 'filters' in session:
            filters = session['filters']

        # Store current filters in session
        session['filters'] = filters

        # Load data with current filters
        df, total = load_csv(
            page=page,
            page_size=page_size,
            sort_column=sort_column,
            ascending=ascending,
            filter_params=filters
        )

        # Calculate total pages
        total_pages = (total // page_size) + (1 if total % page_size > 0 else 0)

        # Format numeric columns
        formatters = {"Valor Deferido": format_number} if "Valor Deferido" in df.columns else {}

        table_html = df.to_html(
            classes='styled-table',
            index=False,
            justify='center',
            border=0,
            formatters=formatters,
            float_format="%.2f"
        )

        # Encode filters for template
        encoded_filters = json.dumps(filters)

        return render_template(
            'home.html',
            table_html=table_html,
            total=total,
            total_pages=total_pages,
            page=page,
            page_size=page_size,
            active_filters=encoded_filters,
            sort_column=sort_column,
            ascending=ascending
        )

    except Exception as e:
        logging.error(f"Erro em /home: {str(e)}")
        raise

def open_browser():
    threading.Timer(1.0, lambda: webbrowser.open('http://127.0.0.1:5000')).start()

if __name__ == '__main__':
    logging.info("Iniciando aplicação")
    try:
        open_browser()
        app.run(debug=False, host='127.0.0.1', port=5000)
    except Exception as e:

        logging.error(f"Erro ao iniciar o servidor: {str(e)}")



