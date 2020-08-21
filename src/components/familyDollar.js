import React, { Component } from 'react';
import Papa from 'papaparse'

// custom imports

class FamilyDollar extends React.Component {
    constructor() {
      super();
      this.state = {
        csvfile: undefined,
        listItems: null,
      };
      this.updateData = this.updateData.bind(this);
    }
  
    handleChange = event => {
      this.setState({
        csvfile: event.target.files[0]
      });
    };
  
    importCSV = () => {
      const { csvfile } = this.state;
      Papa.parse(csvfile, {
        complete: this.updateData,
        header: true
      });
    };
  
    updateData(result) {
      var data = result.data;
      console.log(data);
      const items = data.map(result =>
        <div key={result.postalCode}>
          <br/>
            <p>-------------------------------------------------------------</p>
            <p ><strong>Address: {result.streetAddress} </strong></p>
            <p>Locality: {result.addressLocality}</p>
            <p>Region: {result.addressRegion}</p>
            <p>Postal Code: {result.postalCode} </p>
            <p>-------------------------------------------------------------</p>
            <br/>
        </div>
        );
        this.setState({
            listItems: items
        })
    }
  
    render() {
      console.log(this.state.csvfile);
      return (
        <div className="App">
          <h2>Import CSV File!</h2>
          <input
            className="csv-input"
            type="file"
            ref={input => {
              this.filesInput = input;
            }}
            name="file"
            placeholder={null}
            onChange={this.handleChange}
          />
          <p />
          <button onClick={this.importCSV}> Render Data</button>
            <div className='container'>
              <div className="card">
                {this.state.listItems}
              </div>
            </div>
        </div>
      );
    }
  }
  
  export default FamilyDollar;