mg = require('./generated_js/mg.js');

let fs = require('fs');
let data = fs.readFileSync(__dirname + "/assets/data.json");
mg.DataStorage.shared().initialize_json(data.toString());

class LoggerImpl extends mg.Logger {
	message(message) {
		console.log (message);
	}
}

let logger = new LoggerImpl();

let result = true;
// result = mg.AllTests.run(logger) && result;
// console.log(result);

let tests = new mg.RunAllTests();
tests.initialize(logger);
result = result && tests.execute();

console.log(result);
if(!result){
    throw 'Tests not passed'
}
