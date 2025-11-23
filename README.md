# Aprenda Inglês Online

> Plataforma web gamificada criada para um seminário universitário em grupo, oferecendo uma trilha de 10 slides interativos para introdução ao inglês.

## Visão Geral
- Aplicação Flask com interface responsiva em tela cheia e estética futurista baseada em glassmorphism.
- Trilhas guiadas por slides com navegação por teclado, toques e botões; conteúdo inclui vocabulário, gramática, quizzes e exercícios drag-and-drop.
- Sistema de autenticação simples com registro/login, armazenamento de progresso, conquistas e estatísticas individuais.
- Persistência de dados em arquivos JSON para usuários e progresso, pensada para prototipagem acadêmica.
- Pronta para deploy em serviços estilo Heroku/Render por meio de `Procfile`, `runtime.txt` e `gunicorn`.

## Stack
- Python 3.12
- Flask 3.x + Werkzeug
- Jinja2 e templates HTML/CSS customizados
- JavaScript vanilla para animações, navegação e recursos interativos
- Font Awesome e Google Fonts (Poppins)

## Arquitetura em Alto Nível
- `app.py`: ponto de entrada Flask e registro das rotas.
- `routes/`: módulos que organizam regras de negócio (`main.py`) e autenticação (`auth.py`).
- `templates/`: base layout, páginas de progresso/perfil/login e 10 slides temáticos.
- `static/`: estilos (`presentation.css`) e scripts (`presentation.js`) para animações, swipe, speech synthesis e UX.
- `data/`: JSONs que armazenam usuários (senha com SHA-256) e progresso (slides concluídos, tempo, conquistas).

## Estrutura Resumida
```
seminario/
├─ app.py
├─ routes/
│  ├─ auth.py
│  └─ main.py
├─ templates/
│  ├─ base.html
│  ├─ lessons.html
│  ├─ progress.html
│  ├─ profile.html
│  └─ slides/slide1.html … slide10.html
├─ static/
│  ├─ css/presentation.css
│  └─ js/presentation.js
├─ data/users.json
├─ data/user_progress.json
├─ requirements.txt
├─ runtime.txt
└─ Procfile
```

## Slides Disponíveis
| Slide | Tema                               | Destaques principais                   |
|-------|------------------------------------|----------------------------------------|
| 1     | Boas-vindas                        | Objetivos do curso                     |
| 2     | Metodologia e plano de estudo      | Cronograma e abordagem                 |
| 3     | Vocabulário básico                 | Grade com áudio por speech synthesis   |
| 4     | Gramática – presente simples       | Exemplos guiados                       |
| 5     | Exercício drag-and-drop            | Feedback instantâneo                   |
| 6     | Frases essenciais                  | Botões com pronúncia                   |
| 7     | Números e cores                    | Cartas responsivas                     |
| 8     | Exercício interativo avançado      | Cards com hotspots                     |
| 9     | Prática de conversação             | Diálogo guiado                         |
| 10    | Conclusão                          | Mensagem final e CTA                   |
| 11    | Passive Voice - Voz Passiva        | Gramática avançada com exemplos técnicos |
| 12    | Conditional Sentences              | Condicionais com analogias de programação |
| 13    | Technical Vocabulary & False Friends | Vocabulário técnico e falsos cognatos   |

## Como Rodar Localmente
1. Garanta Python 3.12 instalado (`runtime.txt` define a versão).
2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Linux/Mac
   .venv\Scripts\activate      # Windows
   ```
3. Instale dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. (Opcional) Defina variáveis:
   ```bash
   export FLASK_ENV=development
   export SECRET_KEY="uma-chave-segura"
   ```
5. Inicie:
   ```bash
   python app.py
   ```
6. Acesse `http://localhost:8325`. Sem login, o usuário é levado ao Slide 1; com login, há acesso às páginas de lições, progresso e perfil.

## Persistência e Segurança
- Usuários e progresso ficam em `data/users.json` e `data/user_progress.json`. Em produção, substitua por um banco real (PostgreSQL, MongoDB etc.).
- Senhas são armazenadas com SHA-256; recomenda-se trocar por `werkzeug.security.generate_password_hash`.
- `SECRET_KEY` deve ser configurada via variável de ambiente no deploy.

## Deploy Rápido
- O projeto já traz `Procfile` (`web: gunicorn app:app`) e `runtime.txt` (Python 3.12.3) para plataformas compatíveis com buildpacks.
- Configure variáveis de ambiente (`SECRET_KEY`, `PORT`) na plataforma escolhida.
- Garanta permissão de escrita na pasta `data/` para persistir JSON durante o deploy.

## Trabalho em Equipe
- Centralize tarefas em board (Kanban/Trello) com colunas Ideias → Em andamento → Revisão → Concluído.
- Sugestão de papéis:
  - Conteúdo pedagógico: revisa slides e narrativa.
  - Front-end/UX: mantém visual consistente em `templates/` e `static/`.
  - Back-end/Integrações: cuida de rotas, progresso, melhorias de segurança.
  - QA/Apresentação: testa navegabilidade e prepara roteiro da apresentação.
- Antes de mergear alterações, rodar `python app.py` localmente e testar login, cadastro, navegação móvel e feedback de conquistas.

## Próximos Passos Recomendados
- Migrar dados para banco SQL ou Firebase.
- Implementar testes automatizados (Pytest) para rotas críticas.
- Adicionar relatórios mais ricos (gráficos) na página de progresso.
- Internacionalizar mensagens e conteúdos.
- Criar roteiro de apresentação destacando motivação, solução e resultados obtidos.

## Equipe
- Mauricio Neto
- Karina
- Miguel
- Iago Chiapetta

Boa apresentação! Ajustem livremente o texto para alinhar com as diretrizes da disciplina e o estilo do grupo.
