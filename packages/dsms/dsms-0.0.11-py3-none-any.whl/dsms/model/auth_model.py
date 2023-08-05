class AuthModel:
  def __init__(self):
    self.user_tokens = {}

  def register(self, token):
    self.user_tokens[token] = token

  def is_exist(self, token):
    return token in self.user_tokens
