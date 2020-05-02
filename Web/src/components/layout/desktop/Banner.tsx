import React, { Component } from 'react';

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
        if (visible) {
            return <div id="banner" className="expand"></div>;
        } else {
            return <div id="banner" className="collapse"></div>;
        }
    }
}

export default Banner;
