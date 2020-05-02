import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { IconName } from '@fortawesome/fontawesome-svg-core';

export interface NavigationProps {
    visible: boolean;
}
export interface NavigationState {}

class Navigation extends Component<NavigationProps, NavigationState> {
    constructor(props: NavigationProps) {
        super(props);
        this.state = {};
    }

    createLink(where: string, iconTag: string, info: string) {
        const { visible } = this.props;
        if (visible) {
            return (
                <Link to={where} key={where}>
                    <div className="option">
                        <FontAwesomeIcon icon={iconTag as IconName} />
                        <div>{info}</div>
                    </div>
                </Link>
            );
        } else {
            return (
                <Link to={where} key={where}>
                    <div className="option">
                        <i className={iconTag}></i>
                    </div>
                </Link>
            );
        }
    }

    createLinks(link: { where: string[]; icons: string[]; info: string[] }) {
        let links = new Array<JSX.Element>();
        for (let i = 0; i < link.where.length; i++) {
            links.push(
                this.createLink(link.where[i], link.icons[i], link.info[i])
            );
        }
        return links;
    }

    render() {
        let links = {
            where: ['about', 'temp', 'info', 'contact'],
            icons: ['info-circle', 'sitemap', 'shopping-basket', 'address-card'],
            info: ['About', 'Temporary', 'Info', 'Contact'],
        };

        return <nav>{this.createLinks(links)}</nav>;
    }
}

export default Navigation;
