module.exports = {
  apps : [{
    name      : 'covidfrontend', // App name that shows in `pm2 ls`
    exec_mode : 'cluster', // enables clustering
    instances : '2', // or an integer
    //cwd       : './current', // only if using a subdirectory
    script    : './node_modules/nuxt-start/bin/nuxt-start.js', // The magic ke
    log_file  : '/tmp/covidfrontend.log'
  }],

  deploy : {
    production : {
      user : 'SSH_USERNAME',
      host : 'SSH_HOSTMACHINE',
      ref  : 'origin/master',
      repo : 'GIT_REPOSITORY',
      path : 'DESTINATION_PATH',
      'pre-deploy-local': '',
      'post-deploy' : 'npm install && pm2 reload ecosystem.config.js --env production',
      'pre-setup': ''
    }
  }
};
