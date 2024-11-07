const express = require('express');
const multer = require('multer');
const { exec } = require('child_process');
const app = express();
const port = 3000;

// Set up file upload handling
const storage = multer.memoryStorage(); // Store the file in memory
const upload = multer({ storage: storage });

app.use(express.static('public'));

// Endpoint to handle script upload and execution
app.post('/run-script', upload.single('file'), (req, res) => {
  const script = req.file.buffer.toString('utf8');

  // Save the script temporarily in a file
  const fs = require('fs');
  const scriptPath = './temp_script.ahk';
  fs.writeFileSync(scriptPath, script);

  // Run the script using AHK (ensure AHK is installed on Replit or your cloud server)
  exec(`autohotkey "${scriptPath}"`, (error, stdout, stderr) => {
    if (error) {
      return res.status(500).json({ output: stderr });
    }
    res.json({ output: stdout });
  });
});

// Start server
app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});
