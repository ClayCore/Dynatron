import express from 'express';
import userModel from './users';
import mongoose, { NativeError } from 'mongoose';

const router = express.Router();

router.get('/get', async (req: express.Request, res: express.Response) => {
    userModel
        .find()
        .exec()
        .then((data: mongoose.Document[]) => (err: any) => {
            if (err) return res.json({ success: false, error: err });
            return res.json({ success: true, data: data });
        })
        .catch((err: any) => {
            return res.json({ success: false, error: err });
        });
});

export default router;
