#📊 Avaliador de Testes A/B com IA (Méliuz)
Projeto desenvolvido como parte do processo seletivo de estágio do Méliuz, com o objetivo de automatizar a análise estratégica de testes A/B de parceiros utilizando Inteligência Artificial (Google Gemini), oferecendo flexibilidade de execução via Terminal (CLI) ou Interface Web (Streamlit).

##Tecnologias/LIBS Utilizadas:
- Python 3.10+
- Gemini (melhoras textuais nos executaveis e auxilio em soluções de erros)
- Google GenAI SDK ( integração do assistente virtual )
- Streamlit (Interface Web)
- Pandas
- Pathlib / Dotenv 

##📖 Instruções de Instalação e Execução:
Caso esteja executando o projeto a partir de uma versão compactada (.zip ou .rar), siga os passos abaixo:

Extração:

Extraia o conteúdo do arquivo compactado em uma pasta de sua preferência na máquina.

Configuração da API:

Certifique-se de que o arquivo .env contendo a sua chave da API (GEMINI_API_KEY=sua_chave) está posicionado na raiz do projeto junto com os arquivos.

##Dependências:##

Abra o terminal na pasta do projeto e instale as dependências necessárias listadas no arquivo requirements.txt utilizando o comando:

pip install -r requirements.txt

##Inicialização:

Utilize o arquivo .bat correspondente ao modo de execução desejado:

💻 Modo Terminal (CMD): Dê dois cliques no script de execução via linha de comando para interagir pelo terminal.

🌐 Modo Web (Streamlit): Dê dois cliques no script de execução web para abrir o painel interativo diretamente no navegador padrão.

##📂 Organização dos Resultados (output/)
Após a realização das análises (seja de arquivos únicos ou em lote), os artefatos gerados pelo sistema são salvos automaticamente na pasta *output/*:

Relatórios Executivos (output/reports/): Arquivos em formato .txt contendo a análise estratégica detalhada gerada pela IA, salvos com registro de data e hora (timestamp) para histórico completo.

Registro Consolidado (output/registro_testes.csv): Arquivo estruturado com os dados consolidados das decisões tomadas pelo modelo.

Desenvolvido por Ryan Kaique.
