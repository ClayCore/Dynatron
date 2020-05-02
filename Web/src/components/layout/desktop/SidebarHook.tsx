import React, { Component } from 'react';

export interface SidebarHookProps {
    visible: boolean;
    handle: Function;
}
export interface SidebarHookState {
    arrow: string;
    iconNode: Element | null;
    icon: Element | null;
}

class SidebarHook extends Component<SidebarHookProps, SidebarHookState> {
    constructor(props: SidebarHookProps) {
        super(props);

        this.state = {
            arrow: 'caret-back',
            iconNode: null,
            icon: null,
        };

        this.click = this.click.bind(this);
    }

    componentDidMount() {
        const { arrow } = this.state;
        let iconNode = document.querySelector('#sidebar #button');

        let ionicIcon = document.createElement('ion-icon');
        ionicIcon.setAttribute('name', arrow);
        iconNode?.appendChild(ionicIcon);

        let icon = document.querySelector('#sidebar #button ion-icon');
        this.setState({ iconNode: iconNode, icon: icon });
    }

    // Toggle the icon rotation
    update() {
        let icon = document.querySelector('#sidebar #button ion-icon');
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
        return <div id="button" onClick={this.click}></div>;
    }
}

export default SidebarHook;
