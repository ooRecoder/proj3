@echo off
setlocal

echo ================================
echo Criando ambiente virtual...
echo ================================

REM Verifica se o Python está disponível
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERRO: Python não encontrado no PATH.
    pause
    exit /b 1
)

REM Cria o ambiente virtual
python -m venv venv
if %ERRORLEVEL% NEQ 0 (
    echo ERRO: Falha ao criar o ambiente virtual.
    pause
    exit /b 1
)

echo ================================
echo Ativando ambiente virtual...
echo ================================

REM Verifica se o script de ativação existe
if not exist "venv\Scripts\activate.bat" (
    echo ERRO: Script de ativação não encontrado. Algo deu errado na criação do ambiente.
    pause
    exit /b 1
)

call venv\Scripts\activate.bat

if errorlevel 1 (
    echo ERRO: Falha ao ativar o ambiente virtual.
    pause
    exit /b 1
)

echo ================================
echo Instalando dependências...
echo ================================

REM Verifica se requirements.txt existe
if not exist "requirements.txt" (
    echo AVISO: O arquivo requirements.txt não foi encontrado. Nenhum pacote sera instalado.
) else (
    pip install --upgrade pip
    pip install -r requirements.txt

    if %ERRORLEVEL% NEQ 0 (
        echo ERRO: Falha na instalação das dependências.
        pause
        exit /b 1
    )
)

echo ================================
echo Ambiente configurado com sucesso!
echo ================================

pause
exit /b 0
