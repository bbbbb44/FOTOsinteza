var mongoose = require('mongoose');
var Schema   = mongoose.Schema;

var imageSchema = new Schema({
	'description' : String,
	'datetime' : String,
	'fk_location' : Number,
	'fk_user' : String,
	'fk_plant' : String,
	'path' : String
});

module.exports = mongoose.model('image', imageSchema);
