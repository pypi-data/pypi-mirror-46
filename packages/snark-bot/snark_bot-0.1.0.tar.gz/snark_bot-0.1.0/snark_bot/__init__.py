from smart_getenv import getenv
from dotenv import load_dotenv


load_dotenv()

if not getenv("IS_PROD", type=bool):
    import stackprinter

    stackprinter.set_excepthook(style="color")
