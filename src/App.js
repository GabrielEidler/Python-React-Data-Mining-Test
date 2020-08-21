import React, { Component } from 'react';
import {BrowserRouter, Route, Switch} from 'react-router-dom';

//custom imports
import FamilyDollar from './components/familyDollar'

class App extends Component {
    render () {
        return (
            <BrowserRouter>
             <Switch>
                <Route path="/" >
                    <FamilyDollar />
                </Route>
             </Switch>
            </BrowserRouter>
        );
    }
}

export default App;