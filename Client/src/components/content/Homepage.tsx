import React, { Component } from 'react';

export interface HomepageProps {};
export interface HomepageState {};

class Homepage extends Component<HomepageProps, HomepageState> {
    constructor(props: HomepageProps) {
        super(props);

        this.state = {};
    }

    render() {
        return(
            <article>
                
            </article>
        )
    }
}

export default Homepage;