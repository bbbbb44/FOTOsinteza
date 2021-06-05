var express = require('express');
var router = express.Router();
var plantsController = require('../controllers/plantsController.js');

/*
 * GET
 */
router.get('/', plantsController.list);

/*
 * GET
 */
router.get('/:id', plantsController.show);

/*
 * POST
 */
router.post('/', plantsController.create);

/*
 * PUT
 */
router.put('/:id', plantsController.update);

/*
 * DELETE
 */
router.delete('/:id', plantsController.remove);

module.exports = router;
