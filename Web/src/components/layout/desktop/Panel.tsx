import React, { Component } from 'react';
import Banner from './Banner';
import Searchbar from './Searchbar';
import Navigation from './Navigation';

export interface PanelProps {
    visible: boolean;
}
export interface PanelState {
    panel: Element | null;
}

class Panel extends Component<PanelProps, PanelState> {
    constructor(props: PanelProps) {
        super(props);

        this.state = {
            panel: null,
        };

        this.togglePanel = this.togglePanel.bind(this);
    }

    componentDidMount() {
        this.setState({ panel: document.querySelector('#panel') });
    }

    togglePanel(visible: boolean) {
        const { panel } = this.state;
        if (panel) {
            if (visible) {
                panel!.classList.remove('collapse');
                panel!.classList.add('expand');
            } else {
                panel!.classList.remove('expand');
                panel!.classList.add('collapse');
            }
        }
    }

    render() {
        const { visible } = this.props;
        this.togglePanel(visible);

        return (
            <div id="panel">
                <Banner visible={visible} />
                <Searchbar visible={visible} />
                <Navigation visible={visible} />
            </div>
        );
    }
}

export default Panel;
