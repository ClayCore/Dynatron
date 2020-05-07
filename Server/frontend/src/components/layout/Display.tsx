import React, { ReactNode, Component } from 'react';
import Sidebar from '~/components/layout/desktop/Sidebar';
import Topbar from '~/components/layout/desktop/Topbar';

export interface DisplayProps {
    sub: ReactNode;
}
export interface DisplayState {
    visible: boolean
}

class Display extends Component<DisplayProps, DisplayState> {
    constructor(props: DisplayProps) {
        super(props);

        this.state = {
            visible: true
        };

        this.getStateVisible = this.getStateVisible.bind(this);
    }

    // Gets the "toggle" state of the sidebar
    getStateVisible(visible: boolean) {
        this.setState({visible: visible})
    }

    render() {
        const { visible } = this.state;
        return (
            <main id="display">
                <div id="mobile"></div>
                <div id="desktop">
                    <Sidebar getVisibleState={this.getStateVisible}/>
                    <Topbar visible={visible}/>
                    {this.props.sub}
                </div>
            </main>
        );
    }
}

export default Display;
