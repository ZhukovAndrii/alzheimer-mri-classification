const express = require('express');
const multer = require('multer');
const path = require('path');
const cors = require('cors');
const app = express();
const fs = require('fs');

app.use(cors()); 
app.use(express.json());

const callPythonScript = async (route, name) => {
    const spawner = require('child_process').spawn;

    return new Promise((resolve, reject) => {
        const pythonProcess = spawner('myenv\\Scripts\\python', ['./RequestManager.py', JSON.stringify(route), JSON.stringify(name)]);
        pythonProcess.stdout.on('data', (data) => {
            console.log('Data received from python script:', data.toString());
            resolve(data.toString()); // Resolve the promise with the data
        });

        pythonProcess.stderr.on('data', (error) => {
            console.error('Error from Python script:', error.toString());
            reject(error.toString()); // Reject the promise on error
        });

        pythonProcess.on('close', (code) => {
            console.log(`Python process exited with code ${code}`);
        });
    });
};

const clearUploadsFolder = (folderPath) => {
    fs.readdir(folderPath, (err, files) => {
        if (err) {
            console.error(`Directory can not be reached: ${err}`);
            return;
        }
        files.forEach((file) => {
            const filePath = path.join(folderPath, file);
            fs.unlink(filePath, (err) => {
                if (err) {
                    console.error(`The error while trying to delete ${file}: ${err}`);
                } else {
                    console.log(`The file ${file} deleted`);
                }
            });
        });
    });
};

app.post('/process', async (req, res) => {
    try {
        const response = await callPythonScript('process');
        clearUploadsFolder("uploads/");
        res.json(response);
    } catch (error) {
        res.status(500).json({ error: error.toString() });
    }
});

const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, 'uploads/');
    },
    filename: (req, file, cb) => {
        cb(null, file.originalname);
    },
});


const upload = multer({ storage });
  
app.post('/upload', upload.single('image'), (req, res) => {
if (!req.file) {
    return res.status(400).send('No file uploaded.');
}
res.json({ filePath: `uploads/${req.file.filename}` });
});

const PORT = 5000;
app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});