#NoEnv
#Persistent
#SingleInstance Force
SetWorkingDir %A_ScriptDir%
SendMode Input
SetTitleMatchMode 2

; ===== CONFIG =====
python_exe     := A_ScriptDir "\python-capado\python.exe"
stateFile      := A_ScriptDir "\cinhud_state.txt"
tf2StateFile   := A_ScriptDir "\tf2state.txt"

; ===== STATE =====
gameWasRunning := false
revertExecuted := false

; Hotkey inicia desabilitada
Hotkey, +g, ToggleCinhud, Off

; Primeira checagem imediata + timer
Gosub, PollTF2
SetTimer, PollTF2, 12000
return

; ===== TIMER =====
PollTF2:
    isRunning := IsTF2Running()

    ; TF2 acabou de abrir
    if (isRunning && !gameWasRunning) {
        Hotkey, +g, ToggleCinhud, On
        revertExecuted := false
        WriteTF2State("running")
        TrayTip, Cinhud, HUD Toggle ativado (Shift + G), 3
    }
    ; TF2 acabou de fechar
    else if (!isRunning && gameWasRunning) {
        Hotkey, +g, ToggleCinhud, Off
        if (!revertExecuted) {
            RunPy("revert.py")
            revertExecuted := true
            WriteTF2State("closed_and_reverted")

            ; Sincroniza o cinhud_state.txt para 0
            if (FileExist(stateFile))
                FileDelete, %stateFile%
            FileAppend, 0, %stateFile%

            TrayTip, Cinhud, TF2 fechado — revert aplicado e estado=0., 3
            Send, {F11}
        }
    }
    ; Estados estáveis (opcional: manter log atualizado)
    else {
        if (isRunning) {
            WriteTF2State("running")
        } else {
            if (revertExecuted)
                WriteTF2State("closed_and_reverted")
            else
                WriteTF2State("closed")
        }
    }

    gameWasRunning := isRunning
return

; ===== HOTKEY =====
ToggleCinhud:
    currentState := ReadState(stateFile, "0")
    if (currentState = "0") {
        RunPy("addtogame.py")
        FileDelete, %stateFile%
        FileAppend, 1, %stateFile%
        TrayTip, Cinhud, HUD ativado, 2
    } else {
        RunPy("revert.py")
        FileDelete, %stateFile%
        FileAppend, 0, %stateFile%
        TrayTip, Cinhud, HUD desativado, 2
    }
    Send, {F11}
return

; ===== FUNÇÕES =====
IsTF2Running() {
    Process, Exist, tf.exe
    pid := ErrorLevel
    if (!pid) {
        Process, Exist, tf_win64.exe
        pid := ErrorLevel
    }
    return !!pid
}

RunPy(script) {
    global python_exe
    ; Garante aspas corretas e usa a pasta do script como CWD
    cmd := """" . python_exe . """ " . script
    RunWait, %cmd%, %A_ScriptDir%, Hide
}

ReadState(file, default) {
    if !FileExist(file)
        return default
    FileRead, content, %file%
    return Trim(content)
}

WriteTF2State(text) {
    global tf2StateFile
    FileDelete, %tf2StateFile%
    FileAppend, %text%, %tf2StateFile%
}
