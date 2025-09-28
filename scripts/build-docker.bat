@echo off
setlocal enabledelayedexpansion

REM Build script for OpenAvatarChat Docker images (Windows)
REM Usage: build-docker.bat [avatar|lam|both] [tag_suffix]

REM Default values
set "IMAGE_TYPE=%~1"
set "TAG_SUFFIX=%~2"
if "%IMAGE_TYPE%"=="" set "IMAGE_TYPE=both"
if "%TAG_SUFFIX%"=="" set "TAG_SUFFIX=latest"
if "%REGISTRY%"=="" set "REGISTRY=ghcr.io"

REM Get repository name from current directory
for %%I in ("%CD%") do set "REPO_NAME=%%~nI"
if "%REPO_NAME%"=="" set "REPO_NAME=open-avatar-chat"

echo [INFO] Starting Docker build process...
echo [INFO] Image Type: %IMAGE_TYPE%
echo [INFO] Tag Suffix: %TAG_SUFFIX%
echo [INFO] Registry: %REGISTRY%
echo [INFO] Repository: %REPO_NAME%

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker is not running. Please start Docker and try again.
    exit /b 1
)

REM Validate IMAGE_TYPE
if not "%IMAGE_TYPE%"=="avatar" if not "%IMAGE_TYPE%"=="lam" if not "%IMAGE_TYPE%"=="both" (
    echo [ERROR] Invalid image type: %IMAGE_TYPE%
    echo [ERROR] Valid options: avatar, lam, both
    exit /b 1
)

REM Check if required config files exist
if "%IMAGE_TYPE%"=="avatar" goto :check_avatar
if "%IMAGE_TYPE%"=="both" goto :check_avatar
goto :check_lam

:check_avatar
if not exist "config\chat_with_dify.yaml" (
    echo [ERROR] Avatar config file not found: config\chat_with_dify.yaml
    exit /b 1
)
if "%IMAGE_TYPE%"=="avatar" goto :build_avatar

:check_lam
if "%IMAGE_TYPE%"=="lam" goto :check_lam_file
if "%IMAGE_TYPE%"=="both" goto :check_lam_file
goto :build_avatar

:check_lam_file
if not exist "config\chat_with_lam_dify.yaml" (
    echo [ERROR] LAM config file not found: config\chat_with_lam_dify.yaml
    exit /b 1
)

:build_avatar
if "%IMAGE_TYPE%"=="lam" goto :build_lam
echo [INFO] Building Avatar (Dify) image...
set "AVATAR_TAG=%REGISTRY%/%REPO_NAME%-avatar:%TAG_SUFFIX%"

docker build --build-arg CONFIG_FILE=config/chat_with_dify.yaml -t "%AVATAR_TAG%" -f Dockerfile .
if errorlevel 1 (
    echo [ERROR] Failed to build Avatar image
    exit /b 1
)

echo [SUCCESS] Successfully built Avatar image: %AVATAR_TAG%

REM Ask if user wants to push
set /p "PUSH_AVATAR=Do you want to push Avatar image to registry? (y/N): "
if /i "%PUSH_AVATAR%"=="y" (
    echo [INFO] Pushing Avatar image to registry...
    docker push "%AVATAR_TAG%"
    if errorlevel 1 (
        echo [ERROR] Failed to push Avatar image
    ) else (
        echo [SUCCESS] Successfully pushed Avatar image
    )
)

if "%IMAGE_TYPE%"=="avatar" goto :summary

:build_lam
echo [INFO] Building LAM (Dify) image...
set "LAM_TAG=%REGISTRY%/%REPO_NAME%-lam:%TAG_SUFFIX%"

docker build --build-arg CONFIG_FILE=config/chat_with_lam_dify.yaml -t "%LAM_TAG%" -f Dockerfile .
if errorlevel 1 (
    echo [ERROR] Failed to build LAM image
    exit /b 1
)

echo [SUCCESS] Successfully built LAM image: %LAM_TAG%

REM Ask if user wants to push
set /p "PUSH_LAM=Do you want to push LAM image to registry? (y/N): "
if /i "%PUSH_LAM%"=="y" (
    echo [INFO] Pushing LAM image to registry...
    docker push "%LAM_TAG%"
    if errorlevel 1 (
        echo [ERROR] Failed to push LAM image
    ) else (
        echo [SUCCESS] Successfully pushed LAM image
    )
)

:summary
echo.
echo [SUCCESS] All builds completed successfully!
echo.
echo [INFO] Built images:
if "%IMAGE_TYPE%"=="avatar" echo   - %REGISTRY%/%REPO_NAME%-avatar:%TAG_SUFFIX%
if "%IMAGE_TYPE%"=="lam" echo   - %REGISTRY%/%REPO_NAME%-lam:%TAG_SUFFIX%
if "%IMAGE_TYPE%"=="both" (
    echo   - %REGISTRY%/%REPO_NAME%-avatar:%TAG_SUFFIX%
    echo   - %REGISTRY%/%REPO_NAME%-lam:%TAG_SUFFIX%
)
echo.
echo [INFO] Usage examples:
if "%IMAGE_TYPE%"=="avatar" echo   docker run --rm --gpus all -p 8282:8282 %REGISTRY%/%REPO_NAME%-avatar:%TAG_SUFFIX%
if "%IMAGE_TYPE%"=="lam" echo   docker run --rm --gpus all -p 8282:8282 %REGISTRY%/%REPO_NAME%-lam:%TAG_SUFFIX%
if "%IMAGE_TYPE%"=="both" (
    echo   docker run --rm --gpus all -p 8282:8282 %REGISTRY%/%REPO_NAME%-avatar:%TAG_SUFFIX%
    echo   docker run --rm --gpus all -p 8283:8282 %REGISTRY%/%REPO_NAME%-lam:%TAG_SUFFIX%
)

endlocal
exit /b 0
