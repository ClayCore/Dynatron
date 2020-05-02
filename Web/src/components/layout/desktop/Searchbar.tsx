import React, { Component } from 'react';

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
                <div id="searchbar" className="expand">
                    <input type="text" placeholder="Search..." />
                </div>
            );
        } else {
            return (
                <div id="searchbar" className="collapse">
                    <input type="text" placeholder="Search..." />
                </div>
            );
        }
    }

    render() {
        return this.createSearchbar();
    }
}

export default Searchbar;
