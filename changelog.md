

# Changelog


## [0.0.1] - 29/03/2025
- Adicionado: dockerfile
- Adicionado: Subdiretorio "views" em _api
- arquivo views.py -> Dividido em 4 arquivos diferentes: Auth, 


## [0.0.2] - 30/03/2025

### Modificações no módulo API
- Nono sub-módulo "services", contém serviços internos da API
- Novo sub-módulo "models", contém arquivos separando o contexto dos modelos -> credentials, proposta, usuario 
- Sub-módulo "views", mesma abordagem para separar o contexto das views em arquivos

#### proposta_views.py
- Lista todas as propostas
- Lista todas as propostas de um Cliente
- Obtém uma proposta via ID da proposta

#### usuario_views.py
- Cria um novo usuário -> salva o hash da senha na tabela de credenciais
- Autentica um usuário via email e senha
- Obtem um usuario por ID


## [0.0.3] - 01/04/2025

- Remoção de serviços nativos do Django: auth, sessions, content-type, CSRF-cookie
- Implementação de Middleware personalizado para autenticação de tokens
- Implementação de cache com memoria local -> futuramente implementar Redis
- 