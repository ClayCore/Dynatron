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
        let icon = document.querySelector('#sidebar button svg');
        this.setState({ icon: icon });
    }

    createButton() {
        const { visible } = this.props;

        if (visible) {
            return (
                <button id="button" onClick={this.click}>
                    <FontAwesomeIcon icon="angle-double-left" />
                    <div>Collapse Sidebar</div>
                </button>
            );
        } else {
            return (
                <button id="button" onClick={this.click} className="collapse">
                    <FontAwesomeIcon icon="angle-double-left" />
                    <div style={{ opacity: 0 }}>Collapse Sidebar</div>
                </button>
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

        // FIXME
        const { visible } = this.props;
        if (visible) {
            document.querySelector('#topbar')?.classList.add('collapse');
        } else {
            document.querySelector('#topbar')?.classList.remove('collapse');
        }

        this.update();
    }

    render() {
        return this.createButton();
    }
}

export default SidebarHook;
