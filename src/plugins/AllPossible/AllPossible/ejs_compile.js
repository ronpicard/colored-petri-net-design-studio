var fs = require('fs');
var ejs = require('ejs');
var compiled = ejs.compile(fs.readFileSync(__dirname + process.argv[2], 'utf8'));
var html = compiled({ title : 'EJS', text : 'Trace' });
console.log(html);



