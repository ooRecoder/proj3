@echo off
echo Criando ambiente virtual...
python -m venv venv

echo Ativando ambiente...
call venv\Scripts\activate

echo Instalando dependências...
pip install -r requirements.txt

echo Instalação concluída.
pause
