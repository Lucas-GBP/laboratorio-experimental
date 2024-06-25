# Laboratório de Física Experimental

## Notebook enviroment
Para começar a usar os notebooks, primeiro você deve ter instalado no seu computador a ferramenta [Poetry](https://python-poetry.org/), usada para gerenciar os pacotes e bibliotecas do projeto em python.

Após instalado, execute os seguintes comandos:
```bash
poetry install
poetry run ipython kernel install --user --name=fisica-experimental
poetry run jupyter notebook
```

Por fim, use sua IDE de preferência para usar os notebooks, seja o próprio navegador ou o vscode, por exemplo. Apenas lembre que ser for usar uma Ide é necessário dizer qual kernel você estará usando para executar o notebook, nesse caso "fisica-experimental".
