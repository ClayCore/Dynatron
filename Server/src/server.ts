import http from 'http';
import createError, { HttpError } from 'http-errors';
import bodyParser from 'body-parser';
import path from 'path';
import logger from 'morgan';
import cors from 'cors';
import compression from 'compression';
import express, { NextFunction } from 'express';
import debug from 'debug';
import mongoose from 'mongoose';

const adminRouter = require('./routes/admin');
const dataRouter = require('./routes/db');
const getSecret = require('./routes/connect');

const app: express.Application = express();
mongoose.connect(getSecret('dbUri'), {
    useNewUrlParser: true,
    useUnifiedTopology: true,
});
let db = mongoose.connection;
db.on('error', console.error.bind(console, 'MongoDB connection error: '));

app.use(cors());
app.use(compression());
app.use(logger('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));

app.use('/', express.static(path.join(__dirname, '../server/build')));
app.use('/', adminRouter);
app.use('/api', dataRouter);

const port = normalizePort(process.env.PORT || '5000');
app.set('port', port);

let server = http.createServer(app);

app.use(function (req, res, next) {
    next(createError(404));
});

app.use(function (
    err: HttpError,
    req: express.Request,
    res: express.Response,
    next: NextFunction
) {
    res.locals.message = err.message;
    res.locals.error = req.app.get('env') === 'development' ? err : {};

    res.status(err.status || 500);
    res.json({ success: false, error: err });
});

server.listen(port);
server.on('error', onError);
server.on('listening', onListen);

function normalizePort(p: string) {
    let port = parseInt(p, 10);

    if (isNaN(port)) {
        return p;
    }

    if (port >= 0) {
        return port;
    }

    return false;
}

function onError(error: HttpError) {
    if (error.syscall !== 'listen') {
        throw error;
    }

    let bind = typeof port === 'string' ? 'Pipe: ' + port : 'Port: ' + port;

    switch (error.code) {
        case 'EACCESS': {
            console.error(
                `[ERROR/Thread]: ${bind} requires elevated privileges!`
            );
            process.exit(1);
            break;
        }
        case 'EADDRINUSE': {
            console.error(`[ERROR/Thread]: ${bind} is already in use!`);
            process.exit(1);
            break;
        }
        default:
            throw error;
    }
}

function onListen() {
    let addr = server.address();

    let bind = typeof port === 'string' ? 'Pipe: ' + port : 'Port: ' + port;
    debug(`Listening on ${bind}`);
}
