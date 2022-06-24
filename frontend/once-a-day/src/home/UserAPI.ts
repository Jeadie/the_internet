import {
	AuthenticationDetails,
	CognitoUserPool,
	CognitoUserAttribute,
	CognitoUser,
	CognitoUserSession,
	ICognitoUserData
} from 'amazon-cognito-identity-js';

var poolData = {
	UserPoolId: 'us-east-1_UT3yIKEIo', // TODO
	ClientId: '7cuqpu6g3ho18sg0v6a4cfkjoj', // TODO
};

class UserAPI {
	private userPool: CognitoUserPool;

    constructor(userPoolId: string, clientId: string) {
        this.userPool = new CognitoUserPool({UserPoolId: userPoolId, ClientId: clientId});
    }

	createAccount(email: string, password: string, onSuccess?: (user: CognitoUser) => void, onFailure?: (err: Error) => void) {
		this.userPool.signUp(
			this.createUsername(email),
			password,
			[
				new CognitoUserAttribute({
					Name: 'email',
					Value: email,
				}),
				new CognitoUserAttribute({
					Name: 'custom:subscription_type',
					Value: "FREE"
				})
			], [], (err, result) => {
			if (err && onFailure) {
				onFailure(err!)
			}
			if (!err && onSuccess) {
				onSuccess(result?.user!)
			}
		});
	}

	login(email: string, password: string, onSuccess?: (session: CognitoUserSession) => void, onFailure?: (err: Error) => void) {
		var cognitoUser = new CognitoUser(this.getUserData(email));
		cognitoUser.authenticateUser(new AuthenticationDetails({
				Username: this.createUsername(email),
				Password: password,
			}), {
			onSuccess: onSuccess ? onSuccess : () => {},
			onFailure: onFailure ? onFailure: () => {}
		});
	}

	confirmRegistration(email: string, confirmationCode: string, onSuccess?: (session: CognitoUserSession) => void, onFailure?: (err: Error) => void) {
		let user = new CognitoUser(this.getUserData(email))
		user.confirmRegistration(confirmationCode, true, (err: Error, result: any) => {
			if (err && onFailure) {
				onFailure(err)
			}
			if (onSuccess && result) {
				console.log(result)
				console.log(typeof result)
			}
		})
	}

	resendRegistrationCode(email: string, onSuccess?: (session: CognitoUserSession) => void, onFailure?: (err: Error) => void) {
		let user = new CognitoUser(this.getUserData(email))
		user.resendConfirmationCode((err: Error | undefined, result: any) => {
			err && onFailure ? onFailure(err) : {};
			result && onSuccess ? onSuccess(result): {}; 
		})
	}

	logout() {
		this.userPool.getCurrentUser()?.signOut()
	}

	createUsername(email: string): string {
		return email.replace("@", "")
	}

	getUserData(email: string): ICognitoUserData {
		return {
			Username: this.createUsername(email),
			Pool: this.userPool,
		};
	}


}

export default new UserAPI(poolData.UserPoolId, poolData.ClientId);