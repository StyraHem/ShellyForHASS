import { App, Instance } from "../data";
import React, { Component } from 'react';
import ReactMarkdown from 'react-markdown';

export default class ShellyDocPanel extends Component {
  render() {
    return (<>
      <div className="docpanel">
        <ReactMarkdown># Hello, *world*!</ReactMarkdown>
      </div>
    </>);   
  }
}
 