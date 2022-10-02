const join = require('path').join;
const platform = process.platform;

const python = platform === "win32" ? join(__dirname, "venv", "Scripts", "python.exe") : join(__dirname, "venv", "bin", "python");
const PM2_config =  {
  apps: [
    {
      name: "server",
      cwd: __dirname,
      script: join(__dirname, "pm2_main.py"),
      interpreter: python,
      exec_mode: "fork",
      instances: 1,
      autorestart: true,
      watch: false,
      max_restarts: 10,
      pid: join(__dirname, "pm2.pid"),
      output: join(__dirname, "pm2.run.log"),
      error: join(__dirname, "pm2.error.log"),
      wait_ready: true, // configure PM2 to wait for 5s the "ready" message from the server
      listen_timeout: 5000,
      shutdown_with_message: true, // configure PM2 to send a "shutdown" message when stops the server
      kill_timeout: 10000, // if the server doesn't exit in 10s, PM2 force its quit
    }
  ]
};

module.exports = PM2_config;
