import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
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

    // NOTE: we're using the 'where' parameter as a unique key ID
    // for the element we're creating
    createLink(where: string, iconTag: string, info: string) {
        const { visible } = this.props;
        if (visible) {
            return (
                <Link to={where} key={where}>
                    <div className="option">
                        <FontAwesomeIcon icon={iconTag as IconName} />
                        <section>{info}</section>
                    </div>
                </Link>
            );
        } else {
            return (
                <Link to={where} key={where} className="collapse">
                    <div className="option">
                        <FontAwesomeIcon icon={iconTag as IconName} />
                        <section style={{display: 'none'}}>{info}</section>
                    </div>
                </Link>
            );
        }
    }

    createLinks(link: { where: string[]; icons: string[]; info: string[] }) {
        const { visible } = this.props;
        let links = new Array<JSX.Element>();
        for (let i = 0; i < link.where.length; i++) {
            links.push(
                this.createLink(link.where[i], link.icons[i], link.info[i])
            );
        }
        return links;
    }

    render() {
        const { visible } = this.props;
        let links: { where: string[]; icons: string[]; info: string[] } = {
            where: ['about', 'temp', 'info', 'contact'],
            icons: [
                'info-circle',
                'sitemap',
                'shopping-basket',
                'address-card',
            ],
            info: ['About', 'Temporary', 'Info', 'Contact'],
        };

        if (visible) {
            return (
                <nav>
                    <label>MAIN NAVIGATION</label>
                    {this.createLinks(links)}
                </nav>
            )
        } else {
            return (
                <nav>
                    <label style={{display: 'none', opacity: 0}}>MAIN NAVIGATION</label>
                    {this.createLinks(links)}
                </nav>
            )
        }
    }
}

export default Navigation;
