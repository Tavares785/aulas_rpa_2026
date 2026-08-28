BOT_NAME = "CyberBot"
MAX_RETRIES = 5
EXECUTION_TIMEOUT = 30.0
IS_PRODUCTION = False

print("======== Inicializacao do bot =====================================")
print(f"{'BOT_NAME':<20} {BOT_NAME!s:<25} {type(BOT_NAME).__name__}")
print(f"{'MAX_RETRIES':<20} {MAX_RETRIES!s:<25} {type(MAX_RETRIES).__name__}")
print(f"{'EXECUTION_TIMEOUT':<20} {EXECUTION_TIMEOUT!s:<25} {type(EXECUTION_TIMEOUT).__name__}")
print(f"{'IS_PRODUCTION':<20} {IS_PRODUCTION!s:<25} {type(IS_PRODUCTION).__name__}")
print("===================================================================")