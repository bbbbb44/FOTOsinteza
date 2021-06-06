var mongoose = require('mongoose');
var Schema   = mongoose.Schema;

var imageSchema = new Schema({
	'description' : String,
	'datetime' : String,
	'lat' : Number,
	'lon' : Number, 
	'metaPodatki' : String,
	'fk_user' : String,
	'fk_plant' : String,
	'path' : String
});

module.exports = mongoose.model('image', imageSchema);
