import {
	CognitoUserPool,
	CognitoUserAttribute,
	CognitoUser,
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
		const attributeList = [
			new CognitoUserAttribute({
				Name: 'email',
				Value: 'email@mydomain.com',
			}),
			new CognitoUserAttribute({
				Name: 'subscription_type',
				Value: "FREE"
			})
		]
		this.userPool.signUp(email.replace("@", ""), password, attributeList, [], (err, result) => {
			if (err && onFailure) {
				onFailure(err!)
			}
			if (!err && onSuccess) {
				onSuccess(result?.user!)
			}
		});
	}

	login(email: string, password: string, onSuccess?: (user: CognitoUser) => void, onFailure?: (err: Error) => void) {
		if (this.userPool.getCurrentUser() && onSuccess) {
			onSuccess(this.userPool.getCurrentUser()!!)
		}
		if (!this.userPool.getCurrentUser() && onFailure) {
			onFailure(Error("No user currently authenticated, somehow"))
		}
	}

	logout() {
		this.userPool.getCurrentUser()?.signOut()
	}
}

export default new UserAPI(poolData.UserPoolId, poolData.ClientId);