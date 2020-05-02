import React, { ReactNode, Component } from 'react';

import Loader from './Loader';
import Mobile from './Mobile';

export interface WrapperProps {
    children: ReactNode;
}
export interface WrapperState {}

class Wrapper extends Component<WrapperProps, WrapperState> {
    constructor(props: WrapperProps) {
        super(props);

        this.state = {};
    }

    render() {
        return (
            <div id="wrapper">
                <Mobile sub={this.props.children}></Mobile>
                <Loader />
            </div>
        );
    }
}

export default Wrapper;
