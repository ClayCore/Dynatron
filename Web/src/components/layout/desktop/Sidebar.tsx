import React, { Component } from 'react';
import Panel from './Panel';
import SidebarHook from './SidebarHook';

export interface SidebarProps {}
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

    render() {
        const { visible } = this.state;
        return (
            <div id="sidebar">
                <Panel visible={visible} />
                <SidebarHook visible={visible} handle={this.toggleSidebar} />
            </div>
        );
    }
}

export default Sidebar;
