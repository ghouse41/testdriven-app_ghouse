import React from 'react';
import { Redirect,Link } from 'react-router-dom';


const Form = (props) => {
    
    if (props.isAuthenticated) {
        return <Redirect to='/' />;
    }

    let message = ''
    if (props.isError){
        message = props.errormessage
    }
    return (
        <div>
            {message}
            <h1 className="title is-1">{props.formType}</h1>
            <hr/><br/>
            <form onSubmit={(event) => props.handleUserFormSubmit(event)}>
                {props.formType === 'Register' &&
                    <div className="field">
                        <input
                        name="username"
                        className="input is-medium"
                        type="text"
                        placeholder="Enter a username"
                        required
                        value={props.formData.username}
                        onChange={props.handleFormChange}
                        />
                    </div>
                }
                <div className="field">
                    <input
                    name="email"
                    className="input is-medium"
                    type="email"
                    placeholder="Enter an email address"
                    required
                    value={props.formData.email}
                    onChange={props.handleFormChange}
                    />
                </div>
                <div className="field">
                    <input
                    name="password"
                    className="input is-medium"
                    type="password"
                    placeholder="Enter a password"
                    required
                    value={props.formData.password}
                    onChange={props.handleFormChange}
                    />
                </div>
                <input
                type="submit"
                className="button is-primary is-medium is-fullwidth"
                value="Submit"
                />

                {props.formType === 'Login' &&
                    <div>
                        <br></br>
                        <p>Forgot your passowed?&nbsp; &nbsp; <span>
                            <Link to="/resetpassword" >
                            Reset Password
                            </Link>
                            </span>
                        </p>
                        
                        <p>Not Yet a User?&nbsp;  &nbsp; <span>
                            <Link to="/register">Sign Up</Link>
                        </span>

                        </p>
                    </div>
                    
                }

                {props.formType === 'Register' &&
                    <div>
                        <br></br>
                        <p>Already Have an Account?&nbsp; &nbsp; <span>
                            <Link to="/login" >
                            Login
                            </Link>
                            </span>
                        </p>
                        
                        
                    </div>
                    
                }

            </form>
        </div>
    )};


export default Form;