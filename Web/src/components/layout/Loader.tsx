import React, { Component } from 'react';

export interface LoaderProps {}
export interface LoaderState {}

class Loader extends Component<LoaderProps, LoaderState> {
    constructor(props: LoaderProps) {
        super(props);

        this.state = {};
    }

    render() {
        return (
            <div id="loader-wrapper">
                <div className="loader">
                    <div className="loader-section"></div>
                    <div className="loader-section" id="delayed"></div>
                </div>
            </div>
        );
    }
}

export default Loader;
