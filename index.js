const express = require('express');
const multer = require('multer');
const { exec } = require('child_process');
const cors = require('cors');
const fs = require('fs');
const app = express();

// Enable CORS for cross-origin requests
app.use(cors());

// Set up Multer to store uploaded files in memory
const storage = multer.memoryStorage();
const upload = multer({ storage: storage });

// POST endpoint to handle script upload and execution
app.post('/run-script', upload.single('file'), (req, res) => {
  if (!req.file) {
    return res.status(400).json({ output: 'No file uploaded.' });
  }

  const script = req.file.buffer.toString('utf8');
  const scriptPath = './temp_script.ahk';  // Path to save temporary AHK script

  // Write the AHK script to a temporary file
  fs.writeFileSync(scriptPath, script);

  // Execute the AHK script (you need AutoHotkey installed on your server)
  exec(`autohotkey "${scriptPath}"`, (error, stdout, stderr) => {
    if (error) {
      return res.status(500).json({ output: `Error: ${stderr}` });
    }
    res.json({ output: stdout }); // Send the output back to the client
  });
});

// Start the server
const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
