import React, { Component } from 'react';
import { Route, Switch } from 'react-router-dom';
import axios from 'axios';

import UsersList from './components/UsersList';
import AddUser from './components/AddUser';
import About from './components/About';
import NavBar from './components/NavBar';
import Form from './components/Form';
import Logout from './components/Logout';
import ResetPassword from './components/PasswordResetForm';
import UserStatus from './components/UserStatus';

class App extends Component {
    constructor() {
        super();
        this.state = {
            users: [],
            username: '',
            email: '',
            title: 'Ingme', // new
            formData: {
                username: '',
                email: '',
                password: ''
            },
            isAuthenticated: false,
            isMailSentToUser: false,
            isError:false,
            ErrorMessage:''
        };
        // this.addUser = this.addUser.bind(this);
    }

    componentDidMount() {
        this.getUsers();
        console.log('[App.js] - componentDidMount');
    };

    handleUserFormSubmit = (event) => {
        event.preventDefault();
        const formType = window.location.href.split('/').reverse()[0];
        let data = {
            email: this.state.formData.email,
            password: this.state.formData.password,
        };
        if (formType === 'register') {
            data.username = this.state.formData.username;
        }
        const url = `${process.env.REACT_APP_USERS_SERVICE_URL}/auth/${formType}`
        axios.post(url, data)
        .then((res) => {
            console.log(res.data);
            this.clearFormState();
            window.localStorage.setItem('authToken', res.data.auth_token);
            this.setState({ isAuthenticated: true, isError: false});
            this.getUsers();
        })
        .catch((err) => { console.log("User doesn't exist");
            this.setState({ isError: true,
                            ErrorMessage: "User Name or Password is incorrect." });
        });
    };

    handleUserResetFormSubmit = (event) => {
        event.preventDefault();
        let data = {
            email: this.state.formData.email
        }
        const url = `${process.env.REACT_APP_USERS_SERVICE_URL}/auth/reset_password_request`
        axios.post(url, data)
        .then((res) => {
            console.log(res.data); 
            this.setState({ isMailSentToUser: true, });           
        })
        .catch((err) => { console.log(err); });
    }

    handleFormChange = (event) => {
        const obj = this.state.formData;
        obj[event.target.name] = event.target.value;
        this.setState(obj);
    };

    clearFormState() {
        this.setState({
            formData: { username: '', email: '', password: '' },
            username: '',
            email: ''
        });
    };

    logoutUser = () => {
        window.localStorage.clear();
        this.setState({ isAuthenticated: false });
    };

    addUser = (event) => {
        event.preventDefault();

        const data = {
          username: this.state.username,
          email:this.state.email  
        };

        axios.post(`${process.env.REACT_APP_USERS_SERVICE_URL}/users`,data)
        .then(res => { 
            this.getUsers(); // to update all users on screen.
            this.setState({username: '', email: ''});
         })
        .catch(err => { console.log(err); })

        console.log('sanity check!');
        console.log(this.state);
    };

    handleChange = (event) => {
        const obj = {};
        obj[event.target.name] = event.target.value; // E.g. obj contains {username: "ghouse", email: "test@test.com"}
        // console.log(obj);
        this.setState(obj);
    };

    getUsers = () => {
        axios.get(`${process.env.REACT_APP_USERS_SERVICE_URL}/users`)
        .then(res => { this.setState({ users: res.data.data.users}); })
        .catch(err => { console.log(err); });
    };

    render() {
        return (
            <div>
                <NavBar
                    title={this.state.title}
                    isAuthenticated={this.state.isAuthenticated}
                 />
                <section className="section">
                <div className="container">
                    <div className="columns">
                        <div className="column is-one-third">
                            <br/>
                            <Switch>
                                <Route exact path='/' render={() => (
                                    <UsersList
                                        users={this.state.users}
                                    />
                                    )} 
                                />
                                <Route exact path='/about' component={About}/>
                                <Route exact path='/register' render={() => (
                                    <Form
                                        formType={'Register'}
                                        formData={this.state.formData}
                                        handleUserFormSubmit={this.handleUserFormSubmit}
                                        handleFormChange={this.handleFormChange}
                                        isAuthenticated={this.state.isAuthenticated}
                                    />
                                        
                                )}/>
                                <Route exact path='/login' render={() => (
                                    <Form
                                        formType={'Login'}
                                        formData={this.state.formData}
                                        handleUserFormSubmit={this.handleUserFormSubmit}
                                        handleFormChange={this.handleFormChange}
                                        isAuthenticated={this.state.isAuthenticated}
                                        isError={this.state.isError}
                                        errormessage={this.state.ErrorMessage}
                                    />
                                )}/>

                                <Route exact path='/logout' render={() => (
                                    <Logout
                                    logoutUser={this.logoutUser}
                                    isAuthenticated={this.state.isAuthenticated}
                                    />
                                    )} />

                                <Route exact path='/resetpassword' render={() => (
                                    <ResetPassword
                                        formType={'Reset Password'}
                                        formData={this.state.formData}
                                        handleUserFormSubmit={this.handleUserResetFormSubmit}
                                        handleFormChange={this.handleFormChange}
                                        isMailSentToUser={this.state.isMailSentToUser}
                                    />
                                
                                )}/>
                                <Route exact path='/status' render={() => (
                                    <UserStatus
                                        isAuthenticated={this.state.isAuthenticated}
                                    />
                                    )}
                                />
                            </Switch>
                        </div>
                    </div>
                </div>
                </section>
            </div>
            
        );
    }

}


export default App;