var mongoose = require('mongoose');
var Schema   = mongoose.Schema;

var plantsSchema = new Schema({
	'index' : String,
	'name' : String,
	'description' : String
});

module.exports = mongoose.model('plants', plantsSchema);
