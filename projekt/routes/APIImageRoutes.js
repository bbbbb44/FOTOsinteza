var express = require('express');
var router = express.Router();
var APIImageController = require('../controllers/APIImageController.js');

var multer = require('multer');
var upload = multer({dest: 'public/images/'});
/*
 * GET
 */
router.get('/', APIImageController.list);

/*
 * GET
 */
router.get('/:id', APIImageController.show);
/*
 * POST
 */
router.post('/dodaj', upload.single('slika'), APIImageController.create);

/*
 * PUT
 */
router.put('/:id', APIImageController.update);

/*
 * DELETE
 */
router.delete('/:id', APIImageController.remove);

module.exports = router;
