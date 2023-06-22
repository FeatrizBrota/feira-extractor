# Feira Extractor


Este repositório contém um código Python para extrair dados de feiras de um site e salvá-los em formato JSON e em um banco de dados MongoDB. A aplicação foi desenvolvida com o objetivo de facilitar a extração e armazenamento de informações sobre feiras de diferentes tipos.

Características:
- Extrai informações como título, endereço, bairro, telefone e observação de feiras de um site específico.
- Converte a observação da feira para um formato padronizado, incluindo dia da semana e horário de funcionamento.
- Salva os dados das feiras em formato JSON e no banco de dados MongoDB.
- Permite que o usuário forneça o link do site e o tipo de feira ao executar a aplicação.
- Lida com diferentes padrões de observação, incluindo casos em que há múltiplos dias da semana e horários de funcionamento.

Pré-requisitos:
- Python 3.x
- Bibliotecas: requests, beautifulsoup4, pymongo

Utilização:
1. Clone este repositório em seu ambiente local.
2. Instale as bibliotecas necessárias mencionadas acima.
3. Execute o arquivo 'extractor.py' em um terminal.
4. Digite o link do site que contém as informações das feiras.
5. Digite o tipo de feira que deseja extrair.
6. Aguarde até que o processo de extração e salvamento seja concluído.
7. Os dados das feiras serão salvos em um arquivo JSON e também serão inseridos no banco de dados MongoDB.

Sinta-se à vontade para usar, modificar e contribuir para este projeto. Se você encontrar problemas ou tiver sugestões de melhoria, não hesite em abrir uma issue neste repositório.

