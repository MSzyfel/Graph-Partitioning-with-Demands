@echo off
setlocal enabledelayedexpansion

:: Sprawdzenie czy istnieje poster.tex
IF NOT EXIST poster.tex (
    echo Plik poster.tex nie istnieje w tym katalogu!
    exit /b
)

:loop
    echo.
    echo ==============================
    echo Kompilacja pdfLaTeX (1/4)...
    pdflatex -interaction=nonstopmode poster.tex

    echo Uruchamianie BibTeX (2/4)...
    bibtex poster

    echo Kompilacja pdfLaTeX (2/4)...
    pdflatex -interaction=nonstopmode poster.tex

    echo Kompilacja pdfLaTeX (3/4)...
    pdflatex -interaction=nonstopmode poster.tex

    echo Kompilacja zakonczona.
    echo ==============================
    echo.

    :: Sprawdź czy user cos kliknął
    choice /c CQ /n /t 0 /d C >nul
    if errorlevel 2 (
        echo Wykryto zadanie zamkniecia. Koniec.
        exit /b
    )

goto loop
