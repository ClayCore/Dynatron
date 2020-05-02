import React, { Component } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';

export interface SidebarHookProps {
    visible: boolean;
    handle: Function;
}
export interface SidebarHookState {
    icon: Element | null;
}

class SidebarHook extends Component<SidebarHookProps, SidebarHookState> {
    constructor(props: SidebarHookProps) {
        super(props);

        this.state = {
            icon: null,
        };

        this.click = this.click.bind(this);
    }

    componentDidMount() {
        let icon = document.querySelector('#sidebar #button svg');
        this.setState({ icon: icon });
    }

    createButton() {
        const { visible } = this.props;

        if (visible) {
            return (
                <div id="button" onClick={this.click}>
                    <FontAwesomeIcon icon="angle-double-left" />
                    <div>Collapse Sidebar</div>
                </div>
            );
        } else {
            return (
                <div id="button" onClick={this.click} className="collapse">
                    <FontAwesomeIcon icon="angle-double-left" />
                    <div style={{ opacity: 0 }}>Collapse Sidebar</div>
                </div>
            );
        }
    }

    // Toggle the icon rotation
    update() {
        const { icon } = this.state;
        const { visible } = this.props;

        if (icon) {
            let degrees = visible ? 180 : 0;
            icon.setAttribute('style', `transform: rotate(${degrees}deg)`);
        }
    }

    click(event: React.MouseEvent) {
        // Prevent a browser reload/refresh
        event.preventDefault();

        // Invoke the handler function for the button
        this.props.handle();

        this.update();
    }

    render() {
        return this.createButton();
    }
}

export default SidebarHook;
