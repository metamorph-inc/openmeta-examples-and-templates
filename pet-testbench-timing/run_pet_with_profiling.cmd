rem Run from a PET's results directory to run the PET with profiling enabled

FOR /F "skip=2 tokens=2,*" %%A IN ('C:\Windows\SysWoW64\REG.exe query "HKLM\software\META" /v "META_PATH"') DO set META_PATH=%%B
set META_PYTHON_PATH="%META_PATH%\bin\Python311\Python.exe"

%META_PYTHON_PATH% -m run_mdao --profile