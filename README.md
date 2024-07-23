# Tutorial para o Script de Empilhamento de Vídeos

Este script processa vídeos empilhando dois vídeos verticalmente e mantém o áudio do vídeo de cima. A seguir, um guia completo para configurar e executar o script.

## Requisitos

Antes de começar, certifique-se de que você tem os seguintes requisitos instalados:

1. **Python 3.x**: O script foi desenvolvido para Python 3.x. Você pode baixar o Python [aqui](https://www.python.org/downloads/).
 2. **Pacotes Python**: O script utiliza pacotes Python externos que precisam ser instalados. Você pode instalar todos os pacotes necessários usando o `pip`. Execute o seguinte comando no terminal ou prompt de comando:
`pip install opencv-python numpy`
3.  **FFmpeg**: O FFmpeg é uma ferramenta de linha de comando para processar vídeo e áudio. Baixe e instale o FFmpeg [aqui](https://ffmpeg.org/download.html) e adicione o caminho do executável (`ffmpeg.exe`) ao seu PATH do sistema.

## Preparação do Ambiente

### Estrutura de Diretórios

Certifique-se de que a estrutura de diretórios do projeto seja semelhante à seguinte:

    project-directory/
    │
    ├── video-input/
    │   ├── 1/
    │   │   ├── video1.mp4
    │   │   └── video2.mp4
    │   ├── 2/
    │   │   ├── video3.mp4
    │   │   └── video4.mp4
    │   └── ...  # Outras pastas com vídeos a serem processados
    │
    ├── video-output/
    │   # Vídeos processados serão salvos aqui
    │
    ├── stack_videos.py  # O script Python
    │
    └── run_stack_videos.bat  # Arquivo para executar o script automaticamente

### Configuração do Script

### Localize o Caminho do FFmpeg

Atualize o caminho do FFmpeg no script. No script, `ffmpeg_path` está definido como:
`ffmpeg_path = "C:\\ffmpeg\\bin\\ffmpeg.exe"` 

Certifique-se de que este caminho aponte para o executável `ffmpeg.exe` em seu sistema.

## Executando o Script

### Usando o Arquivo `.bat`

Para facilitar a execução do script, você pode usar o arquivo `run_stack_videos.bat`. Este arquivo configura o caminho do interpretador Python e o caminho para o script Python.

O conteúdo do `run_stack_videos.bat` é o seguinte:

`@echo off
REM Defina o caminho do interpretador Python
set PYTHON_PATH=C:\path\to\your\python.exe

REM Execute o script Python
%PYTHON_PATH% stack_videos.py

pause` 

Para usar o `run_stack_videos.bat`:

1.  **Navegue até o Diretório do Projeto**: Abra o terminal ou prompt de comando e navegue até o diretório onde o arquivo `run_stack_videos.bat` está localizado:

    `cd /caminho/para/o/diretório/do/projeto` 
    
2.  **Execute o Script**: Execute o arquivo `.bat`:
    
    `run_stack_videos.bat` 
    
O script processará todos os vídeos nas subpastas da pasta `video-input` e salvará os vídeos processados na pasta `video-output`.

## Personalização

Você pode personalizar o script conforme necessário:

-   **Tamanho do Vídeo**: Modifique as funções `resize_frame` e `adjust_fps` para ajustar a resolução dos vídeos.
-   **Configurações do FFmpeg**: Altere os parâmetros no comando FFmpeg dentro do script para ajustar a codificação do vídeo e do áudio conforme necessário.

## Suporte

Se você encontrar problemas ou tiver dúvidas sobre o script, sinta-se à vontade para abrir um problema no repositório do projeto ou entrar em contato com o desenvolvedor.

Este `README.md` fornece um guia detalhado sobre como configurar e executar o script de empilhamento de vídeos, incluindo a estrutura de diretórios, requisitos, configuração do script, e personalizações.
