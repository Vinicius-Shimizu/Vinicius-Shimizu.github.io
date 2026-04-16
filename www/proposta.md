# Proposta

## Contexto
<p> Shogi é um jogo de estratégia japonês semelhante ao xadrez, que apresenta uma complexidade maior do que sua contraparte ocidental. Isso se deve principalmente a mecânicas como a reutilização de peças capturadas. Ao longo dos anos, ferramentas como o Lishogi surgiram com o intuito de facilitar o acesso ao aprendizado, permitindo partidas online ou resolução de problemas como formas de treino, focando no aprendizado por reforço. <p> 

## Motivação
<p>
O principal problema das atuais plataformas de Shogi voltadas ao aprendizado está na abordagem de ensino adotada. Como o foco destas ferramentas está apenas na prática, não costumam oferecer material de estudo ou alguma orientação concreta a respeito dos erros cometidos e como corrigi-los. Dessa forma, jogadores iniciantes podem ter dificuldade em compreender conceitos fundamentais, tornando o processo de aprendizado mais lento e potencialmente levando à frustração e ao abandono do jogo.
<p>

## Objetivo
<p>
Este trabalho, portanto, tem como objetivo desenvolver uma ferramenta de apoio ao ensino do shogi voltada para iniciantes. O sistema proposto organiza o conteúdo em etapas, abordando desde a movimentação das peças até conceitos estratégicos básicos, como aberturas e defesas. Além disso, o usuário receberá feedback sobre seu desempenho de forma clara e visual, enquanto o sistema sugere exercícios de acordo com as dificuldades identificadas, promovendo um aprendizado mais orientado e eficiente.
<p>

## Metodologia
<p>
A biblioteca do Python denominada cshogi, em conjunto com partidas reais, será utilizada para a obtenção de diferentes posições de jogo. Para a geração das soluções desses exercícios, será utilizada uma engine especializada, Yaneuraou, capaz de avaliar posições e sugerir as melhores jogadas. Para exercícios mais básicos, as soluções poderão ser definidas manualmente.
<p>
<p>
As questões serão organizadas por temas, como "Movimentação", "Regras", "Aberturas" e "Defesas", e apresentarão tanto aspectos práticos quanto teóricos, exigindo que o usuário escolha jogadas corretas ou identifique a estratégia utilizada. Cada tema será desbloqueado a partir de uma pontuação mínima no tema anterior, promovendo uma progressão gradual e compatível com o nível do jogador.
<p>
<p>
O progresso do usuário será avaliado com base em métricas como taxa de acerto ao longo de um número determinado de tentativas, de forma a reduzir a influência de respostas aleatórias. Além disso, outras métricas, como tempo médio de resposta e desempenho por categoria, serão utilizadas para analisar o aprendizado do usuário.
<p>
<p>
Para avaliar o desempenho da abordagem apresentada neste trabalho, um grupo de 10-20 pessoas utilizará o sistema por 1-2 semanas. As informações coletadas serão armazenadas num banco de dados, local ou na nuvem, para acompanhar a evolução deste grupo e a eficácia do método adotado. 
<p>
## Cronograma