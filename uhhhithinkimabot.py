import React, { useState, useEffect } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Copy, Code, Play, Save, RefreshCw } from 'lucide-react';

const CodeGenerator = () => {
  const [language, setLanguage] = useState('ahk');
  const [category, setCategory] = useState('game');
  const [description, setDescription] = useState('');
  const [generatedCode, setGeneratedCode] = useState('');
  const [copied, setCopied] = useState(false);
  const [preview, setPreview] = useState(false);

  const languages = [
    { value: 'ahk', label: 'AutoHotkey', categories: ['game', 'hotkey', 'gui', 'automation'] },
    { value: 'html', label: 'HTML', categories: ['webpage', 'form', 'component'] },
    { value: 'javascript', label: 'JavaScript', categories: ['function', 'class', 'game'] },
    { value: 'python', label: 'Python', categories: ['script', 'automation', 'game'] }
  ];

  const codeTemplates = {
    ahk: {
      game: {
        basic: `#SingleInstance Force
#NoEnv
SetWorkingDir %A_ScriptDir%
#MaxThreadsPerHotkey 2
CoordMode, Pixel, Screen
CoordMode, Mouse, Screen

; Configuration
global isRunning := false
global pauseScript := false
global gameConfig := {}

; Hotkeys
F7::ToggleScript()
F8::PauseScript()
F9::RecordPosition()
^r::ReloadScript()

ToggleScript() {
    global isRunning
    isRunning := !isRunning
    ShowStatus("Script " . (isRunning ? "Started" : "Stopped"))
    if (isRunning)
        SetTimer, MainGameLoop, 50
    else
        SetTimer, MainGameLoop, Off
}

PauseScript() {
    global pauseScript
    pauseScript := !pauseScript
    ShowStatus("Script " . (pauseScript ? "Paused" : "Resumed"))
}

MainGameLoop:
{
    if (!isRunning || pauseScript)
        return
    
    try {
        GameAction()
        ApplyAntiDetection()
    } catch e {
        LogError(e)
    }
    return
}

GameAction() {
    MouseGetPos, mouseX, mouseY
    PixelGetColor, color, %mouseX%, %mouseY%
    
    if (CheckPixelColor(100, 100, 0xFF0000)) {
        SmartClick(100, 100)
        Sleep, % Random(500, 1000)
    }
}

ApplyAntiDetection() {
    Random, delay, 50, 150
    Sleep, %delay%
    
    if (Mod(A_TickCount, 10000) < 100) {
        HumanMouseMovement()
    }
}

HumanMouseMovement() {
    MouseGetPos, startX, startY
    Random, endX, 0, A_ScreenWidth
    Random, endY, 0, A_ScreenHeight
    
    SmoothMouseMove(startX, startY, endX, endY)
}

SmoothMouseMove(startX, startY, endX, endY) {
    steps := 10
    stepX := (endX - startX) / steps
    stepY := (endY - startY) / steps
    
    Loop, %steps% {
        currentX := startX + (A_Index * stepX)
        currentY := startY + (A_Index * stepY)
        MouseMove, %currentX%, %currentY%, 2
        Sleep, 10
    }
}

ShowStatus(message) {
    ToolTip, %message%
    SetTimer, RemoveToolTip, -1000
}

RemoveToolTip:
ToolTip
return`,
        advanced: `#SingleInstance Force
#NoEnv
SetWorkingDir %A_ScriptDir%
#MaxThreadsPerHotkey 2
CoordMode, Pixel, Screen
CoordMode, Mouse, Screen

; Advanced Configuration
global CONFIG := {}
CONFIG.DELAYS := {MIN: 800, MAX: 2000}
CONFIG.MOUSE := {SPEED_MIN: 2, SPEED_MAX: 8}
CONFIG.PATTERNS := []
CONFIG.ANTI_DETECTION := true

; GUI Creation
CreateGUI()
LoadSettings()

; Advanced Hotkey System
#if WinActive("ahk_exe YourGame.exe")
    F7::ToggleScript()
    F8::PauseScript()
    F9::RecordPattern()
    ^r::ReloadScript()
#if

class GameAutomation {
    __New() {
        this.running := false
        this.paused := false
        this.patterns := []
        this.currentPattern := 1
    }
    
    Toggle() {
        this.running := !this.running
        if (this.running)
            this.StartMainLoop()
        else
            this.StopMainLoop()
    }
    
    StartMainLoop() {
        SetTimer, MainGameLoop, 50
    }
    
    StopMainLoop() {
        SetTimer, MainGameLoop, Off
    }
    
    ExecutePattern() {
        if (this.patterns.Length() = 0)
            return
            
        pattern := this.patterns[this.currentPattern]
        this.ExecuteSinglePattern(pattern)
        
        this.currentPattern := Mod(this.currentPattern, this.patterns.Length()) + 1
    }
    
    ExecuteSinglePattern(pattern) {
        switch pattern.type {
            case "click":
                this.SmartClick(pattern.x, pattern.y)
            case "move":
                this.HumanMouseMove(pattern.x, pattern.y)
            case "key":
                this.SendKey(pattern.key)
        }
    }
    
    SmartClick(x, y) {
        this.HumanMouseMove(x, y)
        Random, delay, 50, 150
        Sleep, %delay%
        Click
    }
    
    HumanMouseMove(targetX, targetY) {
        MouseGetPos, startX, startY
        points := this.GenerateBezierPoints(startX, startY, targetX, targetY)
        
        for index, point in points {
            if (!this.running || this.paused)
                return
                
            MouseMove, % point.x, % point.y, 2
            Sleep, 10
        }
    }
    
    GenerateBezierPoints(startX, startY, endX, endY) {
        points := []
        
        Random, ctrlX1, % Min(startX, endX), % Max(startX, endX)
        Random, ctrlY1, % Min(startY, endY), % Max(startY, endY)
        Random, ctrlX2, % Min(startX, endX), % Max(startX, endX)
        Random, ctrlY2, % Min(startY, endY), % Max(startY, endY)
        
        steps := 20
        Loop, %steps% {
            t := A_Index / steps
            
            x := (1-t)**3 * startX + 3*(1-t)**2 * t * ctrlX1 + 3*(1-t) * t**2 * ctrlX2 + t**3 * endX
            y := (1-t)**3 * startY + 3*(1-t)**2 * t * ctrlY1 + 3*(1-t) * t**2 * ctrlY2 + t**3 * endY
            
            points.Push({x: Round(x), y: Round(y)})
        }
        
        return points
    }
    
    SendKey(key) {
        if (this.running && !this.paused) {
            Random, delay, 50, 150
            Sleep, %delay%
            Send, {%key%}
        }
    }
}

; Create instance
global GAME := new GameAutomation()

CreateGUI() {
    Gui, Main:New, +AlwaysOnTop +ToolWindow
    Gui, Main:Add, GroupBox, x5 y5 w290 h60, Status
    Gui, Main:Add, Text, x15 y25 w270 vStatusText, Ready
    
    Gui, Main:Add, GroupBox, x5 y70 w290 h120, Settings
    Gui, Main:Add, Checkbox, x15 y90 vAntiDetection gSaveSettings, Enable Anti-Detection
    Gui, Main:Add, Text, x15 y115, Min Delay:
    Gui, Main:Add, Edit, x80 y112 w50 vMinDelay, 800
    Gui, Main:Add, Text, x140 y115, Max Delay:
    Gui, Main:Add, Edit, x205 y112 w50 vMaxDelay, 2000
    
    Gui, Main:Add, ListView, x5 y200 w290 h100 vPatternList, Time|Type|X|Y|Key
    
    Gui, Main:Show,, Game Automation
}

MainGameLoop:
GAME.ExecutePattern()
return`
      },
      gui: `#SingleInstance Force
#NoEnv
SetWorkingDir %A_ScriptDir%

; Create main GUI
Gui, Main:New, +AlwaysOnTop +Resize
Gui, Main:Add, Tab3,, General|Settings|Patterns

; General Tab
Gui, Tab, 1
Gui, Main:Add, GroupBox, x10 y30 w280 h190, Controls
Gui, Main:Add, Button, x20 y50 w120 h30 gStartScript, Start
Gui, Main:Add, Button, x150 y50 w120 h30 gStopScript, Stop
Gui, Main:Add, Text, x20 y90, Status:
Gui, Main:Add, Edit, x20 y110 w260 h100 vStatusBox ReadOnly

; Settings Tab
Gui, Tab, 2
Gui, Main:Add, GroupBox, x10 y30 w280 h190, Configuration
Gui, Main:Add, Checkbox, x20 y50 vAntiDetection, Enable Anti-Detection
Gui, Main:Add, Text, x20 y80, Delay (ms):
Gui, Main:Add, Edit, x100 y77 w60 vDelay, 1000
Gui, Main:Add, Button, x20 y110 w120 h30 gSaveSettings, Save
Gui, Main:Add, Button, x150 y110 w120 h30 gLoadSettings, Load

; Patterns Tab
Gui, Tab, 3
Gui, Main:Add, ListView, x10 y30 w280 h150 vPatternList, Time|Action|X|Y
Gui, Main:Add, Button, x10 y190 w135 h30 gRecordPattern, Record
Gui, Main:Add, Button, x155 y190 w135 h30 gClearPatterns, Clear

Gui, Main:Show, w300 h250, Automation Control

return

GuiClose:
ExitApp

StartScript:
{
    GuiControl,, StatusBox, Script started...
    return
}

StopScript:
{
    GuiControl,, StatusBox, Script stopped.
    return
}

SaveSettings:
{
    Gui, Submit, NoHide
    SaveToFile()
    return
}

LoadSettings:
{
    LoadFromFile()
    return
}

RecordPattern:
{
    GuiControl,, StatusBox, Recording pattern...
    return
}

ClearPatterns:
{
    LV_Delete()
    return
}`,
      hotkey: `#SingleInstance Force
#NoEnv
SetWorkingDir %A_ScriptDir%

; Configuration
global HOTKEYS := {}
global ENABLED := true

; Initialize hotkeys
InitializeHotkeys()

InitializeHotkeys() {
    ; Gaming hotkeys
    Hotkey, ~LButton, GameClick
    Hotkey, ~RButton, GameRightClick
    Hotkey, ~Space, GameJump
    
    ; Function keys
    Hotkey, F1, QuickHeal
    Hotkey, F2, QuickBuff
    Hotkey, F3, QuickItem
    Hotkey, F4, QuickSpell
    
    ; Combo keys
    Hotkey, ^q, Combo1  ; Ctrl+Q
    Hotkey, ^e, Combo2  ; Ctrl+E
    Hotkey, ^r, Combo3  ; Ctrl+R
    
    ; Toggle key
    Hotkey, ^F12, ToggleScript  ; Ctrl+F12
}

; Action handlers
GameClick:
{
    if (!ENABLED)
        return
    
    ; Add click enhancement logic here
    return
}

GameRightClick:
{
    if (!ENABLED)
        return
    
    ; Add right-click enhancement logic here
    return
}

GameJump:
{
    if (!ENABLED)
        return
    
    ; Add jump enhancement logic here
    return
}

QuickHeal:
{
    if (!ENABLED)
        return
    
    Send, {1}  ; Assuming health potion is on key 1
    return
}

QuickBuff:
{
    if (!ENABLED)
        return
    
    Send, {2}  ; Assuming buff item is on key 2
    return
}

QuickItem:
{
    if (!ENABLED)
        return
    
    Send, {3}  ; Assuming special item is on key 3
    return
}

QuickSpell:
{
    if (!ENABLED)
        return
    
    Send, {4}  ; Assuming spell is on key 4
    return
}

Combo1:
{
    if (!ENABLED)
        return
    
    ; Execute skill combo 1
    Send, {1}
    Sleep, 100
    Send, {2}
    Sleep, 100
    Send, {3}
    return
}

Combo2:
{
    if (!ENABLED)
        return
    
    ; Execute skill combo 2
    Send, {4}
    Sleep, 100
    Send, {5}
    Sleep, 100
    Send, {6}
    return
}

Combo3:
{
    if (!ENABLED)
        return
    
    ; Execute skill combo 3
    Send, {7}
    Sleep, 100
    Send, {8}
    Sleep, 100
    Send, {9}
    return
}

ToggleScript:
{
    ENABLED := !ENABLED
    ToolTip, % "Script " . (ENABLED ? "Enabled" : "Disabled")
    SetTimer, RemoveToolTip, -1000
    return
}

RemoveToolTip:
ToolTip
return`
    }
  };

  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(generatedCode);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy:', err);
    }
  };

  const generateCode = () => {
    const template = codeTemplates[language]?.[category]?.advanced || 
                    codeTemplates[language]?.[category]?.basic || 
                    'Code template not found';
    setGeneratedCode(template);
  };

  return (
    <div className="max-w-6xl mx-auto p-4 space-y-4">
      <Card className="p-6">
        <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Smart Quiz Generator</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/tailwindcss/2.2.19/tailwind.min.css" rel="stylesheet">
</head>
<body class="bg-gray-100 p-6">
    <div class="max-w-4xl mx-auto">
        <!-- Input -->
        <div class="bg-white rounded-lg shadow p-6 mb-6">
            <h1 class="text-2xl font-bold mb-4">Smart Quiz Generator</h1>
            <textarea 
                id="notesInput" 
                class="w-full h-64 p-4 border rounded"
                placeholder="Paste your notes here..."
            ></textarea>
            <div class="mt-4 flex space-x-4">
                <select id="questionLimit" class="border rounded p-2">
                    <option value="5">5 Questions</option>
                    <option value="10" selected>10 Questions</option>
                    <option value="15">15 Questions</option>
                    <option value="20">20 Questions</option>
                </select>
                <button 
                    onclick="makeQuiz()" 
                    class="flex-1 bg-blue-500 text-white px-6 py-3 rounded hover:bg-blue-600"
                >
                    Create Quiz
                </button>
            </div>
        </div>

        <!-- Quiz -->
        <div id="quizDisplay" class="hidden">
            <div id="questionList" class="space-y-6">
                <!-- Questions will appear here -->
            </div>
            <button 
                onclick="checkAnswers()" 
                class="mt-6 w-full bg-green-500 text-white px-6 py-3 rounded hover:bg-green-600"
            >
                Check Answers
            </button>
        </div>
    </div>

    <script>
        const questionTypes = {
            what: (topic) => ({
                question: `What is ${topic} about?`,
                correctAnswer: `${topic} is a key concept that explains important aspects of the subject`,
                wrongAnswers: [
                    `${topic} is an unrelated concept`,
                    `${topic} has no clear definition`,
                    `${topic} is from a different subject`
                ]
            }),
            
            how: (topic) => ({
                question: `How does ${topic} work?`,
                correctAnswer: `${topic} works by addressing key principles in the subject`,
                wrongAnswers: [
                    `${topic} doesn't have a clear function`,
                    `${topic} works randomly without pattern`,
                    `${topic} has no practical application`
                ]
            }),
            
            why: (topic) => ({
                question: `Why is ${topic} important?`,
                correctAnswer: `${topic} is important because it's fundamental to understanding the subject`,
                wrongAnswers: [
                    `${topic} isn't actually important`,
                    `${topic} is a minor detail`,
                    `${topic} could be ignored entirely`
                ]
            }),

            when: (topic) => ({
                question: `When would you apply ${topic}?`,
                correctAnswer: `${topic} is applied when dealing with core aspects of this subject`,
                wrongAnswers: [
                    `${topic} is never applied in practice`,
                    `${topic} is only used in emergencies`,
                    `${topic} is outdated and not used anymore`
                ]
            }),

            where: (topic) => ({
                question: `Where is ${topic} most relevant?`,
                correctAnswer: `${topic} is most relevant in understanding this subject area`,
                wrongAnswers: [
                    `${topic} is only relevant in other fields`,
                    `${topic} has no relevant applications`,
                    `${topic} is only used in theory`
                ]
            })
        };

        function makeQuiz() {
            const notes = document.getElementById('notesInput').value;
            if (!notes) {
                alert('Please enter some notes!');
                return;
            }

            const limit = parseInt(document.getElementById('questionLimit').value);
            const lines = notes.split('\n').map(line => line.trim()).filter(line => line.length > 0);
            let questions = [];
            
            lines.forEach(line => {
                const words = line.split(' ');
                const mainWords = words.filter(word => word.length > 4 && !isCommonWord(word));
                
                if (mainWords.length > 0) {
                    const topic = mainWords[0];
                    Object.values(questionTypes).forEach(questionMaker => {
                        questions.push(questionMaker(topic));
                    });
                }
            });

            questions = questions.sort(() => Math.random() - 0.5).slice(0, limit);
            
            const questionList = document.getElementById('questionList');
            questionList.innerHTML = `
                <div class="mb-6">
                    <div class="bg-gray-200 rounded-full h-2.5 mb-2">
                        <div class="bg-blue-600 h-2.5 rounded-full" style="width: 0%" id="progressBar"></div>
                    </div>
                    <div class="text-right text-sm text-gray-600">Progress: <span id="progressText">0%</span></div>
                </div>
            `;

            questionList.innerHTML += questions.map((q, i) => `
                <div class="bg-white rounded-lg shadow p-6">
                    <p class="font-bold mb-4">Question ${i + 1} of ${limit}: ${q.question}</p>
                    <div class="space-y-2">
                        ${[q.correctAnswer, ...q.wrongAnswers]
                            .sort(() => Math.random() - 0.5)
                            .map((answer, j) => `
                                <div class="flex items-center">
                                    <input type="radio" 
                                           name="q${i}" 
                                           value="${answer}"
                                           id="q${i}a${j}" 
                                           onchange="updateProgress()"
                                           class="mr-2">
                                    <label for="q${i}a${j}">${answer}</label>
                                </div>
                            `).join('')}
                    </div>
                </div>
            `).join('');

            questionList.innerHTML += `
                <button onclick="saveQuiz()" class="mt-4 bg-purple-500 text-white px-6 py-2 rounded hover:bg-purple-600">
                    Save Quiz
                </button>
            `;

            document.getElementById('quizDisplay').classList.remove('hidden');
        }

        function updateProgress() {
            const totalQuestions = document.getElementsByClassName('bg-white rounded-lg shadow p-6').length;
            const answeredQuestions = document.querySelectorAll('input[type="radio"]:checked').length;
            const percentage = Math.round((answeredQuestions / totalQuestions) * 100);
            
            document.getElementById('progressBar').style.width = `${percentage}%`;
            document.getElementById('progressText').textContent = `${percentage}%`;
        }

        function checkAnswers() {
            const questions = document.getElementsByClassName('bg-white rounded-lg shadow p-6');
            let score = 0;
            let total = 0;

            for (let question of questions) {
                const selected = question.querySelector('input:checked');
                if (selected) {
                    total++;
                    if (selected.value.includes('key concept') || 
                        selected.value.includes('works by') || 
                        selected.value.includes('important because') ||
                        selected.value.includes('is applied when') ||
                        selected.value.includes('most relevant')) {
                        score++;
                    }
                }
            }

            alert(`You got ${score} out of ${total} correct!`);
            saveScore(score, total);
        }

        function saveQuiz() {
            const quizData = {
                notes: document.getElementById('notesInput').value,
                questions: Array.from(document.getElementsByClassName('bg-white rounded-lg shadow p-6'))
                    .map(q => ({
                        question: q.querySelector('p').textContent,
                        answers: Array.from(q.querySelectorAll('input')).map(i => i.value)
                    }))
            };
            
            localStorage.setItem('savedQuiz', JSON.stringify(quizData));
            alert('Quiz saved! You can access it later.');
        }

        function saveScore(score, total) {
            const scores = JSON.parse(localStorage.getItem('quizScores') || '[]');
            scores.push({
                date: new Date().toISOString(),
                score: score,
                total: total,
                percentage: Math.round((score/total) * 100)
            });
            localStorage.setItem('quizScores', JSON.stringify(scores));
        }

        function isCommonWord(word) {
            const common = ['about', 'above', 'after', 'again', 'their', 'there', 
                          'these', 'those', 'which', 'while', 'would', 'because', 
                          'could', 'should', 'where', 'when', 'what', 'with'];
            return common.includes(word.toLowerCase());
        }
    </script>
</body>
</html>
