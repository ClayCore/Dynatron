import React, { Component } from 'react';
import banner from '~/../assets/images/banner.png';

// let this be a shitshow for everyone to see, how much trouble i went through
// to resolve a path for an image and editing the tsconfig.json and package.json file
// twenty thousand times just to be able to do the import above.
// note: ts extension in vscode still doesn't like that import
//
// import banner from '~/images/banner.png';
// import banner from 'assets/image/banner.png';
// import banner from '~../assets/image/banner.png';
// const images = require('~/images/*.png');
// const images = require('~images/*.png');
// const images = require('assets/images/*.png');
// const images = require('~/assets/images/*.png');
// const images = require('./assets/images/*.png');
// const images = require('/assets/images/*.png');
// const images = require('../../../../assets/images/*.png');

export interface BannerProps {
    visible: boolean;
}
export interface BannerState {}

class Banner extends Component<BannerProps, BannerState> {
    constructor(props: BannerProps) {
        super(props);

        this.state = {};
    }

    render() {
        const { visible } = this.props;

        return visible ? (
            <div id="banner">
                <img src={banner}></img>
            </div>
        ) : (
            <div id="banner" className="collapse">
                <img src={banner} style={{opacity: 0}}></img>
            </div>
        );
    }
}

export default Banner;
