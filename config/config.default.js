'use strict';

var config = require('./config.webgme'),
    validateConfig = require('webgme/config/validator');

// Add/overwrite any additional settings here
// config.server.port = 8080;
// config.mongo.uri = 'mongodb://127.0.0.1:27017/webgme_my_app';



config.plugin.allowServerExecution = true;
config.core.enableCustomConstraints = true;

config.requirejsPaths.lodash = './node_modules/lodash/lodash.min';
config.requirejsPaths.backbone = './node_modules/backbone/backbone.min';

validateConfig(config);
module.exports = config;
