from cx_Freeze import setup, Executable

setup(
    name="Nom_de_votre_application",
    version="1.0",
    description="Description de votre application",
    executables=[Executable("interface.py")]
)
