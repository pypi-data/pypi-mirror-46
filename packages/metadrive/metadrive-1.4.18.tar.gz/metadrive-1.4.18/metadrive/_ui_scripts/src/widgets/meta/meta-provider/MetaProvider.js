import React, { Component } from 'react';
import { connect } from 'react-redux';
import queryString from 'query-string';
import { isEqual, uniq } from 'lodash';
import MetaContext from './MetaContext';
import { setData } from './actions';

class MetaProvider extends Component {
  getKey = () => {
    const { drive, type, widget } = this.props;
    return `${drive}:${type}:${widget}:`.toLowerCase();
  };

  getParam = param => {
    const fullParam = this.getKey() + param.toLowerCase();
    const searchParams = queryString.parse(this.props.location.search);
    return searchParams[fullParam] || '';
  };

  setParam = (param, value) => {
    const fullParam = this.getKey() + param.toLowerCase();
    const searchParams = queryString.parse(this.props.location.search);
    searchParams[fullParam] = value;
    const search = queryString.stringify(searchParams);

    this.props.history.push({
      ...this.props.location,
      search
    });
  };

  getData = defaultValue => {
    const {
      meta: { data },
      setData
    } = this.props;
    const value = data.get(this.getKey());
    if (value === undefined) {
      setData(this.getKey(), defaultValue);
      return defaultValue;
    }
    return value;
  };

  setData = data => {
    const { setData } = this.props;
    if (typeof data === 'function') {
      setData(this.getKey(), data(this.getData()));
    } else {
      setData(this.getKey(), data);
    }
  };

  shouldComponentUpdate(nextProps) {
    const key = this.getKey();
    const data = this.props.meta.data.get(key);
    const nextData = nextProps.meta.data.get(key);

    const searchParams = queryString.parse(this.props.location.search);
    const nextSearchParams = queryString.parse(nextProps.location.search);
    const params = uniq([
      ...Object.keys(searchParams),
      ...Object.keys(nextSearchParams)
    ]);
    return (
      !isEqual(data, nextData) ||
      params
        .filter(param => param.startsWith(key))
        .some(param => searchParams[param] !== nextSearchParams[param])
    );
  }

  render() {
    const {
      app: {
        api: { server }
      },
      drive,
      type
    } = this.props;
    return (
      <MetaContext.Provider
        value={{
          url: `${server}/drive/${drive}/${type}`,
          getParam: this.getParam,
          setParam: this.setParam,
          getData: this.getData,
          setData: this.setData
        }}
      >
        {this.props.children}
      </MetaContext.Provider>
    );
  }
}

const mapStateToProps = ({ app, meta }) => ({
  app,
  meta
});

const mapDispatchToProps = dispatch => ({
  setData: (key, data) => dispatch(setData(key, data))
});

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(MetaProvider);
