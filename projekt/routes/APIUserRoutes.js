var express = require('express');
var router = express.Router();
var APIuserController = require('../controllers/APIUserController.js');

/*
 * GET
 */
router.get('/', APIuserController.list);
router.get('/profile', APIuserController.profile);
router.get('/logout', APIuserController.logout);
/*
 * GET
 */
router.get('/:id', APIuserController.show);

/*
 * POST
 */
router.post('/', APIuserController.create);
router.post('/login', APIuserController.login);

/*
 * PUT
 */
router.put('/:id', APIuserController.update);

/*
 * DELETE
 */
router.delete('/:id', APIuserController.remove);

module.exports = router;
