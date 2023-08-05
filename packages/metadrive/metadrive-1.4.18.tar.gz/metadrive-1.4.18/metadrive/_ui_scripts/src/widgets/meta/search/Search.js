import React, { PureComponent, createRef, Fragment } from 'react';
import Columns from 'react-columns';
import {
  Navbar,
  NavbarGroup,
  InputGroup,
  Spinner,
  NonIdealState,
  Alignment,
  Classes
} from '@blueprintjs/core';
import { IconNames } from '@blueprintjs/icons';
import MetaContext from '../meta-provider/MetaContext';
import Item from './Item';
import './Search.css';

class Search extends PureComponent {
  static contextType = MetaContext;

  static defaultData = {
    search: '',
    results: [],
    status: null
  };

  timeout = null;

  resultsEl = createRef();

  handleChangeSearch = e => {
    if (this.timeout) {
      clearTimeout(this.timeout);
    }

    const search = e.target.value;
    const { setParam } = this.context;
    this.timeout = setTimeout(() => setParam('search', search), 1500);
  };

  handleScroll = () => {
    this.checkUpdating();
  };

  getFirstData = () => {
    const { url, getParam, setData } = this.context;
    const search = getParam('search');

    setData({
      search,
      status: 'loading'
    });
    return fetch(`${url}._filter`, {
      method: 'POST',
      body: JSON.stringify({ search })
    })
      .then(response => response.json())
      .then(({ results, next }) => {
        setData({
          results,
          next,
          status: 'success'
        });
        this.checkUpdating();
      })
      .catch(() => setData({ status: 'error' }));
  };

  getNextData = () => {
    const { getParam, getData, setData } = this.context;
    const { next } = getData(Search.defaultData);
    const search = getParam('search');

    setData({
      status: 'updating'
    });
    return fetch(next, { method: 'POST', body: JSON.stringify({ search }) })
      .then(response => response.json())
      .then(({ results, next }) => {
        setData(data => ({
          results: [...data.results, ...results],
          next,
          status: 'success'
        }));
        this.checkUpdating();
      })
      .catch(() => setData({ status: 'error' }));
  };

  checkUpdating = () => {
    const { getData } = this.context;
    const { status } = getData(Search.defaultData);
    if (status === 'success') {
      const { clientHeight, scrollHeight, scrollTop } = this.resultsEl.current;
      if (scrollTop + clientHeight > scrollHeight * 0.9) {
        this.getNextData();
      }
    }
  };

  renderResults = () => {
    const { getData } = this.context;
    const { results, status } = getData(Search.defaultData);

    if (status === 'success' || status === 'updating') {
      return (
        <Fragment>
          <Columns>
            {results.map((item, index) => (
              <Item key={index} item={item} />
            ))}
          </Columns>
          {status === 'updating' && (
            <div className="search_updating">
              <Spinner />
            </div>
          )}
        </Fragment>
      );
    } else if (status === 'error') {
      return (
        <NonIdealState
          icon={IconNames.ERROR}
          title="The request did not succeed"
        />
      );
    } else if (status === 'loading') {
      return (
        <div className="search_loading">
          <Spinner size={Spinner.SIZE_LARGE} />
        </div>
      );
    }
  };

  componentDidMount() {
    const { getData } = this.context;
    const data = getData(Search.defaultData);
    if (data.status === null) {
      this.getFirstData();
    }
  }

  componentDidUpdate() {
    const { getParam, getData } = this.context;
    const { search: lastSearch } = getData(Search.defaultData);
    const search = getParam('search');
    if (search !== lastSearch) {
      this.getFirstData();
    }
  }

  render() {
    const { getParam } = this.context;
    const search = getParam('search');

    return (
      <div className="search widget">
        <Navbar className="search_navbar">
          <NavbarGroup align={Alignment.CENTER}>
            <InputGroup
              type="search"
              className={Classes.FILL}
              leftIcon={IconNames.SEARCH}
              defaultValue={search}
              placeholder="Search..."
              onChange={this.handleChangeSearch}
            />
          </NavbarGroup>
        </Navbar>
        <div
          className="search_results"
          onScroll={this.handleScroll}
          ref={this.resultsEl}
        >
          {this.renderResults()}
        </div>
      </div>
    );
  }
}

export default Search;
