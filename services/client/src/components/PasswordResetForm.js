import React,{Component} from 'react';


class PasswordRequestForm extends Component {

render() {
    let message = '' 

    if (this.props.isMailSentToUser) {
        message = <p>Check your email for the instructions to reset your password.</p>
    }

    return (
        <div>
            {message}
            <h1 className="title is-1">{this.props.formType}</h1>
            <hr/><br/>           
            <form onSubmit={(event) => this.props.handleUserFormSubmit(event)}>             
                <div className="field">
                    <input
                    name="email"
                    className="input is-medium"
                    type="email"
                    placeholder="Enter an email address"
                    required
                    value={this.props.formData.email}
                    onChange={this.props.handleFormChange}
                    />
                </div>                
                <input
                type="submit"
                className="button is-primary is-medium is-fullwidth"
                value="Submit"
                />
            </form>
        </div>
    )
}
}


export default PasswordRequestForm;