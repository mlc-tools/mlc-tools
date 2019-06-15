mg = require('./generated_js/mg.js');

class LoggerImpl extends mg.Logger {
	message(message) {
		console.log(message);
	}
}


let logger = new LoggerImpl();
tests = new mg.RunAllTests();
tests.initialize(logger);
result = tests.execute();

if(!result){
    throw 'Tests not passed'
}