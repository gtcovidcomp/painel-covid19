# COVID-19-Macae
Código do painel para visualização de dados de COVID-19 no endereço https://painelcovid19.macae.ufrj.br/

## Instruções de Uso
Para rodar o painel localmente, é preciso ter Python versão 3.6 ou maior instalado no computador. Os módulos e suas versões necessários para o painel estão listadas no arquivo `requirements.txt` e podem ser instaladas com o comando `pip install -r requirements.txt` no terminal.

Com o python e os módulos já instalados, basta inserir o comando `python index.py` para inicial o painel.

### Configurar e-mail de mensagem de erros
O código tem a possibilidade de enviar e-mails (por uma conta gmail) com as mensagens de erro que ocorreram no programa.

Para isso, é necessário [ativar o API do gmail](https://developers.google.com/gmail/api/quickstart/python) e [permitir acesso a arquivos menos seguros à sua conta](https://myaccount.google.com/security).

Em seguida, deve-se editar o código no arquivo `/data/send_email.py`, apagando o `#` nas linhas abaixo, inserindo (entre aspas simples) o login e senha do e-mail remetente na primeira linha e os e-mails destinatários (também entre aspas simples), separados por vírgulas, na segunda linha.
```
#email_from = {'login':'email@gmail.com','password':'senha_do_email'}
#emails_to = ['email@exemplo.com','email2@exemplo.com']
```

## Sobre
O Painel Covid-19 foi desenvolvido pelo Grupo de Trabalho Computação e Saúde que se originou com a parceria entre professores da UFRJ – Campus Macaé e da UFF – Campus Rio das Ostras que atuam de maneira direta ou indireta na área de computação, para oferecer soluções no enfrentamento da pandemia do COVID19. Atualmente o grupo Informação em Saúde e é um subgrupo do Grupo de Trabalho Multidisciplinar para o enfrentamento da COVID 19 (GT COVID 19 UFRJ MACAÉ).

Os dados utilizados são coletados diariamente no Painel Coronavírus do Ministério da Saúde e nos boletins e informes publicados nos sites e nas páginas oficiais do Facebook e Instagram das prefeituras. Os dados são tabulados de acordo com a data de publicação dos Boletins e informes.

Os dados sobre o isolamento são gentilmente fornecidos pela empresa InLoco (www.inloco.com.br).

Os dados de população de cada cidade, utilizados para calcular as Taxas de Incidência e Letalidade foram retirados do site do IBGE, e referem-se à população estimada para 2019.

### Equipe Responsável Pelo Projeto
Profa. Janaína Sant’Anna Gomide Gomes (UFRJ)
Prof. Matheus Ferreira de Barros (UFRJ)
Profa. Fernanda Teles Morais do Nascimento (UFRJ)
Profa Karla Santa Cruz Coelho (UFRJ)
Profa. Leila Weitzel (UFF)
Prof. Carlos Bazilio Martins (UFF)
Prof.ª Laura Emmanuella Alves dos Santos Santana (UFRJ)
Prof. Leonardo de Oliveira Carvalho (UFF)
André Branco de Menezes Rafael da Silva (Engenharia - UFRJ)
Isabelle Cristina Antunes Thomaz (Engenharia - UFRJ)

## Contato
gtcovidufrjmacae@gmail.com
