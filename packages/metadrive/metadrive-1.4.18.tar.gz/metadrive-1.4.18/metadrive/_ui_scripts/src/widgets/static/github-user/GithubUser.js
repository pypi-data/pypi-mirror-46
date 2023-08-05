import React, { PureComponent } from 'react';
import queryString from 'query-string';
import { RestfulProvider, Get } from 'restful-react';
import {
  Navbar,
  NavbarGroup,
  InputGroup,
  NonIdealState,
  Card,
  Alignment,
  Classes,
  Icon,
  Colors
} from '@blueprintjs/core';
import { IconNames } from '@blueprintjs/icons';
import './GithubUser.css';

export default class GithubUser extends PureComponent {
  timeout = 0;

  handleSearch = searchQuery => {
    if (this.timeout) {
      clearTimeout(this.timeout);
    }

    const search = queryString.stringify(searchQuery);

    this.timeout = setTimeout(
      () =>
        this.props.history.push({
          ...this.props.location,
          search
        }),
      1500
    );
  };

  onChangeSearch = e => {
    const searchQuery = queryString.parse(this.props.location.search);
    searchQuery.username = e.target.value;
    this.handleSearch(searchQuery);
  };

  render() {
    const queryParams = queryString.parse(this.props.location.search);
    const username = queryParams.username || '';

    return (
      <RestfulProvider base="https://api.github.com">
        <div className="widget">
          <Navbar>
            <NavbarGroup align={Alignment.CENTER}>
              <InputGroup
                type="search"
                className={Classes.FILL}
                leftIcon={IconNames.USER}
                defaultValue={username}
                placeholder="Username..."
                onChange={this.onChangeSearch}
              />
            </NavbarGroup>
          </Navbar>
          <Get path={'/users/' + username}>
            {(data, { loading, error }) => {
              if (loading) {
                return <Card>Loading data...</Card>;
              }

              if (error) {
                return (
                  <NonIdealState
                    icon={IconNames.SEARCH}
                    title="No search results"
                  />
                );
              }

              return (
                <Card>
                  <h5>{data.name}</h5>
                  <div className="user-info">
                    {data.avatar_url && (
                      <img
                        className="user-info_avatar"
                        alt={data.name}
                        src={data.avatar_url}
                      />
                    )}
                    <div className="user-info_description">
                      {data.email && (
                        <p>
                          <Icon
                            icon={IconNames.ENVELOPE}
                            color={Colors.GRAY1}
                          />{' '}
                          {data.email}
                        </p>
                      )}
                      {data.company && (
                        <p>
                          <Icon icon={IconNames.PEOPLE} color={Colors.GRAY1} />{' '}
                          {data.company}
                        </p>
                      )}
                      {data.location && (
                        <p>
                          <Icon
                            icon={IconNames.MAP_MARKER}
                            color={Colors.GRAY1}
                          />{' '}
                          {data.location}
                        </p>
                      )}
                      <p>{data.bio}</p>
                    </div>
                  </div>
                </Card>
              );
            }}
          </Get>
        </div>
      </RestfulProvider>
    );
  }
}
