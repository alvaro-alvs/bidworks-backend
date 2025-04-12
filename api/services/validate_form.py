


CAMPOS_USUARIO = ['first_name', 'last_name', 'email', 'password']

CAMPOS_MODELO = ['first_name', 'last_name', 'email', 'telefone', 'dn', 'password']

#* Função de validação de formulario de Novo Usuário
def validateForm(body, required_fields=None, min_password_length=8):
    """
    Valida o payload do formulário com regras customizáveis.
    
    Args:
        body (dict): Dados do formulário a serem validados.
        required_fields (list): Campos obrigatórios (opcional, usa CAMPOS_USUARIO por padrão).
        min_password_length (int): Tamanho mínimo da senha (padrão: 8).
    
    Returns:
        tuple: (bool, str) -> (True, "") em caso de sucesso ou (False, "mensagem de erro") em falha.
    """
    if not body or not isinstance(body, dict):
        return False, "Payload inválido ou vazio"
    
    required_keys = required_fields if required_fields else CAMPOS_USUARIO
    
    # Verifica campos obrigatórios
    missing_fields = [key for key in required_keys if key not in body or not body[key]]
    
    if missing_fields:
        return False, f"Campos obrigatórios faltando: {', '.join(missing_fields)}"
    
    # Validação específica da senha
    if 'password' in body and len(body['password']) < min_password_length:
        return False, f"A senha deve ter no mínimo {min_password_length} caracteres"
    
    # Validação de e-mail (exemplo adicional)
    if 'email' in body and '@' not in body['email']:
        return False, "E-mail inválido"
    
    return True, ""