var PlantsModel = require('../models/plantsModel.js');

/**
 * plantsController.js
 *
 * @description :: Server-side logic for managing plantss.
 */
module.exports = {

    /**
     * plantsController.list()
     */
    list: function (req, res) {
        PlantsModel.find(function (err, plantss) {
            if (err) {
                return res.status(500).json({
                    message: 'Error when getting plants.',
                    error: err
                });
            }

            return res.json(plantss);
        });
    },

    /**
     * plantsController.show()
     */
    show: function (req, res) {
        var id = req.params.id;

        PlantsModel.findOne({_id: id}, function (err, plants) {
            if (err) {
                return res.status(500).json({
                    message: 'Error when getting plants.',
                    error: err
                });
            }

            if (!plants) {
                return res.status(404).json({
                    message: 'No such plants'
                });
            }

            return res.json(plants);
        });
    },

    /**
     * plantsController.create()
     */
    create: function (req, res) {
        var plants = new PlantsModel({
			index : req.body.index,
			name : req.body.name,
			description : req.body.description
        });

        plants.save(function (err, plants) {
            if (err) {
                return res.status(500).json({
                    message: 'Error when creating plants',
                    error: err
                });
            }

            return res.status(201).json(plants);
        });
    },

    /**
     * plantsController.update()
     */
    update: function (req, res) {
        var id = req.params.id;

        PlantsModel.findOne({_id: id}, function (err, plants) {
            if (err) {
                return res.status(500).json({
                    message: 'Error when getting plants',
                    error: err
                });
            }

            if (!plants) {
                return res.status(404).json({
                    message: 'No such plants'
                });
            }

            plants.index = req.body.index ? req.body.index : plants.index;
			plants.name = req.body.name ? req.body.name : plants.name;
			plants.description = req.body.description ? req.body.description : plants.description;
			
            plants.save(function (err, plants) {
                if (err) {
                    return res.status(500).json({
                        message: 'Error when updating plants.',
                        error: err
                    });
                }

                return res.json(plants);
            });
        });
    },

    /**
     * plantsController.remove()
     */
    remove: function (req, res) {
        var id = req.params.id;

        PlantsModel.findByIdAndRemove(id, function (err, plants) {
            if (err) {
                return res.status(500).json({
                    message: 'Error when deleting the plants.',
                    error: err
                });
            }

            return res.status(204).json();
        });
    }
};
