import React, { Component } from 'react';
import { HashRouter as Router, Switch, Route } from 'react-router-dom';
import platform from 'platform';

import Wrapper from './components/layout/Wrapper';

// Utility export functions
export function isMobile() {
    let deviceWidth = window.screen.width * window.devicePixelRatio;
    let mobileAgent = platform.name!.includes('Mobile');

    return deviceWidth < 800 || mobileAgent;
}

export interface AppProps {}
export interface AppState {}

class App extends Component<AppProps, AppState> {
    constructor(props: AppProps) {
        super(props);

        this.state = {};
    }

    render() {
        return (
            <Router>
                <Switch>
                    <Route exact path="/">
                        <Wrapper>
                            
                        </Wrapper>
                    </Route>
                </Switch>
            </Router>
        );
    }
}

export default App;
