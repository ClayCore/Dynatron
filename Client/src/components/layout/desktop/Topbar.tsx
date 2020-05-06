import React, { Component } from 'react';
import { Link } from 'react-router-dom';

export interface TopbarProps {
    visible: boolean;
}
export interface TopbarState {}

class Topbar extends Component<TopbarProps, TopbarState> {
    constructor(props: TopbarProps) {
        super(props);

        this.state = {};
    }

    createTopbar() {
        const { visible } = this.props;
        if (visible) {
            return (
                <header id="topbar">
                    <section id="info">
                        Version: &nbsp;
                        <span>{process.env.REACT_APP_VERSION}</span>
                    </section>
                    <Link to="login">
                        <div className="option">Sign in</div>
                    </Link>
                    <Link to="register">
                        <div className="option">Register</div>
                    </Link>
                </header>
            );
        } else {
            return (
                <header id="topbar" className="collapse">
                    <section id="info">
                        Version: &nbsp;
                        <span>{process.env.REACT_APP_VERSION}</span>
                    </section>
                    <Link to="login">
                        <div className="option">Sign in</div>
                    </Link>
                    <Link to="register">
                        <div className="option">Register</div>
                    </Link>
                </header>
            );
        }
    }

    render() {
        return this.createTopbar();
    }
}

export default Topbar;
