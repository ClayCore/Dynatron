import React, { ReactNode, Component } from 'react';

import Loader from '~/components/layout/Loader';
import Display from '~/components/layout/Display';

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
            <section id="wrapper">
                <Display sub={this.props.children}></Display>
                <Loader />
            </section>
        );
    }
}

export default Wrapper;
