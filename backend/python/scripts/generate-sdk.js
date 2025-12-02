const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 7174;
const HEALTH_URL = `http://localhost:${PORT}/api/health`;
const OPENAPI_URL = `http://localhost:${PORT}/api/openapi.yaml`;
const SDK_OUTPUT_DIR = path.join(__dirname, '../../../sdk/ts');

let serverProcess = null;

// Function to check if server is ready
function checkHealth(maxAttempts = 30, attemptDelay = 1000) {
  return new Promise((resolve, reject) => {
    let attempts = 0;

    const tryHealth = () => {
      attempts++;
      console.log(`[${attempts}/${maxAttempts}] Checking server health...`);

      http.get(HEALTH_URL, (res) => {
        if (res.statusCode === 200) {
          console.log('✓ Server is ready!');
          resolve();
        } else {
          if (attempts >= maxAttempts) {
            reject(new Error(`Server health check failed after ${maxAttempts} attempts`));
          } else {
            setTimeout(tryHealth, attemptDelay);
          }
        }
      }).on('error', (err) => {
        if (attempts >= maxAttempts) {
          reject(new Error(`Server health check failed: ${err.message}`));
        } else {
          setTimeout(tryHealth, attemptDelay);
        }
      });
    };

    tryHealth();
  });
}

// Function to start the Python backend server
function startServer() {
  return new Promise((resolve, reject) => {
    console.log('Starting Python backend server...');

    const env = { ...process.env, PORT: PORT.toString() };

    // Check if we're on Windows or Unix-like system
    const pythonCommand = process.platform === 'win32' ? 'python' : 'python3';

    serverProcess = spawn(pythonCommand, ['-m', 'uvicorn', 'main:app', '--host', '0.0.0.0', '--port', PORT.toString()], {
      cwd: path.join(__dirname, '..'),
      env,
      shell: true,
      stdio: 'pipe'
    });

    serverProcess.stdout.on('data', (data) => {
      console.log(`[server] ${data.toString().trim()}`);
    });

    serverProcess.stderr.on('data', (data) => {
      console.error(`[server error] ${data.toString().trim()}`);
    });

    serverProcess.on('error', (error) => {
      reject(error);
    });

    // Give the server a moment to start
    setTimeout(() => resolve(), 3000);
  });
}

// Function to stop the server
function stopServer() {
  return new Promise((resolve) => {
    if (serverProcess) {
      console.log('Stopping Python backend server...');

      // Try graceful shutdown first
      serverProcess.kill('SIGTERM');

      setTimeout(() => {
        if (serverProcess && !serverProcess.killed) {
          console.log('Force killing server...');
          serverProcess.kill('SIGKILL');
        }
        resolve();
      }, 2000);
    } else {
      resolve();
    }
  });
}

// Function to clean SDK directory
function cleanSDKDirectory() {
  console.log('Cleaning SDK directory...');

  if (fs.existsSync(SDK_OUTPUT_DIR)) {
    fs.rmSync(SDK_OUTPUT_DIR, { recursive: true, force: true });
  }

  fs.mkdirSync(SDK_OUTPUT_DIR, { recursive: true });
  console.log('✓ SDK directory cleaned');
}

// Function to generate SDK
function generateSDK() {
  return new Promise((resolve, reject) => {
    console.log('Generating TypeScript SDK from Python backend...');

    const generator = spawn('npx', [
      '@openapitools/openapi-generator-cli',
      'generate',
      '-i', OPENAPI_URL,
      '-g', 'typescript-fetch',
      '-o', SDK_OUTPUT_DIR,
      '--additional-properties=npmName=@technight/api,supportsES6=true,npmVersion=1.0.0'
    ], {
      shell: true,
      stdio: 'inherit'
    });

    generator.on('close', async (code) => {
      if (code === 0) {
        console.log('✓ SDK generated successfully from Python backend!');
        
        // Compile the SDK
        console.log('Compiling SDK...');
        try {
          await compileSDK();
          resolve();
        } catch (error) {
          reject(error);
        }
      } else {
        reject(new Error(`SDK generation failed with code ${code}`));
      }
    });

    generator.on('error', (error) => {
      reject(error);
    });
  });
}

// Function to compile SDK
function compileSDK() {
  return new Promise((resolve, reject) => {
    console.log('Installing SDK dependencies and compiling...');
    
    // Install dependencies and build
    const build = spawn('npm', ['install'], {
      cwd: SDK_OUTPUT_DIR,
      shell: true,
      stdio: 'inherit'
    });

    build.on('close', (code) => {
      if (code === 0) {
        const compile = spawn('npm', ['run', 'build'], {
          cwd: SDK_OUTPUT_DIR,
          shell: true,
          stdio: 'inherit'
        });

        compile.on('close', (compileCode) => {
          if (compileCode === 0) {
            console.log('✓ SDK compiled successfully!');
            resolve();
          } else {
            reject(new Error(`SDK compilation failed with code ${compileCode}`));
          }
        });

        compile.on('error', (error) => {
          reject(error);
        });
      } else {
        reject(new Error(`SDK dependency installation failed with code ${code}`));
      }
    });

    build.on('error', (error) => {
      reject(error);
    });
  });
}

// Main execution
async function main() {
  try {
    console.log('=== Python Backend SDK Generation Started ===\n');

    // Step 1: Clean SDK directory
    cleanSDKDirectory();

    // Step 2: Start Python server
    await startServer();

    // Step 3: Wait for server to be ready
    await checkHealth();

    // Step 4: Generate SDK
    await generateSDK();

    console.log('\n=== Python Backend SDK Generation Completed Successfully ===');

  } catch (error) {
    console.error('\n=== Python Backend SDK Generation Failed ===');
    console.error(error.message);
    process.exitCode = 1;

  } finally {
    // Step 5: Always stop the server
    await stopServer();
    process.exit(process.exitCode || 0);
  }
}

// Handle termination signals
process.on('SIGINT', async () => {
  console.log('\nReceived SIGINT, cleaning up...');
  await stopServer();
  process.exit(1);
});

process.on('SIGTERM', async () => {
  console.log('\nReceived SIGTERM, cleaning up...');
  await stopServer();
  process.exit(1);
});

// Run main function
main();
