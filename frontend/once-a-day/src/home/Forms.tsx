import { CognitoUser, CognitoUserSession } from "amazon-cognito-identity-js";
import { ReactNode, useEffect, useState } from "react"
import { useLocation, useNavigate } from "react-router-dom";
import Popup from 'reactjs-popup';

import { AuthenticationForm, Button, ErrorText, FormBox, FormButton, InputField, PlanPricingCard, PopupContent } from "./FormFields"
import UserAPI from "./UserAPI";
import { URL } from "../constants"
import Analytics from "../ana";

let delay = (ms: number) => new Promise(res => setTimeout(res, ms));

export function CreateAccount() {
    useEffect(() => {Analytics.visited("CreateAccount")}, [])
    let navigate = useNavigate();
    let [err_node, set_err_node] = useState("")

    return AuthenticationForm(
        "Get Started Today!",
        "We promise to get you right back to the news",
        "Create an Account",
        "Sign up",
        <p className="py-3 text-sm text-center text-gray-500">{"Have an account? "}
            <a className="underline" href={URL.LOGIN}>Log in</a>
        </p>,
        err_node,
        (input) => {
            UserAPI.createAccount(
                input["email"],
                input["password"],
                (u: CognitoUser) => {navigate(URL.CONFIRM_ACCOUNT)},
                (err: Error) => {set_err_node(err.message)}
            )
        }
    )
}

export function Login() {
    useEffect(() => {Analytics.visited("Login")}, [useLocation])
    let navigate = useNavigate();
    let [err_node, set_err_node] = useState("")

    return AuthenticationForm(
        "news.onceaday.fyi",
        "",
        "Sign in to your account",
        "Sign in",
        <p className="py-3 text-sm text-center text-gray-500">{"No account? "}
            <a className="underline" href={URL.CREATE_ACCOUNT}>Sign up</a>
        </p>,
        err_node,
        (input) => {
            UserAPI.login(input["email"], input["password"], (_: CognitoUserSession) => {navigate(URL.NEWS_BASE)}, (err: Error) => {set_err_node(err.message)})
        }
    )
}

export function ConfirmAccount() {
    useEffect(() => {Analytics.visited("ConfirmAccount")}, [])
    let navigate = useNavigate();

    interface ConfirmState {
        "Verification Code": string
        "err_node": string | ReactNode
        disable_resend: boolean
    }
    let [state, setState] = useState<ConfirmState>({"Verification Code": "", "err_node": "", disable_resend: false})


    const inputOnChange = (e: React.FormEvent<HTMLInputElement>) => {
      setState({
        // Order is important. Override current state with new update.
        ...state,
        [e.currentTarget.id]: e.currentTarget.value,
      });
    };

    const submit = () => {
        UserAPI.confirmRegistration(
            state["Verification Code"],

            // TODO: change to URL.SUBSCRIPTIONS when out of Beta.
            () => {navigate(URL.NEWS_BASE)},
            handleError
        )
    }

    const resend = () => {
        // Reduce spamming of emails
        if (state.disable_resend) {return}

        setState({...state, disable_resend: true})
        UserAPI.resendRegistrationCode(() => {}, handleError)
        delay(2000).then(() => {setState({...state, disable_resend: false})})
    }

    const handleError = (e: Error) => {
        if (e.message == "NoUser") {
            setState({...state, err_node: <p className="text-md text-center">You already have an account. Please login, <a className="underline" href={URL.LOGIN}>here</a></p>})
        } else {
            setState({...state, err_node: ErrorText(e.message)})
        }
    }

    return FormBox(
        "Check your inbox",
        "We've sent you a verification code to your email", (
        <form onSubmit={(e => {e.preventDefault(); submit()})}>
            {InputField("Verification Code", "Abc123...", inputOnChange, true)}
            {FormButton("Verify")}
            {state.err_node && state.err_node}
            <p className="py-3 text-sm text-center text-gray-500">{"Didn't receive it? "}
                <a className={!state.disable_resend ? "underline": ""} onClick={resend}>Resend code</a>
            </p>
        </form>
    ))
}

export function SelectSubscription() {
    useEffect(() => {Analytics.visited("SelectSubscription")}, [useLocation()])
    let navigate = useNavigate();
    
    const title = "Select an option"

    return  (
        <div>
            <h3 className="block p-6 text-center lg:my-8 text-4xl font-bold text-test-600 justify-center">{title}</h3>
            <div className="flex flex-row justify-center">
                <div className="lg:basis-1/4 xl:basis-1/4"></div>
                <div className="lg:basis-2/4 grid md:grid-cols-1 sm:grid-cols-1 xl:grid-cols-2">
                    <div className="col-span-1 lg:px-5 my-5">
                    {PlanPricingCard(
                        "Free",
                        "We won't charge our Beta users now, or ever.", // No strings attached",
                        0, 
                        "Quarterly", 
                        "Select",
                        ["News from across the Internet", "Basic search & filtering"], 
                        () => {navigate(URL.NEWS_BASE)}
                    )}</div>
                    <div className="col-span-1 lg:px-5 my-5">
                    {PlanPricingCard(
                        "Full",
                        "When we finish all the features, stabilise and get out of Beta",
                        3, 
                        "Quarterly", 
                        <Popup trigger={Button(() => {}, "Not yet")} position="right center">
                            {PopupContent(
                                "You're too early",
                                "We're glad you're excited about the product, but currently we're in beta. Signup for a free account, and as a Beta user, you'll be free for life!"
                            )}
                        </Popup>,
                        ["Advanced search & filtering", "Saved views", "Bookmarks & saved articles", "Newspaper Requests"], 
                        () => {}
                    )}
                    </div>
                </div>
                <div className="lg:basis-1/4 xl:basis-1/4"></div>
            </div>
        </div>
    )
}