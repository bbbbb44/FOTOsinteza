var UserModel = require('../models/userModel.js');

/**
 * userController.js
 *
 * @description :: Server-side logic for managing users.
 */
module.exports = {

    /**
     * userController.list()
     */
    list: function (req, res) {
        UserModel.find(function (err, users) {
            if (err) {
                return res.status(500).json({
                    message: 'Error when getting user.',
                    error: err
                });
            }
			
			data = [];
			data.users = users;
			return res.render('list/users', data);
        });
    },

    /**
     * userController.show()
     */
    show: function (req, res) {
        var id = req.params.id;

        UserModel.findOne({_id: id}, function (err, user) {
            if (err) {
                return res.status(500).json({
                    message: 'Error when getting user.',
                    error: err
                });
            }

            if (!user) {
                return res.status(404).json({
                    message: 'No such user'
                });
            }

            return res.json(user);
        });
    },

    /**
     * userController.create()
     */
    create: function (req, res) {
        var user = new UserModel({
			username : req.body.username,
			gmail : req.body.gmail,
			password : req.body.password
        });

        user.save(function (err, user) {
            if (err) {
                return res.status(500).json({
                    message: 'Error when creating user',
                    error: err
                });
            }

            return res.redirect('users/login');
        });
    },

    /**
     * userController.update()
     */
    update: function (req, res) {
        var id = req.params.id;

        UserModel.findOne({_id: id}, function (err, user) {
            if (err) {
                return res.status(500).json({
                    message: 'Error when getting user',
                    error: err
                });
            }

            if (!user) {
                return res.status(404).json({
                    message: 'No such user'
                });
            }

            user.username = req.body.username ? req.body.username : user.username;
			user.gmail = req.body.gmail ? req.body.gmail : user.gmail;
			user.password = req.body.password ? req.body.password : user.password;
			
            user.save(function (err, user) {
                if (err) {
                    return res.status(500).json({
                        message: 'Error when updating user.',
                        error: err
                    });
                }

                return res.render('list/users');
            });
        });
    },

    /**
     * userController.remove()
     */
    remove: function (req, res) {
        var id = req.params.id;

        UserModel.findByIdAndRemove(id, function (err, user) {
            if (err) {
                return res.status(500).json({
                    message: 'Error when deleting the user.',
                    error: err
                });
            }

            return res.status(204).json();
        });
    },
	
	login: function (req, res){
		UserModel.authenticate(req.body.username, req.body.password, function(error, user){
            if(error || !user){
                var err = new Error("Wrong username or password");
                return res.status(401).json({
                    message: 'Wrong username or password',
                    error: err
                });
            } else {
                req.session.userId = user._id;
				req.session.username = user.username;
                return res.redirect('profile');
            }
        });
	},
	
	logout: function (req,res,next){
        if(req.session){
            req.session.destroy(function(err){
                if(err){
                    return next(err);
                } else {
                    return res.redirect('/');
                }
            });
        }
    },
	
    profile: function(req, res, next){
        UserModel.findById(req.session.userId)
            .exec(function( error, user){
                if(error){
                    return next(error);
                } else {
                    if (user === null){
                        var err = new Error("Not authorized! Go back!");
                        err.status = 400;
                        return next(err);
                    } else{
                        res.render('user/profile', user);
                    }
                }
            });
    },
	
	showLogin: function (req, res) {
		return res.render('user/login');
	},
	
	showRegister: function (req, res) {
		return res.render('user/register');
	}
};
