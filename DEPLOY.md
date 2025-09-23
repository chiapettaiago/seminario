# Deploy no Heroku - Apresentação de Inglês Online

## Arquivos de Configuração Criados

### 1. `Procfile`
Define como o Heroku deve executar a aplicação:
```
web: gunicorn app:app
```

### 2. `requirements.txt`
Lista as dependências Python necessárias:
```
Flask==3.0.0
gunicorn==21.2.0
Werkzeug==3.0.1
```

### 3. `runtime.txt`
Especifica a versão do Python:
```
python-3.12.3
```

### 4. `app.py` (modificado)
Ajustado para usar a porta dinâmica do Heroku e configuração de produção.

## Como fazer o deploy

### Pré-requisitos
1. Conta no Heroku (https://heroku.com)
2. Heroku CLI instalado (https://devcenter.heroku.com/articles/heroku-cli)
3. Git configurado no projeto

### Passos para deploy:

1. **Fazer login no Heroku**:
```bash
heroku login
```

2. **Criar aplicação no Heroku**:
```bash
heroku create nome-da-sua-app
```

3. **Adicionar arquivos ao Git**:
```bash
git add .
git commit -m "Configuração para deploy no Heroku"
```

4. **Fazer o deploy**:
```bash
git push heroku main
```

5. **Abrir a aplicação**:
```bash
heroku open
```

## Comandos úteis do Heroku

- Ver logs: `heroku logs --tail`
- Escalar dynos: `heroku ps:scale web=1`
- Ver status: `heroku ps`
- Executar comandos: `heroku run python`

## Estrutura final do projeto

```
seminario/
├── app.py              # Aplicação Flask principal
├── Procfile           # Configuração Heroku
├── requirements.txt   # Dependências Python
├── runtime.txt       # Versão Python
├── .gitignore        # Arquivos ignorados
├── routes/
│   └── main.py       # Rotas da aplicação
├── templates/
│   └── index.html    # Template da apresentação
└── static/
    ├── css/
    │   └── presentation.css
    └── js/
        └── presentation.js
```

## URL da aplicação
Após o deploy, sua aplicação estará disponível em:
`https://nome-da-sua-app.herokuapp.com`

## Troubleshooting

Se encontrar problemas:
1. Verifique os logs: `heroku logs --tail`
2. Confirme que todos os arquivos estão commitados
3. Verifique se o Procfile está na raiz do projeto
4. Confirme que requirements.txt tem todas as dependências