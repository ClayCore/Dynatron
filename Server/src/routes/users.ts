import mongoose from 'mongoose';

const Schema = mongoose.Schema;

const userSchema = new Schema(
    {
        id: Number,
        username: String,
        usermail: String,
        displayname: String,
        avatar: String,
        password: String,
    },
    { collection: 'users' }
);

const userModel = mongoose.model('Users', userSchema, 'users');

export default userModel;