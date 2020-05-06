import React, { Component } from 'react';
import Panel from './Panel';
import SidebarHook from './SidebarHook';

export interface SidebarProps {
    getVisibleState: Function;
}
export interface SidebarState {
    visible: boolean;
}

class Sidebar extends Component<SidebarProps, SidebarState> {
    constructor(props: SidebarProps) {
        super(props);

        this.state = {
            visible: true,
        };

        this.toggleSidebar = this.toggleSidebar.bind(this);
    }

    toggleSidebar() {
        const { visible } = this.state;

        this.setState({ visible: !visible });
    }

    // Used for forwarding the sidebar toggle state
    // to parent component
    sendVisibleState() {
        const { visible } = this.state;
        return this.props.getVisibleState(visible);
    }

    render() {
        const { visible } = this.state;
        return (
            <section id="sidebar">
                <Panel visible={visible} />
                <SidebarHook visible={visible} handle={this.toggleSidebar} />
            </section>
        );
    }
}

export default Sidebar;
