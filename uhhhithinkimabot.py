import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Select } from '@/components/ui/select';
import { Code, Copy, CheckCircle } from 'lucide-react';

const CodeGenerator = () => {
  const [language, setLanguage] = useState('ahk');
  const [description, setDescription] = useState('');
  const [generatedCode, setGeneratedCode] = useState('');
  const [copied, setCopied] = useState(false);
  
  const languages = [
    { value: 'ahk', label: 'AutoHotkey' },
    { value: 'html', label: 'HTML' },
    { value: 'javascript', label: 'JavaScript' },
    { value: 'python', label: 'Python' },
    { value: 'cpp', label: 'C++' },
    { value: 'csharp', label: 'C#' },
    { value: 'java', label: 'Java' }
  ];

  // Code templates for different languages
  const codeTemplates = {
    ahk: {
      hotkey: `
#SingleInstance Force
SetWorkingDir %A_ScriptDir%

; Hotkey Configuration
^j::  ; Ctrl+J
{
    MsgBox, Hotkey Pressed!
    return
}`,
      game_automation: `
#SingleInstance Force
SetWorkingDir %A_ScriptDir%
#MaxThreadsPerHotkey 2

; Global Variables
global isRunning := false
global pauseScript := false

; Toggle Script
F7::
{
    isRunning := !isRunning
    if (isRunning) {
        SetTimer, MainLoop, 100
        ToolTip, Script Running
    } else {
        SetTimer, MainLoop, Off
        ToolTip, Script Stopped
    }
    SetTimer, RemoveToolTip, -1000
    return
}

; Main Automation Loop
MainLoop:
{
    if (!isRunning || pauseScript)
        return
        
    ; Add your game automation logic here
    MouseGetPos, mouseX, mouseY
    PixelGetColor, color, %mouseX%, %mouseY%
    
    ; Example: Click if specific color found
    if (color = 0xFF0000) {
        Click
        Sleep, 1000
    }
    return
}`,
      gui: `
#SingleInstance Force
Gui, Main:New, +AlwaysOnTop
Gui, Main:Add, Text,, Enter your name:
Gui, Main:Add, Edit, vUserName w150
Gui, Main:Add, Button, gSubmit, Submit
Gui, Main:Show
return

Submit:
{
    Gui, Submit, NoHide
    MsgBox, Hello %UserName%!
    return
}

GuiClose:
ExitApp`
    },
    html: {
      basic: `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Website</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Welcome to My Website</h1>
        <p>This is a basic HTML template.</p>
    </div>
</body>
</html>`,
      form: `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Contact Form</title>
    <style>
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
        }
        input, textarea {
            width: 100%;
            padding: 8px;
        }
    </style>
</head>
<body>
    <form action="/submit" method="POST">
        <div class="form-group">
            <label for="name">Name:</label>
            <input type="text" id="name" name="name" required>
        </div>
        <div class="form-group">
            <label for="email">Email:</label>
            <input type="email" id="email" name="email" required>
        </div>
        <div class="form-group">
            <label for="message">Message:</label>
            <textarea id="message" name="message" rows="4" required></textarea>
        </div>
        <button type="submit">Send</button>
    </form>
</body>
</html>`
    }
  };

  const generateCode = () => {
    let code = '';
    const lowercaseDesc = description.toLowerCase();
    
    // AHK-specific generation
    if (language === 'ahk') {
      if (lowercaseDesc.includes('hotkey') || lowercaseDesc.includes('key')) {
        code = codeTemplates.ahk.hotkey;
      } else if (lowercaseDesc.includes('game') || lowercaseDesc.includes('automation')) {
        code = codeTemplates.ahk.game_automation;
      } else if (lowercaseDesc.includes('gui') || lowercaseDesc.includes('interface')) {
        code = codeTemplates.ahk.gui;
      }
    }
    
    // HTML-specific generation
    else if (language === 'html') {
      if (lowercaseDesc.includes('form') || lowercaseDesc.includes('input')) {
        code = codeTemplates.html.form;
      } else {
        code = codeTemplates.html.basic;
      }
    }
    
    setGeneratedCode(code);
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

  return (
    <div className="w-full max-w-4xl mx-auto p-4">
      <Card className="mb-4">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Code className="w-6 h-6" />
            Code Generation Assistant
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div>
              <label className="block mb-2 font-medium">Select Language:</label>
              <select 
                className="w-full p-2 border rounded-md"
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
              >
                {languages.map((lang) => (
                  <option key={lang.value} value={lang.value}>
                    {lang.label}
                  </option>
                ))}
              </select>
            </div>
            
            <div>
              <label className="block mb-2 font-medium">Describe what you want to create:</label>
              <textarea
                className="w-full p-2 border rounded-md min-h-[100px]"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Example: Create a hotkey for gaming automation..."
              />
            </div>
            
            <Button 
              className="w-full"
              onClick={generateCode}
            >
              Generate Code
            </Button>
            
            {generatedCode && (
              <div className="relative">
                <pre className="bg-gray-100 p-4 rounded-md overflow-x-auto">
                  <code>{generatedCode}</code>
                </pre>
                <Button
                  className="absolute top-2 right-2"
                  variant="outline"
                  size="sm"
                  onClick={copyToClipboard}
                >
                  {copied ? (
                    <CheckCircle className="w-4 h-4 text-green-500" />
                  ) : (
                    <Copy className="w-4 h-4" />
                  )}
                </Button>
              </div>
            )}
          </div>
        </CardContent>
      </Card>
      
      <Card>
        <CardHeader>
          <CardTitle>Quick Tips</CardTitle>
        </CardHeader>
        <CardContent>
          <ul className="list-disc pl-6 space-y-2">
            <li>For AHK scripts, try asking for "hotkeys", "game automation", or "GUI interfaces"</li>
            <li>For HTML, try asking for "forms", "layouts", or "responsive designs"</li>
            <li>Be specific about what functionality you need</li>
            <li>Include key features you want in your description</li>
          </ul>
        </CardContent>
      </Card>
    </div>
  );
};

export default CodeGenerator;
