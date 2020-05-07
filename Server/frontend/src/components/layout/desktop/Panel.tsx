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
            } else {
                panel!.classList.add('collapse');
            }
        }
    }

    render() {
        const { visible } = this.props;
        this.togglePanel(visible);

        return (
            <section id="panel">
                <Banner visible={visible} />
                <Searchbar visible={visible} />
                <Navigation visible={visible} />
            </section>
        );
    }
}

export default Panel;
