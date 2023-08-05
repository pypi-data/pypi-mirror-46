import React, { PureComponent } from 'react';
import './Clock.css';

export default class Clock extends PureComponent {
  render() {
    return (
      <div className="clock">
        <svg className="clock_icon" viewBox="0 0 100 100">
          <circle
            fill="none"
            stroke="#fff"
            strokeWidth="4"
            strokeMiterlimit="10"
            cx="50"
            cy="50"
            r="48"
          />
          <line
            fill="none"
            strokeLinecap="round"
            stroke="#fff"
            strokeWidth="4"
            strokeMiterlimit="10"
            x1="50"
            y1="50"
            x2="85"
            y2="50.5"
          >
            <animateTransform
              attributeName="transform"
              dur="2s"
              type="rotate"
              from="0 50 50"
              to="360 50 50"
              repeatCount="indefinite"
            />
          </line>
          <line
            fill="none"
            strokeLinecap="round"
            stroke="#fff"
            strokeWidth="4"
            strokeMiterlimit="10"
            x1="50"
            y1="50"
            x2="49.5"
            y2="74"
          >
            <animateTransform
              attributeName="transform"
              dur="15s"
              type="rotate"
              from="0 50 50"
              to="360 50 50"
              repeatCount="indefinite"
            />
          </line>
        </svg>
      </div>
    );
  }
}
