# 📊 Avaliador de Testes A/B com IA (Méliuz)<br>
Projeto desenvolvido como parte do processo seletivo de estágio do Méliuz<br>
com o objetivo de automatizar a análise estratégica de testes A/B de parceiros<br>
utilizando Inteligência Artificial (Google Gemini), oferecendo flexibilidade de execução via Terminal (CLI) ou Interface Web (Streamlit).<br>

## Tecnologias/LIBS Utilizadas:<br>
- Python 3.10+<br>
- Gemini (melhoras textuais nos executaveis e auxilio em soluções de erros)<br>
- Google GenAI SDK ( integração do assistente virtual )<br>
- Streamlit (Interface Web)<br>
- Pandas<br>
- Pathlib / Dotenv <br>

## 📖 Instruções de Instalação e Execução:<br>
*ATENÇÂO, REQUER QUE VOCÊ TENHA HABILITADO A EXECUÇÂO DE .bat e A EXTENÇÂO DOS ARQUIVOS.*
Caso esteja executando o projeto a partir de uma versão compactada (.zip ou .rar), siga os passos abaixo:<br>

Extração:<br>

Extraia o conteúdo do arquivo compactado em uma pasta de sua preferência na máquina.<br>
Configuração da API:

Certifique-se de que o arquivo .env contendo a sua chave da API (GEMINI_API_KEY=sua_chave) está posicionado na raiz do projeto junto com os arquivos.<br>
Caso não contenha um arquivo .env, abra o .bat (qualquer um dos dois) e insira a chave api quando solicitado<br>


## Dependências:<br>

Abra o terminal na pasta do projeto e instale as dependências necessárias listadas no arquivo requirements.txt utilizando o comando:<br>
```text
pip install -r requirements.txt<br>
OU <br>
python -m pip install -r requirements.txt<br>
```
## Inicialização:<br>

Utilize o arquivo .bat correspondente ao modo de execução desejado:<br>

💻 Modo Terminal (CMD): Dê dois cliques no script de execução via linha de comando para interagir pelo terminal.<br>

🌐 Modo Web (Streamlit): Dê dois cliques no script de execução web para abrir o painel interativo diretamente no navegador padrão.<br>

## 📂 Organização dos Resultados (output/)<br>
Após a realização das análises (seja de arquivos únicos ou em lote), os artefatos gerados pelo sistema são salvos automaticamente na pasta *output*:<br>

Relatórios Executivos (output/reports/): Arquivos em formato .txt contendo a análise estratégica detalhada gerada pela IA, salvos com registro de data e hora (timestamp) para histórico completo.

Registro Consolidado (output/registro_testes.csv): Arquivo estruturado com os dados consolidados das decisões tomadas pelo modelo.

Desenvolvido por Ryan Kaique.
