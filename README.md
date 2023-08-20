#Smart Cars
Projeto de desenvolvimento de uma Rede Neural Artificial criada para aprender a pilotar os carros dentro do jogo, criado utilizando a biblioteca PyGame do Python.

![](https://github.com/VitorMarinheiro/SmartCars/blob/main/assets/running.gif)

## Execução
Para realizar a execução do jogo basta utilizar o seguinte comando:

`python3 main.py`

## Configurações adicionais de Execução
O projeto contém o arquivo `config.properties` com alguns campos que servem como parâmetro para a execução da rede neural e do jogo.
Você pode editar os valores e analisar como a rede neural se comporta em cada cenário.

```
[geracoes]
population=250      <- Quantidade de indivíduos que serão treinados em cada geração.
learningRate=0.2   <- Taxa de Aprendizagem dos indivíduos, quanto maior, mais diferente serao os indivíduos da próxima geraçao.

[pygame]
track=course       <- Nome do percurso que será carregado na pasta de assets. [obstacle_course ou course]
fps=60             <- Taxa de atualização de frames do PyGame.

```
