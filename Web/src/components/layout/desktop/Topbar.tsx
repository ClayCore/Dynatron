import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import Settings from './Settings';

export interface TopbarProps {}
export interface TopbarState {}

class Topbar extends Component<TopbarProps, TopbarState> {
    constructor(props: TopbarProps) {
        super(props);

        this.state = {};
    }

    render() {
        return (
            <div id="topbar">
                <div id="info">
                    Version: &nbsp;<span>{process.env.REACT_APP_VERSION}</span>
                </div>
                <Link to="login">
                    <div className="option">Sign in</div>
                </Link>
                <Link to="register">
                    <div className="option">Register</div>
                </Link>
                <Settings />
            </div>
        );
    }
}

export default Topbar;
