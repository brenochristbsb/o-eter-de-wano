O ÉTER DE WANO — configuração para Render sem pasta handlers

ESTRUTURA
Envie todos os arquivos desta pasta para a raiz do repositório GitHub.
Os arquivos combat.py, explore.py, inventory.py, lore.py, menu.py, start.py e status.py
ficam no mesmo nível de main.py. A pasta data/ deve continuar existindo.

CONFIGURAÇÃO DO SERVIÇO WEB NO RENDER
- Runtime: Python
- Root Directory: deixe vazio (ou use o diretório raiz do repositório)
- Build Command: pip install -r requirements.txt
- Start Command: python main.py

VARIÁVEL DE AMBIENTE
Em Render > seu serviço > Environment, adicione:
Key: BOT_TOKEN
Value: token real do seu bot do Telegram (não publique no GitHub)

PUBLICAÇÃO
1. Faça backup do repositório atual.
2. Na raiz do repositório, envie os arquivos deste ZIP, mantendo a pasta data/.
3. Não coloque tudo dentro de uma pasta extra chamada seu_projeto.
4. Faça commit das alterações.
5. No Render, confirme os comandos acima e a variável BOT_TOKEN.
6. Selecione Manual Deploy > Deploy latest commit.
7. Consulte Logs. Se surgir outro traceback, corrija o novo erro conforme a mensagem.

NOTA
Este ZIP adapta as importações para os módulos na raiz e remove a dependência de handlers/.
Não é possível garantir funcionamento total sem testar com o token e o ambiente do Render.
