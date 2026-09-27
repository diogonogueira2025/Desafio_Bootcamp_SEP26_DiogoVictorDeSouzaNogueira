# Reflexão

- **Por que citar a fonte?**
  A fonte permite que o colaborador confira a origem da resposta e consulte a seção completa da política. Neste projeto, indicar o documento e a seção, além do filtro de vigência, ajuda a evitar orientações baseadas em regras revogadas. Em uma empresa real, uma resposta sem referência tornaria a verificação difícil e poderia levar a pedidos de reembolso fora do prazo ou ao uso incorreto das regras de trabalho remoto. A citação facilita a verificação, mas não elimina a necessidade de buscar o trecho exato.


- **Qual foi a decisão mais difícil?**
  A decisão mais difícil foi escolher o threshold, porque ele decide quando responder e quando dizer que não se encontrou informação. Eu escolhi 0,30 depois de comparar os scores de P01 e P02, que tinham resposta e obtiveram 0,41 e 0,53, com o de P10, que pede uma informação que não está no corpus e teve 0,27. O assistente depois acertou as dez perguntas na avaliação, mas P04 ficou perto do limite, com 0,31. Isso mostra que o valor funciona para o gabarito, mas precisamos ter cuidado com novas perguntas: um limite alto pode rejeitar informações úteis, enquanto um limite baixo pode trazer uma política que não se relaciona bem com a dúvida.

- **O que mudaria com um LLM?**
  Na Parte 4, o modelo poderia criar uma resposta mais direta usando os trechos recuperados, mantendo a fonte e a regra de não encontrado. O novo risco seria criar detalhes que não existem ou mudar condições importantes da política. Por exemplo, se o modelo esquecer a exigência de aprovação para usar dados de clientes em ferramentas externas, poderia incentivar a exposição indevida dessas informações. Por isso, precisamos verificar a fidelidade das respostas aos documentos.
