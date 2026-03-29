from pydantic import BaseSettings

class Settings(BaseSettings):
    database_hostname: str = "localhost"

print("Fields:", list(Settings.__fields__.keys()))
s = Settings()
print("Dict:", s.dict())
