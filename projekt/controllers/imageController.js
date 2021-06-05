var ImageModel = require('../models/imageModel.js');
var PlantsModel = require('../models/plantsModel.js');

/**
 * imageController.js
 *
 * @description :: Server-side logic for managing images.
 */
module.exports = {

    /**
     * imageController.list()
     */
    list: function (req, res) {
        ImageModel.find({fk_user : req.session.userId}, function (err, images) {
            if (err) {
                return res.status(500).json({
                    message: 'Error when getting image.',
                    error: err
                });
            }
			data = [];
			data.images = images;
            return res.render('image/images', data);
        });
    },

    /**
     * imageController.show()
     */
    show: function (req, res) {
        var id = req.params.id;

        ImageModel.findOne({_id: id}, function (err, image) {
            if (err) {
                return res.status(500).json({
                    message: 'Error when getting image.',
                    error: err
                });
            }

            if (!image) {
                return res.status(404).json({
                    message: 'No such image'
                });
            }
			
			var plantIndex = image.fk_plant;
			PlantsModel.findOne({index : plantIndex}, function (err, plant){
				  if (err) {
					return res.status(500).json({
						message: 'Error when getting plant.',
						error: err
					});
				}

				if (!plant) {
					return res.status(404).json({
						message: 'No such plant'
					});
				}
					return res.render('image/image', {image : image, plant : plant})
			});
        });
    },

    /**
     * imageController.create()
     */
    create: function (req, res) {
        var image = new ImageModel({
			description : req.body.description,
			datetime : new Date(),
			lon : req.body.lon,
			lat : req.body.lat, 
			fk_user : req.session.userId,
			fk_plant : -1,
			path : 'images/'+req.file.filename,
        });

        image.save(function (err, image) {
            if (err) {
                return res.status(500).json({
                    message: 'Error when creating image',
                    error: err
                });
            }
			return res.redirect('/images');
        });
    },

    /**
     * imageController.update()
     */
    update: function (req, res) {
        var id = req.params.id;

        ImageModel.findOne({_id: id}, function (err, image) {
            if (err) {
                return res.status(500).json({
                    message: 'Error when getting image',
                    error: err
                });
            }

            if (!image) {
                return res.status(404).json({
                    message: 'No such image'
                });
            }

            image.datetime = req.body.datetime ? req.body.datetime : image.datetime;
			image.fk_location = req.body.fk_location ? req.body.fk_location : image.fk_location;
			image.fk_user = req.body.fk_user ? req.body.fk_user : image.fk_user;
			image.path = req.body.path ? req.body.path : image.path;
			
            image.save(function (err, image) {
                if (err) {
                    return res.status(500).json({
                        message: 'Error when updating image.',
                        error: err
                    });
                }

                return res.json(image);
            });
        });
    },

    /**
     * imageController.remove()
     */
    remove: function (req, res) {
        var id = req.params.id;

        ImageModel.findByIdAndRemove(id, function (err, image) {
            if (err) {
                return res.status(500).json({
                    message: 'Error when deleting the image.',
                    error: err
                });
            }

            return res.status(204).json();
        });
    },
	
	showDodaj: function (req, res){
		return res.render('image/dodaj');
	}
};
