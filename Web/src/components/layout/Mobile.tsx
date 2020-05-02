import React, { ReactNode, Component } from 'react';
import Sidebar from './desktop/Sidebar';
import Topbar from './desktop/Topbar';

export interface MobileProps {
    sub: ReactNode;
}
export interface MobileState {}

class Mobile extends Component<MobileProps, MobileState> {
    constructor(props: MobileProps) {
        super(props);

        this.state = {};
    }

    render() {
        return (
            <main id="display">
                <div id="mobile"></div>
                <div id="desktop">
                    <Sidebar />
                    <Topbar />
                    {this.props.sub}
                </div>
            </main>
        );
    }
}

export default Mobile;
