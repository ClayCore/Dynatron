import React, { Component } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';

export interface SearchbarProps {
    visible: boolean;
}
export interface SearchbarState {}

class Searchbar extends Component<SearchbarProps, SearchbarState> {
    constructor(props: SearchbarProps) {
        super(props);

        this.state = {};
    }

    createSearchbar() {
        const { visible } = this.props;

        if (visible) {
            return (
                <section id="searchbar">
                    <input type="text" placeholder="Search..." />
                    <div className="option">
                        <FontAwesomeIcon icon="search"></FontAwesomeIcon>
                    </div>
                </section>
            );
        } else {
            return (
                <section id="searchbar" className="collapse">
                    <input type="text" style={{display: 'none', paddingLeft: 0}}/>
                    <div className="option">
                        <FontAwesomeIcon icon="search"></FontAwesomeIcon>
                    </div>
                </section>
            );
        }
    }

    render() {
        return this.createSearchbar();
    }
}

export default Searchbar;
