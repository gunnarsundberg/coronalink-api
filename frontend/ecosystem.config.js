module.exports = {
  apps : [{
    name      : 'covidfrontend', // App name that shows in `pm2 ls`
    //exec_mode : 'cluster', // enables clustering
    instances : '1',
    //cwd       : './current', // only if using a subdirectory
    script: 'npm run build && npm run start',
    watch: true,
  }],
};
