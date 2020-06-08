module.exports = {
  apps : [{
    name      : 'covidfrontend', // App name that shows in `pm2 ls`
    //exec_mode : 'cluster', // enables clustering
    //instances : '2', // or an integer
    //cwd       : './current', // only if using a subdirectory
    script: 'npm run clear && npm run build && npm run start',
    instances: 1,
    watch: true,
    max_memory_restart: maxMemoryRestart,
    //env: dotenv.config({ path: './config/.env.pro' }).parsed
  }],
};
