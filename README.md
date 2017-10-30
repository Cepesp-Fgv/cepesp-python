# cepesp-python 
Api python para acessar dados do TSE *_<Python 2.7>_*

[Clique para ver exemplos](examples/examples.ipynb)

## Sobre a API interna do CEPESPdata
Esta biblioteca se comunica com nossa API CEPESPdata. O repositório de dados foi totalmente extraído da base dados do TSE, pós-processada e organizada usando HiveQL e Pandas (Biblioteca Python). Além disso também é utilizado um cache interno à API que minimiza o tempo de resposta para consultas previamente feitas.
